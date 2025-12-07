"""
Unit tests for backend/config.py
Tests configuration management and environment variable handling
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from backend.config import Settings, settings


class TestSettings:
    """Test suite for Settings configuration class"""
    
    def test_default_settings(self):
        """Test that default settings are properly initialized"""
        test_settings = Settings()
        
        assert test_settings.mongo_url == "mongodb://localhost:27017"
        assert test_settings.db_name == "nowhere_digital"
        assert test_settings.jwt_algorithm == "HS256"
        assert test_settings.jwt_expiration == 24 * 60 * 60
        assert test_settings.debug is False
        
    def test_cors_origins_list(self):
        """Test CORS origins are properly defined"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        assert len(test_settings.cors_origins) > 0
        assert "http://localhost:3000" in test_settings.cors_origins
        
    def test_allowed_file_types(self):
        """Test allowed file types configuration"""
        test_settings = Settings()
        
        assert isinstance(test_settings.allowed_file_types, list)
        assert "image/jpeg" in test_settings.allowed_file_types
        assert "image/png" in test_settings.allowed_file_types
        assert "application/pdf" in test_settings.allowed_file_types
        
    def test_max_file_size(self):
        """Test max file size is within reasonable bounds"""
        test_settings = Settings()
        
        assert test_settings.max_file_size == 10 * 1024 * 1024  # 10MB
        assert test_settings.max_file_size > 0
        
    def test_rate_limiting_config(self):
        """Test rate limiting configuration"""
        test_settings = Settings()
        
        assert test_settings.rate_limit_requests == 100
        assert test_settings.rate_limit_period == 60
        assert test_settings.rate_limit_period > 0
        
    @patch.dict(os.environ, {
        'MONGO_URL': 'mongodb://testhost:27017',
        'DB_NAME': 'test_db',
        'DEBUG': 'true',
        'JWT_SECRET': 'test-secret-key'
    })
    def test_environment_variable_override(self):
        """Test that environment variables override default settings"""
        test_settings = Settings()
        
        assert test_settings.mongo_url == 'mongodb://testhost:27017'
        assert test_settings.db_name == 'test_db'
        assert test_settings.debug is True
        assert test_settings.jwt_secret == 'test-secret-key'  # noqa: S105
        
    @patch.dict(os.environ, {
        'SENDGRID_API_KEY': 'sg-test-key',
        'SENDGRID_FROM_EMAIL': 'test@example.com',
        'ADMIN_EMAIL': 'admin@test.com'
    })
    def test_email_configuration(self):
        """Test email configuration from environment"""
        test_settings = Settings()
        
        assert test_settings.sendgrid_api_key == 'sg-test-key'
        assert test_settings.sendgrid_from_email == 'test@example.com'
        assert test_settings.admin_email == 'admin@test.com'
        
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'sk-test-openai',
        'EMERGENT_LLM_KEY': 'sk-test-emergent',
        'DEFAULT_AI_MODEL': 'gpt-4'
    })
    def test_ai_configuration(self):
        """Test AI service configuration"""
        test_settings = Settings()
        
        assert test_settings.openai_api_key == 'sk-test-openai'
        assert test_settings.emergent_llm_key == 'sk-test-emergent'
        assert test_settings.default_ai_model == 'gpt-4'
        assert test_settings.ai_provider == 'openai'
        
    @patch.dict(os.environ, {
        'STRIPE_API_KEY': 'sk_test_stripe',
        'TWILIO_ACCOUNT_SID': 'ACtest123',
        'TWILIO_AUTH_TOKEN': 'test_token',
        'TWILIO_VERIFY_SERVICE': 'VAtest123'
    })
    def test_integration_credentials(self):
        """Test third-party integration credentials"""
        test_settings = Settings()
        
        assert test_settings.stripe_api_key == 'sk_test_stripe'
        assert test_settings.twilio_account_sid == 'ACtest123'
        assert test_settings.twilio_auth_token == 'test_token'  # noqa: S105
        assert test_settings.twilio_verify_service == 'VAtest123'
        
    def test_api_prefix(self):
        """Test API prefix configuration"""
        test_settings = Settings()
        
        assert test_settings.api_prefix == "/api"
        assert test_settings.api_prefix.startswith("/")
        
    def test_email_templates_directory(self):
        """Test email templates directory configuration"""
        test_settings = Settings()
        
        assert test_settings.email_templates_dir == "email_templates"
        assert isinstance(test_settings.email_templates_dir, str)
        
    def test_global_settings_instance(self):
        """Test global settings instance is accessible"""
        assert settings is not None
        assert isinstance(settings, Settings)


