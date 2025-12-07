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

# ============================================================================
# COMPREHENSIVE TESTS FOR CORS ORIGINS CONFIGURATION UPDATE
# Testing the updated CORS origins that include create-25.preview domain
# ============================================================================

class TestCORSOriginsConfiguration:
    """Test suite for CORS origins configuration changes"""
    
    def test_cors_origins_includes_new_preview_domain(self):
        """Test that CORS origins includes the new create-25 preview domain"""
        settings = Settings()
        expected_domain = "https://create-25.preview.emergentagent.com"
        assert expected_domain in settings.cors_origins, \
            f"Expected {expected_domain} in CORS origins"
    
    def test_cors_origins_includes_production_domain(self):
        """Test that CORS origins still includes production domain"""
        settings = Settings()
        expected_domain = "https://fix-it-6.emergent.host"
        assert expected_domain in settings.cors_origins, \
            f"Expected {expected_domain} in CORS origins"
    
    def test_cors_origins_includes_localhost(self):
        """Test that CORS origins includes localhost for development"""
        settings = Settings()
        assert "http://localhost:3000" in settings.cors_origins, \
            "Expected localhost:3000 in CORS origins for development"
    
    def test_cors_origins_count(self):
        """Test that CORS origins has exactly 3 domains configured"""
        settings = Settings()
        assert len(settings.cors_origins) == 3, \
            f"Expected 3 CORS origins, got {len(settings.cors_origins)}"
    
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins contains no duplicate entries"""
        settings = Settings()
        unique_origins = set(settings.cors_origins)
        assert len(unique_origins) == len(settings.cors_origins), \
            "CORS origins contains duplicate entries"
    
    def test_cors_origins_all_valid_urls(self):
        """Test that all CORS origins are valid URLs"""
        import re
        settings = Settings()
        url_pattern = re.compile(r'^https?://[a-zA-Z0-9.-]+(:\d+)?$')
        for origin in settings.cors_origins:
            assert url_pattern.match(origin), \
                f"Invalid URL format in CORS origin: {origin}"
    
    def test_cors_origins_https_for_production(self):
        """Test that production domains use HTTPS"""
        settings = Settings()
        for origin in settings.cors_origins:
            if 'localhost' not in origin:
                assert origin.startswith('https://'), \
                    f"Production domain should use HTTPS: {origin}"
    
    def test_cors_origins_no_trailing_slashes(self):
        """Test that CORS origins don't have trailing slashes"""
        settings = Settings()
        for origin in settings.cors_origins:
            assert not origin.endswith('/'), \
                f"CORS origin should not have trailing slash: {origin}"
    
    def test_cors_origins_from_env_variable(self, monkeypatch):
        """Test that CORS origins can be overridden by environment variable"""
        custom_origins = "https://custom1.com,https://custom2.com"
        monkeypatch.setenv("CORS_ORIGINS", custom_origins)
        settings = Settings()
        assert len(settings.cors_origins) == 2
        assert "https://custom1.com" in settings.cors_origins
        assert "https://custom2.com" in settings.cors_origins
    
    def test_cors_origins_env_variable_splits_correctly(self, monkeypatch):
        """Test that CORS_ORIGINS environment variable splits on commas"""
        origins = "http://test1.com,http://test2.com,http://test3.com"
        monkeypatch.setenv("CORS_ORIGINS", origins)
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert all(origin in settings.cors_origins for origin in origins.split(','))
    
    def test_cors_origins_empty_env_variable_uses_defaults(self, monkeypatch):
        """Test that empty CORS_ORIGINS environment variable falls back to defaults"""
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert "http://localhost:3000" in settings.cors_origins
    
    def test_cors_origins_whitespace_handling(self, monkeypatch):
        """Test that CORS origins handles whitespace in environment variable"""
        origins_with_spaces = " http://test1.com , http://test2.com "
        monkeypatch.setenv("CORS_ORIGINS", origins_with_spaces)
        settings = Settings()
        # Should handle whitespace gracefully
        assert len(settings.cors_origins) == 2
    
    def test_cors_origins_case_sensitivity(self):
        """Test that CORS origins preserves case sensitivity"""
        settings = Settings()
        for origin in settings.cors_origins:
            # Domain names should be lowercase
            domain = origin.split('://')[1] if '://' in origin else origin
            assert domain == domain.lower(), \
                f"Domain should be lowercase: {domain}"
    
    def test_cors_origins_no_wildcards(self):
        """Test that CORS origins doesn't contain wildcards"""
        settings = Settings()
        for origin in settings.cors_origins:
            assert '*' not in origin, \
                f"CORS origin should not contain wildcards: {origin}"
    
    def test_cors_origins_specific_domains_only(self):
        """Test that CORS origins only includes specific, expected domains"""
        settings = Settings()
        expected_domains = {
            "http://localhost:3000",
            "https://create-25.preview.emergentagent.com",
            "https://fix-it-6.emergent.host"
        }
        actual_domains = set(settings.cors_origins)
        assert actual_domains == expected_domains, \
            f"CORS origins mismatch. Expected: {expected_domains}, Got: {actual_domains}"


