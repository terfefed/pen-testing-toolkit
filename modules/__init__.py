"""
Kali Linux Security Testing Framework - Modules Package

This package contains all the security testing modules including:
- Web Application Scanner
- Network Scanner
- API Tester
- Wireless Scanner
- Password Tools
- Forensics Tools
- Exploitation Tools
- Social Engineering Tools
"""

from .web_scanner import WebScanner
from .network_scanner import NetworkScanner
from .api_tester import APITester
from .phishing_tools import PhishingAnalyzer
from .wireless_scanner import WirelessScanner
from .password_tools import PasswordTools
from .forensics_tools import ForensicsTools
from .exploitation import ExploitationTools
from .social_engineering import SocialEngineeringTools

__all__ = [
    'WebScanner',
    'NetworkScanner',
    'APITester',
    'PhishingAnalyzer',
    'WirelessScanner',
    'PasswordTools',
    'ForensicsTools',
    'ExploitationTools',
    'SocialEngineeringTools'
]

__version__ = '1.0.0'
__author__ = 'Abc'
__email__ = 'vitecm701@gmail.com'
