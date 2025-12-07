"""
Comprehensive Unit Tests for Configuration Settings
Tests the Settings class in backend/config.py

This test suite covers:
- Environment variable loading and defaults
- CORS origins parsing and validation
- Database configuration
- Email settings (SendGrid)
- AI provider settings (OpenAI, Emergent)
- Payment settings (Stripe)
- SMS settings (Twilio)
- Security settings (JWT)
- API configuration
- File upload settings
- Rate limiting configuration
- Edge cases and error handling
Total: 30+ comprehensive unit tests
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from typing import List

# Import the Settings class
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import Settings


# ================================================================================================
# SETTINGS INITIALIZATION TESTS
# ================================================================================================

class TestSettingsInitialization:
    """Tests for Settings class initialization and default values"""
    
    def test_settings_initialization_with_defaults(self):
        """Test Settings initialization uses default values when no env vars set"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Database defaults
            assert settings.mongo_url == "mongodb://localhost:27017"
            assert settings.db_name == "nowhere_digital"
            
            # Email defaults
            assert settings.sendgrid_api_key == ""
            assert settings.sendgrid_from_email == "noreply@nowhere.ai"
            assert settings.sender_email == "hello@nowhere.ai"
            assert settings.admin_email == "admin@nowhere.ai"
    
    def test_settings_initialization_with_env_vars(self):
        """Test Settings initialization uses environment variables when provided"""
        test_env = {
            "MONGO_URL": "mongodb://test-db:27017",
            "DB_NAME": "test_database",
            "SENDGRID_API_KEY": "test_api_key_123",
            "SENDGRID_FROM_EMAIL": "test@example.com",
            "OPENAI_API_KEY": "test_openai_key",
            "STRIPE_API_KEY": "test_stripe_key"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.mongo_url == "mongodb://test-db:27017"
            assert settings.db_name == "test_database"
            assert settings.sendgrid_api_key == "test_api_key_123"
            assert settings.sendgrid_from_email == "test@example.com"
            assert settings.openai_api_key == "test_openai_key"
            assert settings.stripe_api_key == "test_stripe_key"
    
    def test_settings_empty_string_values(self):
        """Test Settings handles empty string environment variables correctly"""
        test_env = {
            "SENDGRID_API_KEY": "",
            "OPENAI_API_KEY": "",
            "STRIPE_API_KEY": ""
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.sendgrid_api_key == ""
            assert settings.openai_api_key == ""
            assert settings.stripe_api_key == ""


# ================================================================================================
# CORS ORIGINS TESTS
# ================================================================================================

class TestCORSOrigins:
    """Comprehensive tests for CORS origins configuration"""
    
    def test_cors_origins_default_value(self):
        """Test CORS origins uses correct default value"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert isinstance(settings.cors_origins, list)
            assert len(settings.cors_origins) == 3
            assert "http://localhost:3000" in settings.cors_origins
            assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
            assert "https://fix-it-6.emergent.host" in settings.cors_origins
    
    def test_cors_origins_from_environment_single(self):
        """Test CORS origins parsing with single origin"""
        with patch.dict(os.environ, {"CORS_ORIGINS": "https://example.com"}, clear=True):
            settings = Settings()
            
            assert settings.cors_origins == ["https://example.com"]
    
    def test_cors_origins_from_environment_multiple(self):
        """Test CORS origins parsing with multiple origins"""
        cors_string = "http://localhost:3000,https://app.example.com,https://api.example.com"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": cors_string}, clear=True):
            settings = Settings()
            
            assert len(settings.cors_origins) == 3
            assert "http://localhost:3000" in settings.cors_origins
            assert "https://app.example.com" in settings.cors_origins
            assert "https://api.example.com" in settings.cors_origins
    
    def test_cors_origins_with_whitespace(self):
        """Test CORS origins handles whitespace in comma-separated list"""
        cors_string = "http://localhost:3000 , https://app.example.com , https://api.example.com"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": cors_string}, clear=True):
            settings = Settings()
            
            # Should preserve whitespace as split is done on comma only
            assert len(settings.cors_origins) == 3
    
    def test_cors_origins_empty_string(self):
        """Test CORS origins with empty string"""
        with patch.dict(os.environ, {"CORS_ORIGINS": ""}, clear=True):
            settings = Settings()
            
            assert settings.cors_origins == [""]
    
    def test_cors_origins_updated_preview_url(self):
        """Test that the default CORS origins includes the updated preview URL"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Verify the new preview URL is present (from the recent change)
            assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
            # Verify it's not the old URL
            assert "https://fix-it-6.preview.emergentagent.com" not in settings.cors_origins
    
    def test_cors_origins_localhost_variants(self):
        """Test CORS origins with various localhost formats"""
        cors_string = "http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": cors_string}, clear=True):
            settings = Settings()
            
            assert len(settings.cors_origins) == 3
            assert "http://localhost:3000" in settings.cors_origins
            assert "http://127.0.0.1:3000" in settings.cors_origins
            assert "http://0.0.0.0:3000" in settings.cors_origins
    
    def test_cors_origins_with_trailing_slashes(self):
        """Test CORS origins preserves trailing slashes"""
        cors_string = "http://localhost:3000/,https://app.example.com/"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": cors_string}, clear=True):
            settings = Settings()
            
            assert "http://localhost:3000/" in settings.cors_origins
            assert "https://app.example.com/" in settings.cors_origins