class TestConfigurationIntegrity:
    """Test suite for overall configuration integrity after CORS changes"""
    
    def test_settings_singleton_consistency(self):
        """Test that multiple Settings instances have same CORS configuration"""
        settings1 = Settings()
        settings2 = Settings()
        assert settings1.cors_origins == settings2.cors_origins, \
            "Settings instances should have consistent CORS origins"
    
    def test_cors_configuration_with_other_settings(self):
        """Test that CORS configuration works alongside other settings"""
        settings = Settings()
        # Verify CORS is set
        assert len(settings.cors_origins) > 0
        # Verify other critical settings are still accessible
        assert hasattr(settings, 'api_prefix')
        assert hasattr(settings, 'jwt_secret')
        assert hasattr(settings, 'mongo_url')
    
    def test_cors_origins_type_is_list(self):
        """Test that cors_origins is a list type"""
        settings = Settings()
        assert isinstance(settings.cors_origins, list), \
            f"cors_origins should be a list, got {type(settings.cors_origins)}"
    
    def test_cors_origins_contains_strings(self):
        """Test that all CORS origins are strings"""
        settings = Settings()
        for origin in settings.cors_origins:
            assert isinstance(origin, str), \
                f"CORS origin should be string, got {type(origin)}: {origin}"
    
    def test_cors_origins_non_empty_strings(self):
        """Test that CORS origins don't contain empty strings"""
        settings = Settings()
        for origin in settings.cors_origins:
            assert origin.strip() != '', \
                "CORS origins should not contain empty strings"


class TestCORSSecurityConsiderations:
    """Test suite for security aspects of CORS configuration"""
    
    def test_cors_no_insecure_protocols_in_production(self):
        """Test that production environments don't use insecure protocols"""
        settings = Settings()
        production_domains = [
            origin for origin in settings.cors_origins 
            if 'localhost' not in origin and '127.0.0.1' not in origin
        ]
        for domain in production_domains:
            assert domain.startswith('https://'), \
                f"Production domain must use HTTPS: {domain}"
    
    def test_cors_no_ip_addresses_in_origins(self):
        """Test that CORS origins use domain names, not IP addresses"""
        import re
        settings = Settings()
        ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        for origin in settings.cors_origins:
            # Localhost IP is acceptable
            if '127.0.0.1' in origin:
                continue
            assert not ip_pattern.search(origin), \
                f"CORS origin should use domain names: {origin}"
    
    def test_cors_origins_no_default_ports_exposed(self):
        """Test that CORS origins don't expose non-standard ports (except localhost)"""
        settings = Settings()
        for origin in settings.cors_origins:
            if 'localhost' in origin:
                continue  # Localhost can have ports
            # Check for port numbers in production URLs
            if ':' in origin.split('://')[1]:
                port = origin.split(':')[-1]
                assert port in ['80', '443'], \
                    f"Production URL should use standard ports: {origin}"


