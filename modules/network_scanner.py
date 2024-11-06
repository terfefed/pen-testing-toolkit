# modules/network_scanner.py
import os
import subprocess
import time
import signal
from datetime import datetime

class NetworkScanner:
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = os.path.join(output_dir, 'network')
        os.makedirs(self.output_dir, exist_ok=True)
        self.tcpdump_process = None

    def run_nmap_scan(self):
        """Run Nmap scan with progress indicator"""
        output_file = os.path.join(self.output_dir, 'nmap_scan.xml')
        try:
            print("[*] Starting Nmap scan...")
            subprocess.run([
                'nmap',
                '-sS', '-sV', '-sC',  # SYN scan, Version detection, Default scripts
                '-T4',                 # Aggressive timing
                '--max-retries', '2',  # Limit retries
                '-A',
                '-oX', output_file,
                self.target
            ], check=True)
            print("[+] Nmap scan completed")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running Nmap: {str(e)}")
            return None

    def capture_traffic(self, interface, duration=30):
        """
        Capture network traffic with timeout
        duration: capture time in seconds (default 30s)
        """
        output_file = os.path.join(self.output_dir, 'traffic_capture.pcap')
        try:
            print(f"[*] Starting packet capture on {interface} for {duration} seconds...")
            
            # Start tcpdump with specific filters
            self.tcpdump_process = subprocess.Popen([
                'tcpdump',
                '-i', interface,
                '-w', output_file,
                'not port 22',  # Exclude SSH traffic
                '-c', '1000'    # Capture max 1000 packets
            ])
            
            # Show progress bar
            for i in range(duration):
                progress = (i + 1) / duration * 100
                print(f"\rProgress: [{('=' * int(progress/2)).ljust(50)}] {progress:.1f}%", end='')
                time.sleep(1)
                
                # Check if capture completed early
                if self.tcpdump_process.poll() is not None:
                    break
            
            print("\n[+] Packet capture completed")
            return output_file
            
        except subprocess.CalledProcessError as e:
            print(f"\n[-] Error capturing traffic: {str(e)}")
            return None
        finally:
            self.stop_capture()

    def stop_capture(self):
        """Stop ongoing packet capture"""
        if self.tcpdump_process:
            self.tcpdump_process.terminate()
            try:
                self.tcpdump_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.tcpdump_process.kill()
            self.tcpdump_process = None

def run_network_scans(network_scanner, interface):
    """Run all network-related scans"""
    print("\n[+] Starting network security assessment...")
    
    try:
        print("[*] Running Nmap scan...")
        network_scanner.run_nmap_scan()
        
        print(f"\n[*] Capturing network traffic on {interface}...")
        network_scanner.capture_traffic(interface, duration=30)  # 30 seconds capture
        
    except Exception as e:
        print(f"[-] Error during network scanning: {str(e)}")
    finally:
        network_scanner.stop_capture()
