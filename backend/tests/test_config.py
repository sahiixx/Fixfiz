"""
Comprehensive Unit Tests for backend/config.py

Tests the Settings class configuration management including:
- Environment variable loading
- Default values
- Data type validation
- CORS origins parsing
- Security settings
- API configuration
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from pydantic import ValidationError


# Test module imports
def test_config_imports():
    """Test that config module imports successfully"""
    try:
        from backend.config import Settings
        assert Settings is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Settings: {e}")


class TestSettingsDefaults:
    """Test default values for all settings"""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_database_settings(self):
        """Test database default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.mongo_url == "mongodb://localhost:27017"
        assert settings.db_name == "nowhere_digital"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_email_settings(self):
        """Test email default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.sendgrid_api_key == ""
        assert settings.sendgrid_from_email == "noreply@nowhere.ai"
        assert settings.sender_email == "hello@nowhere.ai"
        assert settings.admin_email == "admin@nowhere.ai"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_ai_settings(self):
        """Test AI service default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.openai_api_key == ""
        assert settings.default_ai_model == "gpt-4o"
        assert settings.ai_provider == "openai"
        assert settings.emergent_llm_key == "sk-emergent-8A3Bc7c1f91F43cE8D"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_payment_settings(self):
        """Test payment default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.stripe_api_key == "sk_test_emergent"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_sms_settings(self):
        """Test SMS/Twilio default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.twilio_account_sid == ""
        assert settings.twilio_auth_token == ""
        assert settings.twilio_verify_service == ""
        assert settings.twilio_phone_number == ""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_security_settings(self):
        """Test security default settings"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.jwt_secret == "your-secret-key-change-in-production"
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_expiration == 24 * 60 * 60  # 24 hours
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_cors_settings(self):
        """Test CORS default settings with multiple origins"""
        from backend.config import Settings
        settings = Settings()
        
        expected_origins = [
            "http://localhost:3000",
            "https://create-25.preview.emergentagent.com",
            "https://fix-it-6.emergent.host"
        ]
        assert settings.cors_origins == expected_origins
        assert len(settings.cors_origins) == 3
        assert isinstance(settings.cors_origins, list)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_api_settings(self):
        """Test API configuration defaults"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.api_prefix == "/api"
        assert settings.debug is False
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_file_upload_settings(self):
        """Test file upload configuration defaults"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.max_file_size == 10 * 1024 * 1024  # 10MB
        assert settings.allowed_file_types == [
            "image/jpeg",
            "image/png",
            "image/gif",
            "application/pdf"
        ]
        assert len(settings.allowed_file_types) == 4


class TestEnvironmentVariableOverrides:
    """Test that environment variables properly override defaults"""
    
    def test_mongo_url_override(self):
        """Test MONGO_URL environment variable override"""
        from backend.config import Settings
        test_url = "mongodb://testhost:27018/testdb"
        
        with patch.dict(os.environ, {"MONGO_URL": test_url}):
            settings = Settings()
            assert settings.mongo_url == test_url
    
    def test_db_name_override(self):
        """Test DB_NAME environment variable override"""
        from backend.config import Settings
        test_db = "test_database"
        
        with patch.dict(os.environ, {"DB_NAME": test_db}):
            settings = Settings()
            assert settings.db_name == test_db
    
    def test_openai_api_key_override(self):
        """Test OPENAI_API_KEY environment variable override"""
        from backend.config import Settings
        test_key = "sk-test-key-12345"
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": test_key}):
            settings = Settings()
            assert settings.openai_api_key == test_key
    
    def test_default_ai_model_override(self):
        """Test DEFAULT_AI_MODEL environment variable override"""
        from backend.config import Settings
        test_model = "gpt-4-turbo"
        
        with patch.dict(os.environ, {"DEFAULT_AI_MODEL": test_model}):
            settings = Settings()
            assert settings.default_ai_model == test_model
    
    def test_ai_provider_override(self):
        """Test AI_PROVIDER environment variable override"""
        from backend.config import Settings
        test_provider = "anthropic"
        
        with patch.dict(os.environ, {"AI_PROVIDER": test_provider}):
            settings = Settings()
            assert settings.ai_provider == test_provider
    
    def test_jwt_secret_override(self):
        """Test JWT_SECRET environment variable override"""
        from backend.config import Settings
        test_secret = "super-secret-production-key"
        
        with patch.dict(os.environ, {"JWT_SECRET": test_secret}):
            settings = Settings()
            assert settings.jwt_secret == test_secret
    
    def test_debug_mode_true(self):
        """Test DEBUG environment variable set to true"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"DEBUG": "true"}):
            settings = Settings()
            assert settings.debug is True
    
    def test_debug_mode_false(self):
        """Test DEBUG environment variable set to false"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"DEBUG": "false"}):
            settings = Settings()
            assert settings.debug is False
    
    def test_debug_mode_uppercase(self):
        """Test DEBUG environment variable case insensitivity"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"DEBUG": "TRUE"}):
            settings = Settings()
            assert settings.debug is True
    
    def test_sendgrid_email_overrides(self):
        """Test SendGrid email configuration overrides"""
        from backend.config import Settings
        
        env_vars = {
            "SENDGRID_API_KEY": "SG.test_key_123",
            "SENDGRID_FROM_EMAIL": "custom@example.com",
            "SENDER_EMAIL": "sender@example.com",
            "ADMIN_EMAIL": "admin@example.com"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            assert settings.sendgrid_api_key == "SG.test_key_123"
            assert settings.sendgrid_from_email == "custom@example.com"
            assert settings.sender_email == "sender@example.com"
            assert settings.admin_email == "admin@example.com"
    
    def test_twilio_settings_override(self):
        """Test Twilio configuration overrides"""
        from backend.config import Settings
        
        env_vars = {
            "TWILIO_ACCOUNT_SID": "AC1234567890",
            "TWILIO_AUTH_TOKEN": "auth_token_test",
            "TWILIO_VERIFY_SERVICE": "VA1234567890",
            "TWILIO_PHONE_NUMBER": "+971501234567"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            assert settings.twilio_account_sid == "AC1234567890"
            assert settings.twilio_auth_token == "auth_token_test"
            assert settings.twilio_verify_service == "VA1234567890"
            assert settings.twilio_phone_number == "+971501234567"


class TestCORSOriginsParsing:
    """Test CORS origins parsing from environment variable"""
    
    def test_single_cors_origin(self):
        """Test parsing single CORS origin"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000"}):
            settings = Settings()
            assert settings.cors_origins == ["http://localhost:3000"]
            assert len(settings.cors_origins) == 1
    
    def test_multiple_cors_origins(self):
        """Test parsing multiple CORS origins"""
        from backend.config import Settings
        
        origins = "http://localhost:3000,https://example.com,https://api.example.com"
        with patch.dict(os.environ, {"CORS_ORIGINS": origins}):
            settings = Settings()
            assert len(settings.cors_origins) == 3
            assert "http://localhost:3000" in settings.cors_origins
            assert "https://example.com" in settings.cors_origins
            assert "https://api.example.com" in settings.cors_origins
    
    def test_cors_origins_with_spaces(self):
        """Test CORS origins parsing handles spaces"""
        from backend.config import Settings
        
        origins = "http://localhost:3000, https://example.com , https://api.example.com"
        with patch.dict(os.environ, {"CORS_ORIGINS": origins}):
            settings = Settings()
            # Note: spaces after commas remain in the parsed values
            assert len(settings.cors_origins) == 3
    
    def test_cors_origins_empty_string(self):
        """Test CORS origins with empty string"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"CORS_ORIGINS": ""}):
            settings = Settings()
            assert settings.cors_origins == [""]
    
    def test_production_cors_origins(self):
        """Test production CORS origins configuration"""
        from backend.config import Settings
        
        origins = "https://create-25.preview.emergentagent.com,https://fix-it-6.emergent.host"
        with patch.dict(os.environ, {"CORS_ORIGINS": origins}):
            settings = Settings()
            assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
            assert "https://fix-it-6.emergent.host" in settings.cors_origins
            assert len(settings.cors_origins) == 2


class TestSecuritySettings:
    """Test security-related configuration"""
    
    def test_jwt_expiration_type(self):
        """Test JWT expiration is integer"""
        from backend.config import Settings
        settings = Settings()
        
        assert isinstance(settings.jwt_expiration, int)
        assert settings.jwt_expiration > 0
    
    def test_jwt_expiration_24_hours(self):
        """Test JWT expiration defaults to 24 hours in seconds"""
        from backend.config import Settings
        settings = Settings()
        
        expected_seconds = 24 * 60 * 60  # 86400 seconds
        assert settings.jwt_expiration == expected_seconds
    
    def test_jwt_algorithm(self):
        """Test JWT algorithm is HS256"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.jwt_algorithm == "HS256"
    
    def test_weak_jwt_secret_warning(self):
        """Test that default JWT secret is the weak development secret"""
        from backend.config import Settings
        settings = Settings()
        
        # In production, this should be overridden
        assert settings.jwt_secret == "your-secret-key-change-in-production"
    
    def test_stripe_test_key_format(self):
        """Test Stripe test key format"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.stripe_api_key.startswith("sk_test")


class TestFileUploadSettings:
    """Test file upload configuration"""
    
    def test_max_file_size_bytes(self):
        """Test max file size is in bytes"""
        from backend.config import Settings
        settings = Settings()
        
        expected_bytes = 10 * 1024 * 1024  # 10MB
        assert settings.max_file_size == expected_bytes
    
    def test_max_file_size_10mb(self):
        """Test max file size equals 10MB"""
        from backend.config import Settings
        settings = Settings()
        
        assert settings.max_file_size == 10485760  # 10 * 1024 * 1024
    
    def test_allowed_file_types_list(self):
        """Test allowed file types is a list"""
        from backend.config import Settings
        settings = Settings()
        
        assert isinstance(settings.allowed_file_types, list)
    
    def test_allowed_image_formats(self):
        """Test allowed image file formats"""
        from backend.config import Settings
        settings = Settings()
        
        assert "image/jpeg" in settings.allowed_file_types
        assert "image/png" in settings.allowed_file_types
        assert "image/gif" in settings.allowed_file_types
    
    def test_allowed_pdf_format(self):
        """Test PDF format is allowed"""
        from backend.config import Settings
        settings = Settings()
        
        assert "application/pdf" in settings.allowed_file_types
    
    def test_disallowed_file_types(self):
        """Test that dangerous file types are not in allowed list"""
        from backend.config import Settings
        settings = Settings()
        
        dangerous_types = [
            "application/x-executable",
            "application/x-sh",
            "text/html",
            "application/javascript"
        ]
        
        for dangerous_type in dangerous_types:
            assert dangerous_type not in settings.allowed_file_types


class TestSettingsValidation:
    """Test Settings validation and type checking"""
    
    def test_settings_instantiation(self):
        """Test Settings can be instantiated without errors"""
        from backend.config import Settings
        
        try:
            settings = Settings()
            assert settings is not None
        except Exception as e:
            pytest.fail(f"Failed to instantiate Settings: {e}")
    
    def test_cors_origins_is_list(self):
        """Test CORS origins is always a list type"""
        from backend.config import Settings
        settings = Settings()
        
        assert isinstance(settings.cors_origins, list)
    
    def test_api_prefix_string(self):
        """Test API prefix is string type"""
        from backend.config import Settings
        settings = Settings()
        
        assert isinstance(settings.api_prefix, str)
        assert settings.api_prefix.startswith("/")
    
    def test_debug_boolean(self):
        """Test debug is boolean type"""
        from backend.config import Settings
        settings = Settings()
        
        assert isinstance(settings.debug, bool)


class TestProductionReadiness:
    """Test production environment configuration"""
    
    def test_production_mongodb_url(self):
        """Test production MongoDB URL configuration"""
        from backend.config import Settings
        
        prod_url = "mongodb+srv://user:pass@cluster.mongodb.net/dbname"
        with patch.dict(os.environ, {"MONGO_URL": prod_url}):
            settings = Settings()
            assert "mongodb+srv" in settings.mongo_url
            assert settings.mongo_url == prod_url
    
    def test_production_cors_configuration(self):
        """Test production CORS allows only specific domains"""
        from backend.config import Settings
        
        prod_origins = "https://create-25.preview.emergentagent.com,https://fix-it-6.emergent.host"
        with patch.dict(os.environ, {"CORS_ORIGINS": prod_origins}):
            settings = Settings()
            
            # Should not include localhost
            assert not any("localhost" in origin for origin in settings.cors_origins)
            # Should only include https URLs
            assert all(origin.startswith("https://") for origin in settings.cors_origins)
    
    def test_production_jwt_secret_override(self):
        """Test production JWT secret is overridden"""
        from backend.config import Settings
        
        strong_secret = "prod-secret-" + "x" * 64
        with patch.dict(os.environ, {"JWT_SECRET": strong_secret}):
            settings = Settings()
            assert settings.jwt_secret != "your-secret-key-change-in-production"
            assert len(settings.jwt_secret) > 32
    
    def test_production_debug_disabled(self):
        """Test debug mode is disabled in production"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"DEBUG": "false"}):
            settings = Settings()
            assert settings.debug is False


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_environment_variables(self):
        """Test handling of empty environment variables"""
        from backend.config import Settings
        
        env_vars = {
            "OPENAI_API_KEY": "",
            "SENDGRID_API_KEY": "",
            "TWILIO_ACCOUNT_SID": ""
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            assert settings.openai_api_key == ""
            assert settings.sendgrid_api_key == ""
            assert settings.twilio_account_sid == ""
    
    def test_special_characters_in_secrets(self):
        """Test special characters in secret keys"""
        from backend.config import Settings
        
        special_secret = "key!@#$%^&*()_+-={}[]|:;<>?,./`~"
        with patch.dict(os.environ, {"JWT_SECRET": special_secret}):
            settings = Settings()
            assert settings.jwt_secret == special_secret
    
    def test_unicode_in_email_addresses(self):
        """Test unicode characters in email addresses"""
        from backend.config import Settings
        
        unicode_email = "admin@تست.ai"
        with patch.dict(os.environ, {"ADMIN_EMAIL": unicode_email}):
            settings = Settings()
            assert settings.admin_email == unicode_email
    
    def test_very_long_cors_origin_list(self):
        """Test handling of many CORS origins"""
        from backend.config import Settings
        
        origins = ",".join([f"https://domain{i}.example.com" for i in range(50)])
        with patch.dict(os.environ, {"CORS_ORIGINS": origins}):
            settings = Settings()
            assert len(settings.cors_origins) == 50
    
    def test_numeric_string_values(self):
        """Test numeric strings in text fields"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"DB_NAME": "12345"}):
            settings = Settings()
            assert settings.db_name == "12345"
            assert isinstance(settings.db_name, str)


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""
    
    def test_development_environment(self):
        """Test typical development environment configuration"""
        from backend.config import Settings
        
        dev_env = {
            "MONGO_URL": "mongodb://localhost:27017",
            "DEBUG": "true",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:8000"
        }
        
        with patch.dict(os.environ, dev_env):
            settings = Settings()
            assert settings.debug is True
            assert "localhost" in settings.cors_origins[0]
            assert settings.mongo_url == "mongodb://localhost:27017"
    
    def test_staging_environment(self):
        """Test typical staging environment configuration"""
        from backend.config import Settings
        
        staging_env = {
            "MONGO_URL": "mongodb://staging-db:27017/staging_db",
            "DEBUG": "false",
            "CORS_ORIGINS": "https://staging.example.com",
            "JWT_SECRET": "staging-secret-key-12345"
        }
        
        with patch.dict(os.environ, staging_env):
            settings = Settings()
            assert settings.debug is False
            assert "staging" in settings.mongo_url
            assert "staging.example.com" in settings.cors_origins[0]
    
    def test_production_environment(self):
        """Test typical production environment configuration"""
        from backend.config import Settings
        
        prod_env = {
            "MONGO_URL": "mongodb+srv://prod:password@cluster.mongodb.net/prod_db",
            "DEBUG": "false",
            "CORS_ORIGINS": "https://create-25.preview.emergentagent.com,https://fix-it-6.emergent.host",
            "JWT_SECRET": "production-secret-key-with-high-entropy-12345678",
            "OPENAI_API_KEY": "sk-prod-key",
            "SENDGRID_API_KEY": "SG.prod-key",
            "STRIPE_API_KEY": "sk_live_production"
        }
        
        with patch.dict(os.environ, prod_env):
            settings = Settings()
            assert settings.debug is False
            assert "mongodb+srv" in settings.mongo_url
            assert all("https://" in origin for origin in settings.cors_origins)
            assert settings.openai_api_key.startswith("sk-")
            assert settings.stripe_api_key.startswith("sk_live")


class TestBackwardsCompatibility:
    """Test backwards compatibility with old configurations"""
    
    def test_old_cors_format_single_origin(self):
        """Test old format with single CORS origin still works"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000"}):
            settings = Settings()
            assert isinstance(settings.cors_origins, list)
            assert len(settings.cors_origins) == 1
    
    def test_missing_optional_api_keys(self):
        """Test system works with missing optional API keys"""
        from backend.config import Settings
        
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            # Should not raise errors, uses empty string defaults
            assert settings.openai_api_key == ""
            assert settings.sendgrid_api_key == ""
            assert settings.twilio_account_sid == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])