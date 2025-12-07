"""
Unit tests for backend/config.py
Tests configuration settings, CORS origins, and environment variable handling
"""

import pytest
import os
from unittest.mock import patch
from backend.config import Settings


class TestSettings:
    """Test suite for Settings configuration class"""
    
    def test_default_database_settings(self):
        """Test default database configuration values"""
        settings = Settings()
        assert settings.mongo_url == "mongodb://localhost:27017"
        assert settings.db_name == "nowhere_digital"
    
    def test_default_email_settings(self):
        """Test default email configuration values"""
        settings = Settings()
        assert settings.sendgrid_from_email == "noreply@nowhere.ai"
        assert settings.sender_email == "hello@nowhere.ai"
        assert settings.admin_email == "admin@nowhere.ai"
    
    def test_default_ai_settings(self):
        """Test default AI provider configuration"""
        settings = Settings()
        assert settings.default_ai_model == "gpt-4o"
        assert settings.ai_provider == "openai"
        assert settings.emergent_llm_key == "sk-emergent-8A3Bc7c1f91F43cE8D"
    
    def test_default_security_settings(self):
        """Test JWT and security configuration"""
        settings = Settings()
        assert settings.jwt_secret == "your-secret-key-change-in-production"
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_expiration == 24 * 60 * 60  # 24 hours
    
    def test_default_cors_origins(self):
        """Test default CORS origins includes required URLs"""
        settings = Settings()
        assert len(settings.cors_origins) >= 3
        assert "http://localhost:3000" in settings.cors_origins
        assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
        assert "https://fix-it-6.emergent.host" in settings.cors_origins
    
    def test_cors_origins_format(self):
        """Test CORS origins are properly formatted as a list"""
        settings = Settings()
        assert isinstance(settings.cors_origins, list)
        for origin in settings.cors_origins:
            assert isinstance(origin, str)
            assert origin.startswith("http://") or origin.startswith("https://")
    
    def test_api_settings(self):
        """Test API configuration defaults"""
        settings = Settings()
        assert settings.api_prefix == "/api"
        assert settings.debug is False
    
    def test_file_upload_settings(self):
        """Test file upload configuration"""
        settings = Settings()
        assert settings.max_file_size == 10 * 1024 * 1024  # 10MB
        assert isinstance(settings.allowed_file_types, list)
        assert "image/jpeg" in settings.allowed_file_types
        assert "image/png" in settings.allowed_file_types
        assert "application/pdf" in settings.allowed_file_types
    
    def test_rate_limiting_settings(self):
        """Test rate limiting configuration"""
        settings = Settings()
        assert settings.rate_limit_requests == 100
        assert settings.rate_limit_period == 60  # seconds
    
    @patch.dict(os.environ, {"MONGO_URL": "mongodb://test:27017"})
    def test_mongo_url_from_env(self):
        """Test MongoDB URL can be overridden by environment variable"""
        settings = Settings()
        assert settings.mongo_url == "mongodb://test:27017"
    
    @patch.dict(os.environ, {"DB_NAME": "test_database"})
    def test_db_name_from_env(self):
        """Test database name can be overridden by environment variable"""
        settings = Settings()
        assert settings.db_name == "test_database"
    
    @patch.dict(os.environ, {"SENDGRID_API_KEY": "test-api-key-123"})
    def test_sendgrid_api_key_from_env(self):
        """Test SendGrid API key can be set via environment variable"""
        settings = Settings()
        assert settings.sendgrid_api_key == "test-api-key-123"
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"})
    def test_openai_api_key_from_env(self):
        """Test OpenAI API key can be set via environment variable"""
        settings = Settings()
        assert settings.openai_api_key == "sk-test-key"
    
    @patch.dict(os.environ, {"DEFAULT_AI_MODEL": "gpt-4-turbo"})
    def test_ai_model_from_env(self):
        """Test AI model can be overridden by environment variable"""
        settings = Settings()
        assert settings.default_ai_model == "gpt-4-turbo"
    
    @patch.dict(os.environ, {"JWT_SECRET": "super-secret-key"})
    def test_jwt_secret_from_env(self):
        """Test JWT secret can be set via environment variable"""
        settings = Settings()
        assert settings.jwt_secret == "super-secret-key"
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test1.com,http://test2.com"})
    def test_cors_origins_from_env(self):
        """Test CORS origins can be overridden by environment variable"""
        settings = Settings()
        assert len(settings.cors_origins) == 2
        assert "http://test1.com" in settings.cors_origins
        assert "http://test2.com" in settings.cors_origins
    
    @patch.dict(os.environ, {"DEBUG": "true"})
    def test_debug_mode_enabled(self):
        """Test debug mode can be enabled via environment variable"""
        settings = Settings()
        assert settings.debug is True
    
    @patch.dict(os.environ, {"DEBUG": "false"})
    def test_debug_mode_disabled(self):
        """Test debug mode can be explicitly disabled"""
        settings = Settings()
        assert settings.debug is False
    
    @patch.dict(os.environ, {"DEBUG": "True"})
    def test_debug_mode_case_insensitive(self):
        """Test debug mode is case insensitive"""
        settings = Settings()
        assert settings.debug is True
    
    def test_stripe_api_key_default(self):
        """Test Stripe API key has default test value"""
        settings = Settings()
        assert settings.stripe_api_key == "sk_test_emergent"
    
    def test_twilio_settings_default(self):
        """Test Twilio settings have empty defaults"""
        settings = Settings()
        assert settings.twilio_account_sid == ""
        assert settings.twilio_auth_token == ""
        assert settings.twilio_verify_service == ""
        assert settings.twilio_phone_number == ""
    
    @patch.dict(os.environ, {"TWILIO_ACCOUNT_SID": "AC123456"})
    def test_twilio_account_sid_from_env(self):
        """Test Twilio account SID can be set via environment variable"""
        settings = Settings()
        assert settings.twilio_account_sid == "AC123456"
    
    def test_email_templates_directory(self):
        """Test email templates directory configuration"""
        settings = Settings()
        assert settings.email_templates_dir == "email_templates"
    
    def test_allowed_file_types_validation(self):
        """Test that allowed file types are properly configured"""
        settings = Settings()
        expected_types = ["image/jpeg", "image/png", "image/gif", "application/pdf"]
        for file_type in expected_types:
            assert file_type in settings.allowed_file_types
    
    def test_cors_origins_no_trailing_slashes(self):
        """Test CORS origins don't have trailing slashes"""
        settings = Settings()
        for origin in settings.cors_origins:
            assert not origin.endswith("/"), f"Origin {origin} should not have trailing slash"
    
    def test_cors_origins_production_urls(self):
        """Test that production CORS URLs are correctly configured"""
        settings = Settings()
        # Check for the updated preview URL
        preview_url = "https://create-25.preview.emergentagent.com"
        production_url = "https://fix-it-6.emergent.host"
        
        assert preview_url in settings.cors_origins, f"Preview URL {preview_url} should be in CORS origins"
        assert production_url in settings.cors_origins, f"Production URL {production_url} should be in CORS origins"
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000"})
    def test_cors_single_origin(self):
        """Test CORS with single origin"""
        settings = Settings()
        assert len(settings.cors_origins) == 1
        assert settings.cors_origins[0] == "http://localhost:3000"
    
    @patch.dict(os.environ, {"CORS_ORIGINS": ""})
    def test_cors_empty_string_handling(self):
        """Test CORS handles empty string appropriately"""
        settings = Settings()
        # Empty string split results in list with one empty string
        assert isinstance(settings.cors_origins, list)
    
    def test_jwt_expiration_value(self):
        """Test JWT expiration is set to 24 hours in seconds"""
        settings = Settings()
        expected_seconds = 24 * 60 * 60
        assert settings.jwt_expiration == expected_seconds
        assert settings.jwt_expiration == 86400
    
    def test_max_file_size_in_bytes(self):
        """Test max file size is correctly set in bytes (10MB)"""
        settings = Settings()
        expected_bytes = 10 * 1024 * 1024
        assert settings.max_file_size == expected_bytes
        assert settings.max_file_size == 10485760
    
    @patch.dict(os.environ, {"AI_PROVIDER": "anthropic"})
    def test_alternative_ai_provider(self):
        """Test alternative AI provider can be configured"""
        settings = Settings()
        assert settings.ai_provider == "anthropic"
    
    def test_settings_instance_creation(self):
        """Test that Settings instance can be created multiple times"""
        settings1 = Settings()
        settings2 = Settings()
        assert settings1.mongo_url == settings2.mongo_url
        assert settings1.cors_origins == settings2.cors_origins
    
    def test_cors_origins_localhost_included(self):
        """Test localhost is always included in default CORS origins"""
        settings = Settings()
        localhost_found = any("localhost" in origin for origin in settings.cors_origins)
        assert localhost_found, "localhost should be in CORS origins for development"
    
    @patch.dict(os.environ, {"SENDGRID_FROM_EMAIL": "custom@test.com"})
    def test_custom_sendgrid_from_email(self):
        """Test SendGrid from email can be customized"""
        settings = Settings()
        assert settings.sendgrid_from_email == "custom@test.com"
    
    @patch.dict(os.environ, {"ADMIN_EMAIL": "admin@custom.com"})
    def test_custom_admin_email(self):
        """Test admin email can be customized"""
        settings = Settings()
        assert settings.admin_email == "admin@custom.com"
    
    def test_rate_limit_period_reasonable(self):
        """Test rate limit period is reasonable (60 seconds)"""
        settings = Settings()
        assert settings.rate_limit_period == 60
        assert settings.rate_limit_period <= 300  # Not more than 5 minutes
    
    def test_rate_limit_requests_reasonable(self):
        """Test rate limit requests is reasonable (100 per period)"""
        settings = Settings()
        assert settings.rate_limit_requests == 100
        assert settings.rate_limit_requests > 0
    
    def test_config_class_attributes(self):
        """Test Config class has correct attributes"""
        assert hasattr(Settings.Config, 'env_file')
        assert Settings.Config.env_file == ".env"
        assert Settings.Config.env_file_encoding == "utf-8"


