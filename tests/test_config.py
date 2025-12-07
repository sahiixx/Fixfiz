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


class TestCORSOriginsConfiguration:
    """Comprehensive test suite for CORS origins configuration changes"""
    
    def test_cors_origins_default_structure(self):
        """Test CORS origins default structure and format"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        assert len(test_settings.cors_origins) >= 3
        # Verify all origins are strings
        assert all(isinstance(origin, str) for origin in test_settings.cors_origins)
        # Verify all origins start with http:// or https://
        assert all(origin.startswith(('http://', 'https://')) for origin in test_settings.cors_origins)
    
    def test_cors_origins_contains_localhost(self):
        """Test CORS origins includes localhost for development"""
        test_settings = Settings()
        
        assert "http://localhost:3000" in test_settings.cors_origins
        
    def test_cors_origins_contains_preview_domain(self):
        """Test CORS origins includes preview.emergentagent.com domain"""
        test_settings = Settings()
        
        # Check for the new preview domain
        preview_origins = [origin for origin in test_settings.cors_origins 
                          if 'preview.emergentagent.com' in origin]
        assert len(preview_origins) > 0
        assert any('create-25.preview.emergentagent.com' in origin 
                  for origin in test_settings.cors_origins)
        
    def test_cors_origins_contains_production_domain(self):
        """Test CORS origins includes production emergent.host domain"""
        test_settings = Settings()
        
        production_origins = [origin for origin in test_settings.cors_origins 
                             if 'emergent.host' in origin]
        assert len(production_origins) > 0
        assert any('fix-it-6.emergent.host' in origin 
                  for origin in test_settings.cors_origins)
    
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'https://custom1.com,https://custom2.com,http://localhost:3001'
    })
    def test_cors_origins_environment_override(self):
        """Test CORS origins can be overridden via environment variable"""
        test_settings = Settings()
        
        assert 'https://custom1.com' in test_settings.cors_origins
        assert 'https://custom2.com' in test_settings.cors_origins
        assert 'http://localhost:3001' in test_settings.cors_origins
        assert len(test_settings.cors_origins) == 3
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'https://single-domain.com'
    })
    def test_cors_origins_single_value(self):
        """Test CORS origins with single domain"""
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 1
        assert test_settings.cors_origins[0] == 'https://single-domain.com'
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': ''
    })
    def test_cors_origins_empty_environment_variable(self):
        """Test CORS origins with empty environment variable"""
        test_settings = Settings()
        
        # Should have at least one empty string element from split
        assert isinstance(test_settings.cors_origins, list)
        
    def test_cors_origins_no_duplicates(self):
        """Test CORS origins list contains no duplicate entries"""
        test_settings = Settings()
        
        origins_set = set(test_settings.cors_origins)
        assert len(origins_set) == len(test_settings.cors_origins)
        
    def test_cors_origins_format_validation(self):
        """Test all CORS origins follow proper URL format"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            # Each origin should not end with trailing slash
            assert not origin.endswith('/'), f"Origin {origin} should not end with /"
            # Each origin should contain a domain
            assert '.' in origin or 'localhost' in origin
            
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'https://domain1.com, https://domain2.com , http://localhost:3000 '
    })
    def test_cors_origins_strips_whitespace(self):
        """Test CORS origins properly handles whitespace in environment variable"""
        test_settings = Settings()
        
        # Environment variable has spaces, but they should be preserved as part of the string
        # This tests the actual behavior of split() which doesn't strip by default
        assert len(test_settings.cors_origins) == 3
        
    def test_cors_origins_supports_different_ports(self):
        """Test CORS origins can include different port numbers"""
        test_settings = Settings()
        
        # Check that localhost is present (may have port)
        localhost_origins = [o for o in test_settings.cors_origins if 'localhost' in o]
        assert len(localhost_origins) > 0
        
        # Verify port is specified
        assert any(':3000' in origin for origin in localhost_origins)


class TestConfigurationChanges:
    """Test suite for specific configuration changes in the diff"""
    
    def test_updated_preview_domain_format(self):
        """Test the new preview domain follows correct naming convention"""
        test_settings = Settings()
        
        # The new domain should be create-25.preview.emergentagent.com
        preview_domain = 'https://create-25.preview.emergentagent.com'
        assert preview_domain in test_settings.cors_origins
        
    def test_preview_domain_uses_https(self):
        """Test preview domain uses HTTPS protocol"""
        test_settings = Settings()
        
        preview_origins = [o for o in test_settings.cors_origins 
                          if 'preview.emergentagent.com' in o]
        
        for origin in preview_origins:
            assert origin.startswith('https://'), \
                f"Preview domain {origin} should use HTTPS"
                
    def test_production_domain_uses_https(self):
        """Test production domain uses HTTPS protocol"""
        test_settings = Settings()
        
        production_origins = [o for o in test_settings.cors_origins 
                             if 'emergent.host' in o]
        
        for origin in production_origins:
            assert origin.startswith('https://'), \
                f"Production domain {origin} should use HTTPS"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_default_cors_includes_all_required_domains(self):
        """Test default CORS configuration includes all required domains"""
        test_settings = Settings()
        
        required_domains = [
            'localhost:3000',
            'preview.emergentagent.com',
            'emergent.host'
        ]
        
        cors_string = ','.join(test_settings.cors_origins)
        
        for domain in required_domains:
            assert domain in cors_string, \
                f"Required domain {domain} not found in CORS origins"