class TestSettingsValidation:
    """Test configuration validation and edge cases"""
    
    @patch.dict(os.environ, {'DEBUG': 'false'})
    def test_debug_false_string(self):
        """Test debug mode with 'false' string"""
        test_settings = Settings()
        assert test_settings.debug is False
        
    @patch.dict(os.environ, {'DEBUG': 'True'})
    def test_debug_true_capitalized(self):
        """Test debug mode with capitalized 'True'"""
        test_settings = Settings()
        assert test_settings.debug is True
        
    @patch.dict(os.environ, {'DEBUG': '1'})
    def test_debug_with_numeric_value(self):
        """Test debug mode with numeric value"""
        test_settings = Settings()
        # Should be false since it's not "true"
        assert test_settings.debug is False
        
    def test_jwt_expiration_is_positive(self):
        """Test JWT expiration is a positive number"""
        test_settings = Settings()
        assert test_settings.jwt_expiration > 0
        
    def test_rate_limits_are_reasonable(self):
        """Test rate limit values are within reasonable bounds"""
        test_settings = Settings()
        
        assert 0 < test_settings.rate_limit_requests <= 10000
        assert 0 < test_settings.rate_limit_period <= 3600

    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,https://create-25.preview.emergentagent.com,https://fix-it-6.emergent.host'
    })
    def test_cors_origins_with_new_preview_url(self):
        """Test CORS origins with the new create-25 preview URL"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        assert len(test_settings.cors_origins) == 3
        assert "http://localhost:3000" in test_settings.cors_origins
        assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
        assert "https://fix-it-6.emergent.host" in test_settings.cors_origins
        
    def test_cors_origins_default_includes_preview_url(self):
        """Test that default CORS origins include the new preview URL"""
        test_settings = Settings()
        
        # Check that the new preview URL is in defaults
        assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'https://example.com,https://test.com'
    })
    def test_cors_origins_custom_override(self):
        """Test CORS origins can be fully overridden via environment"""
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 2
        assert "https://example.com" in test_settings.cors_origins
        assert "https://test.com" in test_settings.cors_origins
        assert "http://localhost:3000" not in test_settings.cors_origins
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'https://single-origin.com'
    })
    def test_cors_origins_single_value(self):
        """Test CORS origins with a single value"""
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 1
        assert test_settings.cors_origins[0] == "https://single-origin.com"
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': ''
    })
    def test_cors_origins_empty_string(self):
        """Test CORS origins with empty string"""
        test_settings = Settings()
        
        # Empty string split results in ['']
        assert isinstance(test_settings.cors_origins, list)
        
    def test_cors_origins_url_format_validation(self):
        """Test that CORS origins are valid URL formats"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            # Each origin should start with http:// or https://
            assert origin.startswith('http://') or origin.startswith('https://'), \
                f"Invalid origin format: {origin}"
                
    def test_cors_origins_no_trailing_slashes(self):
        """Test that CORS origins don't have trailing slashes"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            assert not origin.endswith('/'), \
                f"Origin should not have trailing slash: {origin}"
                
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,https://api.example.com,https://app.example.com'
    })
    def test_cors_origins_multiple_domains(self):
        """Test CORS origins with multiple different domains"""
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 3
        # Verify no duplicates
        assert len(set(test_settings.cors_origins)) == len(test_settings.cors_origins)
        
    def test_cors_origins_preserves_order(self):
        """Test that CORS origins maintain their order"""
        test_settings = Settings()
        
        # Default should have localhost first
        assert test_settings.cors_origins[0] == "http://localhost:3000"


class TestCORSSecurityValidation:
    """Test CORS security configurations and edge cases"""
    
    def test_cors_origins_localhost_development(self):
        """Test localhost is available for development"""
        test_settings = Settings()
        
        localhost_origins = [o for o in test_settings.cors_origins if 'localhost' in o]
        assert len(localhost_origins) > 0, "Localhost should be in CORS origins for development"
        
    def test_cors_origins_https_production(self):
        """Test production origins use HTTPS"""
        test_settings = Settings()
        
        production_origins = [o for o in test_settings.cors_origins if 'localhost' not in o]
        for origin in production_origins:
            assert origin.startswith('https://'), \
                f"Production origin must use HTTPS: {origin}"
                
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://unsecure.com,https://secure.com'
    })
    def test_cors_mixed_http_https_warning(self):
        """Test handling of mixed HTTP/HTTPS origins"""
        test_settings = Settings()
        
        http_origins = [o for o in test_settings.cors_origins if o.startswith('http://')]
        https_origins = [o for o in test_settings.cors_origins if o.startswith('https://')]
        
        # Both should be present as configured
        assert len(http_origins) > 0
        assert len(https_origins) > 0
        
    def test_cors_origins_wildcard_not_present(self):
        """Test that wildcards are not used in CORS origins"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            assert '*' not in origin, \
                "Wildcard CORS origins are a security risk"
                
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,http://localhost:3001,https://staging.example.com'
    })
    def test_cors_multiple_localhost_ports(self):
        """Test handling multiple localhost ports"""
        test_settings = Settings()
        
        localhost_origins = [o for o in test_settings.cors_origins if 'localhost' in o]
        assert len(localhost_origins) == 2
        assert "http://localhost:3000" in test_settings.cors_origins
        assert "http://localhost:3001" in test_settings.cors_origins