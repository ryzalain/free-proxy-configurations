#!/usr/bin/env python3
"""
Configuration Validator.

Validates proxy configurations for security and correctness.
"""

import argparse
import base64
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class ConfigValidator:
    """Validates various proxy configuration files."""

    def __init__(self):
        """Initializes the ConfigValidator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_subscription_format(self, content: str) -> bool:
        """Validate the format of a proxy subscription file."""
        self.info.append("Validating subscription content...")
        urls = []
        try:
            decoded_content = base64.b64decode(content).decode("utf-8")
            urls = decoded_content.strip().splitlines()
            self.info.append("Detected base64 encoded subscription.")
        except (ValueError, UnicodeDecodeError):
            urls = content.strip().splitlines()
            self.info.append("Detected plain text subscription.")

        if not urls:
            self.errors.append("Subscription is empty.")
            return False

        valid_urls = sum(1 for url in urls if self._validate_proxy_url(url))
        self.info.append(
            f"Found {valid_urls} valid proxy URLs out of {len(urls)}."
        )
        if valid_urls == 0:
            self.errors.append("No valid proxy URLs found in subscription.")
        return valid_urls > 0

    def _validate_proxy_url(self, url: str) -> bool:
        """Validate a single proxy URL."""
        return url.startswith(('ss://', 'vmess://', 'trojan://'))

    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"   • {error}")
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        if self.info:
            print("\nℹ️  INFO:")
            for info_msg in self.info:
                print(f"   • {info_msg}")

        if not self.errors:
            print("\n✅ Configuration validation passed!")
        else:
            print("\n❌ Configuration validation failed.")


def main() -> int:
    """Run the complete validation process."""
    parser = argparse.ArgumentParser(
        description="Validate proxy configurations."
    )
    parser.add_argument(
        "config", help="Path to the configuration file to validate."
    )
    parser.add_argument(
        "--type", choices=["singbox", "subscription"],
        default="singbox", help="The type of configuration file."
    )
    args = parser.parse_args()

    validator = ConfigValidator()
    try:
        with open(args.config, "r", encoding="utf-8") as f:
            content = f.read()

        if args.type == "subscription":
            validator.validate_subscription_format(content)
        else:
            print("Sing-box validation not implemented in this version.")

    except (IOError, json.JSONDecodeError) as e:
        validator.errors.append(f"Failed to load or parse config: {e}")

    validator.print_results()
    return 1 if validator.errors else 0


if __name__ == "__main__":
    sys.exit(main())

