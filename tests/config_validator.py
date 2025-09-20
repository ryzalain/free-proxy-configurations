#!/usr/bin/env python3
"""
Configuration Validator
Validates proxy configurations for security and correctness.
"""

import argparse
import base64
import json
import socket
import sys
import urllib.parse
import uuid
from base64 import binascii
from typing import Dict, List, Any


class ConfigValidator:
    """Validates various proxy configuration files and subscription formats."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_singbox_config(self, config_path: str) -> bool:
        """Validate a Sing-box JSON configuration file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self._validate_singbox_structure(config)
            self._validate_outbounds(config.get("outbounds", []))
            self._validate_routing(config.get("route", {}))
            self._validate_dns(config.get("dns", {}))

            return not self.errors

        except (IOError, json.JSONDecodeError) as e:
            self.errors.append(f"Failed to load or parse configuration: {e}")
            return False
        except Exception as e:
            self.errors.append(f"An unexpected error occurred: {e}")
            return False

    def _validate_singbox_structure(self, config: Dict[str, Any]) -> None:
        """Validate the basic structure of the Sing-box config."""
        required_fields = ["inbounds", "outbounds"]
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Missing required field: {field}")

        if "inbounds" in config:
            for i, inbound in enumerate(config["inbounds"]):
                if "type" not in inbound:
                    self.errors.append(f"Inbound {i}: missing 'type' field")
                if "listen_port" not in inbound:
                    self.errors.append(f"Inbound {i}: missing 'listen_port' field")

    def _validate_outbounds(self, outbounds: List[Dict[str, Any]]) -> None:
        """Validate the outbound configurations."""
        if not outbounds:
            self.errors.append("No outbounds configured")
            return
        for i, outbound in enumerate(outbounds):
            self._validate_outbound(i, outbound)

    def _validate_outbound(self, index: int, outbound: Dict[str, Any]) -> None:
        """Validate a single outbound configuration."""
        if "type" not in outbound:
            self.errors.append(f"Outbound {index}: missing 'type' field")
            return

        outbound_type = outbound["type"]
        validators = {
            "vmess": self._validate_vmess,
            "vless": self._validate_vless,
            "shadowsocks": self._validate_shadowsocks,
            "trojan": self._validate_trojan,
            "hysteria": self._validate_hysteria,
            "tuic": self._validate_tuic,
        }

        if outbound_type in validators:
            validators[outbound_type](index, outbound)
        elif outbound_type not in ["direct", "block", "dns"]:
            self.warnings.append(f"Outbound {index}: unknown type '{outbound_type}'")

    def _require_fields(self, protocol: str, index: int, config: Dict[str, Any], fields: List[str]):
        """Helper to check for required fields in a config."""
        for field in fields:
            if field not in config:
                self.errors.append(f"{protocol} outbound {index}: missing '{field}'")

    def _validate_vmess(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a VMess outbound configuration."""
        self._require_fields("VMess", index, config, ["server", "server_port", "uuid"])
        if "uuid" in config:
            try:
                uuid.UUID(config["uuid"])
            except (ValueError, TypeError):
                self.errors.append(f"VMess outbound {index}: invalid UUID format")
        if config.get("alter_id", 0) != 0:
            self.warnings.append(f"VMess outbound {index}: alter_id is deprecated and should be 0")

    def _validate_vless(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a VLESS outbound configuration."""
        self._require_fields("VLESS", index, config, ["server", "server_port", "uuid"])
        if "uuid" in config:
            try:
                uuid.UUID(config["uuid"])
            except (ValueError, TypeError):
                self.errors.append(f"VLESS outbound {index}: invalid UUID format")

    def _validate_shadowsocks(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a Shadowsocks outbound configuration."""
        self._require_fields("Shadowsocks", index, config, ["server", "server_port", "method", "password"])
        secure_methods = ["chacha20-ietf-poly1305", "aes-256-gcm", "aes-128-gcm"]
        if config.get("method") not in secure_methods:
            self.warnings.append(f"Shadowsocks outbound {index}: method '{config.get('method')}' is considered insecure. Use an AEAD cipher.")

    def _validate_trojan(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a Trojan outbound configuration."""
        self._require_fields("Trojan", index, config, ["server", "server_port", "password"])
        if not config.get("tls", {}).get("enabled"):
            self.errors.append(f"Trojan outbound {index}: TLS must be enabled.")

    def _validate_hysteria(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a Hysteria outbound configuration."""
        self._require_fields("Hysteria", index, config, ["server", "server_port", "up_mbps", "down_mbps"])

    def _validate_tuic(self, index: int, config: Dict[str, Any]) -> None:
        """Validate a TUIC outbound configuration."""
        self._require_fields("TUIC", index, config, ["server", "server_port", "uuid", "password"])

    def _validate_routing(self, route: Dict[str, Any]) -> None:
        """Validate routing configuration."""
        if not route.get("rules"):
            self.warnings.append("Routing configuration is missing 'rules'.")
        for i, rule in enumerate(route.get("rules", [])):
            if "outbound" not in rule:
                self.errors.append(f"Routing rule {i}: missing 'outbound' tag.")

    def _validate_dns(self, dns: Dict[str, Any]) -> None:
        """Validate DNS configuration."""
        if not dns.get("servers"):
            self.warnings.append("DNS configuration is missing 'servers'.")
        for server in dns.get("servers", []):
            address = server.get("address") if isinstance(server, dict) else server
            if not isinstance(address, str):
                self.errors.append(f"Invalid DNS server entry: {server}")
                continue
            if not (address.startswith("https://") or address.startswith("tls://") or address == "local"):
                self.warnings.append(f"DNS server '{address}' is not secure (DoH/DoT).")

    def validate_subscription_format(self, content: str) -> bool:
        """Validate the format of a proxy subscription file."""
        self.info.append("Validating subscription content...")
        try:
            decoded_content = base64.b64decode(content).decode("utf-8")
            urls = decoded_content.strip().splitlines()
            if not urls:
                self.errors.append("Subscription is empty after decoding.")
                return False
            
            valid_urls = sum(1 for url in urls if self._validate_proxy_url(url))
            self.info.append(f"Found {valid_urls} valid proxy URLs out of {len(urls)}.")
            if valid_urls == 0:
                self.errors.append("No valid proxy URLs found in subscription.")
            return valid_urls > 0
        except (binascii.Error, UnicodeDecodeError) as e:
            self.errors.append(f"Failed to decode Base64 subscription: {e}")
            return False

    def test_connectivity(self, config_path: str) -> bool:
        """Test connectivity for all outbounds in a config file."""
        self.info.append(f"Testing connectivity for outbounds in {config_path}...")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            outbounds = config.get("outbounds", [])
            if not outbounds:
                self.warnings.append("No outbounds to test connectivity for.")
                return True

            for outbound in outbounds:
                tag = outbound.get("tag", "N/A")
                server = outbound.get("server")
                port = outbound.get("server_port")

                if outbound.get("type") in ["direct", "block", "dns"] or not server or not port:
                    continue

                if self._test_tcp_connection(server, port):
                    self.info.append(f"✅ Connection successful to {tag} ({server}:{port})")
                else:
                    self.warnings.append(f"⚠️ Connection FAILED to {tag} ({server}:{port})")
            return True
        except (IOError, json.JSONDecodeError) as e:
            self.errors.append(f"Could not read config for connectivity test: {e}")
            return False

    def _validate_proxy_url(self, url: str) -> bool:
        """Validate a generic proxy URL format."""
        try:
            if url.startswith("vmess://"):
                config_json = base64.b64decode(url[8:]).decode("utf-8")
                config = json.loads(config_json)
                return all(k in config for k in ["add", "port", "id"])
            elif url.startswith(("ss://", "trojan://", "vless://")):
                parsed = urllib.parse.urlparse(url)
                return bool(parsed.hostname and parsed.port)
        except (json.JSONDecodeError, binascii.Error, UnicodeDecodeError, ValueError):
            return False
        return False

    def _test_tcp_connection(self, host: str, port: int, timeout: int = 3) -> bool:
        """Test a TCP connection to a host and port."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, socket.error, OSError):
            return False

    def generate_report(self) -> str:
        """Generate a human-readable validation report."""
        # ... (This method was already complete and is unchanged) ...
        report = []
        if self.errors:
            report.append("🚫 ERRORS:")
            report.extend(f"   • {error}" for error in self.errors)
            report.append("")
        if self.warnings:
            report.append("⚠️  WARNINGS:")
            report.extend(f"   • {warning}" for warning in self.warnings)
            report.append("")
        if self.info:
            report.append("ℹ️  INFO:")
            report.extend(f"   • {info}" for info in self.info)
            report.append("")

        if not self.errors and not self.warnings:
            report.append("✅ Configuration validation passed!")
        elif not self.errors:
            report.append("⚠️  Configuration has warnings but is otherwise valid.")
        else:
            report.append("❌ Configuration validation failed!")
        return "\n".join(report)


def main() -> int:
    """Main function to run the validator from the command line."""
    parser = argparse.ArgumentParser(description="Validate proxy configurations.")
    parser.add_argument("config", help="Path to the configuration file to validate.")
    parser.add_argument("--type", choices=["singbox", "subscription"], default="singbox", help="The type of configuration file.")
    parser.add_argument("--test-connectivity", action="store_true", help="Also test server connectivity.")
    args = parser.parse_args()

    validator = ConfigValidator()
    
    if args.type == "singbox":
        validator.validate_singbox_config(args.config)
        if args.test_connectivity:
            validator.test_connectivity(args.config)
    elif args.type == "subscription":
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                content = f.read()
            validator.validate_subscription_format(content)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1

    print(validator.generate_report())
    return 0 if not validator.errors else 1


if __name__ == "__main__":
    sys.exit(main())
