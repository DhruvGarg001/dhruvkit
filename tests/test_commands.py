"""
Tests for CLI commands
"""

import pytest
from pathlib import Path
import tempfile
import sys
import os
from io import StringIO

from dhruvkit.commands.new import cmd_new
from dhruvkit.commands.init import cmd_init
from dhruvkit.commands.add import cmd_add


@pytest.fixture
def temp_cwd(tmp_path, monkeypatch):
    """Fixture to create a temporary directory and change to it"""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestNewCommand:
    """Test the 'new' command"""
    
    def test_new_command_with_template(self, temp_cwd):
        """Test creating a new project with a template"""
        # Simulate command: dhruvkit new test_project --template basic
        args = ["dhruvkit", "new", "test_project", "--template", "basic"]
        cmd_new(args)
        
        # Check that project was created
        project_path = temp_cwd / "test_project"
        assert project_path.exists()
        assert (project_path / "src" / "main.py").exists()
    
    def test_new_command_with_short_template_flag(self, temp_cwd):
        """Test creating a new project with -t flag"""
        # Simulate command: dhruvkit new test_project -t flask
        args = ["dhruvkit", "new", "test_project", "-t", "flask"]
        cmd_new(args)
        
        # Check that project was created
        project_path = temp_cwd / "test_project"
        assert project_path.exists()
        assert (project_path / "src" / "main.py").exists()
    
    def test_new_with_invalid_template(self, temp_cwd, capsys):
        """Test that invalid template name is handled gracefully"""
        args = ["dhruvkit", "new", "test_project", "--template", "invalid_template_name"]
        cmd_new(args)
        
        # Should not crash, should print error
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()
        
        # Project should not be created
        project_path = temp_cwd / "test_project"
        assert not project_path.exists()
    
    def test_new_with_invalid_license(self, temp_cwd):
        """Test that invalid license falls back gracefully"""
        args = ["dhruvkit", "new", "test_project", "--license", "invalid_license"]
        cmd_new(args)
        
        # Should create project with default/fallback license
        project_path = temp_cwd / "test_project"
        assert project_path.exists()
    
    def test_new_with_invalid_addon(self, temp_cwd):
        """Test that invalid add-on is ignored"""
        args = ["dhruvkit", "new", "test_project", "--template", "fastapi", "--invalid-addon"]
        cmd_new(args)
        
        # Should create project, ignoring invalid addon flag
        project_path = temp_cwd / "test_project"
        assert project_path.exists()
    
    def test_new_prints_success_message(self, temp_cwd, capsys):
        """Test that success message is printed"""
        args = ["dhruvkit", "new", "test_project", "--template", "basic"]
        cmd_new(args)
        
        captured = capsys.readouterr()
        assert "success" in captured.out.lower() or "created" in captured.out.lower()
    
    def test_new_with_license(self, temp_cwd):
        """Test creating project with license"""
        args = ["dhruvkit", "new", "test_project", "--template", "basic", "--license", "mit"]
        cmd_new(args)
        
        project_path = temp_cwd / "test_project"
        assert (project_path / "LICENSE").exists()
        
        license_content = (project_path / "LICENSE").read_text()
        assert "MIT" in license_content or "Massachusetts Institute of Technology" in license_content


