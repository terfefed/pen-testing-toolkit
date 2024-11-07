import os
import subprocess

class SocialEngineeringTools:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'social_engineering')
        os.makedirs(self.output_dir, exist_ok=True)
        self.timeout = 300

    def run_set_toolkit(self):
        output_file = os.path.join(self.output_dir, 'set_results.txt')
        try:
            config = os.path.join(self.output_dir, 'set_config')
            with open(config, 'w') as f:
                f.write("""
1
2
3
""")
            
            subprocess.run([
                'setoolkit',
                '-c', config
            ], check=True, timeout=self.timeout)
            return output_file
        except subprocess.TimeoutExpired:
            print("[-] Social Engineering Toolkit timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error running SET: {str(e)}")
            return None

    def run_gophish(self):
        config_file = os.path.join(self.output_dir, 'gophish_config.json')
        try:
            subprocess.run([
                'gophish',
                '--config', config_file
            ], check=True, timeout=self.timeout)
            return config_file
        except subprocess.TimeoutExpired:
            print("[-] Gophish timed out after 5 minutes")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error running Gophish: {str(e)}")
            return None

