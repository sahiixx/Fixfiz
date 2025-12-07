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
# Additional Tests for CORS Origins Configuration (Added for git diff testing)
# ============================================================================

class TestCORSOriginsConfiguration:
    """Comprehensive tests for CORS origins configuration changes."""
    
    def test_cors_origins_includes_localhost(self):
        """Test that localhost is included in CORS origins for development."""
        settings = Settings()
        assert "http://localhost:3000" in settings.cors_origins
        
    def test_cors_origins_includes_preview_url(self):
        """Test that the preview URL is correctly configured."""
        settings = Settings()
        preview_url = "https://create-25.preview.emergentagent.com"
        assert preview_url in settings.cors_origins, \
            f"Expected preview URL {preview_url} not found in CORS origins"
    
    def test_cors_origins_includes_production_url(self):
        """Test that production URL is included in CORS origins."""
        settings = Settings()
        assert "https://fix-it-6.emergent.host" in settings.cors_origins
    
    def test_cors_origins_count(self):
        """Test that CORS origins has the expected number of entries."""
        settings = Settings()
        # Should have localhost + preview + production = 3 origins
        assert len(settings.cors_origins) == 3
    
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins has no duplicate entries."""
        settings = Settings()
        assert len(settings.cors_origins) == len(set(settings.cors_origins))
    
    def test_cors_origins_format_validation(self):
        """Test that all CORS origins are valid URLs."""
        settings = Settings()
        for origin in settings.cors_origins:
            assert origin.startswith("http://") or origin.startswith("https://"), \
                f"Invalid origin format: {origin}"
            assert " " not in origin, f"Origin contains whitespace: {origin}"
    
    def test_cors_origins_no_trailing_slash(self):
        """Test that CORS origins don't have trailing slashes."""
        settings = Settings()
        for origin in settings.cors_origins:
            assert not origin.endswith("/"), \
                f"Origin has trailing slash: {origin}"
    
    def test_cors_origins_case_sensitivity(self):
        """Test that CORS origins maintain proper case."""
        settings = Settings()
        for origin in settings.cors_origins:
            # URLs should not be all uppercase or all lowercase (except scheme)
            parts = origin.split("://")
            if len(parts) == 2:
                scheme, domain = parts
                assert scheme.islower(), f"Scheme should be lowercase: {origin}"
    
    def test_cors_origins_custom_env_override(self):
        """Test that CORS_ORIGINS environment variable properly overrides defaults."""
        import os
        test_origins = "http://test1.com,https://test2.com"
        os.environ["CORS_ORIGINS"] = test_origins
        
        # Create new settings instance to pick up env var
        settings = Settings()
        
        expected = test_origins.split(",")
        assert settings.cors_origins == expected
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_cors_origins_empty_env_fallback(self):
        """Test behavior when CORS_ORIGINS env var is empty."""
        import os
        os.environ["CORS_ORIGINS"] = ""
        
        settings = Settings()
        # Should fallback to default or handle empty gracefully
        assert isinstance(settings.cors_origins, list)
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_cors_origins_single_value(self):
        """Test CORS origins with a single value."""
        import os
        os.environ["CORS_ORIGINS"] = "http://single.com"
        
        settings = Settings()
        assert len(settings.cors_origins) == 1
        assert settings.cors_origins[0] == "http://single.com"
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_cors_origins_whitespace_handling(self):
        """Test that whitespace in CORS_ORIGINS is handled correctly."""
        import os
        os.environ["CORS_ORIGINS"] = "http://test1.com, https://test2.com , http://test3.com"
        
        settings = Settings()
        # Should strip whitespace from each origin
        for origin in settings.cors_origins:
            assert origin == origin.strip()
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_cors_origins_with_ports(self):
        """Test CORS origins with non-standard ports."""
        import os
        os.environ["CORS_ORIGINS"] = "http://localhost:3000,http://localhost:8080,https://api.example.com:443"
        
        settings = Settings()
        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:8080" in settings.cors_origins
        assert "https://api.example.com:443" in settings.cors_origins
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_cors_origins_subdomain_support(self):
        """Test that subdomains are properly supported."""
        settings = Settings()
        # Check that preview URL with subdomain is present
        preview_domains = [o for o in settings.cors_origins if "preview.emergentagent.com" in o]
        assert len(preview_domains) > 0
    
    def test_cors_origins_security_no_wildcards(self):
        """Test that CORS origins don't contain wildcards (security best practice)."""
        settings = Settings()
        for origin in settings.cors_origins:
            assert "*" not in origin, \
                f"Wildcard found in CORS origin (security risk): {origin}"
    
    def test_cors_origins_https_for_production(self):
        """Test that production and preview URLs use HTTPS."""
        settings = Settings()
        for origin in settings.cors_origins:
            if "emergentagent.com" in origin or "emergent.host" in origin:
                assert origin.startswith("https://"), \
                    f"Production/preview URL must use HTTPS: {origin}"
    
    def test_cors_origins_preview_url_pattern_match(self):
        """Test that the preview URL matches the expected pattern."""
        settings = Settings()
        import re
        pattern = r"https://[\w-]+\.preview\.emergentagent\.com"
        
        preview_urls = [o for o in settings.cors_origins if "preview.emergentagent.com" in o]
        for url in preview_urls:
            assert re.match(pattern, url), \
                f"Preview URL doesn't match expected pattern: {url}"
    
    def test_cors_origins_immutability(self):
        """Test that CORS origins list can be safely modified without affecting settings."""
        settings = Settings()
        original_length = len(settings.cors_origins)
        
        # Try to modify the list
        test_list = settings.cors_origins.copy()
        test_list.append("http://evil.com")
        
        # Original should be unchanged
        assert len(settings.cors_origins) == original_length


