#!/usr/bin/env python3
"""
Automatic Proxy Configuration Updater
Fetches and validates proxy servers from multiple sources.
"""

import base64
import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List
from urllib.parse import parse_qs, unquote, urlparse

import requests

# Add the scripts directory to the path for local imports
sys.path.insert(0, str(Path(__file__).parent))

from proxy_generator import ProxyGenerator  # noqa: E402


class ProxyUpdater:
    """Fetches, deduplicates, and manages proxy server lists from various
    sources."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.generator = ProxyGenerator()
        self.sources = self._load_sources()

    def _setup_logging(self) -> logging.Logger:
        """Set up the logging configuration."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "updater.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        return logging.getLogger(__name__)

    def _load_sources(self) -> List[Dict]:
        """Load the configuration for proxy sources."""
        return [
            {
                "name": "Free Shadowsocks Configs",
                "url": ("https://raw.githubusercontent.com/freefq/free/"
                        "master/v2"),
                "type": "subscription",
            },
            {
                "name": "Proxy Pool",
                "url": ("https://raw.githubusercontent.com/mahdibland/"
                        "V2RayAggregator/master/sub/sub_merge.txt"),
                "type": "subscription",
            },
            {
                "name": "Free V2ray Configs",
                "url": ("https://raw.githubusercontent.com/peasoft/"
                        "NoMoreWalls/master/list.txt"),
                "type": "subscription",
            },
            {
                "name": "Clash Configs",
                "url": ("https://raw.githubusercontent.com/Pawdroid/"
                        "Free-servers/main/sub"),
                "type": "subscription",
            },
        ]

    def fetch_all_servers(self) -> List[Dict]:
        """Fetch proxy servers from all configured sources."""
        all_servers = []
        self.logger.info("Starting proxy fetch from all sources...")

        for source in self.sources:
            try:
                fetcher = getattr(self, f"_fetch_from_{source['type']}", None)
                if not fetcher:
                    self.logger.warning(
                        f"No fetcher found for type: {source['type']}"
                    )
                    continue

                servers = fetcher(source)
                all_servers.extend(servers)
                if servers:
                    self.logger.info(
                        f"Fetched {len(servers)} servers from {source['name']}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Failed to fetch from {source['name']}: {e}"
                )

        unique_servers = self._deduplicate_servers(all_servers)
        self.logger.info(
            f"Total unique proxy servers fetched: {len(unique_servers)}"
        )
        return unique_servers

    def _fetch_from_api(self, source: Dict) -> List[Dict]:
        """Fetch servers from a standard API source."""
        response = requests.get(
            source["url"], params=source.get("params", {}), timeout=30
        )
        response.raise_for_status()
        return self._parse_proxy_list(response.text, source["name"])

    def _fetch_from_raw(self, source: Dict) -> List[Dict]:
        """Fetch servers from a raw text file source."""
        response = requests.get(source["url"], timeout=30)
        response.raise_for_status()
        return self._parse_proxy_list(response.text, source["name"])

    def _fetch_from_subscription(self, source: Dict) -> List[Dict]:
        """Fetch servers from subscription-based sources."""
        response = requests.get(source["url"], timeout=30)
        response.raise_for_status()

        # Try to decode base64 content
        try:
            decoded_content = base64.b64decode(response.text).decode('utf-8')
        except Exception:
            decoded_content = response.text

        servers = []
        lines = decoded_content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                if line.startswith('ss://'):
                    server = self._parse_shadowsocks_url(line)
                elif line.startswith('vmess://'):
                    server = self._parse_vmess_url(line)
                elif line.startswith('trojan://'):
                    server = self._parse_trojan_url(line)
                else:
                    continue

                if server:
                    server['source'] = source['name']
                    servers.append(server)

            except Exception as e:
                self.logger.debug(
                    f"Failed to parse line: {line[:50]}... Error: {e}"
                )
                continue

        return servers

    def _parse_shadowsocks_url(self, url: str) -> Dict:
        """Parse Shadowsocks URL format"""
        # Format: ss://base64(method:password)@server:port#name
        match = re.match(r'ss://([^@]+)@([^:]+):(\d+)(?:#(.+))?', url)
        if not match:
            return None

        auth_b64, host, port, name = match.groups()
        try:
            auth_decoded = base64.b64decode(auth_b64).decode('utf-8')
            method, password = auth_decoded.split(':', 1)

            return {
                'protocol': 'shadowsocks',
                'host': host,
                'port': int(port),
                'method': method,
                'password': password,
                'name': unquote(name) if name else f"SS-{host}",
            }
        except Exception:
            return None

    def _parse_vmess_url(self, url: str) -> Dict:
        """Parse VMess URL format"""
        # Format: vmess://base64(json_config)
        if not url.startswith('vmess://'):
            return None

        try:
            config_b64 = url[8:]  # Remove 'vmess://'
            config_json = base64.b64decode(config_b64).decode('utf-8')
            config = json.loads(config_json)

            return {
                'protocol': 'vmess',
                'host': config.get('add', ''),
                'port': int(config.get('port', 0)),
                'uuid': config.get('id', ''),
                'alterId': int(config.get('aid', 0)),
                'security': config.get('scy', 'auto'),
                'network': config.get('net', 'tcp'),
                'path': config.get('path', '/'),
                'host_header': config.get('host', ''),
                'tls': config.get('tls', '') == 'tls',
                'name': config.get('ps', f"VMess-{config.get('add', '')}"),
            }
        except Exception:
            return None

    def _parse_trojan_url(self, url: str) -> Dict:
        """Parse Trojan URL format"""
        # Format: trojan://password@server:port?params#name
        parsed = urlparse(url)
        if parsed.scheme != 'trojan':
            return None

        return {
            'protocol': 'trojan',
            'host': parsed.hostname,
            'port': parsed.port or 443,
            'password': parsed.username,
            'sni': parse_qs(parsed.query).get('sni', [parsed.hostname])[0],
            'name': (unquote(parsed.fragment) if parsed.fragment
                     else f"Trojan-{parsed.hostname}"),
        }

    def _fetch_from_telegram(self, source: Dict) -> List[Dict]:
        """Fetch servers from Telegram channels (placeholder)."""
        self.logger.warning(
            "Telegram fetching is not implemented. "
            "This requires a library like Telethon and API credentials."
        )
        return []

    def _parse_proxy_list(self, text_content: str,
                          source_name: str) -> List[Dict]:
        """Parse a block of text containing host:port entries."""
        servers = []
        for line in text_content.strip().splitlines():
            line = line.strip()
            if ":" in line:
                try:
                    host, port_str = line.split(":", 1)
                    # Handle potential extra text
                    port = int(port_str.split()[0])
                    servers.append(
                        {
                            "host": host,
                            "port": port,
                            "source": source_name,
                        }
                    )
                except ValueError:
                    self.logger.warning(
                        f"Skipping malformed line from {source_name}: {line}"
                    )
                    continue
        return servers

    def _deduplicate_servers(self, servers: List[Dict]) -> List[Dict]:
        """Remove duplicate servers based on host and port."""
        seen = set()
        unique_servers = []
        for server in servers:
            key = f"{server.get('host')}:{server.get('port')}"
            if key not in seen:
                seen.add(key)
                unique_servers.append(server)
        return unique_servers

    def run(self):
        """Run the full update process."""
        servers = self.fetch_all_servers()
        if not servers:
            self.logger.warning("No servers fetched. Exiting.")
            return

        # Convert fetched servers to the format expected by ProxyGenerator
        converted_servers = self._convert_servers_format(servers)

        # Update the generator with new servers and generate configs
        self.generator.update_servers(converted_servers)
        self.generator.generate_all_configs()

        self.logger.info(
            f"Proxy update process finished. "
            f"Generated configs for {len(converted_servers)} servers."
        )

    def _convert_servers_format(self, servers: List[Dict]) -> List[Dict]:
        """Convert fetched servers to ProxyGenerator format"""
        converted = []

        # Group servers by host to create the expected format
        host_groups = {}
        for server in servers:
            host = server.get('host', '')
            if not host:
                continue

            if host not in host_groups:
                host_groups[host] = {
                    'host': host,
                    'country': self._guess_country_from_host(host),
                    'city': self._guess_city_from_host(host),
                    'ports': {}
                }

            # Map protocol to port
            protocol = server.get('protocol', '')
            port = server.get('port', 0)

            if protocol == 'shadowsocks':
                host_groups[host]['ports']['shadowsocks'] = port
            elif protocol == 'vmess':
                host_groups[host]['ports']['vmess'] = port
            elif protocol == 'trojan':
                host_groups[host]['ports']['trojan'] = port

        # Convert to list and ensure all required ports exist
        for host_data in host_groups.values():
            # Ensure all protocols have ports (use defaults if missing)
            if 'shadowsocks' not in host_data['ports']:
                host_data['ports']['shadowsocks'] = 8388
            if 'vmess' not in host_data['ports']:
                host_data['ports']['vmess'] = 10086
            if 'trojan' not in host_data['ports']:
                host_data['ports']['trojan'] = 443

            converted.append(host_data)

        return converted[:10]  # Limit to 10 servers to avoid too many configs

    def _guess_country_from_host(self, host: str) -> str:
        """Guess country from hostname"""
        host_lower = host.lower()
        if 'us' in host_lower or 'america' in host_lower:
            return 'US'
        elif 'uk' in host_lower or 'britain' in host_lower:
            return 'GB'
        elif 'jp' in host_lower or 'japan' in host_lower:
            return 'JP'
        elif 'de' in host_lower or 'german' in host_lower:
            return 'DE'
        elif 'fr' in host_lower or 'france' in host_lower:
            return 'FR'
        elif 'sg' in host_lower or 'singapore' in host_lower:
            return 'SG'
        else:
            return 'XX'  # Unknown

    def _guess_city_from_host(self, host: str) -> str:
        """Guess city from hostname"""
        host_lower = host.lower()
        if 'newyork' in host_lower or 'ny' in host_lower:
            return 'New York'
        elif 'london' in host_lower:
            return 'London'
        elif 'tokyo' in host_lower:
            return 'Tokyo'
        elif 'singapore' in host_lower:
            return 'Singapore'
        elif 'paris' in host_lower:
            return 'Paris'
        else:
            return 'Unknown'


if __name__ == "__main__":
    updater = ProxyUpdater()
    updater.run()
