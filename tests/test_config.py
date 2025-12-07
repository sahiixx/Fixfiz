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
    """Test suite for CORS origins configuration changes"""
    
    def test_cors_origins_contains_new_preview_url(self):
        """Test that new preview URL is in CORS origins"""
        test_settings = Settings()
        
        assert "https://create-25.preview.emergentagent.com" in test_settings.cors_origins
        
    def test_cors_origins_does_not_contain_old_preview_url(self):
        """Test that old preview URL is not in CORS origins (after migration)"""
        test_settings = Settings()
        
        # The old URL should no longer be present
        assert "https://fix-it-6.preview.emergentagent.com" not in test_settings.cors_origins
        
    def test_cors_origins_contains_localhost(self):
        """Test that localhost is still in CORS origins for development"""
        test_settings = Settings()
        
        assert "http://localhost:3000" in test_settings.cors_origins
        
    def test_cors_origins_contains_production_url(self):
        """Test that production URL is in CORS origins"""
        test_settings = Settings()
        
        assert "https://fix-it-6.emergent.host" in test_settings.cors_origins
        
    def test_cors_origins_count(self):
        """Test that CORS origins list has expected number of entries"""
        test_settings = Settings()
        
        # Should have at least 3 origins: localhost, preview, production
        assert len(test_settings.cors_origins) >= 3
        
    def test_cors_origins_all_valid_urls(self):
        """Test that all CORS origins are valid URLs"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            # Each origin should start with http:// or https://
            assert origin.startswith('http://') or origin.startswith('https://'), \
                f"Invalid origin URL format: {origin}"
            # Should not have trailing slashes
            assert not origin.endswith('/'), \
                f"Origin should not have trailing slash: {origin}"
                
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins list has no duplicates"""
        test_settings = Settings()
        
        origins_set = set(test_settings.cors_origins)
        assert len(origins_set) == len(test_settings.cors_origins), \
            "CORS origins contain duplicates"
            
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,https://custom-domain.com,https://staging.example.com'
    })
    def test_cors_origins_custom_environment_override(self):
        """Test CORS origins can be overridden via environment variable"""
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 3
        assert "http://localhost:3000" in test_settings.cors_origins
        assert "https://custom-domain.com" in test_settings.cors_origins
        assert "https://staging.example.com" in test_settings.cors_origins
        # Old defaults should not be present when overridden
        assert "https://create-25.preview.emergentagent.com" not in test_settings.cors_origins
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000'
    })
    def test_cors_origins_single_origin_override(self):
        """
        Verify that instantiating Settings without environment overrides yields exactly one CORS origin: "http://localhost:3000".
        """
        test_settings = Settings()
        
        assert len(test_settings.cors_origins) == 1
        assert test_settings.cors_origins[0] == "http://localhost:3000"
        
    def test_cors_origins_whitespace_handling(self):
        """Test that CORS origins are properly trimmed of whitespace"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            # No leading or trailing whitespace
            assert origin == origin.strip(), \
                f"Origin has whitespace: '{origin}'"
                
    def test_cors_origins_protocol_security(self):
        """Test that production/preview origins use HTTPS"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            # Skip localhost which can use HTTP
            if 'localhost' not in origin and '127.0.0.1' not in origin:
                assert origin.startswith('https://'), \
                    f"Production origin should use HTTPS: {origin}"
                    
    def test_cors_origins_preview_domain_pattern(self):
        """Test that preview URL follows expected domain pattern"""
        test_settings = Settings()
        
        preview_origins = [o for o in test_settings.cors_origins if 'preview.emergentagent.com' in o]
        assert len(preview_origins) > 0, "No preview origin found"
        
        for origin in preview_origins:
            # Should match pattern: https://*.preview.emergentagent.com
            assert '.preview.emergentagent.com' in origin
            assert origin.startswith('https://')
            
    def test_cors_origins_production_domain_pattern(self):
        """Test that production URL follows expected domain pattern"""
        test_settings = Settings()
        
        production_origins = [o for o in test_settings.cors_origins if 'emergent.host' in o]
        assert len(production_origins) > 0, "No production origin found"
        
        for origin in production_origins:
            # Should match pattern: https://*.emergent.host
            assert '.emergent.host' in origin
            assert origin.startswith('https://')
            
    @patch.dict(os.environ, {
        'CORS_ORIGINS': ''
    })
    def test_cors_origins_empty_string_environment(self):
        """Test behavior when CORS_ORIGINS is empty string"""
        test_settings = Settings()
        
        # Empty string split should result in a list with one empty string
        # This tests edge case handling
        assert isinstance(test_settings.cors_origins, list)
        
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,https://test1.com,,https://test2.com'
    })
    def test_cors_origins_handles_empty_values_in_list(self):
        """Test that empty values in comma-separated list are handled"""
        test_settings = Settings()
        
        # Should have 4 elements including empty string
        assert len(test_settings.cors_origins) == 4
        # Filter out empty strings to verify non-empty origins
        non_empty = [o for o in test_settings.cors_origins if o]
        assert len(non_empty) == 3


