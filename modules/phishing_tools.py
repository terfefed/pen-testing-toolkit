import os
import subprocess

class PhishingAnalyzer:
    def __init__(self, domain, output_dir):
        self.domain = domain
        self.output_dir = os.path.join(output_dir, 'phishing')
        os.makedirs(self.output_dir, exist_ok=True)
        self.timeout = 300

    def analyze_domain(self):
        output_file = os.path.join(self.output_dir, 'domain_analysis.txt')
        try:
            subprocess.run([
                'sslyze',
                self.domain,
                '--json_out', output_file
            ], check=True, timeout=self.timeout)
            
            subprocess.run([
                'dnstwist',
                self.domain,
                '--format', 'json',
                '--output', os.path.join(self.output_dir, 'similar_domains.json')
            ], check=True, timeout=self.timeout)
            
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] Domain analysis timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error analyzing domain: {str(e)}")
            return None

