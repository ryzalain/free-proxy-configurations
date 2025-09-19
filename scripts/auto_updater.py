#!/usr/bin/env python3
"""
Automatic Proxy Configuration Updater
Fetches and validates proxy servers from multiple sources
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List

import requests
import schedule
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
                "url": (
                    "https://raw.githubusercontent.com/clarketm/proxy-list/"
                    "master/proxy-list-raw.txt"
                ),
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
        # Add code here for raw parsing
        return servers

    def _fetch_from_telegram(self, source: Dict) -> List[Dict]:
        """Fetch servers from Telegram channels"""
        servers = []
        # Add code here for Telegram parsing
        return servers

    def _deduplicate_servers(self, servers: List[Dict]) -> List[Dict]:
        seen = set()
        result = []
        for s in servers:
            key = f"{s.get('host')}:{s.get('port')}"
            if key not in seen:
                seen.add(key)
                result.append(s)
        return result