class TestCORSConfiguration:
    """Specific test suite for CORS configuration changes"""
    
    def test_cors_preview_url_updated(self):
        """Test that CORS preview URL has been updated to create-25"""
        settings = Settings()
        old_url = "https://fix-it-6.preview.emergentagent.com"
        new_url = "https://create-25.preview.emergentagent.com"
        
        assert new_url in settings.cors_origins, "New preview URL should be in CORS origins"
        assert old_url not in settings.cors_origins, "Old preview URL should not be in CORS origins"
    
    def test_cors_production_url_unchanged(self):
        """Test that production URL remains unchanged"""
        settings = Settings()
        production_url = "https://fix-it-6.emergent.host"
        assert production_url in settings.cors_origins
    
    def test_cors_all_required_environments(self):
        """Test CORS includes all required environments: local, preview, production"""
        settings = Settings()
        has_local = any("localhost" in origin for origin in settings.cors_origins)
        has_preview = any("preview.emergentagent.com" in origin for origin in settings.cors_origins)
        has_production = any("emergent.host" in origin for origin in settings.cors_origins)
        
        assert has_local, "CORS should include localhost for development"
        assert has_preview, "CORS should include preview environment"
        assert has_production, "CORS should include production environment"


class TestEnvironmentVariableHandling:
    """Test suite for environment variable handling edge cases"""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_all_defaults_when_no_env_vars(self):
        """Test all settings use defaults when no environment variables are set"""
        settings = Settings()
        assert settings.mongo_url == "mongodb://localhost:27017"
        assert settings.db_name == "nowhere_digital"
        assert settings.debug is False
    
    @patch.dict(os.environ, {"DEBUG": "invalid"})
    def test_debug_invalid_value(self):
        """Test debug mode with invalid value defaults to False"""
        settings = Settings()
        assert settings.debug is False
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test1.com, http://test2.com, http://test3.com"})
    def test_cors_with_spaces_in_env(self):
        """Test CORS origins with spaces in environment variable"""
        settings = Settings()
        # Note: Spaces after commas will be included in the origin strings
        assert len(settings.cors_origins) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])