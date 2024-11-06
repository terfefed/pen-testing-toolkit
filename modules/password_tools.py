import os
import subprocess

class PasswordTools:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'passwords')
        os.makedirs(self.output_dir, exist_ok=True)

    def run_john(self, hash_file):
        """Run John the Ripper for password cracking"""
        output_file = os.path.join(self.output_dir, 'john_results.txt')
        try:
            subprocess.run([
                'john',
                '--wordlist=/usr/share/wordlists/rockyou.txt',
                '--format=raw-md5',
                '--output=' + output_file,
                hash_file
            ], check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running John: {str(e)}")
            return None

    def run_hashcat(self, hash_file, hash_type):
        """Run Hashcat for GPU-accelerated password cracking"""
        output_file = os.path.join(self.output_dir, 'hashcat_results.txt')
        try:
            subprocess.run([
                'hashcat',
                '-m', hash_type,
                '-a', '0',
                hash_file,
                '/usr/share/wordlists/rockyou.txt',
                '--output', output_file
            ], check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running Hashcat: {str(e)}")
            return None