# ================================================================================================
# DATABASE CONFIGURATION TESTS
# ================================================================================================

class TestDatabaseConfiguration:
    """Tests for database-related settings"""
    
    def test_database_default_mongo_url(self):
        """Test default MongoDB URL"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.mongo_url == "mongodb://localhost:27017"
    
    def test_database_custom_mongo_url(self):
        """Test custom MongoDB URL from environment"""
        mongo_url = "mongodb://user:pass@prod-db.example.com:27017/dbname?authSource=admin"
        
        with patch.dict(os.environ, {"MONGO_URL": mongo_url}, clear=True):
            settings = Settings()
            
            assert settings.mongo_url == mongo_url
    
    def test_database_default_name(self):
        """Test default database name"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.db_name == "nowhere_digital"
    
    def test_database_custom_name(self):
        """Test custom database name from environment"""
        with patch.dict(os.environ, {"DB_NAME": "production_db"}, clear=True):
            settings = Settings()
            
            assert settings.db_name == "production_db"
    
    def test_database_mongodb_atlas_url(self):
        """Test MongoDB Atlas connection string"""
        atlas_url = "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority"
        
        with patch.dict(os.environ, {"MONGO_URL": atlas_url}, clear=True):
            settings = Settings()
            
            assert settings.mongo_url == atlas_url


# ================================================================================================
# EMAIL CONFIGURATION TESTS
# ================================================================================================

