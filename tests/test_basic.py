"""Basic tests to ensure the testing framework works."""

import json
import os
import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def test_python_version():
    """Test that we're running on a supported Python version."""
    assert sys.version_info >= (3, 9)


def test_project_structure():
    """Test that the project has the expected structure."""
    project_root = Path(__file__).parent.parent
    
    # Check for essential directories
    assert (project_root / "scripts").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "docs").exists()
    assert (project_root / "clients").exists()
    
    # Check for essential files
    assert (project_root / "README.md").exists()
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "pyproject.toml").exists()


def test_requirements_file():
    """Test that requirements.txt exists and is readable."""
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    
    assert requirements_file.exists()
    
    with open(requirements_file, "r") as f:
        content = f.read()
        assert "requests" in content
        assert "pyyaml" in content


def test_config_directory_creation():
    """Test that config directories can be created."""
    project_root = Path(__file__).parent.parent
    
    # Create configs directory if it doesn't exist
    configs_dir = project_root / "configs"
    configs_dir.mkdir(exist_ok=True)
    
    assert configs_dir.exists()
    assert configs_dir.is_dir()


def test_templates_directory_creation():
    """Test that templates directories can be created."""
    project_root = Path(__file__).parent.parent
    
    # Create templates directory if it doesn't exist
    templates_dir = project_root / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    assert templates_dir.exists()
    assert templates_dir.is_dir()


def test_logs_directory_creation():
    """Test that logs directories can be created."""
    project_root = Path(__file__).parent.parent
    
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    assert logs_dir.exists()
    assert logs_dir.is_dir()


@pytest.mark.skipif(not Path("scripts/proxy_generator.py").exists(), 
                   reason="proxy_generator.py not found")
def test_proxy_generator_import():
    """Test that proxy_generator can be imported."""
    try:
        import proxy_generator
        assert hasattr(proxy_generator, 'main') or hasattr(proxy_generator, 'ProxyGenerator')
    except ImportError:
        pytest.skip("proxy_generator module not importable")


def test_json_template_validity():
    """Test that any existing JSON templates are valid."""
    project_root = Path(__file__).parent.parent
    templates_dir = project_root / "templates"
    
    if templates_dir.exists():
        for json_file in templates_dir.glob("*.json"):
            with open(json_file, "r") as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {json_file}: {e}")


def test_environment_variables():
    """Test that we can handle environment variables."""
    # Test that we can set and get environment variables
    test_var = "TEST_PROXY_CONFIG"
    test_value = "test_value"
    
    os.environ[test_var] = test_value
    assert os.getenv(test_var) == test_value
    
    # Clean up
    del os.environ[test_var]


if __name__ == "__main__":
    pytest.main([__file__])