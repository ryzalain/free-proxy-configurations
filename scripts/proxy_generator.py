#!/usr/bin/env python3
"""
Proxy Configuration Generator
Generates secure proxy configurations for various protocols
"""

import random
import string
import uuid
from typing import Dict, List


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
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