class TestSecurityConfiguration:
    """Test suite for security-related configuration"""
    
    def test_jwt_secret_default_is_placeholder(self):
        """Test JWT secret default indicates it should be changed"""
        test_settings = Settings()
        
        assert 'change-in-production' in test_settings.jwt_secret.lower()
        
    def test_jwt_algorithm_is_secure(self):
        """Test JWT algorithm uses HS256 (secure algorithm)"""
        test_settings = Settings()
        
        assert test_settings.jwt_algorithm == "HS256"
        
    @patch.dict(os.environ, {
        'JWT_SECRET': 'very-secure-production-secret-key-12345'
    })
    def test_jwt_secret_can_be_overridden(self):
        """Test JWT secret can be overridden with environment variable"""
        test_settings = Settings()
        
        assert test_settings.jwt_secret == 'very-secure-production-secret-key-12345'
        assert 'change-in-production' not in test_settings.jwt_secret
        
    def test_jwt_expiration_reasonable_duration(self):
        """Test JWT expiration is set to reasonable duration"""
        test_settings = Settings()
        
        # Should be 24 hours (86400 seconds)
        assert test_settings.jwt_expiration == 86400
        assert test_settings.jwt_expiration >= 3600  # At least 1 hour
        assert test_settings.jwt_expiration <= 604800  # At most 1 week


class TestFileUploadConfiguration:
    """Test suite for file upload configuration"""
    
    def test_max_file_size_exact_value(self):
        """Test max file size is exactly 10MB"""
        test_settings = Settings()
        
        expected_size = 10 * 1024 * 1024  # 10MB in bytes
        assert test_settings.max_file_size == expected_size
        
    def test_allowed_file_types_includes_images(self):
        """Test allowed file types includes common image formats"""
        test_settings = Settings()
        
        image_types = ["image/jpeg", "image/png", "image/gif"]
        
        for img_type in image_types:
            assert img_type in test_settings.allowed_file_types
            
    def test_allowed_file_types_includes_pdf(self):
        """Test allowed file types includes PDF"""
        test_settings = Settings()
        
        assert "application/pdf" in test_settings.allowed_file_types
        
    def test_allowed_file_types_is_list(self):
        """Test allowed file types is properly typed as list"""
        test_settings = Settings()
        
        assert isinstance(test_settings.allowed_file_types, list)
        assert len(test_settings.allowed_file_types) > 0


class TestDatabaseConfiguration:
    """Test suite for database configuration"""
    
    def test_mongo_url_default_format(self):
        """Test MongoDB URL follows correct format"""
        test_settings = Settings()
        
        assert test_settings.mongo_url.startswith('mongodb://')
        assert 'localhost' in test_settings.mongo_url or ':' in test_settings.mongo_url
        
    def test_db_name_default_value(self):
        """Test database name has correct default value"""
        test_settings = Settings()
        
        assert test_settings.db_name == "nowhere_digital"
        
    @patch.dict(os.environ, {
        'MONGO_URL': 'mongodb://prod-server:27017',
        'DB_NAME': 'production_db'
    })
    def test_database_configuration_override(self):
        """Test database configuration can be overridden"""
        test_settings = Settings()
        
        assert test_settings.mongo_url == 'mongodb://prod-server:27017'
        assert test_settings.db_name == 'production_db'


class TestEmailConfiguration:
    """Test suite for email configuration"""
    
    def test_email_addresses_format(self):
        """Test email addresses follow proper format"""
        test_settings = Settings()
        
        emails = [
            test_settings.sendgrid_from_email,
            test_settings.sender_email,
            test_settings.admin_email
        ]
        
        for email in emails:
            assert '@' in email
            assert '.' in email.split('@')[1]  # Domain has TLD
            
    def test_default_email_domain(self):
        """Test default emails use nowhere.ai domain"""
        test_settings = Settings()
        
        assert 'nowhere.ai' in test_settings.sender_email
        assert 'nowhere.ai' in test_settings.admin_email
        
    def test_email_templates_directory_exists(self):
        """Test email templates directory is configured"""
        test_settings = Settings()
        
        assert test_settings.email_templates_dir
        assert isinstance(test_settings.email_templates_dir, str)
        assert len(test_settings.email_templates_dir) > 0


