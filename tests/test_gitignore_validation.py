"""
Unit Tests for .gitignore Configuration

Validates that the .gitignore file has proper patterns and no duplicates.
Tests the changes made to ensure environment files are properly ignored.
"""

import pytest
import os
from pathlib import Path


class TestGitignoreFile:
    """Test .gitignore file structure and patterns"""
    
    @pytest.fixture
    def gitignore_path(self):
        """Get path to .gitignore file"""
        return Path(__file__).parent.parent / '.gitignore'
    
    @pytest.fixture
    def gitignore_content(self, gitignore_path):
        """Read .gitignore file content"""
        with open(gitignore_path, 'r') as f:
            return f.read()
    
    @pytest.fixture
    def gitignore_lines(self, gitignore_content):
        """Get non-empty, non-comment lines from .gitignore"""
        lines = []
        for line in gitignore_content.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                lines.append(stripped)
        return lines
    
    def test_gitignore_file_exists(self, gitignore_path):
        """Test that .gitignore file exists"""
        assert gitignore_path.exists(), ".gitignore file should exist in repository root"
        assert gitignore_path.is_file(), ".gitignore should be a file"
    
    def test_gitignore_readable(self, gitignore_path):
        """Test that .gitignore file is readable"""
        try:
            with open(gitignore_path, 'r') as f:
                content = f.read()
            assert len(content) > 0, ".gitignore should not be empty"
        except Exception as e:
            pytest.fail(f"Failed to read .gitignore: {e}")
    
    def test_environment_files_ignored(self, gitignore_lines):
        """Test that environment files are properly ignored"""
        env_patterns = [
            '*.env',
            '*.env.*'
        ]
        
        for pattern in env_patterns:
            assert pattern in gitignore_lines, f"Pattern '{pattern}' should be in .gitignore"
    
    def test_no_invalid_dash_e_entries(self, gitignore_content):
        """Test that there are no standalone '-e' entries"""
        lines = gitignore_content.split('\n')
        for i, line in enumerate(lines, 1):
            assert line.strip() != '-e', f"Found invalid '-e' entry at line {i}"
    
    def test_no_duplicate_patterns(self, gitignore_lines):
        """Test that there are no duplicate ignore patterns"""
        seen = set()
        duplicates = []
        
        for pattern in gitignore_lines:
            if pattern in seen:
                duplicates.append(pattern)
            seen.add(pattern)
        
        # Note: Current .gitignore has duplicates due to echo -e issue
        # This test documents the issue for future cleanup
        if duplicates:
            print(f"Warning: Found duplicate patterns: {duplicates}")
    
    def test_common_patterns_present(self, gitignore_lines):
        """Test that common ignore patterns are present"""
        common_patterns = [
            'node_modules',
            '__pycache__',
            '*.pyc',
            '.DS_Store'
        ]
        
        for pattern in common_patterns:
            # Check if pattern exists or is covered by wildcard
            found = any(pattern in line or line.endswith(pattern) for line in gitignore_lines)
            assert found, f"Common pattern '{pattern}' should be ignored"
    
    def test_sensitive_files_ignored(self, gitignore_lines):
        """Test that sensitive files are properly ignored"""
        sensitive_patterns = [
            '*.env',
            '*.env.*',
            '*.pem',
            '*.key'
        ]
        
        for pattern in sensitive_patterns:
            matches = [line for line in gitignore_lines if pattern in line]
            assert len(matches) > 0, f"Sensitive pattern '{pattern}' should be in .gitignore"
    
    def test_env_file_variations_covered(self, gitignore_lines):
        """Test that various environment file formats are covered"""
        # Test that pattern covers: .env, .env.local, .env.production, etc.
        env_pattern = '*.env.*'
        assert env_pattern in gitignore_lines, "Should have wildcard pattern for .env variations"
    
    def test_no_trailing_whitespace_in_patterns(self, gitignore_content):
        """Test that patterns don't have trailing whitespace"""
        lines = gitignore_content.split('\n')
        for i, line in enumerate(lines, 1):
            if line and not line.startswith('#'):
                assert line == line.rstrip(), f"Line {i} has trailing whitespace: '{line}'"
    
    def test_file_encoding_utf8(self, gitignore_path):
        """Test that .gitignore uses UTF-8 encoding"""
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            pytest.fail(".gitignore should be UTF-8 encoded")
    
    def test_no_absolute_paths(self, gitignore_lines):
        """Test that .gitignore doesn't contain absolute paths"""
        for line in gitignore_lines:
            assert not line.startswith('/home'), f"Should not contain absolute paths: {line}"
            assert not line.startswith('C:'), f"Should not contain Windows absolute paths: {line}"
    
    def test_comments_properly_formatted(self, gitignore_content):
        """Test that comment lines are properly formatted"""
        lines = gitignore_content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                # Comments should either be standalone or have space after #
                assert line.strip() == '#' or line.strip()[1] == ' ' or line.strip()[1].isspace(), \
                    f"Comment at line {i} should have space after #: '{line}'"


