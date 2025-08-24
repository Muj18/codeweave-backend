import pytest

def pytest_addoption(parser):
    parser.addoption("--update-snapshots", action="store_true", default=False,
                     help="Update golden snapshots from current renders")
    parser.addoption("--no-snapshots", action="store_true", default=False,
                     help="Skip snapshot checks")
    parser.addoption("--family", action="append", default=[],
                     help="Only test templates whose path contains this substring (repeatable)")

def pytest_configure(config):
    config.addinivalue_line("markers", "rubric: rubric scoring tests")
