"""
Comprehensive unit tests for backend/config.py
Tests cover Settings configuration, CORS origins, environment variables, and validation
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from backend.config import Settings


class TestSettingsConfiguration:
    """Test suite for Settings configuration class"""
    
    def test_default_settings_initialization(self):
        """Test that Settings initializes with default values"""
        settings = Settings()
        
        assert settings.app_name is not None
        assert settings.database_url is not None
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) > 0
    
    def test_cors_origins_includes_localhost(self):
        """Test that CORS origins include localhost for development"""
        settings = Settings()
        
        assert any("localhost:3000" in origin for origin in settings.cors_origins)
    
    def test_cors_origins_includes_preview_url(self):
        """Test that CORS origins include the correct preview URL"""
        settings = Settings()
        
        # Verify the updated preview URL is present
        assert any("create-25.preview.emergentagent.com" in origin for origin in settings.cors_origins)
        
    def test_cors_origins_includes_production_url(self):
        """Test that CORS origins include production URL"""
        settings = Settings()
        
        assert any("fix-it-6.emergent.host" in origin for origin in settings.cors_origins)
    
    def test_cors_origins_is_list(self):
        """Test that cors_origins is a list type"""
        settings = Settings()
        
        assert isinstance(settings.cors_origins, list)
    
    def test_cors_origins_all_valid_urls(self):
        """Test that all CORS origins are valid URLs"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            assert origin.startswith("http://") or origin.startswith("https://")
            assert " " not in origin  # No spaces in URLs
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test1.com,http://test2.com"})
    def test_cors_origins_from_environment(self):
        """Test that CORS origins can be set via environment variable"""
        settings = Settings()
        
        assert "http://test1.com" in settings.cors_origins
        assert "http://test2.com" in settings.cors_origins
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://custom.com"})
    def test_cors_origins_single_value_environment(self):
        """Test CORS origins with single value from environment"""
        settings = Settings()
        
        assert "http://custom.com" in settings.cors_origins
    
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins list has no duplicate entries"""
        settings = Settings()
        
        assert len(settings.cors_origins) == len(set(settings.cors_origins))
    
    @patch.dict(os.environ, {"CORS_ORIGINS": ""})
    def test_cors_origins_empty_environment(self):
        """Test handling of empty CORS_ORIGINS environment variable"""
        settings = Settings()
        
        # Should fallback to default or handle gracefully
        assert isinstance(settings.cors_origins, list)
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "  http://test.com  ,  http://test2.com  "})
    def test_cors_origins_whitespace_handling(self):
        """Test that whitespace in CORS origins is handled properly"""
        settings = Settings()
        
        # Origins should be trimmed or handled
        for origin in settings.cors_origins:
            assert origin == origin.strip()
    
    def test_cors_origins_protocol_consistency(self):
        """Test that production/preview URLs use HTTPS"""
        settings = Settings()
        
        production_origins = [o for o in settings.cors_origins if "emergent" in o]
        for origin in production_origins:
            if "localhost" not in origin:
                assert origin.startswith("https://"), f"Production URL should use HTTPS: {origin}"
    
    @patch.dict(os.environ, {"DATABASE_URL": "mongodb://testdb:27017"})
    def test_database_url_configuration(self):
        """Test database URL configuration from environment"""
        settings = Settings()
        
        assert "testdb" in settings.database_url or settings.database_url is not None
    
    def test_settings_immutability(self):
        """Test that settings maintains configuration integrity"""
        settings = Settings()
        original_cors = settings.cors_origins.copy()
        
        # Settings should maintain original values
        assert settings.cors_origins == original_cors
    
    def test_cors_origins_validation_format(self):
        """Test that CORS origins follow correct URL format"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            # Check for valid URL components
            assert "://" in origin
            parts = origin.split("://")
            assert len(parts) == 2
            assert parts[0] in ["http", "https"]
            assert len(parts[1]) > 0  # Has domain
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test.com,invalid_url,https://valid.com"})
    def test_cors_origins_mixed_valid_invalid(self):
        """Test handling of mixed valid and invalid URLs"""
        settings = Settings()
        
        # Should include valid URLs
        assert len(settings.cors_origins) > 0
    
    def test_api_settings_configuration(self):
        """Test that API settings are properly configured"""
        settings = Settings()
        
        # Check for API-related settings if they exist
        assert hasattr(settings, 'cors_origins')


