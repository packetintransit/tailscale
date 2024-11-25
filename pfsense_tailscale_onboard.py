import requests

class PfSenseTailscaleOnboard:
    def __init__(self, pfsense_url, pfsense_api_key, pfsense_api_secret, tailscale_api_key):
        """
        Initialize the library.
        :param pfsense_url: Base URL of the pfSense API (e.g., "https://192.168.1.1/api").
        :param pfsense_api_key: API key for the pfSense firewall.
        :param pfsense_api_secret: API secret for the pfSense firewall.
        :param tailscale_api_key: API key for Tailscale.
        """
        self.pfsense_url = pfsense_url.rstrip("/")
        self.pfsense_headers = {
            "Authorization": f"Bearer {pfsense_api_key}:{pfsense_api_secret}",
            "Content-Type": "application/json",
        }
        self.tailscale_api_key = tailscale_api_key
        self.tailscale_api_url = "https://api.tailscale.com/api/v2"

    def onboard_firewall(self, hostname):
        """
        Onboard the pfSense firewall to Tailscale.
        :param hostname: Desired hostname for the Tailscale device.
        """
        try:
            # Step 1: Install and configure Tailscale on the firewall
            self._install_and_configure_tailscale()

            # Step 2: Register the firewall in Tailscale
            self._add_device_to_tailscale(hostname)
            
            print(f"Successfully onboarded pfSense firewall to Tailscale with hostname: {hostname}")
        except Exception as e:
            print(f"Error onboarding firewall: {e}")

    def _install_and_configure_tailscale(self):
        """
        Install and configure Tailscale on the pfSense firewall.
        """
        try:
            # Install Tailscale package
            install_response = requests.post(
                f"{self.pfsense_url}/packages/install",
                headers=self.pfsense_headers,
                json={"name": "tailscale"},
                verify=False,
            )
            if install_response.status_code != 200:
                raise Exception(f"Failed to install Tailscale: {install_response.text}")

            # Configure Tailscale
            config_response = requests.post(
                f"{self.pfsense_url}/services/tailscale",
                headers=self.pfsense_headers,
                json={"action": "start"},
                verify=False,
            )
            if config_response.status_code != 200:
                raise Exception(f"Failed to configure Tailscale: {config_response.text}")

        except Exception as e:
            raise Exception(f"Failed to install/configure Tailscale on pfSense: {e}")

    def _add_device_to_tailscale(self, hostname):
        """
        Register the firewall in the Tailscale network.
        :param hostname: Desired hostname for the Tailscale device.
        """
        try:
            headers = {"Authorization": f"Bearer {self.tailscale_api_key}"}
            data = {
                "hostname": hostname,
                "tags": ["tag:pfsense-firewall"],  # Example tags
            }
            response = requests.post(f"{self.tailscale_api_url}/devices", headers=headers, json=data)

            if response.status_code != 200:
                raise Exception(f"Tailscale API error: {response.text}")
        except Exception as e:
            raise Exception(f"Tailscale device addition failed: {e}")