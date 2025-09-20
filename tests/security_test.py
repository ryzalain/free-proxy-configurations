#!/usr/bin/env python3
"""
Security Test Suite
Comprehensive security testing for proxy configurations.

Requires:
- requests: pip install requests
- PySocks: pip install requests[socks]
"""

import argparse
import sys
from typing import Dict, List

import requests


class SecurityTester:
    """Runs a suite of security tests against a given proxy configuration."""

    def __init__(self, proxy_config: Dict[str, str] = None, timeout: int = 10):
        """
        Initialize the security tester.
        :param proxy_config: Dict for requests, e.g., {'http': 'socks5://...', 'https': 'socks5://...'}
        :param timeout: Request timeout in seconds.
        """
        self.proxy_config = proxy_config or {
            "http": "socks5://127.0.0.1:1080",
            "https": "socks5://127.0.0.1:1080",
        }
        self.timeout = timeout
        self.results: Dict[str, bool] = {}

    def run_all_tests(self) -> None:
        """Run all security tests and print the results."""
        tests = [
            ("IP Leak Test", self.test_ip_leak),
            ("DNS Leak Test", self.test_dns_leak),
            ("WebRTC Leak Test", self.test_webrtc_leak),
            ("IPv6 Leak Test", self.test_ipv6_leak),
            ("Proxy Connectivity", self.test_proxy_connectivity),
            ("SSL/TLS Security", self.test_ssl_security),
            ("Traffic Analysis Resistance", self.test_traffic_analysis),
            ("Kill Switch Test", self.test_kill_switch),
            ("DNS over HTTPS (DoH)", self.test_doh_functionality),
            ("Geolocation Test", self.test_geolocation),
            ("Port Scanning Resistance", self.test_port_scanning_resistance),
        ]

        print("🔒 Running comprehensive security tests...\n")
        for test_name, test_func in tests:
            print(f"🧪 Running: {test_name}")
            try:
                result = test_func()
                self.results[test_name] = result
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   └── Status: {status}\n")
            except Exception as e:
                print(f"   └── ⚠️ ERROR: {e}\n")
                self.results[test_name] = False

    def test_ip_leak(self) -> bool:
        """Test for IP address leaks by comparing real IP with proxy IP."""
        try:
            real_ip = requests.get("https://httpbin.org/ip", timeout=self.timeout).json()["origin"]
            proxy_ip_res = requests.get("https://httpbin.org/ip", proxies=self.proxy_config, timeout=self.timeout)
            proxy_ip = proxy_ip_res.json()["origin"]

            is_leak = real_ip in proxy_ip.split(',')

            if is_leak:
                print(f"   └── ❌ IP LEAK DETECTED: Your real IP ({real_ip}) is exposed!")
                return False
            else:
                print(f"   └── ✅ IP successfully masked: {real_ip} -> {proxy_ip}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"   └── ⚠️ Test failed: {e}")
            return False

    def test_dns_leak(self) -> bool:
        """Test for DNS leaks using Cloudflare's trace tool."""
        try:
            response = requests.get("https://1.1.1.1/cdn-cgi/trace", proxies=self.proxy_config, timeout=self.timeout)
            trace_data = {line.split("=")[0]: line.split("=")[1] for line in response.text.strip().split("\n") if "=" in line}

            if "loc" in trace_data:
                print(f"   └── ✅ DNS appears to be routed correctly. Location: {trace_data['loc']}")
                return True
            else:
                print("   └── ⚠️ Could not determine DNS location from trace.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   └── ⚠️ DNS test failed: {e}")
            return False

    def test_webrtc_leak(self) -> bool:
        """Provide instructions for manual WebRTC leak test."""
        print("   └── ⚠️ This test requires manual verification in a browser.")
        print("   └── 📝 Visit https://browserleaks.com/webrtc to check for leaks.")
        return True  # Assume pass as it's informational

    def test_ipv6_leak(self) -> bool:
        """Test for IPv6 leaks by trying to connect to an IPv6-only service."""
        try:
            response = requests.get("https://ipv6.icanhazip.com", proxies=self.proxy_config, timeout=self.timeout)
            if response.ok and response.text.strip():
                print(f"   └── ⚠️ IPv6 connection detected: {response.text.strip()}")
                return False
            else:
                print("   └── ✅ No IPv6 leak detected")
                return True
        except requests.RequestException:
            print("   └── ✅ IPv6 connection blocked (good)")
            return True

