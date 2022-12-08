import nmap3
from scanInterface import ScannerForm

class scanner(ScannerForm):
    def __init__(self, scan_param):
        super().__init__(scan_param)

    def scan(self):
        """
        parameters = {
            "ports": "<String in nmap formatting stating strings>"
        }
        """
        
        nmap = nmap3.Nmap()
        
        targets = self.scan_param["targets"]
        ports = self.scan_param["parameters"]["ports"]
        for ip in targets["ips"]:
            version_results = nmap.nmap_version_detection(ip, args="-Pn -p "+ports)
            
            print(version_results)
        


if __name__ == "__main__":
    scan_param = {
        "targets": {
            "ips": [ "192.168.1.234", "192.168.1.238", "192.168.1.134"]
        },
        "parameters": {
            "ports" : "70,80,100"
        }
    }
    
    scanner = scanner(scan_param)
    scanner.scan()