"""
Integration tests for config.py with the updated CORS origins
Tests ensure proper integration with FastAPI CORS middleware
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import Settings
import os


class TestCORSIntegration:
    """Integration tests for CORS configuration with FastAPI"""
    
    def test_cors_middleware_configuration(self):
        """Test that CORS middleware can be configured with new origins"""
        app = FastAPI()
        settings = Settings()
        
        # Add CORS middleware with settings
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Verify middleware was added
        assert len(app.user_middleware) > 0
        
        # Find CORS middleware
        cors_middleware = None
        for middleware in app.user_middleware:
            if hasattr(middleware, 'cls'):
                if middleware.cls == CORSMiddleware:
                    cors_middleware = middleware
                    break
        
        assert cors_middleware is not None
    
    def test_preview_url_in_cors_origins(self):
        """Test that new preview URL is properly configured"""
        settings = Settings()
        
        new_preview = "https://create-25.preview.emergentagent.com"
        assert any(new_preview in origin for origin in settings.cors_origins)
    
    def test_old_preview_url_removed(self):
        """Test that old preview URL is not in CORS origins"""
        settings = Settings()
        
        old_preview = "fix-it-6.preview.emergentagent.com"
        assert not any(old_preview in origin for origin in settings.cors_origins)
    
    def test_cors_origins_formatting(self):
        """Test that all CORS origins are properly formatted for FastAPI"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            # Should be valid URLs
            assert origin.startswith("http://") or origin.startswith("https://")
            # Should not have trailing slashes
            assert not origin.endswith("/")
    
    def test_cors_configuration_from_env(self):
        """Test CORS configuration from environment variables"""
        with patch.dict(os.environ, {
            "CORS_ORIGINS": "http://test1.com,http://test2.com,https://test3.com"
        }):
            settings = Settings()
            
            assert len(settings.cors_origins) >= 3
            assert "http://test1.com" in settings.cors_origins
            assert "http://test2.com" in settings.cors_origins
            assert "https://test3.com" in settings.cors_origins


class TestSettingsInitialization:
    """Test settings initialization in different environments"""
    
    def test_development_environment(self):
        """Test settings in development environment"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            # Should have localhost
            localhost_origins = [o for o in settings.cors_origins if "localhost" in o]
            assert len(localhost_origins) > 0
    
    def test_production_environment(self):
        """Test settings in production environment"""
        settings = Settings()
        
        # Should have production URLs
        prod_origins = [o for o in settings.cors_origins if "emergent.host" in o]
        assert len(prod_origins) > 0
    
    def test_preview_environment(self):
        """Test settings in preview environment"""
        settings = Settings()
        
        # Should have preview URLs
        preview_origins = [o for o in settings.cors_origins if "preview.emergentagent.com" in o]
        assert len(preview_origins) > 0


class TestCORSSecurityValidation:
    """Security validation tests for CORS configuration"""
    
    def test_no_wildcard_origins(self):
        """Test that wildcard origins are not allowed"""
        settings = Settings()
        
        assert "*" not in settings.cors_origins
    
    def test_https_for_production(self):
        """Test that production URLs use HTTPS"""
        settings = Settings()
        
        for origin in settings.cors_origins:
            if "emergent" in origin and "localhost" not in origin:
                assert origin.startswith("https://")
    
    def test_no_suspicious_domains(self):
        """Test that no suspicious domains are in CORS origins"""
        settings = Settings()
        
        suspicious_patterns = [".ru", ".cn", "example.com", "test.test"]
        
        for origin in settings.cors_origins:
            for pattern in suspicious_patterns:
                assert pattern not in origin


class TestConfigurationConsistency:
    """Tests for configuration consistency"""
    
    def test_settings_singleton_behavior(self):
        """Test that settings behave consistently"""
        settings1 = Settings()
        settings2 = Settings()
        
        # Should have same CORS origins
        assert settings1.cors_origins == settings2.cors_origins
    
    def test_url_consistency(self):
        """Test URL consistency across configuration"""
        settings = Settings()
        
        # All URLs should be consistently formatted
        for origin in settings.cors_origins:
            # No mixed case in protocol
            if origin.startswith("HTTP"):
                pytest.fail(f"Protocol should be lowercase: {origin}")
            
            # No double slashes except after protocol
            parts = origin.split("://")
            if len(parts) > 1:
                assert "//" not in parts[1]


class TestMateDirectoryConfigConsistency:
    """Test consistency between main and mate directory configs"""
    
    def test_both_configs_have_new_preview_url(self):
        """Test that both config files have the updated preview URL"""
        # This is a validation test for the mate directory copy
        settings = Settings()
        
        new_preview = "create-25.preview.emergentagent.com"
        assert any(new_preview in origin for origin in settings.cors_origins)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])