"""
Tests for utility functions
"""

import pytest
from pathlib import Path

from dhruvkit.utils import (
    create_project_structure,
    apply_addons_to_template
)
from dhruvkit.templates import TEMPLATES, TEMPLATE_ADDONS


@pytest.fixture
def temp_project_dir(tmp_path):
    """Fixture to create a temporary project directory"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


class TestUtils:
    """Test utility functions"""
    
    def test_apply_addons_single_addon(self):
        """Test applying single add-on to template"""
        template = TEMPLATES["fastapi"]
        addons = ["mongodb"]
        
        merged = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged is not None
        assert "files" in merged
        assert "name" in merged
        assert "description" in merged
    
    def test_apply_addons_multiple_addons(self):
        """Test applying multiple add-ons"""
        template = TEMPLATES["fastapi"]
        addons = ["mongodb", "firebase"]
        
        merged = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged is not None
        main_py_func = merged["files"].get("src/main.py", lambda x: "")
        # It's a callable, verify it works
        if callable(main_py_func):
            content = main_py_func("test")
            assert isinstance(content, str)
            assert len(content) > 0
    
    def test_create_project_structure_creates_files(self, temp_project_dir):
        """Test that create_project_structure creates all files"""
        template = TEMPLATES["basic"]
        
        files_created = create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=template,
            license_name=None
        )
        
        # Should have created files
        assert len(files_created) > 0
        
        # Check that common files exist
        assert (temp_project_dir / ".gitignore").exists()
        assert (temp_project_dir / "README.md").exists()
    
    def test_apply_addons_empty_list(self):
        """Test applying empty add-on list"""
        template = TEMPLATES["fastapi"]
        addons = []
        
        merged = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged is not None
        # Should return template structure unchanged
        assert "files" in merged
    
    def test_apply_invalid_addon(self, capsys):
        """Test applying invalid add-on shows warning"""
        template = TEMPLATES["fastapi"]
        addons = ["nonexistent_addon"]
        
        merged = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        # Should still return valid template
        assert merged is not None
        
        # Should have printed warning
        captured = capsys.readouterr()
        assert "warning" in captured.out.lower() or "not found" in captured.out.lower()


class TestFileHandling:
    """Test file handling utilities"""
    
    def test_gitignore_created(self, temp_project_dir):
        """Test that .gitignore is properly created"""
        template = TEMPLATES["basic"]
        
        create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=template,
            license_name=None
        )
        
        gitignore_path = temp_project_dir / ".gitignore"
        assert gitignore_path.exists()
        
        content = gitignore_path.read_text()
        assert ".env" in content
        assert "__pycache__" in content or "*.pyc" in content
    
    def test_readme_created_with_project_name(self, temp_project_dir):
        """Test that README is created with project name"""
        template = TEMPLATES["basic"]
        project_name = "my_awesome_project"
        
        create_project_structure(
            root=temp_project_dir,
            project_name=project_name,
            template=template,
            license_name=None
        )
        
        readme_path = temp_project_dir / "README.md"
        assert readme_path.exists()
        
        content = readme_path.read_text()
        # README should contain the project name
        assert project_name in content or project_name.replace("_", " ") in content.lower()
    
    def test_env_file_created(self, temp_project_dir):
        """Test that .env file is created"""
        template = TEMPLATES["fastapi"]
        
        create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=template,
            license_name=None
        )
        
        env_path = temp_project_dir / ".env"
        assert env_path.exists()


class TestTemplateGeneration:
    """Test template content generation"""
    
    def test_fastapi_with_mongodb_generates_correct_structure(self, temp_project_dir):
        """Test FastAPI with MongoDB generates all needed files"""
        template = TEMPLATES["fastapi"]
        merged = apply_addons_to_template(
            template,
            ["mongodb"],
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=merged,
            license_name=None
        )
        
        # Check MongoDB-specific files
        assert (temp_project_dir / "src" / "main.py").exists()
        assert (temp_project_dir / "requirements.txt").exists()
        
        requirements = (temp_project_dir / "requirements.txt").read_text()
        assert "pymongo" in requirements.lower()
    
    def test_fastapi_with_all_addons(self, temp_project_dir):
        """Test FastAPI with all add-ons"""
        template = TEMPLATES["fastapi"]
        merged = apply_addons_to_template(
            template,
            ["mongodb", "firebase", "secure"],
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=merged,
            license_name=None
        )
        
        assert (temp_project_dir / "src" / "main.py").exists()
        assert (temp_project_dir / "requirements.txt").exists()
        
        requirements = (temp_project_dir / "requirements.txt").read_text()
        assert "pymongo" in requirements.lower()
        assert "firebase" in requirements.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