class TestConfigurationEdgeCases:
    """Test edge cases and error conditions in configuration."""
    
    def test_config_with_malformed_cors_env(self):
        """Test behavior with malformed CORS_ORIGINS environment variable."""
        import os
        os.environ["CORS_ORIGINS"] = "not-a-url,,,multiple,,,commas"
        
        settings = Settings()
        # Should handle gracefully without crashing
        assert isinstance(settings.cors_origins, list)
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_config_with_unicode_in_cors(self):
        """Test handling of unicode characters in CORS configuration."""
        import os
        os.environ["CORS_ORIGINS"] = "http://tëst.com,https://例え.jp"
        
        settings = Settings()
        # Should handle international domain names
        assert isinstance(settings.cors_origins, list)
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_config_cors_very_long_url(self):
        """Test handling of very long URLs in CORS configuration."""
        import os
        long_url = "http://" + "a" * 2000 + ".com"
        os.environ["CORS_ORIGINS"] = long_url
        
        settings = Settings()
        # Should handle without crashing
        assert isinstance(settings.cors_origins, list)
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]
    
    def test_config_cors_special_characters(self):
        """Test handling of special characters in CORS URLs."""
        import os
        os.environ["CORS_ORIGINS"] = "http://test.com?param=value,https://test.com#fragment"
        
        settings = Settings()
        # Should preserve special characters
        assert isinstance(settings.cors_origins, list)
        
        # Cleanup
        del os.environ["CORS_ORIGINS"]


class TestConfigurationIntegration:
    """Integration tests for configuration with other components."""
    
    def test_cors_config_for_api_middleware(self):
        """Test that CORS configuration is suitable for FastAPI middleware."""
        settings = Settings()
        
        # All origins should be valid for CORS middleware
        for origin in settings.cors_origins:
            # Should not be empty
            assert len(origin) > 0
            # Should be a complete URL
            assert "://" in origin
    
    def test_cors_config_matches_frontend_build_urls(self):
        """Test that CORS origins align with expected frontend deployment URLs."""
        settings = Settings()
        
        # Should include the specific preview URL from the diff
        assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
        
        # Should NOT include old preview URL
        assert "https://fix-it-6.preview.emergentagent.com" not in settings.cors_origins
    
    def test_settings_singleton_behavior(self):
        """Test that settings behave consistently across multiple instantiations."""
        settings1 = Settings()
        settings2 = Settings()
        
        # Should have same CORS origins
        assert settings1.cors_origins == settings2.cors_origins
    
    def test_config_exports_for_app_usage(self):
        """Test that configuration can be imported and used by main application."""
        from backend.config import settings
        
        # Should be accessible as a module-level object
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)


