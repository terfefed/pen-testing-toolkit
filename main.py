#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
import time
from datetime import datetime
from urllib.parse import urlparse

# Import modules from local directories
try:
    from modules.web_scanner import WebScanner
    from modules.api_tester import APITester
    from modules.phishing_tools import PhishingAnalyzer
    from modules.network_scanner import NetworkScanner
    from modules.wireless_scanner import WirelessScanner
    from modules.password_tools import PasswordTools
    from modules.forensics_tools import ForensicsTools
    from modules.exploitation import ExploitationTools
    from modules.social_engineering import SocialEngineeringTools
    from utils.tool_checker import check_required_tools, install_missing_tools, setup_environment
    from modules.results_analyzer import ResultsAnalyzer, analyze_results
except ImportError as e:
    print(f"[-] Error importing modules: {str(e)}")
    print("[-] Please ensure all required modules are in the correct directories:")
    print("    - modules/")
    print("    - utils/")
    sys.exit(1)

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════╗
    ║     Kali Linux Security Testing Suite     ║
    ║         Advanced Testing Framework        ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)

def check_and_install_tools():
    """Check and install all required tools"""
    print("[+] Checking required tools...")
    missing_tools = check_required_tools()
    
    if missing_tools:
        print(f"[+] Installing missing tools: {', '.join(missing_tools)}")
        if not install_missing_tools(missing_tools):
            print("[-] Failed to install some tools")
            response = input("Do you want to continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    print("[+] Setting up environment...")
    if not setup_environment():
        print("[-] Failed to setup environment completely")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def create_output_structure(base_dir):
    """Create output directory structure"""
    directories = [
        'web',
        'api',
        'network',
        'wireless',
        'passwords',
        'forensics',
        'exploitation',
        'social_engineering',
        'reports'
    ]
    
    for directory in directories:
        path = os.path.join(base_dir, directory)
        os.makedirs(path, exist_ok=True)
        print(f"[+] Created directory: {path}")

def run_web_scans(web_scanner):
    """Run all web-related scans"""
    print("\n[+] Starting web vulnerability scans...")
    
    try:
        print("[*] Running Nikto scan...")
        web_scanner.run_nikto_scan()
        
        print("[*] Running SQLMap scan...")
        web_scanner.run_sqlmap()
        
        print("[*] Running directory enumeration...")
        web_scanner.run_dirb()
        
        print("[*] Running XSS tests...")
        web_scanner.run_xsser()
        
    except Exception as e:
        print(f"[-] Error during web scanning: {str(e)}")

def run_network_scans(network_scanner, interface):
    """Run all network-related scans"""
    print("\n[+] Starting network security assessment...")
    
    try:
        print("[*] Running Nmap scan...")
        network_scanner.run_nmap_scan()
        
        print(f"[*] Capturing network traffic on {interface}...")
        network_scanner.capture_traffic(interface)
        
    except Exception as e:
        print(f"[-] Error during network scanning: {str(e)}")

def analyze_results(output_dir):
    """Analyze scan results and generate report"""
    print("\n[+] Analyzing scan results...")
    analyzer = ResultsAnalyzer(output_dir)
    report_file = analyzer.generate_report()
    print(f"[+] Analysis complete! Report saved to: {report_file}")
    
    # Open report in default browser
    try:
        import webbrowser
        webbrowser.open('file://' + os.path.abspath(report_file))
    except Exception as e:
        print(f"[-] Could not open report automatically: {str(e)}")
        print(f"[*] Please open the report manually at: {report_file}")

def main():
    # Verify the directory structure exists
    if not os.path.exists('modules') or not os.path.exists('utils'):
        print("[-] Required directories not found. Creating directory structure...")
        os.makedirs('modules', exist_ok=True)
        os.makedirs('utils', exist_ok=True)
        print("[!] Please ensure all required modules are placed in their respective directories.")
        sys.exit(1)

    print_banner()
    
    parser = argparse.ArgumentParser(description='Kali Linux Security Testing Framework')
    
    # Required arguments
    parser.add_argument('--url', required=True, help='Target URL')
    
    # Optional arguments
    parser.add_argument('--api', help='API endpoint to test')
    parser.add_argument('--interface', default='eth0', help='Network interface for traffic capture')
    parser.add_argument('--output', default='security_assessment', help='Output directory')
    parser.add_argument('--wireless', action='store_true', help='Enable wireless scanning')
    parser.add_argument('--password-file', help='File containing hashes to crack')
    parser.add_argument('--forensics-image', help='Path to forensics image')
    parser.add_argument('--memory-dump', help='Path to memory dump file')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode (slower but quieter)')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds for each scan 	(default: 300)')
    parser.add_argument('--quick', action='store_true', help='Perform quick scans only')
    parser.add_argument('--report-only', action='store_true', help='Only analyze existing results without scanning')
    
    args = parser.parse_args()
    
    # Check for root privileges
    if os.geteuid() != 0:
        print("[-] This script must be run as root")
        sys.exit(1)
        
    if args.report_only:
        if os.path.exists(args.output):
            analyze_results(args.output)
            sys.exit(0)
        else:
            print(f"[-] Output directory {args.output} not found!")
            sys.exit(1)
    
    # Check and install required tools
    check_and_install_tools()
    
    # Create output directory structure
    create_output_structure(args.output)
    
    try:
        # Initialize scanners
        web_scanner = WebScanner(args.url, args.output)
        network_scanner = NetworkScanner(urlparse(args.url).netloc, args.output)
        
        # Start scanning
        print("\n[+] Starting comprehensive security assessment...")
        start_time = time.time()
        
        # Web Application Testing
        run_web_scans(web_scanner)
        
        # API Testing
        if args.api:
            print("\n[+] Starting API security testing...")
            api_tester = APITester(args.api, args.output)
            api_tester.run_api_scan()
        
        # Network Scanning
        run_network_scans(network_scanner, args.interface)
        
        # Wireless Scanning
        if args.wireless:
            print("\n[+] Starting wireless security assessment...")
            wireless_scanner = WirelessScanner(args.interface, args.output)
            wireless_scanner.run_aircrack_scan()
            wireless_scanner.run_wifite()
        
        # Password Testing
        if args.password_file:
            print("\n[+] Starting password analysis...")
            password_tools = PasswordTools(args.output)
            password_tools.run_john(args.password_file)
            password_tools.run_hashcat(args.password_file, '0')
        
        # Forensics Analysis
        if args.forensics_image or args.memory_dump:
            print("\n[+] Starting forensics analysis...")
            forensics_tools = ForensicsTools(args.output)
            
            if args.memory_dump:
                forensics_tools.run_volatility(args.memory_dump)
            
            if args.forensics_image:
                forensics_tools.run_autopsy(args.forensics_image)
        
        # Exploitation Testing
        print("\n[+] Running exploitation checks...")
        exploitation_tools = ExploitationTools(args.output)
        exploitation_tools.run_metasploit_scan(urlparse(args.url).netloc)
        exploitation_tools.run_searchsploit(urlparse(args.url).netloc)
        
        # Social Engineering Setup
        print("\n[+] Setting up social engineering tools...")
        social_tools = SocialEngineeringTools(args.output)
        social_tools.run_set_toolkit()
        social_tools.run_gophish()
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        print("\n[+] Assessment Summary:")
        print(f"{'='*50}")
        print(f"Target: {args.url}")
        print(f"Duration: {execution_time:.2f} seconds")
        print(f"Output Directory: {args.output}")
        print(f"{'='*50}")
        
        # Add this line to analyze results after scanning
        analyze_results(args.output)
        
        print("\n[+] Assessment complete! Check the output directory for detailed results.")
        
    except KeyboardInterrupt:
        print("\n[-] Assessment interrupted by user.")
        print("[*] Generating report for completed scans...")
        analyze_results(args.output)
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] An error occurred: {str(e)}")
        print("[*] Attempting to generate report for completed scans...")
        try:
            analyze_results(args.output)
        except Exception as e:
            print(f"[-] Could not generate report: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
