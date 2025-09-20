#!/usr/bin/env python3
"""
Automatic Proxy Configuration Updater
Fetches and validates proxy servers from multiple sources.
"""

import logging
from pathlib import Path
from typing import Dict, List

import requests
from proxy_generator import ProxyGenerator


class ProxyUpdater:
    """Fetches, deduplicates, and manages proxy server lists from various sources."""

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
        # In a real-world application, this might be loaded from a YAML or JSON file.
        return [
            {
                "name": "ProxyScrape API",
                "url": "https://api.proxyscrape.com/v2/",
                "params": {"request": "displayproxies"},
                "type": "api",
            },
            {
                "name": "GitHub Free Proxies",
                "url": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                "type": "raw",
            },
            {
                "name": "Telegram Channels",
                "channels": ["@example_proxy_channel"],
                "type": "telegram",
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
                    self.logger.warning(f"No fetcher found for type: {source['type']}")
                    continue

                servers = fetcher(source)
                all_servers.extend(servers)
                if servers:
                    self.logger.info(
                        f"Fetched {len(servers)} servers from {source['name']}"
                    )

            except Exception as e:
                self.logger.error(f"Failed to fetch from {source['name']}: {e}")

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

    def _fetch_from_telegram(self, source: Dict) -> List[Dict]:
        """Fetch servers from Telegram channels (placeholder)."""
        self.logger.warning(
            "Telegram fetching is not implemented. "
            "This requires a library like Telethon and API credentials."
        )
        # In a real implementation, you would use a Telegram client library here.
        # For example:
        # from telethon.sync import TelegramClient
        # client = TelegramClient('session_name', api_id, api_hash)
        # ... fetch messages from source['channels'] ...
        return []

    def _parse_proxy_list(self, text_content: str, source_name: str) -> List[Dict]:
        """Parse a block of text containing host:port entries."""
        servers = []
        for line in text_content.strip().splitlines():
            line = line.strip()
            if ":" in line:
                try:
                    host, port_str = line.split(":", 1)
                    port = int(port_str.split()[0]) # Handle potential extra text
                    servers.append(
                        {
                            "host": host,
                            "port": port,
                            "source": source_name,
                        }
                    )
                except ValueError:
                    self.logger.warning(f"Skipping malformed line from {source_name}: {line}")
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

        # Here you would use the generator to process the server list
        # For example:
        # self.generator.update_servers(servers)
        # self.generator.generate_all_configs()
        self.logger.info("Proxy update process finished.")


if __name__ == "__main__":
    updater = ProxyUpdater()
    updater.run()
