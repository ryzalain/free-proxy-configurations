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
from typing import Any, Dict, List
from urllib.parse import quote

import yaml


class ProxyGenerator:
    def __init__(self):
        self.servers = self._load_server_list()

    def _load_server_list(self) -> List[Dict]:
        """Load server list from various sources"""
        # This would typically load from external sources
        # For demo purposes, using sample servers
        return [
            {
                "host": "us1.example.com",
                "country": "US",
                "city": "New York",
                "ports": {"shadowsocks": 8388, "trojan": 443, "vmess": 10086},
            },
            {
                "host": "uk1.example.com",
                "country": "GB",
                "city": "London",
                "ports": {"shadowsocks": 8388, "trojan": 443, "vmess": 10086},
            },
            {
                "host": "jp1.example.com",
                "country": "JP",
                "city": "Tokyo",
                "ports": {"shadowsocks": 8388, "trojan": 443, "vmess": 10086},
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
            "plugin_opts": "server;tls;host=" + server["host"],
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
                "fast_open_qlen": 20,
            },
            "remarks": f"Trojan-{server['country']}-{server['city']}",
        }
        return config

    def generate_hysteria_config(self, server: Dict) -> Dict:
        """Generate Hysteria configuration"""
        config = {
            "server": f"{server['host']}:443",
            "protocol": "udp",
            "up_mbps": 100,
            "down_mbps": 100,
            "alpn": "h3",
            "obfs": self._generate_password(16),
            "insecure": False,
            "sni": server["host"],
            "fast_open": True,
            "lazy": False,
            "hop_interval": 30,
            "remarks": f"Hysteria-{server['country']}-{server['city']}",
        }
        return config

    def generate_tuic_config(self, server: Dict) -> Dict:
        """Generate TUIC configuration"""
        uuid_val = str(uuid.uuid4())
        password = self._generate_password(16)
        config = {
            "relay": {
                "server": f"{server['host']}:443",
                "uuid": uuid_val,
                "password": password,
                "ip": server["host"],
                "congestion_control": "bbr",
                "alpn": ["h3"],
                "disable_sni": False,
                "reduce_rtt": True,
                "request_timeout": 8000,
                "task_negotiation_timeout": 3000,
                "heartbeat_interval": 10000,
                "gc_interval": 3000,
                "gc_lifetime": 15000,
            },
            "local": {
                "server": "127.0.0.1:1080",
                "dual_stack": True,
                "max_packet_size": 1500,
            },
            "log_level": "warn",
            "remarks": f"TUIC-{server['country']}-{server['city']}",
        }
        return config

    def generate_reality_config(self, server: Dict) -> Dict:
        """Generate Reality configuration"""
        config = {
            "tag": f"Reality-{server['country']}-{server['city']}",
            "type": "vless",
            "server": server["host"],
            "server_port": 443,
            "uuid": str(uuid.uuid4()),
            "flow": "xtls-rprx-vision",
            "tls": {
                "enabled": True,
                "server_name": "www.microsoft.com",
                "utls": {"enabled": True, "fingerprint": "chrome"},
                "reality": {
                    "enabled": True,
                    "public_key": self._generate_reality_key(),
                    "short_id": self._generate_short_id(),
                },
            },
            "transport": {"type": "tcp", "tcp": {"header": {"type": "none"}}},
        }
        return config

    def generate_ssh_config(self, server: Dict) -> Dict:
        """Generate SSH tunnel configuration"""
        config = {
            "host": server["host"],
            "port": 22,
            "username": "tunnel",
            "password": self._generate_password(),
            "local_port": 1080,
            "remote_port": 1080,
            "compression": True,
            "keep_alive": 60,
            "remarks": f"SSH-{server['country']}-{server['city']}",
        }
        return config

    def generate_singbox_config(self) -> Dict:
        """Generate comprehensive Sing-box configuration"""
        outbounds = []

        for server in self.servers:
            # VMess outbound
            vmess_config = {
                "tag": f"vmess-{server['country'].lower()}",
                "type": "vmess",
                "server": server["host"],
                "server_port": server["ports"]["vmess"],
                "uuid": str(uuid.uuid4()),
                "security": "auto",
                "alter_id": 0,
                "global_padding": False,
                "authenticated_length": True,
                "transport": {
                    "type": "ws",
                    "path": "/vmess",
                    "headers": {"Host": server["host"]},
                },
                "tls": {
                    "enabled": True,
                    "server_name": server["host"],
                    "alpn": ["h2", "http/1.1"],
                },
            }
            outbounds.append(vmess_config)

            # Shadowsocks outbound
            ss_config = {
                "tag": f"ss-{server['country'].lower()}",
                "type": "shadowsocks",
                "server": server["host"],
                "server_port": server["ports"]["shadowsocks"],
                "method": "chacha20-ietf-poly1305",
                "password": self._generate_password(),
                "plugin": "v2ray-plugin",
                "plugin_opts": f"server;tls;host={server['host']}",
            }
            outbounds.append(ss_config)

        config = {
            "log": {"level": "info", "timestamp": True},
            "dns": {
                "servers": [
                    {
                        "tag": "cloudflare",
                        "address": "https://1.1.1.1/dns-query",
                        "detour": "direct",
                    },
                    {"tag": "local", "address": "local", "detour": "direct"},
                ],
                "rules": [{"geosite": "cn", "server": "local"}],
                "final": "cloudflare",
                "strategy": "ipv4_only",
            },
            "inbounds": [
                {
                    "type": "mixed",
                    "listen": "127.0.0.1",
                    "listen_port": 1080,
                    "sniff": True,
                    "sniff_override_destination": True,
                }
            ],
            "outbounds": outbounds
            + [{"tag": "direct", "type": "direct"}, {"tag": "block", "type": "block"}],
            "route": {
                "geoip": {
                    "download_url": "https://github.com/SagerNet/sing-geoip/releases/latest/download/geoip.db",
                    "download_detour": "direct",
                },
                "geosite": {
                    "download_url": "https://github.com/SagerNet/sing-geosite/releases/latest/download/geosite.db",
                    "download_detour": "direct",
                },
                "rules": [
                    {"protocol": "dns", "outbound": "dns-out"},
                    {"geosite": "cn", "geoip": "cn", "outbound": "direct"},
                ],
                "final": outbounds[0]["tag"] if outbounds else "direct",
                "auto_detect_interface": True,
            },
        }
        return config

    def _generate_password(self, length: int = 16) -> str:
        """Generate secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choice(chars) for _ in range(length))

    def _generate_reality_key(self) -> str:
        """Generate Reality public key"""
        return base64.b64encode(random.randbytes(32)).decode()

    def _generate_short_id(self) -> str:
        """Generate Reality short ID"""
        return "".join(random.choice("0123456789abcdef") for _ in range(8))

    def export_shadowsocks_subscription(self) -> str:
        """Export Shadowsocks subscription format"""
        configs = []
        for server in self.servers:
            config = self.generate_shadowsocks_config(server)
            # ss://method:password@server:port#remarks
            auth = f"{config['method']}:{config['password']}"
            auth_b64 = base64.b64encode(auth.encode()).decode()
            url = f"ss://{auth_b64}@{config['server']}:{config['server_port']}#{quote(config['remarks'])}"
            configs.append(url)

        return base64.b64encode("\n".join(configs).encode()).decode()

    def export_vmess_subscription(self) -> str:
        """Export VMess subscription format"""
        configs = []
        for server in self.servers:
            config = self.generate_vmess_config(server)
            config_json = json.dumps(config)
            config_b64 = base64.b64encode(config_json.encode()).decode()
            url = f"vmess://{config_b64}"
            configs.append(url)

        return base64.b64encode("\n".join(configs).encode()).decode()

    def export_universal_subscription(self) -> str:
        """Export universal subscription with all protocols"""
        all_configs = []

        for server in self.servers:
            # Add Shadowsocks
            ss_config = self.generate_shadowsocks_config(server)
            auth = f"{ss_config['method']}:{ss_config['password']}"
            auth_b64 = base64.b64encode(auth.encode()).decode()
            ss_url = f"ss://{auth_b64}@{ss_config['server']}:{ss_config['server_port']}#{quote(ss_config['remarks'])}"
            all_configs.append(ss_url)

            # Add VMess
            vmess_config = self.generate_vmess_config(server)
            vmess_json = json.dumps(vmess_config)
            vmess_b64 = base64.b64encode(vmess_json.encode()).decode()
            vmess_url = f"vmess://{vmess_b64}"
            all_configs.append(vmess_url)

            # Add Trojan
            trojan_config = self.generate_trojan_config(server)
            trojan_url = f"trojan://{trojan_config['password']}@{trojan_config['remote_addr']}:{trojan_config['remote_port']}?sni={trojan_config['ssl']['sni']}#{quote(trojan_config['remarks'])}"
            all_configs.append(trojan_url)

        return base64.b64encode("\n".join(all_configs).encode()).decode()


if __name__ == "__main__":
    generator = ProxyGenerator()

    # Generate sample configurations
    print("Generating proxy configurations...")

    # Generate Sing-box config
    singbox_config = generator.generate_singbox_config()
    with open("../configs/singbox.json", "w") as f:
        json.dump(singbox_config, f, indent=2)

    # Generate subscription links
    universal_sub = generator.export_universal_subscription()
    with open("../configs/universal.txt", "w") as f:
        f.write(universal_sub)

    ss_sub = generator.export_shadowsocks_subscription()
    with open("../configs/shadowsocks.txt", "w") as f:
        f.write(ss_sub)

    vmess_sub = generator.export_vmess_subscription()
    with open("../configs/v2ray.txt", "w") as f:
        f.write(vmess_sub)

    print("Configuration files generated successfully!")
