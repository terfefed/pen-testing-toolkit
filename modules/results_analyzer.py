# modules/results_analyzer.py
import os
import json
import re
from datetime import datetime

class ResultsAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.web_dir = os.path.join(output_dir, 'web')
        self.network_dir = os.path.join(output_dir, 'network')
        self.report_dir = os.path.join(output_dir, 'reports')
        
    def analyze_nikto_results(self):
        """Analyze Nikto scan results"""
        nikto_file = os.path.join(self.web_dir, 'nikto_scan.txt')
        findings = []
        
        if os.path.exists(nikto_file):
            with open(nikto_file, 'r') as f:
                content = f.read()
                # Extract vulnerabilities
                vulns = re.findall(r'\+ (OSVDB-\d+:.+)', content)
                for vuln in vulns:
                    findings.append({
                        'tool': 'Nikto',
                        'type': 'Web Vulnerability',
                        'description': vuln,
                        'severity': self._determine_severity(vuln)
                    })
        return findings
    
    def analyze_sqlmap_results(self):
        """Analyze SQLMap results"""
        sqlmap_dir = os.path.join(self.web_dir, 'sqlmap')
        findings = []
        
        if os.path.exists(sqlmap_dir):
            for root, dirs, files in os.walk(sqlmap_dir):
                for file in files:
                    if file.endswith('.log'):
                        with open(os.path.join(root, file), 'r') as f:
                            content = f.read()
                            if 'SQL injection point' in content:
                                findings.append({
                                    'tool': 'SQLMap',
                                    'type': 'SQL Injection',
                                    'description': 'SQL injection vulnerability found',
                                    'severity': 'High'
                                })
        return findings
    
    def analyze_nmap_results(self):
        """Analyze Nmap scan results"""
        nmap_file = os.path.join(self.network_dir, 'nmap_scan.xml')
        findings = []
        
        if os.path.exists(nmap_file):
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(nmap_file)
                root = tree.getroot()
                
                for host in root.findall('.//host'):
                    ip = host.find('.//address').get('addr')
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        state = port.find('state').get('state')
                        service = port.find('service')
                        if service is not None:
                            service_name = service.get('name')
                            findings.append({
                                'tool': 'Nmap',
                                'type': 'Open Port',
                                'description': f'Port {port_id} ({service_name}) is {state}',
                                'severity': self._determine_port_severity(service_name)
                            })
            except Exception as e:
                print(f"Error parsing Nmap results: {str(e)}")
        return findings
    
    def _determine_severity(self, finding):
        """Determine severity of a finding"""
        high_indicators = ['sql injection', 'remote code execution', 'rce', 'xss', 'csrf']
        medium_indicators = ['information disclosure', 'directory listing', 'deprecated']
        
        finding_lower = finding.lower()
        for indicator in high_indicators:
            if indicator in finding_lower:
                return 'High'
        for indicator in medium_indicators:
            if indicator in finding_lower:
                return 'Medium'
        return 'Low'
    
    def _determine_port_severity(self, service):
        """Determine severity of open ports based on service"""
        critical_services = ['ms-sql', 'mysql', 'oracle', 'telnet', 'ftp']
        high_risk_services = ['ssh', 'rdp', 'vnc', 'smtp']
        
        service_lower = service.lower()
        if any(s in service_lower for s in critical_services):
            return 'Critical'
        if any(s in service_lower for s in high_risk_services):
            return 'High'
        return 'Medium'
    
    def generate_report(self):
        """Generate comprehensive security report"""
        findings = []
        findings.extend(self.analyze_nikto_results())
        findings.extend(self.analyze_sqlmap_results())
        findings.extend(self.analyze_nmap_results())
        
        # Count findings by severity
        severity_count = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for finding in findings:
            severity_count[finding['severity']] = severity_count.get(finding['severity'], 0) + 1
        
        report = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_findings': len(findings),
                'severity_distribution': severity_count
            },
            'findings': findings
        }
        
        # Generate HTML report
        html_report = self._generate_html_report(report)
        report_file = os.path.join(self.report_dir, f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        
        with open(report_file, 'w') as f:
            f.write(html_report)
        
        print(f"\n[+] Report generated: {report_file}")
        return report_file
    
    def _generate_html_report(self, report):
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Assessment Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: #f5f5f5; padding: 20px; margin-bottom: 20px; }}
                .summary {{ margin-bottom: 30px; }}
                .finding {{ border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }}
                .Critical {{ border-left: 5px solid #ff0000; }}
                .High {{ border-left: 5px solid #ff9900; }}
                .Medium {{ border-left: 5px solid #ffcc00; }}
                .Low {{ border-left: 5px solid #99cc00; }}
                .severity-distribution {{ display: flex; margin: 20px 0; }}
                .severity-count {{ margin-right: 20px; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Security Assessment Report</h1>
                    <p>Scan Date: {report['scan_date']}</p>
                </div>
                
                <div class="summary">
                    <h2>Executive Summary</h2>
                    <p>Total Findings: {report['summary']['total_findings']}</p>
                    
                    <div class="severity-distribution">
                        <div class="severity-count" style="background: #ffeeee;">
                            Critical: {report['summary']['severity_distribution'].get('Critical', 0)}
                        </div>
                        <div class="severity-count" style="background: #fff6ee;">
                            High: {report['summary']['severity_distribution'].get('High', 0)}
                        </div>
                        <div class="severity-count" style="background: #fffbee;">
                            Medium: {report['summary']['severity_distribution'].get('Medium', 0)}
                        </div>
                        <div class="severity-count" style="background: #f6ffee;">
                            Low: {report['summary']['severity_distribution'].get('Low', 0)}
                        </div>
                    </div>
                </div>
                
                <h2>Detailed Findings</h2>
        """
        
        # Sort findings by severity
        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        sorted_findings = sorted(report['findings'], 
                               key=lambda x: severity_order.get(x['severity'], 999))
        
        for finding in sorted_findings:
            html += f"""
                <div class="finding {finding['severity']}">
                    <h3>{finding['type']}</h3>
                    <p><strong>Tool:</strong> {finding['tool']}</p>
                    <p><strong>Severity:</strong> {finding['severity']}</p>
                    <p><strong>Description:</strong> {finding['description']}</p>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html

# Add to main.py
def analyze_results(output_dir):
    """Analyze scan results and generate report"""
    print("\n[+] Analyzing scan results...")
    analyzer = ResultsAnalyzer(output_dir)
    report_file = analyzer.generate_report()
    print(f"[+] Analysis complete! Report saved to: {report_file}")
    
    # Open report in default browser
    try:
        import webbrowser
        webbrowser.open(report_file)
    except:
        pass