class TestEmailConfiguration:
    """Tests for email-related settings (SendGrid)"""
    
    def test_email_sendgrid_defaults(self):
        """Test SendGrid default values"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.sendgrid_api_key == ""
            assert settings.sendgrid_from_email == "noreply@nowhere.ai"
            assert settings.sender_email == "hello@nowhere.ai"
            assert settings.admin_email == "admin@nowhere.ai"
    
    def test_email_sendgrid_custom_values(self):
        """Test SendGrid custom values from environment"""
        test_env = {
            "SENDGRID_API_KEY": "SG.test_key_123",
            "SENDGRID_FROM_EMAIL": "noreply@example.com",
            "SENDER_EMAIL": "hello@example.com",
            "ADMIN_EMAIL": "admin@example.com"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.sendgrid_api_key == "SG.test_key_123"
            assert settings.sendgrid_from_email == "noreply@example.com"
            assert settings.sender_email == "hello@example.com"
            assert settings.admin_email == "admin@example.com"
    
    def test_email_valid_email_formats(self):
        """Test various valid email formats"""
        test_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com"
        ]
        
        for email in test_emails:
            with patch.dict(os.environ, {"ADMIN_EMAIL": email}, clear=True):
                settings = Settings()
                assert settings.admin_email == email


# ================================================================================================
# AI PROVIDER CONFIGURATION TESTS
# ================================================================================================

class TestAIConfiguration:
    """Tests for AI provider settings"""
    
    def test_ai_default_settings(self):
        """Test AI provider default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.openai_api_key == ""
            assert settings.default_ai_model == "gpt-4o"
            assert settings.ai_provider == "openai"
            assert settings.emergent_llm_key == "sk-emergent-8A3Bc7c1f91F43cE8D"
    
    def test_ai_custom_openai_settings(self):
        """Test custom OpenAI settings"""
        test_env = {
            "OPENAI_API_KEY": "sk-test123",
            "DEFAULT_AI_MODEL": "gpt-4-turbo",
            "AI_PROVIDER": "openai"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.openai_api_key == "sk-test123"
            assert settings.default_ai_model == "gpt-4-turbo"
            assert settings.ai_provider == "openai"
    
    def test_ai_emergent_provider(self):
        """Test Emergent AI provider settings"""
        test_env = {
            "AI_PROVIDER": "emergent",
            "EMERGENT_LLM_KEY": "sk-emergent-custom-key"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.ai_provider == "emergent"
            assert settings.emergent_llm_key == "sk-emergent-custom-key"
    
    def test_ai_different_models(self):
        """Test various AI model configurations"""
        models = ["gpt-4", "gpt-4o", "gpt-3.5-turbo", "claude-3-opus"]
        
        for model in models:
            with patch.dict(os.environ, {"DEFAULT_AI_MODEL": model}, clear=True):
                settings = Settings()
                assert settings.default_ai_model == model


# ================================================================================================
# PAYMENT CONFIGURATION TESTS
# ================================================================================================

class TestPaymentConfiguration:
    """Tests for payment settings (Stripe)"""
    
    def test_payment_default_stripe_key(self):
        """Test default Stripe API key"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.stripe_api_key == "sk_test_emergent"
    
    def test_payment_custom_stripe_key(self):
        """Test custom Stripe API key"""
        test_key = "sk_live_abc123xyz"
        
        with patch.dict(os.environ, {"STRIPE_API_KEY": test_key}, clear=True):
            settings = Settings()
            
            assert settings.stripe_api_key == test_key
    
    def test_payment_stripe_test_mode(self):
        """Test Stripe test mode key format"""
        test_key = "sk_test_51abc123"
        
        with patch.dict(os.environ, {"STRIPE_API_KEY": test_key}, clear=True):
            settings = Settings()
            
            assert settings.stripe_api_key.startswith("sk_test_")
    
    def test_payment_stripe_live_mode(self):
        """Test Stripe live mode key format"""
        live_key = "sk_live_51abc123"
        
        with patch.dict(os.environ, {"STRIPE_API_KEY": live_key}, clear=True):
            settings = Settings()
            
            assert settings.stripe_api_key.startswith("sk_live_")


# ================================================================================================
# SMS CONFIGURATION TESTS (TWILIO)
# ================================================================================================

class TestSMSConfiguration:
    """Tests for SMS settings (Twilio)"""
    
    def test_sms_default_twilio_settings(self):
        """Test Twilio default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.twilio_account_sid == ""
            assert settings.twilio_auth_token == ""
            assert settings.twilio_verify_service == ""
            assert settings.twilio_phone_number == ""
    
    def test_sms_custom_twilio_settings(self):
        """Test custom Twilio settings"""
        test_env = {
            "TWILIO_ACCOUNT_SID": "AC123abc",
            "TWILIO_AUTH_TOKEN": "auth_token_123",
            "TWILIO_VERIFY_SERVICE": "VA123abc",
            "TWILIO_PHONE_NUMBER": "+1234567890"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.twilio_account_sid == "AC123abc"
            assert settings.twilio_auth_token == "auth_token_123"
            assert settings.twilio_verify_service == "VA123abc"
            assert settings.twilio_phone_number == "+1234567890"
    
    def test_sms_international_phone_formats(self):
        """Test various international phone number formats"""
        phone_numbers = [
            "+971501234567",  # UAE
            "+1234567890",    # US
            "+447123456789",  # UK
            "+33123456789"    # France
        ]
        
        for phone in phone_numbers:
            with patch.dict(os.environ, {"TWILIO_PHONE_NUMBER": phone}, clear=True):
                settings = Settings()
                assert settings.twilio_phone_number == phone


# ================================================================================================
# SECURITY CONFIGURATION TESTS
# ================================================================================================

class TestSecurityConfiguration:
    """Tests for security-related settings"""
    
    def test_security_jwt_defaults(self):
        """Test JWT default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.jwt_secret == "your-secret-key-change-in-production"
            assert settings.jwt_algorithm == "HS256"
            assert settings.jwt_expiration == 24 * 60 * 60  # 24 hours in seconds
    
    def test_security_custom_jwt_secret(self):
        """Test custom JWT secret"""
        custom_secret = "super-secure-production-secret-key-12345"
        
        with patch.dict(os.environ, {"JWT_SECRET": custom_secret}, clear=True):
            settings = Settings()
            
            assert settings.jwt_secret == custom_secret
            assert settings.jwt_algorithm == "HS256"
    
    def test_security_jwt_expiration_value(self):
        """Test JWT expiration is correctly set in seconds"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # 24 hours = 86400 seconds
            assert settings.jwt_expiration == 86400
            assert settings.jwt_expiration == 24 * 60 * 60


# ================================================================================================
# API CONFIGURATION TESTS
# ================================================================================================

class TestAPIConfiguration:
    """Tests for API-related settings"""
    
    def test_api_default_settings(self):
        """Test API default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.api_prefix == "/api"
            assert settings.debug is False
    
    def test_api_debug_mode_true(self):
        """Test API debug mode enabled"""
        with patch.dict(os.environ, {"DEBUG": "true"}, clear=True):
            settings = Settings()
            
            assert settings.debug is True
    
    def test_api_debug_mode_false(self):
        """Test API debug mode disabled"""
        with patch.dict(os.environ, {"DEBUG": "false"}, clear=True):
            settings = Settings()
            
            assert settings.debug is False
    
    def test_api_debug_mode_case_insensitive(self):
        """Test API debug mode is case insensitive"""
        test_values = ["TRUE", "True", "TrUe"]
        
        for value in test_values:
            with patch.dict(os.environ, {"DEBUG": value}, clear=True):
                settings = Settings()
                assert settings.debug is True
    
    def test_api_debug_mode_invalid_values(self):
        """Test API debug mode with invalid values defaults to False"""
        test_values = ["yes", "1", "enabled", ""]
        
        for value in test_values:
            with patch.dict(os.environ, {"DEBUG": value}, clear=True):
                settings = Settings()
                assert settings.debug is False


# ================================================================================================
# FILE UPLOAD CONFIGURATION TESTS
# ================================================================================================

class TestFileUploadConfiguration:
    """Tests for file upload settings"""
    
    def test_file_upload_default_settings(self):
        """Test file upload default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.max_file_size == 10 * 1024 * 1024  # 10MB in bytes
            assert isinstance(settings.allowed_file_types, list)
            assert len(settings.allowed_file_types) == 4
    
    def test_file_upload_allowed_types(self):
        """Test allowed file types list"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert "image/jpeg" in settings.allowed_file_types
            assert "image/png" in settings.allowed_file_types
            assert "image/gif" in settings.allowed_file_types
            assert "application/pdf" in settings.allowed_file_types
    
    def test_file_upload_max_size_calculation(self):
        """Test max file size is correctly calculated"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # 10MB = 10 * 1024 * 1024 bytes = 10485760 bytes
            assert settings.max_file_size == 10485760


# ================================================================================================
# RATE LIMITING CONFIGURATION TESTS
# ================================================================================================

class TestRateLimitConfiguration:
    """Tests for rate limiting settings"""
    
    def test_rate_limit_default_settings(self):
        """Test rate limiting default settings"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.rate_limit_requests == 100
            assert settings.rate_limit_period == 60  # seconds
    
    def test_rate_limit_requests_per_minute(self):
        """Test rate limit is 100 requests per 60 seconds (1 minute)"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            requests_per_minute = settings.rate_limit_requests
            period_seconds = settings.rate_limit_period
            
            assert requests_per_minute == 100
            assert period_seconds == 60


# ================================================================================================
# EMAIL TEMPLATES CONFIGURATION TESTS
# ================================================================================================

class TestEmailTemplatesConfiguration:
    """Tests for email templates settings"""
    
    def test_email_templates_default_directory(self):
        """Test email templates default directory"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.email_templates_dir == "email_templates"


# ================================================================================================
# INTEGRATION TESTS
# ================================================================================================

class TestSettingsIntegration:
    """Integration tests for Settings class"""
    
    def test_settings_all_env_vars_loaded(self):
        """Test Settings loads all environment variables correctly"""
        comprehensive_env = {
            "MONGO_URL": "mongodb://test:27017",
            "DB_NAME": "test_db",
            "SENDGRID_API_KEY": "SG.test",
            "SENDGRID_FROM_EMAIL": "from@test.com",
            "SENDER_EMAIL": "sender@test.com",
            "ADMIN_EMAIL": "admin@test.com",
            "OPENAI_API_KEY": "sk-openai-test",
            "DEFAULT_AI_MODEL": "gpt-4",
            "AI_PROVIDER": "openai",
            "EMERGENT_LLM_KEY": "sk-emergent-test",
            "STRIPE_API_KEY": "sk_test_stripe",
            "TWILIO_ACCOUNT_SID": "AC123",
            "TWILIO_AUTH_TOKEN": "token123",
            "TWILIO_VERIFY_SERVICE": "VA123",
            "TWILIO_PHONE_NUMBER": "+1234567890",
            "JWT_SECRET": "test-secret",
            "CORS_ORIGINS": "http://localhost:3000,https://test.com",
            "DEBUG": "true"
        }
        
        with patch.dict(os.environ, comprehensive_env, clear=True):
            settings = Settings()
            
            # Verify all values are loaded
            assert settings.mongo_url == "mongodb://test:27017"
            assert settings.db_name == "test_db"
            assert settings.sendgrid_api_key == "SG.test"
            assert settings.openai_api_key == "sk-openai-test"
            assert settings.stripe_api_key == "sk_test_stripe"
            assert settings.jwt_secret == "test-secret"
            assert settings.debug is True
            assert len(settings.cors_origins) == 2
    
    def test_settings_partial_env_vars_with_defaults(self):
        """Test Settings uses defaults for missing environment variables"""
        partial_env = {
            "MONGO_URL": "mongodb://custom:27017",
            "OPENAI_API_KEY": "sk-custom-key"
        }
        
        with patch.dict(os.environ, partial_env, clear=True):
            settings = Settings()
            
            # Custom values
            assert settings.mongo_url == "mongodb://custom:27017"
            assert settings.openai_api_key == "sk-custom-key"
            
            # Default values
            assert settings.db_name == "nowhere_digital"
            assert settings.sendgrid_api_key == ""
            assert settings.jwt_algorithm == "HS256"
    
    def test_settings_singleton_behavior(self):
        """Test Settings instance can be created multiple times"""
        with patch.dict(os.environ, {"DB_NAME": "test_db"}, clear=True):
            settings1 = Settings()
            settings2 = Settings()
            
            # Both instances should have the same configuration
            assert settings1.db_name == settings2.db_name == "test_db"
    
    def test_settings_cors_origins_production_like(self):
        """Test CORS origins with production-like configuration"""
        production_cors = "https://app.nowhere.ai,https://api.nowhere.ai,https://www.nowhere.ai"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": production_cors}, clear=True):
            settings = Settings()
            
            assert len(settings.cors_origins) == 3
            assert all(origin.startswith("https://") for origin in settings.cors_origins)
            assert "https://app.nowhere.ai" in settings.cors_origins


# ================================================================================================
# EDGE CASES AND ERROR HANDLING TESTS
# ================================================================================================

class TestSettingsEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_settings_very_long_jwt_secret(self):
        """Test Settings handles very long JWT secret"""
        long_secret = "a" * 1000
        
        with patch.dict(os.environ, {"JWT_SECRET": long_secret}, clear=True):
            settings = Settings()
            
            assert settings.jwt_secret == long_secret
            assert len(settings.jwt_secret) == 1000
    
    def test_settings_special_characters_in_values(self):
        """Test Settings handles special characters in values"""
        special_secret = "test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        
        with patch.dict(os.environ, {"JWT_SECRET": special_secret}, clear=True):
            settings = Settings()
            
            assert settings.jwt_secret == special_secret
    
    def test_settings_unicode_in_email(self):
        """Test Settings handles unicode characters"""
        unicode_email = "admin@tëst.com"
        
        with patch.dict(os.environ, {"ADMIN_EMAIL": unicode_email}, clear=True):
            settings = Settings()
            
            assert settings.admin_email == unicode_email
    
    def test_settings_cors_origins_single_comma(self):
        """Test CORS origins with single comma (empty string in list)"""
        with patch.dict(os.environ, {"CORS_ORIGINS": ","}, clear=True):
            settings = Settings()
            
            assert len(settings.cors_origins) == 2
            assert settings.cors_origins == ["", ""]
    
    def test_settings_cors_origins_many_commas(self):
        """Test CORS origins with multiple consecutive commas"""
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://a.com,,,http://b.com"}, clear=True):
            settings = Settings()
            
            assert len(settings.cors_origins) == 4
            assert "http://a.com" in settings.cors_origins
            assert "http://b.com" in settings.cors_origins
    
    def test_settings_numeric_string_values(self):
        """Test Settings handles numeric string values correctly"""
        with patch.dict(os.environ, {"DB_NAME": "12345"}, clear=True):
            settings = Settings()
            
            assert settings.db_name == "12345"
            assert isinstance(settings.db_name, str)