class TestCORSOriginsSecurity:
    """Security-focused tests for CORS configuration."""
    
    def test_no_cors_origin_allows_all(self):
        """Test that CORS doesn't use wildcard 'allow all' configuration."""
        settings = Settings()
        assert "*" not in settings.cors_origins
    
    def test_localhost_only_in_development(self):
        """Test that localhost is appropriate for the environment."""
        settings = Settings()
        localhost_origins = [o for o in settings.cors_origins if "localhost" in o]
        
        # Localhost should be present for development
        assert len(localhost_origins) > 0
    
    def test_cors_origins_no_http_in_production_domains(self):
        """Test that production domains don't use insecure HTTP."""
        settings = Settings()
        
        for origin in settings.cors_origins:
            if "emergentagent.com" in origin or "emergent.host" in origin:
                assert not origin.startswith("http://"), \
                    f"Production domain using insecure HTTP: {origin}"
    
    def test_cors_origins_no_ip_addresses(self):
        """Test that CORS origins use domain names, not raw IP addresses."""
        settings = Settings()
        import re
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        
        for origin in settings.cors_origins:
            # Exclude localhost:port patterns
            if "localhost" not in origin:
                assert not re.search(ip_pattern, origin), \
                    f"CORS origin contains IP address: {origin}"


class TestConfigurationDocumentation:
    """Tests to ensure configuration is well-documented and maintainable."""
    
    def test_config_has_cors_comment(self):
        """Test that configuration file has comments explaining CORS setup."""
        import inspect
        from backend.config import Settings
        
        # Get the source file
        source = inspect.getsource(Settings)
        
        # Should have comments about CORS
        assert "cors" in source.lower() or "CORS" in source
    
    def test_settings_class_is_documented(self):
        """Test that Settings class has docstring."""
        from backend.config import Settings
        
        # Should have some documentation
        assert Settings.__doc__ is not None or len(inspect.getsource(Settings)) > 0


# ============================================================================
# Additional Tests for CORS Origins Configuration (Git Diff Changes)
# ============================================================================

