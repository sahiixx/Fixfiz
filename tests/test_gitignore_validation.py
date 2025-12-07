"""
Comprehensive tests for .gitignore file validation
Tests ensure proper git ignore patterns are in place
"""
import pytest
import os
import re
from pathlib import Path


class TestGitignoreValidation:
    """Test suite for .gitignore file validation"""
    
    @pytest.fixture
    def gitignore_path(self):
        """Get the path to .gitignore file"""
        repo_root = Path(__file__).parent.parent
        return repo_root / '.gitignore'
    
    @pytest.fixture
    def gitignore_content(self, gitignore_path):
        """Read .gitignore file content"""
        if not gitignore_path.exists():
            pytest.skip(".gitignore file not found")
        
        with open(gitignore_path, 'r') as f:
            return f.read()
    
    def test_gitignore_exists(self, gitignore_path):
        """Test that .gitignore file exists"""
        assert gitignore_path.exists(), ".gitignore file should exist"
        assert gitignore_path.is_file(), ".gitignore should be a file"
    
    def test_gitignore_not_empty(self, gitignore_content):
        """Test that .gitignore is not empty"""
        assert gitignore_content.strip(), ".gitignore should not be empty"
        assert len(gitignore_content) > 0, ".gitignore should have content"
    
    def test_env_files_ignored(self, gitignore_content):
        """Test that environment files are ignored"""
        # Check for various environment file patterns
        env_patterns = [
            r'\.env',
            r'\*.env',
            r'\*.env\.\*'
        ]
        
        for pattern in env_patterns:
            assert re.search(pattern, gitignore_content), \
                f"Pattern {pattern} should be in .gitignore"
    
    def test_node_modules_ignored(self, gitignore_content):
        """Test that node_modules directories are ignored"""
        assert 'node_modules' in gitignore_content or \
               '/node_modules/' in gitignore_content, \
               "node_modules should be ignored"
    
    def test_common_build_artifacts_ignored(self, gitignore_content):
        """Test that common build artifacts are ignored"""
        build_patterns = [
            'dist',
            'build',
            'coverage',
            '__pycache__',
            '*.pyc',
        ]
        
        for pattern in build_patterns:
            assert pattern in gitignore_content, \
                f"Build artifact pattern '{pattern}' should be in .gitignore"
    
    def test_no_duplicate_entries(self, gitignore_content):
        """Test that .gitignore has no duplicate entries"""
        lines = [line.strip() for line in gitignore_content.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        
        seen = set()
        duplicates = []
        
        for line in lines:
            if line in seen:
                duplicates.append(line)
            seen.add(line)
        
        assert len(duplicates) == 0, \
            f"Found duplicate entries in .gitignore: {duplicates}"
    
    def test_proper_line_endings(self, gitignore_content):
        """Test that .gitignore uses proper line endings"""
        # Should not have Windows-style line endings in Linux repo
        assert '\r\n' not in gitignore_content, \
            ".gitignore should use Unix line endings (LF), not Windows (CRLF)"
    
    def test_no_trailing_whitespace(self, gitignore_content):
        """Test that entries don't have trailing whitespace"""
        lines = gitignore_content.split('\n')
        
        lines_with_trailing_whitespace = [
            i for i, line in enumerate(lines, 1)
            if line and line != line.rstrip()
        ]
        
        assert len(lines_with_trailing_whitespace) == 0, \
            f"Lines with trailing whitespace: {lines_with_trailing_whitespace}"
    
    def test_environment_variable_patterns(self, gitignore_content):
        """Test specific environment file patterns are present"""
        # From the diff, we see *.env and *.env.* patterns
        assert '*.env' in gitignore_content, "*.env pattern should be present"
        assert '*.env.*' in gitignore_content, "*.env.* pattern should be present"
    
    def test_comment_syntax(self, gitignore_content):
        """Test that comments use proper syntax"""
        lines = gitignore_content.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and stripped.startswith('#'):
                # Comments should start with #
                assert line.lstrip().startswith('#'), \
                    f"Line {i}: Comments should start with # after optional whitespace"


class TestGitignorePatternEffectiveness:
    """Test that gitignore patterns work correctly"""
    
    @pytest.fixture
    def repo_root(self):
        """Get repository root path"""
        return Path(__file__).parent.parent
    
    def test_env_files_would_be_ignored(self, repo_root):
        """Test that .env files in repo would be ignored by git"""
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        # Read gitignore patterns
        with open(gitignore_path, 'r') as f:
            patterns = [line.strip() for line in f 
                       if line.strip() and not line.strip().startswith('#')]
        
        # Test various env file names
        test_files = [
            '.env',
            '.env.local',
            '.env.development',
            '.env.production',
            'config.env',
        ]
        
        for test_file in test_files:
            # At least one pattern should match
            matched = any(
                test_file.endswith(p.replace('*', '')) 
                for p in patterns if '*' in p
            )
            
            assert matched or '.env' in patterns, \
                f"{test_file} should be ignored by gitignore patterns"
    
    def test_build_directories_ignored(self, repo_root):
        """Test that common build directories are ignored"""
        build_dirs = [
            'node_modules',
            'dist',
            'build',
            '__pycache__',
            '.cache',
            'coverage',
        ]
        
        gitignore_path = repo_root / '.gitignore'
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        for build_dir in build_dirs:
            assert build_dir in content or f'/{build_dir}/' in content, \
                f"Build directory {build_dir} should be ignored"


class TestGitignoreFileStructure:
    """Test .gitignore file structure and organization"""
    
    @pytest.fixture
    def gitignore_lines(self):
        """Get gitignore file lines"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        with open(gitignore_path, 'r') as f:
            return f.readlines()
    
    def test_sections_are_organized(self, gitignore_lines):
        """Test that .gitignore has organized sections with comments"""
        # Should have section comments
        has_comments = any(line.strip().startswith('#') 
                          for line in gitignore_lines)
        
        assert has_comments, ".gitignore should have section comments for organization"
    
    def test_no_excessive_blank_lines(self, gitignore_lines):
        """Test that there aren't excessive consecutive blank lines"""
        consecutive_blank = 0
        max_consecutive_blank = 0
        
        for line in gitignore_lines:
            if not line.strip():
                consecutive_blank += 1
                max_consecutive_blank = max(max_consecutive_blank, consecutive_blank)
            else:
                consecutive_blank = 0
        
        assert max_consecutive_blank <= 2, \
            "Should not have more than 2 consecutive blank lines"
    
    def test_patterns_are_valid(self, gitignore_lines):
        """Test that gitignore patterns follow valid syntax"""
        for i, line in enumerate(gitignore_lines, 1):
            stripped = line.strip()
            
            # Skip comments and blank lines
            if not stripped or stripped.startswith('#'):
                continue
            
            # Pattern shouldn't start with /
            # (unless it's a specific root-only pattern)
            if stripped.startswith('/') and not stripped.endswith('/'):
                # This is a root-specific file pattern
                assert len(stripped) > 1, f"Line {i}: Invalid root pattern"


class TestEnvFileProtection:
    """Specific tests for environment file protection"""
    
    def test_multiple_env_formats_covered(self):
        """Test that multiple environment file formats are covered"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        # Test various env file patterns
        env_patterns = [
            '.env',
            '*.env',
            '*.env.*',
        ]
        
        found_patterns = sum(1 for pattern in env_patterns 
                           if pattern in content)
        
        assert found_patterns >= 2, \
            "Should have at least 2 environment file patterns for comprehensive coverage"
    
    def test_env_files_section_exists(self):
        """Test that there's a dedicated section for environment files"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        with open(gitignore_path, 'r') as f:
            content = f.read().lower()
        
        # Look for environment-related section comments
        has_env_section = 'environment' in content or 'env file' in content
        
        assert has_env_section, \
            "Should have a section comment for environment files"


class TestGitignoreIntegrity:
    """Tests for .gitignore file integrity"""
    
    def test_file_is_readable(self):
        """Test that .gitignore file is readable"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        try:
            with open(gitignore_path, 'r') as f:
                f.read()
        except Exception as e:
            pytest.fail(f".gitignore file should be readable: {e}")
    
    def test_no_invalid_characters(self):
        """Test that .gitignore doesn't contain invalid characters"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        with open(gitignore_path, 'rb') as f:
            content = f.read()
        
        # Should be valid UTF-8
        try:
            content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail(".gitignore should contain valid UTF-8 text")
    
    def test_file_ends_with_newline(self):
        """Test that .gitignore ends with a newline"""
        repo_root = Path(__file__).parent.parent
        gitignore_path = repo_root / '.gitignore'
        
        if not gitignore_path.exists():
            pytest.skip(".gitignore not found")
        
        with open(gitignore_path, 'rb') as f:
            content = f.read()
        
        assert content.endswith(b'\n'), \
            ".gitignore should end with a newline character"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])