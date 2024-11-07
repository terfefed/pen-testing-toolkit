import os
import subprocess

class APITester:
    def __init__(self, api_endpoint, output_dir):
        self.api_endpoint = api_endpoint
        self.output_dir = os.path.join(output_dir, 'api')
        os.makedirs(self.output_dir, exist_ok=True)
        self.timeout = 300

    def run_api_scan(self):
        output_file = os.path.join(self.output_dir, 'api_scan.txt')
        try:
            subprocess.run([
                'zaproxy',
                '-cmd',
                '-quickurl', self.api_endpoint,
                '-quickout', output_file
            ], check=True, timeout=self.timeout)
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] API scan timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"[-] Error running API scan: {str(e)}")
            return None