class TestCORSEnvironmentVariables:
    """Test suite for CORS configuration via environment variables"""
    
    def test_cors_env_override_single_domain(self, monkeypatch):
        """Test CORS configuration with single domain in env variable"""
        monkeypatch.setenv("CORS_ORIGINS", "https://single-domain.com")
        settings = Settings()
        assert len(settings.cors_origins) == 1
        assert settings.cors_origins[0] == "https://single-domain.com"
    
    def test_cors_env_override_multiple_domains(self, monkeypatch):
        """Test CORS configuration with multiple domains in env variable"""
        domains = "https://domain1.com,https://domain2.com,https://domain3.com"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert len(settings.cors_origins) == 3
    
    def test_cors_env_with_localhost_and_production(self, monkeypatch):
        """Test CORS configuration with mixed localhost and production domains"""
        domains = "http://localhost:3000,https://production.com"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert "http://localhost:3000" in settings.cors_origins
        assert "https://production.com" in settings.cors_origins
    
    def test_cors_env_malformed_handling(self, monkeypatch):
        """Test that malformed CORS_ORIGINS env variable is handled"""
        # Test with extra commas
        monkeypatch.setenv("CORS_ORIGINS", "https://domain1.com,,https://domain2.com")
        settings = Settings()
        # Should still parse valid domains
        assert any('domain1.com' in origin for origin in settings.cors_origins)


class TestCORSRegressionTests:
    """Regression tests to ensure CORS changes don't break existing functionality"""
    
    def test_cors_backward_compatibility_localhost(self):
        """Test that localhost:3000 is still supported for development"""
        settings = Settings()
        localhost_found = any('localhost:3000' in origin for origin in settings.cors_origins)
        assert localhost_found, "Localhost:3000 must remain in CORS origins for development"
    
    def test_cors_backward_compatibility_production(self):
        """Test that original production domain is still supported"""
        settings = Settings()
        prod_domain = "https://fix-it-6.emergent.host"
        assert prod_domain in settings.cors_origins, \
            f"Original production domain {prod_domain} must remain in CORS origins"
    
    def test_cors_new_preview_domain_added(self):
        """Test that the new preview domain was successfully added"""
        settings = Settings()
        new_domain = "https://create-25.preview.emergentagent.com"
        assert new_domain in settings.cors_origins, \
            f"New preview domain {new_domain} must be in CORS origins"
    
    def test_cors_old_preview_domain_replaced(self):
        """Test that the old preview domain was replaced"""
        settings = Settings()
        old_domain = "https://fix-it-6.preview.emergentagent.com"
        assert old_domain not in settings.cors_origins, \
            f"Old preview domain {old_domain} should be replaced"


class TestCORSEdgeCases:
    """Test edge cases in CORS configuration"""
    
    def test_cors_with_subdomain_variations(self, monkeypatch):
        """Test CORS with various subdomain patterns"""
        domains = "https://app.example.com,https://api.example.com,https://www.example.com"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert all(origin.endswith('example.com') for origin in settings.cors_origins)
    
    def test_cors_with_ports_in_development(self, monkeypatch):
        """Test CORS with explicit ports for development environments"""
        domains = "http://localhost:3000,http://localhost:3001,http://localhost:8080"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert all('localhost' in origin for origin in settings.cors_origins)
    
    def test_cors_unicode_domain_handling(self, monkeypatch):
        """Test that CORS configuration handles internationalized domains"""
        # Test with ASCII representation of internationalized domain
        domains = "https://xn--example-8k8a.com"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert "https://xn--example-8k8a.com" in settings.cors_origins
    
    def test_cors_very_long_domain_list(self, monkeypatch):
        """Test CORS with a large number of domains"""
        domains = ",".join([f"https://domain{i}.com" for i in range(50)])
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert len(settings.cors_origins) == 50
    
    def test_cors_special_characters_in_subdomain(self, monkeypatch):
        """Test CORS with special characters in subdomain (hyphens)"""
        domains = "https://my-app.example-site.com,https://test-env.staging-domain.io"
        monkeypatch.setenv("CORS_ORIGINS", domains)
        settings = Settings()
        assert len(settings.cors_origins) == 2
        assert all('-' in origin for origin in settings.cors_origins)