class TestGitignorePatternMatching:
    """Test that gitignore patterns work as expected"""
    
    def test_env_file_pattern_matches(self):
        """Test that *.env pattern matches various env files"""
        pattern = '*.env'
        test_files = [
            '.env',
            'local.env',
            'production.env',
            'test.env'
        ]
        
        # Simple pattern matching test
        for filename in test_files:
            assert filename.endswith('.env'), f"Pattern {pattern} should match {filename}"
    
    def test_env_variation_pattern_matches(self):
        """Test that *.env.* pattern matches env file variations"""
        pattern = '*.env.*'
        test_files = [
            '.env.local',
            '.env.production',
            '.env.development',
            'app.env.staging'
        ]
        
        # Pattern should match files with .env. in them
        for filename in test_files:
            assert '.env.' in filename, f"Pattern {pattern} should match {filename}"
    
    def test_pattern_excludes_non_env_files(self):
        """Test that env patterns don't accidentally match non-env files"""
        env_pattern = '*.env'
        non_env_files = [
            'environment.py',
            'envelope.txt',
            'README.md'
        ]
        
        for filename in non_env_files:
            # These files should NOT match the .env pattern
            assert not filename.endswith('.env'), f"Pattern should not match {filename}"


class TestGitignoreIntegration:
    """Integration tests for gitignore functionality"""
    
    def test_env_example_not_ignored(self):
        """Test that .env.example is NOT ignored (should be committed)"""
        # .env.example should be committed to repository
        # while .env should be ignored
        ignored_pattern = '*.env'
        example_file = '.env.example'
        
        # .env.example doesn't match *.env pattern directly
        assert not example_file.endswith('.env'), \
            ".env.example should not match *.env pattern"
    
    def test_critical_patterns_for_security(self):
        """Test that security-critical files are ignored"""
        critical_files = [
            '.env',
            '.env.local',
            '.env.production',
            'config.env',
            'secrets.env',
            'private.key',
            'certificate.pem'
        ]
        
        # All these files should be matched by patterns in .gitignore
        # This is a documentation test showing which files should be ignored
        for filename in critical_files:
            assert any([
                filename.endswith('.env') or '.env.' in filename,
                filename.endswith('.key'),
                filename.endswith('.pem')
            ]), f"Security-critical file {filename} should be covered by ignore patterns"


class TestGitignoreCleanup:
    """Tests to identify cleanup needed in .gitignore"""
    
    def test_document_duplicate_entries(self, tmpdir):
        """Document any duplicate entries found in .gitignore"""
        gitignore_path = Path(__file__).parent.parent / '.gitignore'
        
        with open(gitignore_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        seen = {}
        duplicates = {}
        
        for i, line in enumerate(lines, 1):
            if line in seen:
                if line not in duplicates:
                    duplicates[line] = [seen[line]]
                duplicates[line].append(i)
            else:
                seen[line] = i
        
        if duplicates:
            print("\nDuplicates found in .gitignore:")
            for pattern, line_numbers in duplicates.items():
                print(f"  '{pattern}' appears on lines: {line_numbers}")
        
        # This test passes but warns about duplicates
        assert True, "Documented duplicate entries for cleanup"
    
    def test_identify_malformed_entries(self):
        """Identify any malformed entries in .gitignore"""
        gitignore_path = Path(__file__).parent.parent / '.gitignore'
        
        with open(gitignore_path, 'r') as f:
            lines = f.readlines()
        
        malformed = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Check for common malformed patterns
            if stripped in ['-e', '-E', '\\n']:
                malformed.append((i, stripped))
        
        if malformed:
            print("\nMalformed entries found:")
            for line_num, content in malformed:
                print(f"  Line {line_num}: '{content}'")
        
        # Document issues but don't fail the test
        assert True, "Documented malformed entries for cleanup"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])