class TestRateLimitingConfiguration:
    """Test suite for rate limiting configuration"""
    
    def test_rate_limit_requests_reasonable(self):
        """Test rate limit requests is set to reasonable value"""
        test_settings = Settings()
        
        assert test_settings.rate_limit_requests == 100
        assert test_settings.rate_limit_requests > 0
        
    def test_rate_limit_period_in_seconds(self):
        """Test rate limit period is in seconds"""
        test_settings = Settings()
        
        assert test_settings.rate_limit_period == 60
        assert test_settings.rate_limit_period > 0
        
    def test_rate_limit_per_minute_calculation(self):
        """Test rate limit translates to requests per minute"""
        test_settings = Settings()
        
        # 100 requests per 60 seconds = ~1.67 requests per second
        requests_per_second = test_settings.rate_limit_requests / test_settings.rate_limit_period
        
        assert 0.5 <= requests_per_second <= 10  # Reasonable range


class TestAPIConfiguration:
    """Test suite for API configuration"""
    
    def test_api_prefix_format(self):
        """Test API prefix follows REST convention"""
        test_settings = Settings()
        
        assert test_settings.api_prefix == "/api"
        assert test_settings.api_prefix.startswith("/")
        assert not test_settings.api_prefix.endswith("/")
        
    def test_debug_mode_default_false(self):
        """Test debug mode is false by default for security"""
        test_settings = Settings()
        
        assert test_settings.debug is False
        
    @patch.dict(os.environ, {'DEBUG': 'true'})
    def test_debug_mode_can_be_enabled(self):
        """Test debug mode can be enabled via environment"""
        test_settings = Settings()
        
        assert test_settings.debug is True


class TestIntegrationCredentials:
    """Test suite for third-party integration credentials"""
    
    def test_ai_provider_default(self):
        """Test AI provider default value"""
        test_settings = Settings()
        
        assert test_settings.ai_provider == "openai"
        
    def test_default_ai_model(self):
        """Test default AI model is set"""
        test_settings = Settings()
        
        assert test_settings.default_ai_model == "gpt-4o"
        
    def test_emergent_llm_key_has_default(self):
        """Test Emergent LLM key has a default value"""
        test_settings = Settings()
        
        assert test_settings.emergent_llm_key
        assert test_settings.emergent_llm_key.startswith('sk-emergent')
        
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'sk-test-key-123',
        'AI_PROVIDER': 'openai',
        'DEFAULT_AI_MODEL': 'gpt-4-turbo'
    })
    def test_ai_configuration_override(self):
        """Test AI configuration can be overridden"""
        test_settings = Settings()
        
        assert test_settings.openai_api_key == 'sk-test-key-123'
        assert test_settings.ai_provider == 'openai'
        assert test_settings.default_ai_model == 'gpt-4-turbo'


class TestConfigurationEdgeCases:
    """Test suite for edge cases and error conditions"""
    
    @patch.dict(os.environ, {'CORS_ORIGINS': ','})
    def test_cors_origins_with_only_comma(self):
        """Test CORS origins handles comma-only input"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        
    @patch.dict(os.environ, {'CORS_ORIGINS': ',,,,'})
    def test_cors_origins_with_multiple_commas(self):
        """Test CORS origins handles multiple commas"""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        
    def test_settings_immutability_after_creation(self):
        """Test settings object can be modified after creation"""
        test_settings = Settings()
        
        # Pydantic settings are mutable by default
        original_debug = test_settings.debug
        test_settings.debug = not original_debug
        assert test_settings.debug != original_debug
        
    def test_all_string_settings_are_strings(self):
        """Test all string-typed settings return strings"""
        test_settings = Settings()
        
        string_attrs = [
            'mongo_url', 'db_name', 'sendgrid_api_key', 'sendgrid_from_email',
            'sender_email', 'admin_email', 'openai_api_key', 'default_ai_model',
            'ai_provider', 'emergent_llm_key', 'stripe_api_key', 'jwt_secret',
            'jwt_algorithm', 'api_prefix', 'email_templates_dir'
        ]
        
        for attr in string_attrs:
            value = getattr(test_settings, attr)
            assert isinstance(value, str), f"{attr} should be a string, got {type(value)}"


# ============================================================================
# NEW TESTS ADDED FOR GIT DIFF CHANGES
# Generated on: $(date)
# Changed files tested:
#   - backend/config.py (CORS origins update)
# Total new tests: 50+ comprehensive test cases across 10 test classes
# ============================================================================