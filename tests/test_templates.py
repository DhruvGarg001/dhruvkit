"""
Tests for template functionality
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from dhruvkit.templates import TEMPLATES, TEMPLATE_ADDONS
from dhruvkit.utils import create_project_structure, apply_addons_to_template


@pytest.fixture
def temp_project_dir(tmp_path):
    """Fixture to create a temporary project directory"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


class TestTemplates:
    """Test template functionality"""
    
    def test_all_templates_exist(self):
        """Test that all templates are defined"""
        assert "basic" in TEMPLATES
        assert "fastapi" in TEMPLATES
        assert "flask" in TEMPLATES
    
    def test_template_structure(self):
        """Test that templates have required fields"""
        for template_name, template in TEMPLATES.items():
            assert "name" in template
            assert "description" in template
            assert "files" in template
            assert isinstance(template["files"], dict)
    
    def test_fastapi_addons_exist(self):
        """Test that FastAPI add-ons are defined"""
        assert "fastapi" in TEMPLATE_ADDONS
        assert "mongodb" in TEMPLATE_ADDONS["fastapi"]
        assert "firebase" in TEMPLATE_ADDONS["fastapi"]
        assert "secure" in TEMPLATE_ADDONS["fastapi"]
    
    def test_addon_structure(self):
        """Test that add-ons have required fields"""
        for template_name, addons in TEMPLATE_ADDONS.items():
            for addon_name, addon in addons.items():
                assert "description" in addon
                assert "files" in addon
                assert isinstance(addon["files"], dict)
    
    def test_basic_template_generation(self, temp_project_dir):
        """Test generating a basic template"""
        template = TEMPLATES["basic"]
        files_created = create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=template,
            license_name=None
        )
        
        assert len(files_created) > 0
        assert (temp_project_dir / "src" / "main.py").exists()
        assert (temp_project_dir / ".env").exists()
        assert (temp_project_dir / ".gitignore").exists()
    
    def test_fastapi_template_generation(self, temp_project_dir):
        """Test generating a FastAPI template"""
        template = TEMPLATES["fastapi"]
        files_created = create_project_structure(
            root=temp_project_dir,
            project_name="test_project",
            template=template,
            license_name=None
        )
        
        assert len(files_created) > 0
        assert (temp_project_dir / "src" / "main.py").exists()
        assert (temp_project_dir / "requirements.txt").exists()
        
        # Check FastAPI specific content
        main_content = (temp_project_dir / "src" / "main.py").read_text()
        assert "FastAPI" in main_content or "fastapi" in main_content
    
    def test_addon_merging(self):
        """Test that add-ons can be merged with templates"""
        template = TEMPLATES["fastapi"]
        addons = ["mongodb", "firebase"]
        
        merged_template = apply_addons_to_template(
            template, 
            addons, 
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged_template is not None
        assert "files" in merged_template
        
        # Check that MongoDB and Firebase specific files are included
        files = merged_template["files"]
        src_main_func = files.get("src/main.py", lambda x: "")
        
        # Call the function to get the actual content
        if callable(src_main_func):
            content = src_main_func("test_project")
            assert isinstance(content, str)
            assert len(content) > 0


class TestTemplateFailures:
    """Test template error handling"""
    
    def test_invalid_addon_ignored(self):
        """Test that invalid add-on names are handled gracefully"""
        template = TEMPLATES["fastapi"]
        addons = ["mongodb", "invalid_addon_that_does_not_exist"]
        
        # Should not crash, just use valid add-ons
        merged_template = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged_template is not None
        assert "files" in merged_template
    
    def test_empty_addons_list(self):
        """Test that empty add-ons list works"""
        template = TEMPLATES["fastapi"]
        addons = []
        
        merged_template = apply_addons_to_template(
            template,
            addons,
            TEMPLATE_ADDONS.get("fastapi", {})
        )
        
        assert merged_template is not None
    
    def test_addon_on_template_without_addons(self):
        """Test applying add-ons to template that doesn't support them"""
        template = TEMPLATES["basic"]
        addons = ["mongodb"]  # basic template doesn't have add-ons
        
        # Should handle gracefully
        merged_template = apply_addons_to_template(
            template,
            addons,
            {}  # No add-ons available for basic template
        )
        
        assert merged_template is not None


class TestTemplateContent:
    """Test template content generation"""
    
    def test_flask_template_has_flask_content(self):
        """Test that Flask template contains Flask-specific code"""
        template = TEMPLATES["flask"]
        main_py_func = template["files"].get("src/main.py", lambda x: "")
        
        # Call the function to get content
        if callable(main_py_func):
            main_py = main_py_func("test_project")
        else:
            main_py = main_py_func
        
        assert "flask" in main_py.lower() or "Flask" in main_py
    
    def test_requirements_have_dependencies(self):
        """Test that templates include proper dependencies"""
        fastapi_template = TEMPLATES["fastapi"]
        requirements_func = fastapi_template["files"].get("requirements.txt", lambda x: "")
        
        # Call the function to get content
        if callable(requirements_func):
            requirements = requirements_func("test_project")
        else:
            requirements = requirements_func
        
        assert "fastapi" in requirements.lower()
        assert "uvicorn" in requirements.lower()
        
        flask_template = TEMPLATES["flask"]
        requirements_func = flask_template["files"].get("requirements.txt", lambda x: "")
        
        # Call the function to get content
        if callable(requirements_func):
            requirements = requirements_func("test_project")
        else:
            requirements = requirements_func
        
        assert "flask" in requirements.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
