import os
import subprocess

class SocialEngineeringTools:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'social_engineering')
        os.makedirs(self.output_dir, exist_ok=True)

    def run_set_toolkit(self):
        """Run Social Engineering Toolkit"""
        output_file = os.path.join(self.output_dir, 'set_results.txt')
        try:
            # Create automated SET configuration
            config = os.path.join(self.output_dir, 'set_config')
            with open(config, 'w') as f:
                f.write("""
1
2
3
""")  # Configure based on needed SE attack
            
            subprocess.run([
                'setoolkit',
                '-c', config
            ], check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running SET: {str(e)}")
            return None

    def run_gophish(self):
        """Setup and run Gophish phishing framework"""
        config_file = os.path.join(self.output_dir, 'gophish_config.json')
        try:
            subprocess.run([
                'gophish',
                '--config', config_file
            ], check=True)
            return config_file
        except subprocess.CalledProcessError as e:
            print(f"Error running Gophish: {str(e)}")
            return None