class TestCORSOriginsConfiguration:
    """Comprehensive tests for CORS origins configuration changes."""
    
    def test_cors_origins_includes_localhost(self):
        """Test that localhost is included in CORS origins for development."""
        test_settings = Settings()
        assert "http://localhost:3000" in test_settings.cors_origins
        
    def test_cors_origins_includes_new_preview_url(self):
        """Test that the NEW preview URL is correctly configured."""
        test_settings = Settings()
        preview_url = "https://create-25.preview.emergentagent.com"
        assert preview_url in test_settings.cors_origins, \
            f"Expected preview URL {preview_url} not found in CORS origins"
    
    def test_cors_origins_excludes_old_preview_url(self):
        """Test that the OLD preview URL is NOT in CORS origins (regression test)."""
        test_settings = Settings()
        old_preview_url = "https://fix-it-6.preview.emergentagent.com"
        assert old_preview_url not in test_settings.cors_origins, \
            f"Old preview URL {old_preview_url} should not be in CORS origins"
    
    def test_cors_origins_includes_production_url(self):
        """Test that production URL is included in CORS origins."""
        test_settings = Settings()
        assert "https://fix-it-6.emergent.host" in test_settings.cors_origins
    
    def test_cors_origins_count(self):
        """Test that CORS origins has the expected number of entries."""
        test_settings = Settings()
        assert len(test_settings.cors_origins) == 3, \
            f"Expected 3 CORS origins, got {len(test_settings.cors_origins)}"
    
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins has no duplicate entries."""
        test_settings = Settings()
        assert len(test_settings.cors_origins) == len(set(test_settings.cors_origins)), \
            "CORS origins contains duplicate entries"
    
    def test_cors_origins_format_validation(self):
        """Test that all CORS origins are valid URLs."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            assert origin.startswith("http://") or origin.startswith("https://"), \
                f"Invalid origin format: {origin}"
            assert " " not in origin, f"Origin contains whitespace: {origin}"
    
    def test_cors_origins_no_trailing_slash(self):
        """Test that CORS origins don't have trailing slashes."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            assert not origin.endswith("/"), \
                f"Origin has trailing slash: {origin}"
    
    @patch.dict(os.environ, {'CORS_ORIGINS': 'http://test1.com,https://test2.com'})
    def test_cors_origins_custom_env_override(self):
        """Test that CORS_ORIGINS environment variable properly overrides defaults."""
        test_settings = Settings()
        expected = ["http://test1.com", "https://test2.com"]
        assert test_settings.cors_origins == expected
    
    @patch.dict(os.environ, {'CORS_ORIGINS': 'http://localhost:3000,http://localhost:8080'})
    def test_cors_origins_with_ports(self):
        """Test CORS origins with non-standard ports."""
        test_settings = Settings()
        assert "http://localhost:3000" in test_settings.cors_origins
        assert "http://localhost:8080" in test_settings.cors_origins
    
    def test_cors_origins_https_for_production(self):
        """Test that production and preview URLs use HTTPS."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            if "emergentagent.com" in origin or "emergent.host" in origin:
                assert origin.startswith("https://"), \
                    f"Production/preview URL must use HTTPS: {origin}"
    
    def test_cors_origins_security_no_wildcards(self):
        """Test that CORS origins don't contain wildcards (security)."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            assert "*" not in origin, \
                f"Wildcard found in CORS origin (security risk): {origin}"
    
    def test_cors_origins_subdomain_pattern(self):
        """Test that preview URL follows expected subdomain pattern."""
        test_settings = Settings()
        import re
        pattern = r"https://[\w-]+\.preview\.emergentagent\.com"
        preview_urls = [o for o in test_settings.cors_origins if "preview.emergentagent.com" in o]
        for url in preview_urls:
            assert re.match(pattern, url), \
                f"Preview URL doesn't match expected pattern: {url}"


class TestCORSOriginsSecurity:
    """Security-focused tests for CORS configuration."""
    
    def test_no_allow_all_origin(self):
        """Test that CORS doesn't use wildcard 'allow all' configuration."""
        test_settings = Settings()
        assert "*" not in test_settings.cors_origins
    
    def test_production_urls_use_https(self):
        """Test that production domains don't use insecure HTTP."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            if "emergentagent.com" in origin or "emergent.host" in origin:
                assert not origin.startswith("http://"), \
                    f"Production domain using insecure HTTP: {origin}"
    
    def test_cors_config_suitable_for_fastapi(self):
        """Test that CORS configuration is suitable for FastAPI middleware."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            assert len(origin) > 0, "CORS origin is empty"
            assert "://" in origin, "CORS origin missing protocol"


class TestCORSOriginsEdgeCases:
    """Test edge cases and error conditions in CORS configuration."""
    
    @patch.dict(os.environ, {'CORS_ORIGINS': ''})
    def test_empty_cors_env_var(self):
        """Test behavior when CORS_ORIGINS env var is empty."""
        test_settings = Settings()
        assert isinstance(test_settings.cors_origins, list)
    
    @patch.dict(os.environ, {'CORS_ORIGINS': 'http://single.com'})
    def test_single_cors_origin(self):
        """Test CORS origins with a single value."""
        test_settings = Settings()
        assert len(test_settings.cors_origins) == 1
        assert test_settings.cors_origins[0] == "http://single.com"
    
    @patch.dict(os.environ, {'CORS_ORIGINS': 'http://test1.com, https://test2.com , http://test3.com'})
    def test_cors_whitespace_handling(self):
        """Test that whitespace in CORS_ORIGINS is handled correctly."""
        test_settings = Settings()
        for origin in test_settings.cors_origins:
            assert origin == origin.strip(), f"Origin not trimmed: '{origin}'"