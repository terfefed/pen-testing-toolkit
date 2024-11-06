import subprocess
import sys
import os

def check_required_tools():
    """Check if required Kali Linux tools are installed"""
    tool_mapping = {
        'nmap': 'nmap',
        'nikto': 'nikto',
        'sqlmap': 'sqlmap',
        'dirb': 'dirb',
        'xsser': 'xsser',
        'zaproxy': 'zaproxy',
        'sslyze': 'sslyze',
        'dnstwist': 'dnstwist',
        'tcpdump': 'tcpdump',
        'aircrack-ng': 'aircrack-ng',
        'wifite': 'wifite2',
        'john': 'john',
        'hashcat': 'hashcat',
        'volatility3': 'python3-volatility3',  # Updated package name
        'autopsy': 'autopsy',
        'metasploit-framework': 'metasploit-framework',
        'searchsploit': 'exploitdb',  # Correct package name
        'set': 'set',
        'gophish': None  # Will be handled separately
    }
    
    missing_tools = []
    for tool, package in tool_mapping.items():
        if package and subprocess.run(['which', tool], capture_output=True).returncode != 0:
            missing_tools.append(package)
    
    return missing_tools

def install_missing_tools(tools):
    """Install missing tools using apt and additional methods"""
    try:
        # Update package lists
        print("[+] Updating package lists...")
        subprocess.run(['apt-get', 'update'], check=True)
        
        # Install tools from apt repositories
        for tool in tools:
            print(f"[+] Installing {tool}...")
            try:
                subprocess.run(['apt-get', 'install', '-y', tool], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error installing {tool}: {str(e)}")
                return False
        
        # Install additional tools that need special handling
        install_special_tools()
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {str(e)}")
        return False

def install_special_tools():
    """Install tools that need special handling"""
    # Install Volatility3 using pip if needed
    try:
        subprocess.run(['pip3', 'install', 'volatility3'], check=True)
    except subprocess.CalledProcessError:
        print("Error installing Volatility3 via pip")

    # Install Go if needed (for certain tools)
    try:
        if subprocess.run(['which', 'go'], capture_output=True).returncode != 0:
            subprocess.run(['apt-get', 'install', '-y', 'golang'], check=True)
    except subprocess.CalledProcessError:
        print("Error installing Go")

def setup_environment():
    """Setup additional environment requirements"""
    try:
        # Create necessary directories
        os.makedirs('/usr/share/wordlists', exist_ok=True)
        
        # Download additional wordlists if needed
        if not os.path.exists('/usr/share/wordlists/rockyou.txt'):
            subprocess.run([
                'wget',
                'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt',
                '-O',
                '/usr/share/wordlists/rockyou.txt'
            ], check=True)
        
        # Set up Metasploit database if needed
        subprocess.run(['msfdb', 'init'], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting up environment: {str(e)}")
        return False

# Updated main.py section for tool installation
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