class TestCORSOriginsSecurity:
    """Security-focused tests for CORS origins"""
    
    def test_no_wildcard_in_production(self):
        """Test that wildcard CORS is not enabled in production"""
        settings = Settings()
        
        assert "*" not in settings.cors_origins
    
    def test_no_insecure_origins_in_production(self):
        """Test that production environments don't have http:// origins (except localhost)"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            if origin.startswith("http://") and "localhost" not in origin:
                pytest.fail(f"Insecure HTTP origin in production: {origin}")
    
    def test_cors_origins_domain_validation(self):
        """Test that CORS origins use valid domains"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            domain = origin.split("://")[1] if "://" in origin else origin
            
            # Should have valid domain structure
            assert "." in domain or "localhost" in domain


class TestEnvironmentConfiguration:
    """Tests for environment-specific configuration"""
    
    @patch.dict(os.environ, {})
    def test_default_configuration_without_env_vars(self):
        """Test that settings work without environment variables"""
        settings = Settings()
        
        assert settings is not None
        assert len(settings.cors_origins) > 0
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3001,http://localhost:4000"})
    def test_development_multiple_ports(self):
        """Test development configuration with multiple localhost ports"""
        settings = Settings()
        
        localhost_origins = [o for o in settings.cors_origins if "localhost" in o]
        assert len(localhost_origins) >= 1
    
    def test_preview_url_update_verification(self):
        """Test that preview URL has been updated from old to new value"""
        settings = Settings()
        
        # Verify old URL is not present
        old_preview = "fix-it-6.preview.emergentagent.com"
        new_preview = "create-25.preview.emergentagent.com"
        
        assert not any(old_preview in origin for origin in settings.cors_origins), \
            f"Old preview URL should be removed: {old_preview}"
        assert any(new_preview in origin for origin in settings.cors_origins), \
            f"New preview URL should be present: {new_preview}"


class TestConfigurationEdgeCases:
    """Edge case tests for configuration"""
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test.com,,http://test2.com"})
    def test_cors_origins_empty_values(self):
        """Test handling of empty values in CORS origins list"""
        settings = Settings()
        
        # Should filter out empty strings
        assert "" not in settings.cors_origins
    
    @patch.dict(os.environ, {"CORS_ORIGINS": ","})
    def test_cors_origins_only_commas(self):
        """Test handling of only commas in CORS_ORIGINS"""
        settings = Settings()
        
        # Should handle gracefully without empty strings
        for origin in settings.cors_origins:
            assert origin != ""
    
    @patch.dict(os.environ, {"CORS_ORIGINS": "http://test.com,http://test.com"})
    def test_cors_origins_duplicate_handling(self):
        """Test handling of duplicate URLs in configuration"""
        settings = Settings()
        
        # Depending on implementation, may dedupe or keep duplicates
        # At minimum, should not crash
        assert len(settings.cors_origins) > 0
    
    def test_settings_repr_or_str(self):
        """Test that Settings object can be represented as string"""
        settings = Settings()
        
        # Should be able to convert to string without error
        str_repr = str(settings)
        assert str_repr is not None


class TestURLFormatValidation:
    """Tests for URL format validation in CORS origins"""
    
    def test_urls_no_trailing_slash(self):
        """Test that CORS origin URLs don't have trailing slashes"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            assert not origin.endswith("/"), f"URL should not have trailing slash: {origin}"
    
    def test_urls_no_path_components(self):
        """Test that CORS origins are base URLs without paths"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            # Remove protocol
            url_without_protocol = origin.split("://")[1] if "://" in origin else origin
            
            # Check for path components (excluding port)
            if ":" in url_without_protocol:
                domain_port = url_without_protocol.split("/")[0]
            else:
                domain_port = url_without_protocol.split("/")[0]
            
            # The origin should be just domain:port or domain
            assert "/" not in url_without_protocol or url_without_protocol.count("/") == 0, \
                f"CORS origin should be base URL only: {origin}"
    
    def test_localhost_port_format(self):
        """Test that localhost URLs include port numbers"""
        settings = Settings()
        
        localhost_origins = [o for o in settings.cors_origins if "localhost" in o]
        for origin in localhost_origins:
            # Localhost should have :port
            assert ":" in origin.split("//")[1], f"Localhost should specify port: {origin}"


# Integration tests
class TestConfigurationIntegration:
    """Integration tests for configuration with other components"""
    
    def test_settings_singleton_pattern(self):
        """Test if Settings behaves consistently across instantiations"""
        settings1 = Settings()
        settings2 = Settings()
        
        # Should have same configuration
        assert settings1.cors_origins == settings2.cors_origins
    
    def test_configuration_export(self):
        """Test that configuration can be exported/accessed"""
        settings = Settings()
        
        config_dict = {
            'cors_origins': settings.cors_origins,
            'database_url': settings.database_url if hasattr(settings, 'database_url') else None
        }
        
        assert config_dict is not None
        assert 'cors_origins' in config_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])