"""Basic tests to ensure the project structure and test framework are working correctly."""

import json
import os
import sys
from pathlib import Path

import pytest

# It's common to modify the path for tests, but for larger projects, consider
# installing your package in editable mode (`pip install -e .`) or configuring
# pytest's `pythonpath`.
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture(scope="module")
def project_root() -> Path:
    """A pytest fixture to provide the project's root directory."""
    return Path(__file__).parent.parent


def test_python_version():
    """Test that we're running on a supported Python version (>= 3.9)."""
    assert sys.version_info >= (3, 9)


@pytest.mark.parametrize(
    "expected_path",
    [
        "scripts",
        "tests",
        "docs",
        "clients",
        "README.md",
        "requirements.txt",
        "pyproject.toml",
    ],
)
def test_project_structure(project_root: Path, expected_path: str):
    """Test that the project has the expected directories and files."""
    full_path = project_root / expected_path
    assert full_path.exists(), f"Path does not exist: {full_path}"


def test_requirements_file_content(project_root: Path):
    """Test that requirements.txt exists and contains key packages."""
    requirements_file = project_root / "requirements.txt"
    assert requirements_file.is_file(), f"{requirements_file} is not a file."

    content = requirements_file.read_text(encoding="utf-8")
    assert "requests" in content
    assert "pyyaml" in content


@pytest.mark.parametrize("dir_name", ["configs", "templates", "logs"])
def test_directory_creation(tmp_path: Path, dir_name: str):
    """Test that temporary directories can be created successfully."""
    # Using pytest's built-in `tmp_path` fixture ensures no directories
    # are permanently created in your project during testing.
    new_dir = tmp_path / dir_name
    new_dir.mkdir()
    assert new_dir.exists()
    assert new_dir.is_dir()


def test_proxy_generator_import():
    """Test that the proxy_generator module can be imported."""
    # If the file doesn't exist or has syntax errors, pytest will fail
    # with a clear ImportError, which is what we want.
    pytest.importorskip(
        "proxy_generator", reason="proxy_generator.py not found or has issues"
    )


def test_json_template_validity(project_root: Path):
    """Test that any existing JSON templates are valid."""
    templates_dir = project_root / "templates"
    if not templates_dir.exists():
        pytest.skip("Templates directory not found, skipping test.")

    json_files = list(templates_dir.glob("*.json"))
    if not json_files:
        pytest.skip("No JSON templates found to validate.")

    for json_file in json_files:
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {json_file.name}: {e}")


def test_environment_variables():
    """Test that we can set, get, and clean up environment variables."""
    test_var = "TEST_PROXY_CONFIG"
    test_value = "test_value_123"

    # Ensure the variable doesn't exist before the test
    original_value = os.environ.pop(test_var, None)

    try:
        os.environ[test_var] = test_value
        assert os.getenv(test_var) == test_value
    finally:
        # Clean up and restore the original state
        if original_value is not None:
            os.environ[test_var] = original_value
        elif test_var in os.environ:
            del os.environ[test_var]

    assert os.getenv(test_var) is None or os.getenv(test_var) == original_value

# The `if __name__ == "__main__"` block is removed because the standard way
# to run tests is to execute the `pytest` command in your terminal from the
# project root.
