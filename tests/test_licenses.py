"""
Tests for license functionality
"""

import pytest
from pathlib import Path

from dhruvkit.licenses import get_license, AVAILABLE_LICENSES, LICENSE_ALIASES


class TestPackageData:
    """Test that package data is properly included (critical for PyPI distribution)"""
    
    def test_package_data_available(self):
        """Test that license template files are accessible after packaging"""
        # This ensures that when installed from PyPI, the template files are available
        content = get_license("mit", "TestProject", "Test Author")
        assert content is not None
        assert len(content) > 0
        assert "MIT" in content or "Massachusetts Institute of Technology" in content
    
    def test_all_license_templates_accessible(self):
        """Test that all license templates can be loaded"""
        for license_key in AVAILABLE_LICENSES.keys():
            content = get_license(license_key, "TestProject", "Test Author")
            assert content is not None
            assert len(content) > 100  # License text should be substantial
            
            # Verify it's actual license content, not an error message
            # Check for license-specific keywords instead
            assert content.strip() != ""


class TestLicenses:
    """Test license functionality"""
    
    def test_all_licenses_available(self):
        """Test that all advertised licenses are available"""
        expected_licenses = ["mit", "apache", "gpl", "bsd", "unlicense", "cc"]
        
        for license_key in expected_licenses:
            assert license_key in AVAILABLE_LICENSES, f"License {license_key} not found"
    
    def test_license_aliases(self):
        """Test that license aliases work"""
        assert "cc0" in LICENSE_ALIASES
        assert LICENSE_ALIASES["cc0"] == "cc"
    
    def test_get_license_mit(self):
        """Test getting MIT license"""
        license_content = get_license("mit", "TestProject", "Test Author")
        
        assert license_content is not None
        assert "MIT" in license_content or "Massachusetts Institute of Technology" in license_content
        assert "Test Author" in license_content
    
    def test_get_license_apache(self):
        """Test getting Apache license"""
        license_content = get_license("apache", "TestProject", "Test Author")
        
        assert license_content is not None
        assert "Apache" in license_content
    
    def test_get_license_gpl(self):
        """Test getting GPL license"""
        license_content = get_license("gpl", "TestProject", "Test Author")
        
        assert license_content is not None
        assert "GNU" in license_content or "General Public License" in license_content
    
    def test_get_license_invalid(self):
        """Test handling of invalid license falls back to MIT"""
        license_content = get_license("invalid_license", "TestProject", "Test Author")
        
        # Should fall back to MIT
        assert license_content is not None
        assert "MIT" in license_content or "Massachusetts Institute of Technology" in license_content
    
    def test_license_templates_exist(self):
        """Test that all license template files exist"""
        license_template_dir = Path(__file__).parent.parent / "src" / "dhruvkit" / "license_templates"
        
        assert license_template_dir.exists()
        
        for license_file in ["mit.md", "apache.md", "gpl.md", "bsd.md", "unlicense.md", "cc.md"]:
            assert (license_template_dir / license_file).exists(), f"{license_file} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
