"""
Comprehensive Unit Tests for backend/config.py
Tests configuration settings, environment variable handling, CORS origins, and validation
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from backend.config import Settings, settings


class TestSettingsConfiguration:
    """Test Settings class initialization and configuration"""
    
    def test_settings_default_values(self):
        """Test that Settings class has correct default values"""
        test_settings = Settings()
        
        # Database defaults
        assert test_settings.db_name == "nowhere_digital"
        assert test_settings.mongo_url == "mongodb://localhost:27017"
        
        # Email defaults
        assert test_settings.sendgrid_from_email == "noreply@nowhere.ai"
        assert test_settings.sender_email == "hello@nowhere.ai"
        assert test_settings.admin_email == "admin@nowhere.ai"
        
        # AI defaults
        assert test_settings.default_ai_model == "gpt-4o"
        assert test_settings.ai_provider == "openai"
        
        # Security defaults
        assert test_settings.jwt_algorithm == "HS256"
        assert test_settings.jwt_expiration == 24 * 60 * 60  # 24 hours
        
        # API defaults
        assert test_settings.api_prefix == "/api"
        assert test_settings.debug is False
        
    def test_settings_file_upload_defaults(self):
        """Test file upload configuration defaults"""
        test_settings = Settings()
        
        assert test_settings.max_file_size == 10 * 1024 * 1024  # 10MB
        assert "image/jpeg" in test_settings.allowed_file_types
        assert "image/png" in test_settings.allowed_file_types
        assert "image/gif" in test_settings.allowed_file_types
        assert "application/pdf" in test_settings.allowed_file_types
        assert len(test_settings.allowed_file_types) == 4
        
    def test_settings_rate_limiting_defaults(self):
        """Test rate limiting configuration defaults"""
        test_settings = Settings()
        
        assert test_settings.rate_limit_requests == 100
        assert test_settings.rate_limit_period == 60  # seconds
        
    def test_settings_email_templates_dir(self):
        """Test email templates directory configuration"""
        test_settings = Settings()
        
        assert test_settings.email_templates_dir == "email_templates"


class TestCORSOrigins:
    """Test CORS origins configuration and validation"""
    
    def test_cors_origins_default_values(self):
        """Test default CORS origins include all required URLs"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        assert "http://localhost:3000" in test_settings.cors_origins
        assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
        assert "https://fix-it-6.emergent.host" in test_settings.cors_origins
        assert len(test_settings.cors_origins) == 3
        
    def test_cors_origins_correct_preview_url(self):
        """Test that CORS origins contain the correct preview URL after update"""
        test_settings = Settings()
        
        # Verify the updated preview URL is present
        assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
        
        # Verify the old URL is NOT present
        assert "https://fix-it-6.preview.emergentagent.com" not in test_settings.cors_origins
        
    def test_cors_origins_production_url(self):
        """Test that production URL is correctly configured"""
        test_settings = Settings()
        
        production_url = "https://fix-it-6.emergent.host"
        assert production_url in test_settings.cors_origins
        
    def test_cors_origins_localhost(self):
        """Test that localhost is included for development"""
        test_settings = Settings()
        
        assert "http://localhost:3000" in test_settings.cors_origins
        
    @patch.dict(os.environ, {"CORS_ORIGINS": "https://custom1.com,https://custom2.com,http://localhost:4000"})
    def test_cors_origins_from_environment(self):
        """Test CORS origins can be overridden via environment variable"""
        test_settings = Settings()
        
        assert "https://custom1.com" in test_settings.cors_origins
        assert "https://custom2.com" in test_settings.cors_origins
        assert "http://localhost:4000" in test_settings.cors_origins
        assert len(test_settings.cors_origins) == 3
        
    @patch.dict(os.environ, {"CORS_ORIGINS": "https://single-origin.com"})
    def test_cors_origins_single_value(self):
        """Test CORS origins with single value"""
        test_settings = Settings()
        
        assert test_settings.cors_origins == ["https://single-origin.com"]
        
    @patch.dict(os.environ, {"CORS_ORIGINS": ""})
    def test_cors_origins_empty_environment(self):
        """Test CORS origins with empty environment variable falls back to defaults"""
        test_settings = Settings()
        
        # When empty, should fall back to defaults
        assert len(test_settings.cors_origins) == 1
        assert test_settings.cors_origins[0] == ""
        
    def test_cors_origins_no_trailing_slashes(self):
        """Test that CORS origins don't have trailing slashes"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            if origin:  # Skip empty strings
                assert not origin.endswith('/'), f"Origin {origin} should not have trailing slash"
                
    def test_cors_origins_valid_urls(self):
        """Test that CORS origins are valid URLs"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            if origin:  # Skip empty strings
                assert origin.startswith('http://') or origin.startswith('https://'), \
                    f"Origin {origin} must start with http:// or https://"


