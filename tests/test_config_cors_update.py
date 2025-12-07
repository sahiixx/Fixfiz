"""
Comprehensive unit tests for backend/config.py
Tests focus on CORS configuration, URL validation, and settings management
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from backend.config import Settings


class TestCORSConfiguration:
    """Test suite for CORS origins configuration"""
    
    def test_cors_origins_default_values(self):
        """Test that CORS origins include expected default URLs"""
        # Test default CORS origins when CORS_ORIGINS env var is not set
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Verify the new preview URL is present
            assert "https://create-25.preview.emergentagent.com" in settings.cors_origins
            
            # Verify localhost is present for development
            assert "http://localhost:3000" in settings.cors_origins
            
            # Verify production URL is present
            assert "https://fix-it-6.emergent.host" in settings.cors_origins
    
    def test_cors_origins_from_environment_variable(self):
        """Test CORS origins can be configured via environment variable"""
        custom_origins = "http://localhost:8080,https://custom-domain.com,https://test.example.com"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": custom_origins}):
            settings = Settings()
            
            assert "http://localhost:8080" in settings.cors_origins
            assert "https://custom-domain.com" in settings.cors_origins
            assert "https://test.example.com" in settings.cors_origins
            assert len(settings.cors_origins) == 3
    
    def test_cors_origins_list_type(self):
        """Test that cors_origins is properly parsed as a list"""
        settings = Settings()
        
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) > 0
        
        # Verify each origin is a string
        for origin in settings.cors_origins:
            assert isinstance(origin, str)
            assert len(origin) > 0
    
    def test_cors_origins_no_duplicates(self):
        """Test that CORS origins list has no duplicates"""
        settings = Settings()
        
        origins_set = set(settings.cors_origins)
        assert len(origins_set) == len(settings.cors_origins), \
            "CORS origins should not contain duplicates"
    
    def test_cors_origins_url_format_validation(self):
        """Test that all CORS origins follow valid URL format"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            # Check if origin starts with http:// or https://
            assert origin.startswith("http://") or origin.startswith("https://"), \
                f"Invalid origin format: {origin}"
            
            # Check no trailing slashes
            assert not origin.endswith("/"), \
                f"CORS origin should not have trailing slash: {origin}"
    
    def test_cors_origins_empty_string_handling(self):
        """Test handling of empty or whitespace-only environment variable"""
        with patch.dict(os.environ, {"CORS_ORIGINS": ""}):
            settings = Settings()
            
            # Should still have at least one origin from default
            assert len(settings.cors_origins) >= 1
    
    def test_cors_origins_whitespace_trimming(self):
        """Test that whitespace is properly trimmed from origins"""
        custom_origins = " http://localhost:3000 , https://example.com , https://test.com "
        
        with patch.dict(os.environ, {"CORS_ORIGINS": custom_origins}):
            settings = Settings()
            
            # Verify no leading/trailing whitespace in origins
            for origin in settings.cors_origins:
                assert origin == origin.strip()


class TestSettingsConfiguration:
    """Test suite for general Settings configuration"""
    
    def test_settings_instantiation(self):
        """Test that Settings can be instantiated successfully"""
        settings = Settings()
        
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_cors_origins_attribute_exists(self):
        """Test that cors_origins attribute exists and is accessible"""
        settings = Settings()
        
        assert hasattr(settings, 'cors_origins')
        assert settings.cors_origins is not None
    
    def test_multiple_settings_instances_independence(self):
        """Test that multiple Settings instances maintain independence"""
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000"}):
            settings1 = Settings()
        
        with patch.dict(os.environ, {"CORS_ORIGINS": "https://example.com"}):
            settings2 = Settings()
        
        # Verify settings are not shared between instances
        # Note: This test may need adjustment based on actual Settings implementation
        assert settings1 is not settings2


class TestURLUpdates:
    """Test suite specifically for the preview URL update from fix-it-6 to create-25"""
    
    def test_old_preview_url_not_present(self):
        """Ensure old preview URL has been removed/updated"""
        settings = Settings()
        
        # The old URL should not be present
        old_url = "https://fix-it-6.preview.emergentagent.com"
        assert old_url not in settings.cors_origins, \
            f"Old preview URL should be replaced: {old_url}"
    
    def test_new_preview_url_present(self):
        """Verify new preview URL is correctly configured"""
        settings = Settings()
        
        # The new URL should be present
        new_url = "https://create-25.preview.emergentagent.com"
        assert new_url in settings.cors_origins, \
            f"New preview URL should be present: {new_url}"
    
    def test_production_url_unchanged(self):
        """Verify production URL remains unchanged"""
        settings = Settings()
        
        production_url = "https://fix-it-6.emergent.host"
        assert production_url in settings.cors_origins, \
            f"Production URL should still be present: {production_url}"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_cors_origins_single_url(self):
        """Test CORS configuration with single URL"""
        with patch.dict(os.environ, {"CORS_ORIGINS": "https://single-url.com"}):
            settings = Settings()
            
            assert len(settings.cors_origins) == 1
            assert settings.cors_origins[0] == "https://single-url.com"
    
    def test_cors_origins_many_urls(self):
        """Test CORS configuration with many URLs"""
        many_urls = ",".join([f"https://domain-{i}.com" for i in range(20)])
        
        with patch.dict(os.environ, {"CORS_ORIGINS": many_urls}):
            settings = Settings()
            
            assert len(settings.cors_origins) == 20
    
    def test_cors_origins_special_characters_in_domain(self):
        """Test handling of domains with special characters"""
        custom_origins = "https://test-domain.com,https://sub.domain.example.com,http://localhost:3000"
        
        with patch.dict(os.environ, {"CORS_ORIGINS": custom_origins}):
            settings = Settings()
            
            assert "https://test-domain.com" in settings.cors_origins
            assert "https://sub.domain.example.com" in settings.cors_origins
            assert "http://localhost:3000" in settings.cors_origins


class TestIntegration:
    """Integration tests for Settings with other configuration parameters"""
    
    def test_settings_with_multiple_env_vars(self):
        """Test Settings behavior with multiple environment variables set"""
        env_vars = {
            "CORS_ORIGINS": "http://localhost:3000,https://example.com",
            "DATABASE_URL": "mongodb://localhost:27017/test",
            "API_KEY": "test-api-key"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            
            # Verify CORS origins are correctly set
            assert len(settings.cors_origins) == 2
            assert "http://localhost:3000" in settings.cors_origins


# Performance tests
class TestPerformance:
    """Performance-related tests for Settings"""
    
    def test_settings_instantiation_performance(self):
        """Test that Settings instantiation is fast"""
        import time
        
        start_time = time.time()
        for _ in range(100):
            settings = Settings()
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        # Should be able to instantiate 100 times in less than 1 second
        assert elapsed_time < 1.0, \
            f"Settings instantiation too slow: {elapsed_time:.3f}s for 100 iterations"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])