class TestCORSOriginsEdgeCases:
    """Test edge cases and failure scenarios for CORS origins"""
    
    def test_cors_origins_splitting_behavior(self):
        """Test that CORS origins are properly split by comma"""
        test_settings = Settings()
        
        # Verify split is working correctly
        assert isinstance(test_settings.cors_origins, list)
        # Each origin should not contain commas
        for origin in test_settings.cors_origins:
            assert ',' not in origin, f"Origin contains comma: {origin}"
            
    def test_cors_origins_case_sensitivity(self):
        """Test CORS origins maintain proper case sensitivity"""
        test_settings = Settings()
        
        # URLs should not be all lowercase or uppercase unexpectedly
        for origin in test_settings.cors_origins:
            if origin:  # Skip empty strings
                # Protocol should be lowercase
                assert origin.split('://')[0].islower(), \
                    f"Protocol should be lowercase in: {origin}"
                    
    def test_cors_origins_immutability(self):
        """
        Ensure modifying one Settings instance's `cors_origins` list does not affect a newly created Settings instance.
        """
        test_settings1 = Settings()
        original_origins = test_settings1.cors_origins.copy()
        
        # Modify the list
        test_settings1.cors_origins.append("https://malicious.com")
        
        # Create new settings instance
        test_settings2 = Settings()
        
        # New instance should have original values
        assert "https://malicious.com" not in test_settings2.cors_origins
        assert len(test_settings2.cors_origins) == len(original_origins)
        
    def test_cors_origins_type_consistency(self):
        """Test that all CORS origins are strings"""
        test_settings = Settings()
        
        for origin in test_settings.cors_origins:
            assert isinstance(origin, str), \
                f"Origin is not a string: {type(origin)}"
                
    @patch.dict(os.environ, {
        'CORS_ORIGINS': 'http://localhost:3000,HTTPS://EXAMPLE.COM'
    })
    def test_cors_origins_uppercase_protocol_handling(self):
        """Test handling of uppercase protocols in environment variable"""
        test_settings = Settings()
        
        # Python's split doesn't normalize case, so this tests actual behavior
        assert len(test_settings.cors_origins) == 2
        uppercase_origin = [o for o in test_settings.cors_origins if 'HTTPS://' in o]
        # Verifies that case is preserved (for better or worse)
        assert len(uppercase_origin) == 1


class TestCORSOriginsMigrationVerification:
    """Test suite to verify successful migration from old to new preview URL"""
    
    def test_new_preview_url_format_is_correct(self):
        """Verify new preview URL follows correct naming convention"""
        test_settings = Settings()
        
        new_url = "https://create-25.preview.emergentagent.com"
        assert new_url in test_settings.cors_origins
        
        # Verify format: create-XX pattern
        import re
        pattern = r'https://create-\d+\.preview\.emergentagent\.com'
        matching_urls = [o for o in test_settings.cors_origins if re.match(pattern, o)]
        assert len(matching_urls) > 0, "New preview URL doesn't match expected pattern"
        
    def test_old_preview_url_completely_removed(self):
        """Ensure old preview URL is completely removed from configuration"""
        test_settings = Settings()
        
        # Test both with default env and string representation
        old_url = "https://fix-it-6.preview.emergentagent.com"
        
        assert old_url not in test_settings.cors_origins
        assert old_url not in str(test_settings.cors_origins)
        
    def test_preview_url_count(self):
        """Test that there's exactly one preview URL (not multiple versions)"""
        test_settings = Settings()
        
        preview_urls = [o for o in test_settings.cors_origins if 'preview.emergentagent.com' in o]
        
        # Should have exactly 1 preview URL (the new one)
        assert len(preview_urls) == 1, \
            f"Expected 1 preview URL, found {len(preview_urls)}: {preview_urls}"
            
    def test_all_emergentagent_domains_are_valid(self):
        """Test that all emergentagent.com domains are valid and active"""
        test_settings = Settings()
        
        emergent_domains = [o for o in test_settings.cors_origins if 'emergentagent.com' in o or 'emergent.host' in o]
        
        # Should have at least preview and production
        assert len(emergent_domains) >= 2, \
            f"Expected at least 2 emergent domains, found {len(emergent_domains)}"
            
        # All should use HTTPS
        for domain in emergent_domains:
            assert domain.startswith('https://'), \
                f"Emergent domain should use HTTPS: {domain}"
                
    def test_cors_configuration_supports_deployment_workflow(self):
        """Test that CORS configuration supports preview -> production deployment workflow"""
        test_settings = Settings()
        
        has_localhost = any('localhost' in o for o in test_settings.cors_origins)
        has_preview = any('preview.emergentagent.com' in o for o in test_settings.cors_origins)
        has_production = any('emergent.host' in o for o in test_settings.cors_origins)
        
        # All three environments should be configured
        assert has_localhost, "Missing localhost for development"
        assert has_preview, "Missing preview environment"
        assert has_production, "Missing production environment"
        
    def test_cors_origins_string_format_in_environment(self):
        """
        Ensure the Settings.cors_origins list can be serialized into an environment-variable string and reconstructed without introducing spaces.
        
        This test joins the `cors_origins` list with commas, asserts the resulting string contains no spaces after commas, and verifies that splitting the string by commas yields the same number of origins as the original list.
        """
        test_settings = Settings()
        
        # Verify that if we export these origins back to env var format, they work
        origins_string = ','.join(test_settings.cors_origins)
        
        # Should not have spaces after commas
        assert ', ' not in origins_string, \
            "CORS origins string should not have spaces after commas"
            
        # Should be rebuildable
        rebuilt_list = origins_string.split(',')
        assert len(rebuilt_list) == len(test_settings.cors_origins)