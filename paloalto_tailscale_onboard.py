import requests
import xml.etree.ElementTree as ET

class PaloAltoTailscaleOnboard:
    def __init__(self, palo_alto_ip, palo_alto_api_key, tailscale_api_key):
        """
        Initialize the library.
        :param palo_alto_ip: IP address of the Palo Alto firewall.
        :param palo_alto_api_key: API key for the Palo Alto firewall.
        :param tailscale_api_key: API key for Tailscale.
        """
        self.palo_alto_ip = palo_alto_ip
        self.palo_alto_api_key = palo_alto_api_key
        self.tailscale_api_key = tailscale_api_key
        self.tailscale_api_url = "https://api.tailscale.com/api/v2"

    def onboard_firewall(self, hostname):
        """
        Onboard the Palo Alto firewall to Tailscale.
        :param hostname: Desired hostname for the Tailscale network.
        """
        try:
            # Step 1: Configure Tailscale on the firewall
            self._configure_tailscale_on_firewall()

            # Step 2: Register the firewall in Tailscale
            self._add_device_to_tailscale(hostname)
            
            print(f"Successfully onboarded firewall ({self.palo_alto_ip}) to Tailscale with hostname: {hostname}")
        except Exception as e:
            print(f"Error onboarding firewall: {e}")

    def _configure_tailscale_on_firewall(self):
        """
        Configure Tailscale routing on the Palo Alto firewall.
        """
        try:
            # Example configuration: Add a static route or NAT for Tailscale
            url = f"https://{self.palo_alto_ip}/api/"
            params = {
                "type": "config",
                "action": "set",
                "xpath": "/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/routing-table/ip/static-route/entry[@name='Tailscale-Route']",
                "element": "<destination>100.64.0.0/10</destination><nexthop><ip-address>192.168.1.1</ip-address></nexthop><interface>ethernet1/1</interface><metric>10</metric>",
                "key": self.palo_alto_api_key,
            }
            response = requests.get(url, params=params, verify=False)
            
            if response.status_code != 200 or "<status>success</status>" not in response.text:
                raise Exception("Failed to configure Tailscale routing on the firewall.")
        except Exception as e:
            raise Exception(f"Firewall configuration failed: {e}")

    def _add_device_to_tailscale(self, hostname):
        """
        Register the firewall in the Tailscale network.
        :param hostname: Desired hostname for the Tailscale device.
        """
        try:
            headers = {"Authorization": f"Bearer {self.tailscale_api_key}"}
            data = {
                "hostname": hostname,
                "tags": ["tag:paloalto-firewall"],  # Example tags
            }
            response = requests.post(f"{self.tailscale_api_url}/devices", headers=headers, json=data)

            if response.status_code != 200:
                raise Exception(f"Tailscale API error: {response.text}")
        except Exception as e:
            raise Exception(f"Tailscale device addition failed: {e}")