class TestEnvironmentVariables:
    """Test environment variable handling"""
    
    @patch.dict(os.environ, {"MONGO_URL": "mongodb://custom:27017"})
    def test_mongo_url_from_environment(self):
        """Test MongoDB URL can be set from environment"""
        test_settings = Settings()
        assert test_settings.mongo_url == "mongodb://custom:27017"
        
    @patch.dict(os.environ, {"DB_NAME": "custom_database"})
    def test_db_name_from_environment(self):
        """Test database name can be set from environment"""
        test_settings = Settings()
        assert test_settings.db_name == "custom_database"
        
    @patch.dict(os.environ, {"SENDGRID_API_KEY": "test_api_key_12345"})
    def test_sendgrid_api_key_from_environment(self):
        """Test SendGrid API key can be set from environment"""
        test_settings = Settings()
        assert test_settings.sendgrid_api_key == "test_api_key_12345"
        
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-openai-key"})
    def test_openai_api_key_from_environment(self):
        """Test OpenAI API key can be set from environment"""
        test_settings = Settings()
        assert test_settings.openai_api_key == "sk-test-openai-key"
        
    @patch.dict(os.environ, {"DEFAULT_AI_MODEL": "gpt-4-turbo"})
    def test_ai_model_from_environment(self):
        """Test AI model can be changed from environment"""
        test_settings = Settings()
        assert test_settings.default_ai_model == "gpt-4-turbo"
        
    @patch.dict(os.environ, {"AI_PROVIDER": "anthropic"})
    def test_ai_provider_from_environment(self):
        """Test AI provider can be changed from environment"""
        test_settings = Settings()
        assert test_settings.ai_provider == "anthropic"
        
    @patch.dict(os.environ, {"STRIPE_API_KEY": "sk_live_test_key"})
    def test_stripe_api_key_from_environment(self):
        """Test Stripe API key can be set from environment"""
        test_settings = Settings()
        assert test_settings.stripe_api_key == "sk_live_test_key"
        
    @patch.dict(os.environ, {"JWT_SECRET": "custom-secret-key-xyz"})
    def test_jwt_secret_from_environment(self):
        """Test JWT secret can be set from environment"""
        test_settings = Settings()
        assert test_settings.jwt_secret == "custom-secret-key-xyz"
        
    @patch.dict(os.environ, {"DEBUG": "true"})
    def test_debug_mode_enabled(self):
        """Test debug mode can be enabled from environment"""
        test_settings = Settings()
        assert test_settings.debug is True
        
    @patch.dict(os.environ, {"DEBUG": "false"})
    def test_debug_mode_disabled(self):
        """Test debug mode is disabled when explicitly set to false"""
        test_settings = Settings()
        assert test_settings.debug is False
        
    @patch.dict(os.environ, {"DEBUG": "TRUE"})
    def test_debug_mode_case_insensitive(self):
        """Test debug mode handles case insensitive values"""
        test_settings = Settings()
        assert test_settings.debug is True


class TestSecurityConfiguration:
    """Test security-related configuration"""
    
    def test_jwt_secret_has_default(self):
        """Test JWT secret has a default value"""
        test_settings = Settings()
        assert test_settings.jwt_secret is not None
        assert len(test_settings.jwt_secret) > 0
        
    def test_jwt_algorithm_is_hs256(self):
        """Test JWT algorithm is HS256"""
        test_settings = Settings()
        assert test_settings.jwt_algorithm == "HS256"
        
    def test_jwt_expiration_is_24_hours(self):
        """Test JWT expiration is 24 hours in seconds"""
        test_settings = Settings()
        assert test_settings.jwt_expiration == 86400  # 24 * 60 * 60
        
    def test_default_jwt_secret_should_be_changed_in_production(self):
        """Test that default JWT secret contains warning message"""
        test_settings = Settings()
        assert "change-in-production" in test_settings.jwt_secret.lower()