class TestInitCommand:
    """Test the 'init' command"""
    
    def test_init_command_basic(self, temp_cwd):
        """Test initializing a project in current directory"""
        # Simulate command: dhruvkit init --template basic
        args = ["dhruvkit", "init", "--template", "basic"]
        cmd_init(args)
        
        # Check that files were created in current directory
        assert (temp_cwd / "src" / "main.py").exists()
        assert (temp_cwd / ".env").exists()
    
    def test_init_with_invalid_template(self, temp_cwd, capsys):
        """Test init with invalid template"""
        args = ["dhruvkit", "init", "--template", "nonexistent"]
        cmd_init(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()
    
    def test_init_with_short_flag(self, temp_cwd):
        """Test init with -t short flag"""
        args = ["dhruvkit", "init", "-t", "flask"]
        cmd_init(args)
        
        assert (temp_cwd / "src" / "main.py").exists()
    
    def test_init_with_addons(self, temp_cwd):
        """Test init with add-ons"""
        args = ["dhruvkit", "init", "--template", "fastapi", "--mongodb"]
        cmd_init(args)
        
        assert (temp_cwd / "src" / "main.py").exists()
        assert (temp_cwd / "requirements.txt").exists()
        
        requirements = (temp_cwd / "requirements.txt").read_text()
        assert "pymongo" in requirements.lower()


class TestAddCommand:
    """Test the 'add' command"""
    
    def test_add_license(self, temp_cwd):
        """Test adding a license to existing project"""
        # Simulate command: dhruvkit add --license mit
        args = ["dhruvkit", "add", "--license", "mit"]
        cmd_add(args)
        
        # Check that LICENSE was created
        assert (temp_cwd / "LICENSE").exists()
        
        # Check that it contains MIT license content
        license_content = (temp_cwd / "LICENSE").read_text()
        assert "MIT" in license_content or "Massachusetts Institute of Technology" in license_content
    
    def test_add_different_licenses(self, temp_cwd):
        """Test adding different license types"""
        for license_type in ["apache", "gpl", "bsd"]:
            # Create subdirectory for each license test
            test_dir = temp_cwd / license_type
            test_dir.mkdir()
            os.chdir(test_dir)
            
            args = ["dhruvkit", "add", "--license", license_type]
            cmd_add(args)
            
            assert (test_dir / "LICENSE").exists()
    
    def test_add_license_with_invalid_name(self, temp_cwd, capsys):
        """Test adding license with invalid name shows error"""
        args = ["dhruvkit", "add", "--license", "invalid_license_name"]
        cmd_add(args)
        
        # Should show error message, not create LICENSE
        captured = capsys.readouterr()
        assert "error" in captured.out.lower() or "not found" in captured.out.lower()
        
        # Should NOT create LICENSE file with invalid license
        assert not (temp_cwd / "LICENSE").exists()


class TestIntegration:
    """Integration tests for full workflows"""
    
    def test_full_flow_fastapi_mongodb(self, temp_cwd):
        """Test complete workflow: create FastAPI project with MongoDB"""
        # Create new project with FastAPI template and MongoDB addon
        args = ["dhruvkit", "new", "app", "--template", "fastapi", "--mongodb"]
        cmd_new(args)
        
        project_path = temp_cwd / "app"
        
        # Verify project structure
        assert project_path.exists()
        assert (project_path / "src" / "main.py").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / ".env").exists()
        assert (project_path / ".gitignore").exists()
        assert (project_path / "README.md").exists()
        
        # Verify MongoDB-specific content
        requirements = (project_path / "requirements.txt").read_text()
        assert "pymongo" in requirements.lower()
        
        main_py = (project_path / "src" / "main.py").read_text()
        assert "mongodb" in main_py.lower() or "mongo" in main_py.lower()
    
    def test_full_flow_with_all_addons(self, temp_cwd):
        """Test creating project with all FastAPI add-ons"""
        args = [
            "dhruvkit", "new", "fullapp",
            "--template", "fastapi",
            "--mongodb", "--firebase", "--secure"
        ]
        cmd_new(args)
        
        project_path = temp_cwd / "fullapp"
        
        # Verify all components exist
        assert project_path.exists()
        assert (project_path / "src" / "main.py").exists()
        
        requirements = (project_path / "requirements.txt").read_text()
        assert "pymongo" in requirements.lower()
        assert "firebase" in requirements.lower()
    
    def test_full_flow_init_then_add_license(self, temp_cwd):
        """Test init project then add license"""
        # First initialize project
        args = ["dhruvkit", "init", "--template", "basic"]
        cmd_init(args)
        
        assert (temp_cwd / "src" / "main.py").exists()
        assert not (temp_cwd / "LICENSE").exists()
        
        # Then add license
        args = ["dhruvkit", "add", "--license", "mit"]
        cmd_add(args)
        
        assert (temp_cwd / "LICENSE").exists()
        license_content = (temp_cwd / "LICENSE").read_text()
        assert "MIT" in license_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
