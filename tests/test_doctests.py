import doctest
from pathlib import Path
import importlib.util

def process_file(py_file):
    """Run doctests for a Python file."""
    with open(py_file, 'r') as file:
        file_content = file.read()
    parser = doctest.DocTestParser()
    if not parser.get_doctest(file_content, {}, py_file.stem, py_file, 0).examples:
        return None
    print(f"Testing docstrings in {py_file}")
    spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    failures, _ = doctest.testmod(module)
    if failures > 0:
        raise AssertionError(f"Failed doctests in {py_file}")

def test_doctests():
    """Recursively process doctests in all Python files."""
    src_dir = Path('src/')
    files = list(src_dir.rglob('*.py'))
    failed_files = list(filter(None, map(process_file, files)))
    assert not failed_files, f"Doctests failed in the following files: {failed_files}"
