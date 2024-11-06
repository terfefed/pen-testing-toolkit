# modules/web_scanner.py
import os
import subprocess
import signal
import time

class WebScanner:
    def __init__(self, target_url, output_dir):
        self.target_url = target_url
        self.output_dir = output_dir
        self.web_dir = os.path.join(output_dir, 'web')
        os.makedirs(self.web_dir, exist_ok=True)
        self.timeout = 300  # 5 minutes default timeout

    def run_nikto_scan(self):
        """Run Nikto with timeout"""
        output_file = os.path.join(self.web_dir, 'nikto_scan.txt')
        try:
            print("[*] Starting Nikto scan (timeout: 5 minutes)...")
            process = subprocess.run([
                'nikto',
                '-h', self.target_url,
                '-output', output_file,
                '-maxtime', '300s'  # 5 minutes timeout
            ], timeout=self.timeout)
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] Nikto scan timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running Nikto: {str(e)}")
            return None

    def run_sqlmap(self):
        """Run SQLMap with timeout"""
        output_dir = os.path.join(self.web_dir, 'sqlmap')
        try:
            print("[*] Starting SQLMap scan (timeout: 5 minutes)...")
            process = subprocess.run([
                'sqlmap',
                '-u', self.target_url,
                '--batch',
                '--random-agent',
                '--level', '1',
                '--risk', '1',
                '--timeout', '60',
                '--output-dir', output_dir
            ], timeout=self.timeout)
            return output_dir
        except subprocess.TimeoutExpired:
            print("[-] SQLMap scan timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running SQLMap: {str(e)}")
            return None

    def run_dirb(self):
        """Run DIRB with timeout"""
        output_file = os.path.join(self.web_dir, 'dirb_scan.txt')
        try:
            print("[*] Starting DIRB scan (timeout: 5 minutes)...")
            process = subprocess.run([
                'dirb',
                self.target_url,
                '/usr/share/dirb/wordlists/common.txt',
                '-o', output_file,
                '-w'  # Don't stop on warning messages
            ], timeout=self.timeout)
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] DIRB scan timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running DIRB: {str(e)}")
            return None

    def run_xsser(self):
        """Run XSSer with timeout"""
        output_file = os.path.join(self.web_dir, 'xsser_scan.txt')
        try:
            print("[*] Starting XSSer scan (timeout: 5 minutes)...")
            process = subprocess.run([
                'xsser',
                '--url', self.target_url,
                '--auto',
                '--timeout', '60',
                '--output', output_file
            ], timeout=self.timeout)
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] XSSer scan timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running XSSer: {str(e)}")
            return None

# Update the run_web_scans function in main.py
def run_web_scans(web_scanner):
    """Run all web-related scans with proper timing"""
    print("\n[+] Starting web vulnerability scans...")
    
    try:
        print("\n[*] Running Nikto scan...")
        result = web_scanner.run_nikto_scan()
        if result:
            print("[+] Nikto scan completed")
            print(f"[+] Results saved to: {result}")
        
        print("\n[*] Running SQLMap scan...")
        result = web_scanner.run_sqlmap()
        if result:
            print("[+] SQLMap scan completed")
            print(f"[+] Results saved to: {result}")
        
        print("\n[*] Running directory enumeration...")
        result = web_scanner.run_dirb()
        if result:
            print("[+] DIRB scan completed")
            print(f"[+] Results saved to: {result}")
        
        print("\n[*] Running XSS tests...")
        result = web_scanner.run_xsser()
        if result:
            print("[+] XSSer scan completed")
            print(f"[+] Results saved to: {result}")
        
        print("\n[+] Web scanning completed")
        
    except KeyboardInterrupt:
        print("\n[-] Web scanning interrupted by user")
    except Exception as e:
        print(f"\n[-] Error during web scanning: {str(e)}")
