"""
Comprehensive Unit Tests for Configuration Management (backend/config.py)

This test suite covers:
- Settings initialization with environment variables
- CORS origins parsing and validation
- Default value handling
- Security settings validation
- File upload configuration
- Rate limiting settings
- Edge cases and failure conditions

Total: 25+ comprehensive unit tests
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from typing import List

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import Settings, settings


# ================================================================================================
# SETTINGS INITIALIZATION TESTS
# ================================================================================================

class TestSettingsInitialization:
    """Tests for Settings class initialization and environment variable handling"""
    
    def test_default_settings_initialization(self):
        """Test Settings initializes with default values when no env vars set"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.mongo_url == "mongodb://localhost:27017"
            assert test_settings.db_name == "nowhere_digital"
            assert test_settings.jwt_algorithm == "HS256"
            assert test_settings.jwt_expiration == 24 * 60 * 60
    
    def test_settings_with_environment_variables(self):
        """Test Settings reads from environment variables correctly"""
        test_env = {
            'MONGO_URL': 'mongodb://testhost:27017',
            'DB_NAME': 'test_database',
            'SENDGRID_API_KEY': 'sg_test_key_123',
            'OPENAI_API_KEY': 'sk-test-openai-key',
            'JWT_SECRET': 'test-secret-key-xyz'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.mongo_url == 'mongodb://testhost:27017'
            assert test_settings.db_name == 'test_database'
            assert test_settings.sendgrid_api_key == 'sg_test_key_123'
            assert test_settings.openai_api_key == 'sk-test-openai-key'
            assert test_settings.jwt_secret == 'test-secret-key-xyz'
    
    def test_settings_email_configuration(self):
        """Test email-related settings are properly configured"""
        test_env = {
            'SENDGRID_API_KEY': 'sg_live_key',
            'SENDGRID_FROM_EMAIL': 'noreply@company.com',
            'SENDER_EMAIL': 'hello@company.com',
            'ADMIN_EMAIL': 'admin@company.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.sendgrid_api_key == 'sg_live_key'
            assert test_settings.sendgrid_from_email == 'noreply@company.com'
            assert test_settings.sender_email == 'hello@company.com'
            assert test_settings.admin_email == 'admin@company.com'
    
    def test_settings_ai_configuration(self):
        """Test AI-related settings including provider and model selection"""
        test_env = {
            'OPENAI_API_KEY': 'sk-test-key',
            'DEFAULT_AI_MODEL': 'gpt-4o-mini',
            'AI_PROVIDER': 'openai',
            'EMERGENT_LLM_KEY': 'sk-emergent-custom-key'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.openai_api_key == 'sk-test-key'
            assert test_settings.default_ai_model == 'gpt-4o-mini'
            assert test_settings.ai_provider == 'openai'
            assert test_settings.emergent_llm_key == 'sk-emergent-custom-key'
    
    def test_settings_payment_configuration(self):
        """Test Stripe payment settings"""
        test_env = {
            'STRIPE_API_KEY': 'sk_live_test_key'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.stripe_api_key == 'sk_live_test_key'
    
    def test_settings_sms_configuration(self):
        """Test Twilio SMS settings"""
        test_env = {
            'TWILIO_ACCOUNT_SID': 'AC123456789',
            'TWILIO_AUTH_TOKEN': 'test_auth_token',
            'TWILIO_VERIFY_SERVICE': 'VA987654321',
            'TWILIO_PHONE_NUMBER': '+1234567890'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.twilio_account_sid == 'AC123456789'
            assert test_settings.twilio_auth_token == 'test_auth_token'
            assert test_settings.twilio_verify_service == 'VA987654321'
            assert test_settings.twilio_phone_number == '+1234567890'


# ================================================================================================
# CORS CONFIGURATION TESTS
# ================================================================================================

class TestCORSConfiguration:
    """Tests for CORS origins parsing and validation"""
    
    def test_cors_origins_default_values(self):
        """Test CORS origins default configuration includes all required domains"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert isinstance(test_settings.cors_origins, list)
            assert len(test_settings.cors_origins) == 3
            assert "http://localhost:3000" in test_settings.cors_origins
            assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
            assert "https://fix-it-6.emergent.host" in test_settings.cors_origins
    
    def test_cors_origins_custom_single_origin(self):
        """Test CORS with single custom origin"""
        test_env = {
            'CORS_ORIGINS': 'https://custom.domain.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.cors_origins == ['https://custom.domain.com']
    
    def test_cors_origins_multiple_custom_origins(self):
        """Test CORS with multiple comma-separated origins"""
        test_env = {
            'CORS_ORIGINS': 'https://app1.com,https://app2.com,https://app3.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert len(test_settings.cors_origins) == 3
            assert 'https://app1.com' in test_settings.cors_origins
            assert 'https://app2.com' in test_settings.cors_origins
            assert 'https://app3.com' in test_settings.cors_origins
    
    def test_cors_origins_with_localhost_and_production(self):
        """Test CORS configuration with both localhost and production URLs"""
        test_env = {
            'CORS_ORIGINS': 'http://localhost:3000,http://localhost:8080,https://prod.example.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert len(test_settings.cors_origins) == 3
            assert 'http://localhost:3000' in test_settings.cors_origins
            assert 'http://localhost:8080' in test_settings.cors_origins
            assert 'https://prod.example.com' in test_settings.cors_origins
    
    def test_cors_origins_with_whitespace(self):
        """Test CORS parsing handles whitespace in origin list"""
        test_env = {
            'CORS_ORIGINS': 'https://app1.com, https://app2.com , https://app3.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            # Note: Current implementation doesn't strip whitespace
            # This test documents actual behavior
            assert len(test_settings.cors_origins) == 3
    
    def test_cors_origins_preserves_order(self):
        """Test CORS origins preserve the order from environment variable"""
        test_env = {
            'CORS_ORIGINS': 'https://first.com,https://second.com,https://third.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.cors_origins[0] == 'https://first.com'
            assert test_settings.cors_origins[1] == 'https://second.com'
            assert test_settings.cors_origins[2] == 'https://third.com'
    
    def test_cors_origins_changed_preview_domain(self):
        """Test that the CORS configuration includes the updated preview domain"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            # Verify the new preview domain is included (from the git diff)
            assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
            # Verify the old domain is NOT present
            assert "https://fix-it-6.preview.emergentagent.com" not in test_settings.cors_origins


# ================================================================================================
# SECURITY SETTINGS TESTS
# ================================================================================================

class TestSecuritySettings:
    """Tests for security-related configuration"""
    
    def test_jwt_secret_default_value(self):
        """Test JWT secret has appropriate default value"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.jwt_secret == "your-secret-key-change-in-production"
            assert test_settings.jwt_algorithm == "HS256"
    
    def test_jwt_secret_custom_value(self):
        """Test JWT secret can be customized via environment"""
        test_env = {
            'JWT_SECRET': 'super-secure-production-key-xyz123'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.jwt_secret == 'super-secure-production-key-xyz123'
    
    def test_jwt_expiration_default(self):
        """Test JWT expiration is set to 24 hours by default"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.jwt_expiration == 86400  # 24 * 60 * 60
    
    def test_debug_mode_default_false(self):
        """Test debug mode is False by default"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.debug is False
    
    def test_debug_mode_enabled(self):
        """Test debug mode can be enabled via environment"""
        test_env = {
            'DEBUG': 'true'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.debug is True
    
    def test_debug_mode_case_insensitive(self):
        """Test debug mode parsing is case-insensitive"""
        for value in ['True', 'TRUE', 'true', 'TrUe']:
            test_env = {'DEBUG': value}
            with patch.dict(os.environ, test_env, clear=True):
                test_settings = Settings()
                assert test_settings.debug is True
    
    def test_debug_mode_false_values(self):
        """Test debug mode is False for non-true values"""
        for value in ['false', 'False', 'no', '0', '', 'anything']:
            test_env = {'DEBUG': value}
            with patch.dict(os.environ, test_env, clear=True):
                test_settings = Settings()
                assert test_settings.debug is False


# ================================================================================================
# FILE UPLOAD CONFIGURATION TESTS
# ================================================================================================

class TestFileUploadConfiguration:
    """Tests for file upload settings"""
    
    def test_max_file_size_default(self):
        """Test maximum file size is set to 10MB by default"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.max_file_size == 10 * 1024 * 1024  # 10MB in bytes
    
    def test_allowed_file_types_default(self):
        """Test allowed file types include common formats"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert isinstance(test_settings.allowed_file_types, list)
            assert "image/jpeg" in test_settings.allowed_file_types
            assert "image/png" in test_settings.allowed_file_types
            assert "image/gif" in test_settings.allowed_file_types
            assert "application/pdf" in test_settings.allowed_file_types
            assert len(test_settings.allowed_file_types) == 4


# ================================================================================================
# RATE LIMITING TESTS
# ================================================================================================

class TestRateLimitingConfiguration:
    """Tests for rate limiting settings"""
    
    def test_rate_limit_defaults(self):
        """Test rate limiting has sensible default values"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.rate_limit_requests == 100
            assert test_settings.rate_limit_period == 60  # seconds


# ================================================================================================
# API SETTINGS TESTS
# ================================================================================================

class TestAPISettings:
    """Tests for API configuration"""
    
    def test_api_prefix_default(self):
        """Test API prefix is set correctly"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.api_prefix == "/api"
    
    def test_email_templates_directory(self):
        """Test email templates directory configuration"""
        with patch.dict(os.environ, {}, clear=True):
            test_settings = Settings()
            
            assert test_settings.email_templates_dir == "email_templates"


# ================================================================================================
# GLOBAL SETTINGS INSTANCE TEST
# ================================================================================================

class TestGlobalSettingsInstance:
    """Tests for the global settings instance"""
    
    def test_global_settings_instance_exists(self):
        """Test that a global settings instance is created"""
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_global_settings_has_cors_origins(self):
        """Test global settings instance has CORS origins configured"""
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) > 0


# ================================================================================================
# EDGE CASES AND ERROR HANDLING
# ================================================================================================

class TestEdgeCasesAndErrorHandling:
    """Tests for edge cases and error conditions"""
    
    def test_empty_environment_variables(self):
        """Test settings handle empty string environment variables"""
        test_env = {
            'SENDGRID_API_KEY': '',
            'OPENAI_API_KEY': '',
            'STRIPE_API_KEY': ''
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            # Empty strings should be preserved, not converted to defaults
            assert test_settings.sendgrid_api_key == ''
            assert test_settings.openai_api_key == ''
    
    def test_cors_origins_empty_string(self):
        """Test CORS origins with empty string environment variable"""
        test_env = {
            'CORS_ORIGINS': ''
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            # Empty string split by comma results in ['']
            assert isinstance(test_settings.cors_origins, list)
            assert len(test_settings.cors_origins) == 1
            assert test_settings.cors_origins[0] == ''
    
    def test_settings_config_class_attributes(self):
        """Test Settings.Config class has correct attributes"""
        assert hasattr(Settings.Config, 'env_file')
        assert Settings.Config.env_file == ".env"
        assert Settings.Config.env_file_encoding == "utf-8"


# ================================================================================================
# INTEGRATION TESTS
# ================================================================================================

class TestSettingsIntegration:
    """Integration tests for settings across multiple configurations"""
    
    def test_production_like_configuration(self):
        """Test settings with production-like environment variables"""
        test_env = {
            'MONGO_URL': 'mongodb://prod-cluster:27017',
            'DB_NAME': 'production_db',
            'SENDGRID_API_KEY': 'sg_live_key',
            'OPENAI_API_KEY': 'sk-live-key',
            'STRIPE_API_KEY': 'sk_live_stripe',
            'JWT_SECRET': 'very-secure-production-secret',
            'DEBUG': 'false',
            'CORS_ORIGINS': 'https://app.production.com,https://api.production.com'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.mongo_url == 'mongodb://prod-cluster:27017'
            assert test_settings.debug is False
            assert 'https://app.production.com' in test_settings.cors_origins
            assert test_settings.jwt_secret != "your-secret-key-change-in-production"
    
    def test_development_configuration(self):
        """Test settings with development environment variables"""
        test_env = {
            'DEBUG': 'true',
            'CORS_ORIGINS': 'http://localhost:3000,http://localhost:8000'
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            test_settings = Settings()
            
            assert test_settings.debug is True
            assert 'http://localhost:3000' in test_settings.cors_origins
            assert test_settings.mongo_url == 'mongodb://localhost:27017'


# ================================================================================================
# RUN ALL TESTS
# ================================================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])