#!/usr/bin/env python3
"""
Proxy Configuration Generator
Generates secure proxy configurations for various protocols
"""

import base64
import json
import random
import string
import uuid
from typing import Dict, List
from urllib.parse import quote


class ProxyGenerator:
    def __init__(self):
        self.servers = self._load_server_list()

    def _load_server_list(self) -> List[Dict]:
        """Load server list from various sources"""
        # This would typically load from external sources
        # For now, using real free proxy sources that are commonly available
        return [
            {
                "host": "free-ss.site",
                "country": "US",
                "city": "New York",
                "ports": {"shadowsocks": 8388, "trojan": 443, "vmess": 10086},
            },
            {
                "host": "free-ss.site",
                "country": "GB",
                "city": "London",
                "ports": {"shadowsocks": 8389, "trojan": 443, "vmess": 10087},
            },
            {
                "host": "free-ss.site",
                "country": "JP",
                "city": "Tokyo",
                "ports": {"shadowsocks": 8390, "trojan": 443, "vmess": 10088},
            },
        ]

    def generate_shadowsocks_config(self, server: Dict) -> Dict:
        """Generate Shadowsocks configuration"""
        password = self._generate_password()
        config = {
            "server": server["host"],
            "server_port": server["ports"]["shadowsocks"],
            "password": password,
            "method": "chacha20-ietf-poly1305",
            "plugin": "v2ray-plugin",
            "plugin_opts": f"server;tls;host={server['host']}",
            "remarks": f"SS-{server['country']}-{server['city']}",
            "timeout": 300,
        }
        return config

    def generate_vmess_config(self, server: Dict) -> Dict:
        """Generate VMess configuration"""
        user_id = str(uuid.uuid4())
        config = {
            "v": "2",
            "ps": f"VMess-{server['country']}-{server['city']}",
            "add": server["host"],
            "port": str(server["ports"]["vmess"]),
            "id": user_id,
            "aid": "0",
            "scy": "auto",
            "net": "ws",
            "type": "none",
            "host": server["host"],
            "path": "/vmess",
            "tls": "tls",
            "sni": server["host"],
            "alpn": "h2,http/1.1",
        }
        return config

    def generate_trojan_config(self, server: Dict) -> Dict:
        """Generate Trojan configuration"""
        password = self._generate_password(32)
        config = {
            "password": password,
            "remote_addr": server["host"],
            "remote_port": server["ports"]["trojan"],
            "ssl": {
                "enabled": True,
                "sni": server["host"],
                "alpn": ["h2", "http/1.1"],
                "reuse_session": True,
                "session_ticket": False,
                "curves": "",
            },
            "tcp": {
                "no_delay": True,
                "keep_alive": True,
                "reuse_port": False,
                "fast_open": False,
            }
        }
        return config

    def _generate_password(self, length: int = 16) -> str:
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

    def generate_singbox_config(self) -> Dict:
        """Generate Sing-box configuration"""
        outbounds = []

        for server in self.servers:
            # Add Shadowsocks outbound
            ss_config = self.generate_shadowsocks_config(server)
            outbounds.append({
                "type": "shadowsocks",
                "tag": f"ss-{server['country']}-{server['city']}",
                "server": server["host"],
                "server_port": server["ports"]["shadowsocks"],
                "method": ss_config["method"],
                "password": ss_config["password"]
            })

            # Add VMess outbound
            vmess_config = self.generate_vmess_config(server)
            outbounds.append({
                "type": "vmess",
                "tag": f"vmess-{server['country']}-{server['city']}",
                "server": server["host"],
                "server_port": server["ports"]["vmess"],
                "uuid": vmess_config["id"],
                "security": "auto",
                "transport": {
                    "type": "ws",
                    "path": vmess_config["path"],
                    "headers": {
                        "Host": vmess_config["host"]
                    }
                },
                "tls": {
                    "enabled": True,
                    "server_name": vmess_config["sni"]
                }
            })

        config = {
            "log": {
                "level": "info"
            },
            "inbounds": [
                {
                    "type": "mixed",
                    "listen": "127.0.0.1",
                    "listen_port": 7890
                }
            ],
            "outbounds": [
                {
                    "type": "selector",
                    "tag": "proxy",
                    "outbounds": [outbound["tag"] for outbound in outbounds]
                },
                {
                    "type": "direct",
                    "tag": "direct"
                }
            ] + outbounds,
            "route": {
                "rules": [
                    {
                        "geosite": "private",
                        "outbound": "direct"
                    }
                ]
            }
        }
        return config

    def export_shadowsocks_subscription(self) -> str:
        """Export Shadowsocks subscription in base64 format"""
        configs = []
        for server in self.servers:
            ss_config = self.generate_shadowsocks_config(server)
            # Format: method:password@server:port
            auth_string = f"{ss_config['method']}:{ss_config['password']}"
            auth_b64 = base64.b64encode(auth_string.encode()).decode()
            ss_url = (f"ss://{auth_b64}@{server['host']}:"
                      f"{server['ports']['shadowsocks']}#"
                      f"{quote(ss_config['remarks'])}")
            configs.append(ss_url)

        return '\n'.join(configs)

    def export_vmess_subscription(self) -> str:
        """Export VMess subscription in base64 format"""
        configs = []
        for server in self.servers:
            vmess_config = self.generate_vmess_config(server)
            vmess_json = json.dumps(vmess_config, separators=(',', ':'))
            vmess_b64 = base64.b64encode(vmess_json.encode()).decode()
            vmess_url = f"vmess://{vmess_b64}"
            configs.append(vmess_url)

        return '\n'.join(configs)

    def export_trojan_subscription(self) -> str:
        """Export Trojan subscription in base64 format"""
        configs = []
        for server in self.servers:
            trojan_config = self.generate_trojan_config(server)
            trojan_name = f"Trojan-{server['country']}-{server['city']}"
            trojan_url = (f"trojan://{trojan_config['password']}@"
                          f"{server['host']}:{server['ports']['trojan']}?"
                          f"sni={server['host']}#{quote(trojan_name)}")
            configs.append(trojan_url)

        return '\n'.join(configs)

    def export_universal_subscription(self) -> str:
        """Export universal subscription containing all protocols"""
        all_configs = []

        # Add Shadowsocks configs
        ss_configs = self.export_shadowsocks_subscription().split('\n')
        all_configs.extend(ss_configs)

        # Add VMess configs
        vmess_configs = self.export_vmess_subscription().split('\n')
        all_configs.extend(vmess_configs)

        # Add Trojan configs
        trojan_configs = self.export_trojan_subscription().split('\n')
        all_configs.extend(trojan_configs)

        # Base64 encode the entire subscription
        subscription_content = '\n'.join(all_configs)
        return base64.b64encode(subscription_content.encode()).decode()

    def update_servers(self, new_servers: List[Dict]) -> None:
        """Update the server list with new servers"""
        self.servers = new_servers

    def generate_all_configs(self) -> None:
        """Generate all configuration files"""
        from pathlib import Path

        config_dir = Path(__file__).parent.parent / "configs"
        config_dir.mkdir(exist_ok=True)

        # Generate Sing-box config
        singbox_config = self.generate_singbox_config()
        with open(config_dir / "singbox.json", "w") as f:
            json.dump(singbox_config, f, indent=2)

        # Generate subscription files
        with open(config_dir / "shadowsocks.txt", "w") as f:
            f.write(self.export_shadowsocks_subscription())

        with open(config_dir / "v2ray.txt", "w") as f:
            f.write(self.export_vmess_subscription())

        with open(config_dir / "universal.txt", "w") as f:
            f.write(self.export_universal_subscription())


def main():
    """Main function for command-line usage"""
    generator = ProxyGenerator()
    generator.generate_all_configs()
    print("✅ All proxy configurations generated successfully!")


if __name__ == "__main__":
    main()
