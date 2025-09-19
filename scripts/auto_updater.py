#!/usr/bin/env python3
"""
Automatic Proxy Configuration Updater
Fetches and validates proxy servers from multiple sources
"""

import base64
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List

import requests
import schedule
import yaml
from proxy_generator import ProxyGenerator


class ProxyUpdater:
    def __init__(self):
        self.logger = self._setup_logging()
        self.generator = ProxyGenerator()
        self.sources = self._load_sources()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("../logs/updater.log"),
                logging.StreamHandler(),
            ],
        )
        return logging.getLogger(__name__)

    def _load_sources(self) -> List[Dict]:
        """Load proxy sources configuration"""
        return [
            {
                "name": "Free Proxy List",
                "url": "https://api.proxyscrape.com/v2/",
                "params": {
                    "request": "get",
                    "protocol": "all",
                    "timeout": "10000",
                    "country": "all",
                    "ssl": "all",
                    "anonymity": "all",
                },
                "type": "api",
            },
            {
                "name": "GitHub Free Proxies",
                "url": "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "type": "raw",
            },
            {
                "name": "Telegram Channels",
                "channels": [
                    "@v2ray_config_pool",
                    "@shadowsocks_config",
                    "@trojan_configs",
                ],
                "type": "telegram",
            },
        ]

    def fetch_proxy_servers(self) -> List[Dict]:
        """Fetch proxy servers from all sources"""
        all_servers = []

        for source in self.sources:
            try:
                if source["type"] == "api":
                    servers = self._fetch_from_api(source)
                elif source["type"] == "raw":
                    servers = self._fetch_from_raw(source)
                elif source["type"] == "telegram":
                    servers = self._fetch_from_telegram(source)
                else:
                    continue

                all_servers.extend(servers)
                self.logger.info(
                    f"Fetched {len(servers)} servers from {source['name']}"
                )

            except Exception as e:
                self.logger.error(f"Error fetching from {source['name']}: {e}")

        return self._deduplicate_servers(all_servers)

    def _fetch_from_api(self, source: Dict) -> List[Dict]:
        """Fetch servers from API source"""
        response = requests.get(
            source["url"], params=source.get("params", {}), timeout=30
        )
        response.raise_for_status()

        servers = []
        for line in response.text.strip().split("\n"):
            if ":" in line:
                host, port = line.strip().split(":", 1)
                servers.append(
                    {
                        "host": host,
                        "port": int(port),
                        "country": "Unknown",
                        "city": "Unknown",
                        "source": source["name"],
                    }
                )

        return servers

    def _fetch_from_raw(self, source: Dict) -> List[Dict]:
        """Fetch servers from raw text source"""
        response = requests.get(source["url"], timeout=30)
        response.raise_for_status()

        servers = []
        for line in response.text.strip().split("\n"):
            if ":" in line and not line.startswith("#"):
                try:
                    host, port = line.strip().split(":", 1)
                    servers.append(
                        {
                            "host": host,
                            "port": int(port),
                            "country": "Unknown",
                            "city": "Unknown",
                            "source": source["name"],
                        }
                    )
                except ValueError:
                    continue

        return servers

    def _fetch_from_telegram(self, source: Dict) -> List[Dict]:
        """Fetch configurations from Telegram channels"""
        # This would require Telegram API integration
        # For now, return empty list as placeholder
        self.logger.info("Telegram integration not implemented yet")
        return []

    def _deduplicate_servers(self, servers: List[Dict]) -> List[Dict]:
        """Remove duplicate servers"""
        seen = set()
        unique_servers = []

        for server in servers:
            key = f"{server['host']}:{server['port']}"
            if key not in seen:
                seen.add(key)
                unique_servers.append(server)

        return unique_servers

    def validate_servers(self, servers: List[Dict]) -> List[Dict]:
        """Validate server connectivity"""
        valid_servers = []

        for server in servers:
            if self._test_server_connectivity(server):
                valid_servers.append(server)
                self.logger.info(f"Server {server['host']}:{server['port']} is valid")
            else:
                self.logger.warning(
                    f"Server {server['host']}:{server['port']} is not responding"
                )

        return valid_servers

    def _test_server_connectivity(self, server: Dict) -> bool:
        """Test if server is reachable"""
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((server["host"], server["port"]))
            sock.close()
            return result == 0
        except Exception:
            return False

    def generate_configurations(self, servers: List[Dict]) -> None:
        """Generate configuration files from validated servers"""
        # Update generator with new servers
        self.generator.servers = self._format_servers_for_generator(servers)

        # Generate all configuration formats
        try:
            # Sing-box configuration
            singbox_config = self.generator.generate_singbox_config()
            self._save_config(
                "../configs/singbox.json", json.dumps(singbox_config, indent=2)
            )

            # Subscription links
            universal_sub = self.generator.export_universal_subscription()
            self._save_config("../configs/universal.txt", universal_sub)

            ss_sub = self.generator.export_shadowsocks_subscription()
            self._save_config("../configs/shadowsocks.txt", ss_sub)

            vmess_sub = self.generator.export_vmess_subscription()
            self._save_config("../configs/v2ray.txt", vmess_sub)

            # Generate individual protocol configs
            self._generate_protocol_configs(servers)

            self.logger.info("All configuration files updated successfully")

        except Exception as e:
            self.logger.error(f"Error generating configurations: {e}")

    def _format_servers_for_generator(self, servers: List[Dict]) -> List[Dict]:
        """Format servers for the proxy generator"""
        formatted = []

        for server in servers[:10]:  # Limit to top 10 servers
            formatted.append(
                {
                    "host": server["host"],
                    "country": server.get("country", "US"),
                    "city": server.get("city", "Unknown"),
                    "ports": {"shadowsocks": 8388, "trojan": 443, "vmess": 10086},
                }
            )

        return formatted

    def _generate_protocol_configs(self, servers: List[Dict]) -> None:
        """Generate individual protocol configuration files"""
        protocols = ["shadowsocks", "trojan", "vmess", "hysteria", "tuic", "reality"]

        for protocol in protocols:
            configs = []
            for server in servers[:5]:  # Top 5 servers per protocol
                try:
                    if protocol == "shadowsocks":
                        config = self.generator.generate_shadowsocks_config(
                            self._format_servers_for_generator([server])[0]
                        )
                    elif protocol == "trojan":
                        config = self.generator.generate_trojan_config(
                            self._format_servers_for_generator([server])[0]
                        )
                    elif protocol == "vmess":
                        config = self.generator.generate_vmess_config(
                            self._format_servers_for_generator([server])[0]
                        )
                    elif protocol == "hysteria":
                        config = self.generator.generate_hysteria_config(
                            self._format_servers_for_generator([server])[0]
                        )
                    elif protocol == "tuic":
                        config = self.generator.generate_tuic_config(
                            self._format_servers_for_generator([server])[0]
                        )
                    elif protocol == "reality":
                        config = self.generator.generate_reality_config(
                            self._format_servers_for_generator([server])[0]
                        )

                    configs.append(config)

                except Exception as e:
                    self.logger.error(f"Error generating {protocol} config: {e}")

            if configs:
                filename = f"../configs/{protocol}.json"
                self._save_config(filename, json.dumps(configs, indent=2))

    def _save_config(self, filename: str, content: str) -> None:
        """Save configuration to file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(content)

    def update_status_file(self, server_count: int) -> None:
        """Update status file with latest information"""
        status = {
            "last_updated": datetime.now().isoformat(),
            "server_count": server_count,
            "status": "active",
            "next_update": (datetime.now().timestamp() + 6 * 3600),  # 6 hours
        }

        self._save_config("../configs/status.json", json.dumps(status, indent=2))

    def run_update_cycle(self) -> None:
        """Run complete update cycle"""
        self.logger.info("Starting proxy update cycle...")

        try:
            # Fetch servers
            servers = self.fetch_proxy_servers()
            self.logger.info(f"Fetched {len(servers)} total servers")

            # Validate servers
            valid_servers = self.validate_servers(servers)
            self.logger.info(f"Validated {len(valid_servers)} working servers")

            if valid_servers:
                # Generate configurations
                self.generate_configurations(valid_servers)

                # Update status
                self.update_status_file(len(valid_servers))

                self.logger.info("Update cycle completed successfully")
            else:
                self.logger.warning("No valid servers found")

        except Exception as e:
            self.logger.error(f"Update cycle failed: {e}")

    def start_scheduler(self) -> None:
        """Start the automatic update scheduler"""
        # Schedule updates every 6 hours
        schedule.every(6).hours.do(self.run_update_cycle)

        # Run initial update
        self.run_update_cycle()

        self.logger.info("Scheduler started - updates every 6 hours")

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


if __name__ == "__main__":
    updater = ProxyUpdater()

    # Create logs directory
    os.makedirs("../logs", exist_ok=True)

    # Run single update or start scheduler
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        updater.run_update_cycle()
    else:
        updater.start_scheduler()