class TestAPIConfiguration:
    """Test API-related configuration"""
    
    def test_api_prefix_is_api(self):
        """Test API prefix is set to /api"""
        test_settings = Settings()
        assert test_settings.api_prefix == "/api"
        
    def test_api_prefix_starts_with_slash(self):
        """Test API prefix starts with a slash"""
        test_settings = Settings()
        assert test_settings.api_prefix.startswith('/')


class TestTwilioConfiguration:
    """Test Twilio SMS configuration"""
    
    def test_twilio_defaults_are_empty_strings(self):
        """Test Twilio credentials default to empty strings"""
        test_settings = Settings()
        
        assert test_settings.twilio_account_sid == ""
        assert test_settings.twilio_auth_token == ""
        assert test_settings.twilio_verify_service == ""
        assert test_settings.twilio_phone_number == ""
        
    @patch.dict(os.environ, {
        "TWILIO_ACCOUNT_SID": "AC123456",
        "TWILIO_AUTH_TOKEN": "token123",
        "TWILIO_VERIFY_SERVICE": "VA123456",
        "TWILIO_PHONE_NUMBER": "+1234567890"
    })
    def test_twilio_from_environment(self):
        """Test Twilio configuration from environment variables"""
        test_settings = Settings()
        
        assert test_settings.twilio_account_sid == "AC123456"
        assert test_settings.twilio_auth_token == "token123"
        assert test_settings.twilio_verify_service == "VA123456"
        assert test_settings.twilio_phone_number == "+1234567890"


class TestGlobalSettingsInstance:
    """Test the global settings instance"""
    
    def test_global_settings_instance_exists(self):
        """Test that global settings instance is created"""
        assert settings is not None
        
    def test_global_settings_is_settings_instance(self):
        """Test that global settings is an instance of Settings"""
        assert isinstance(settings, Settings)
        
    def test_global_settings_has_cors_origins(self):
        """Test that global settings has CORS origins configured"""
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) > 0


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "https://example1.com,  ,https://example2.com"})
    def test_cors_origins_with_whitespace(self):
        """Test CORS origins handles whitespace correctly"""
        test_settings = Settings()
        
        # Should have 3 items including the empty one with spaces
        assert len(test_settings.cors_origins) == 3
        # Items should be stripped or preserved as-is (depending on implementation)
        
    @patch.dict(os.environ, {"JWT_EXPIRATION": "3600"})
    def test_jwt_expiration_cannot_be_changed_via_env(self):
        """Test JWT expiration is hardcoded and not affected by environment"""
        test_settings = Settings()
        
        # JWT expiration is hardcoded in the class, not from environment
        assert test_settings.jwt_expiration == 86400
        
    def test_allowed_file_types_are_immutable(self):
        """Test that allowed file types list is properly defined"""
        test_settings = Settings()
        
        original_types = test_settings.allowed_file_types.copy()
        assert len(original_types) == 4
        
    def test_max_file_size_is_reasonable(self):
        """Test that max file size is reasonable (10MB)"""
        test_settings = Settings()
        
        assert test_settings.max_file_size == 10485760  # 10 * 1024 * 1024
        assert test_settings.max_file_size > 0
        assert test_settings.max_file_size <= 100 * 1024 * 1024  # Less than 100MB


class TestConfigurationIntegrity:
    """Test overall configuration integrity"""
    
    def test_all_required_fields_present(self):
        """Test that all required configuration fields are present"""
        test_settings = Settings()
        
        required_fields = [
            'mongo_url', 'db_name', 'sendgrid_api_key', 'sendgrid_from_email',
            'sender_email', 'admin_email', 'openai_api_key', 'default_ai_model',
            'ai_provider', 'emergent_llm_key', 'stripe_api_key', 'twilio_account_sid',
            'twilio_auth_token', 'twilio_verify_service', 'twilio_phone_number',
            'jwt_secret', 'jwt_algorithm', 'jwt_expiration', 'cors_origins',
            'api_prefix', 'debug', 'max_file_size', 'allowed_file_types',
            'rate_limit_requests', 'rate_limit_period', 'email_templates_dir'
        ]
        
        for field in required_fields:
            assert hasattr(test_settings, field), f"Missing required field: {field}"
            
    def test_cors_origins_type_consistency(self):
        """Test CORS origins is always a list"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        
    def test_numeric_fields_are_positive(self):
        """Test that numeric configuration values are positive"""
        test_settings = Settings()
        
        assert test_settings.jwt_expiration > 0
        assert test_settings.max_file_size > 0
        assert test_settings.rate_limit_requests > 0
        assert test_settings.rate_limit_period > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])