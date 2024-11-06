import os
import subprocess
import time

class WirelessScanner:
    def __init__(self, interface, output_dir):
        self.interface = interface
        self.output_dir = os.path.join(output_dir, 'wireless')
        os.makedirs(self.output_dir, exist_ok=True)

    def run_aircrack_scan(self):
        """Run Aircrack-ng suite for wireless scanning"""
        try:
            # Kill interfering processes
            subprocess.run(['airmon-ng', 'check', 'kill'], check=True)
            
            # Start monitor mode
            subprocess.run(['airmon-ng', 'start', self.interface], check=True)
            
            monitor_interface = f"{self.interface}mon"
            output_file = os.path.join(self.output_dir, 'airodump')
            
            # Start scanning
            subprocess.Popen([
                'airodump-ng',
                '--write', output_file,
                '--output-format', 'csv',
                monitor_interface
            ])
            
            # Scan for 60 seconds
            time.sleep(60)
            
            # Kill airodump-ng
            subprocess.run(['pkill', 'airodump-ng'], check=True)
            
            # Stop monitor mode
            subprocess.run(['airmon-ng', 'stop', monitor_interface], check=True)
            
            return output_file + '-01.csv'
        except subprocess.CalledProcessError as e:
            print(f"Error in wireless scanning: {str(e)}")
            return None

    def run_wifite(self):
        """Run Wifite for automated wireless auditing"""
        output_file = os.path.join(self.output_dir, 'wifite_results.txt')
        try:
            subprocess.run([
                'wifite',
                '--interface', self.interface,
                '--kill',
                '--dict', '/usr/share/wordlists/rockyou.txt',
                '--output', output_file
            ], check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running Wifite: {str(e)}")
            return None
