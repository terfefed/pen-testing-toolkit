"""
Kali Linux Security Testing Framework - Utilities Package

This package contains utility functions and helpers including:
- Tool checking and installation
- Environment setup
- Common helper functions
"""

from .tool_checker import (
    check_required_tools,
    install_missing_tools,
    setup_environment
)

__all__ = [
    'check_required_tools',
    'install_missing_tools',
    'setup_environment'
]

__version__ = '1.0.0'
