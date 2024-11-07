import os
import subprocess

class ForensicsTools:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'forensics')
        os.makedirs(self.output_dir, exist_ok=True)
        self.timeout = 300

    def run_volatility(self, memory_dump):
        output_file = os.path.join(self.output_dir, 'volatility_analysis.txt')
        try:
            plugins = ['pslist', 'netscan', 'malfind', 'filescan']
            
            with open(output_file, 'w') as f:
                for plugin in plugins:
                    result = subprocess.run([
                        'volatility',
                        '-f', memory_dump,
                        '--profile=Win10x64', 
                        plugin
                    ], capture_output=True, text=True, timeout=self.timeout)
                    f.write(f"\n=== {plugin} ===\n")
                    f.write(result.stdout)
            
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] Volatility analysis timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error running Volatility: {str(e)}")
            return None

    def run_autopsy(self, evidence_file):
        case_dir = os.path.join(self.output_dir, 'autopsy_case')
        try:
            subprocess.run([
                'autopsy',
                '--case=' + case_dir,
                '--add=' + evidence_file
            ], check=True, timeout=self.timeout)
            return case_dir
        except subprocess.TimeoutExpired:
            print("[-] Autopsy case creation timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error running Autopsy: {str(e)}")
            return None

