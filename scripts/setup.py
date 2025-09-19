#!/usr/bin/env python3
"""
Setup Script for Free Proxy Configurations
Automates the initial setup and configuration
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


class ProxySetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "configs"
        self.logs_dir = self.project_root / "logs"

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")

        required_packages = [
            "requests",
            "pyyaml",
            "jsonschema",
            "cryptography",
            "schedule",
            "python-dotenv",
            "jinja2",
            "click",
            "rich",
        ]

        missing_packages = []

        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"   ✅ {package}")
            except ImportError:
                print(f"   ❌ {package}")
                missing_packages.append(package)

        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install"] + missing_packages
                )
                print("✅ All dependencies installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies")
                return False
        else:
            print("✅ All dependencies are already installed")
            return True

    def create_directories(self) -> None:
        """Create necessary directories"""
        print("📁 Creating directories...")

        directories = [
            self.config_dir,
            self.logs_dir,
            self.project_root / "templates",
            self.project_root / "backups",
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"   ✅ {directory}")

    def generate_initial_configs(self) -> None:
        """Generate initial configuration files"""
        print("⚙️  Generating initial configurations...")

        try:
            # Import and run the proxy generator
            sys.path.append(str(self.project_root / "scripts"))
            from proxy_generator import ProxyGenerator

            generator = ProxyGenerator()

            # Generate Sing-box config
            singbox_config = generator.generate_singbox_config()
            with open(self.config_dir / "singbox.json", "w") as f:
                json.dump(singbox_config, f, indent=2)
            print("   ✅ Sing-box configuration")

            # Generate subscription links
            universal_sub = generator.export_universal_subscription()
            with open(self.config_dir / "universal.txt", "w") as f:
                f.write(universal_sub)
            print("   ✅ Universal subscription")

            ss_sub = generator.export_shadowsocks_subscription()
            with open(self.config_dir / "shadowsocks.txt", "w") as f:
                f.write(ss_sub)
            print("   ✅ Shadowsocks subscription")

            vmess_sub = generator.export_vmess_subscription()
            with open(self.config_dir / "v2ray.txt", "w") as f:
                f.write(vmess_sub)
            print("   ✅ V2ray subscription")

        except Exception as e:
            print(f"   ❌ Failed to generate configurations: {e}")

    def create_systemd_service(self) -> None:
        """Create systemd service file for auto-updater"""
        print("🔧 Creating systemd service...")

        service_content = f"""[Unit]
Description=Free Proxy Auto-Updater
After=network.target

[Service]
Type=simple
User=proxy
Group=proxy
WorkingDirectory={self.project_root}
ExecStart={sys.executable} {self.project_root}/scripts/auto_updater.py
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
"""

        service_file = Path("/etc/systemd/system/proxy-updater.service")

        try:
            with open(service_file, "w") as f:
                f.write(service_content)
            print("   ✅ Systemd service created")
            print("   💡 Run 'sudo systemctl enable proxy-updater' to enable")
        except PermissionError:
            print("   ⚠️  Need sudo permissions to create systemd service")
            print(f"   💡 Manually create {service_file} with the following content:")
            print(service_content)

    def setup_cron_job(self) -> None:
        """Setup cron job for auto-updates"""
        print("⏰ Setting up cron job...")

        cron_command = f"0 */6 * * * {sys.executable} {self.project_root}/scripts/auto_updater.py --once"

        try:
            # Add to crontab
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ""

            if cron_command not in current_cron:
                new_cron = current_cron + f"\n{cron_command}\n"
                subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
                print("   ✅ Cron job added (updates every 6 hours)")
            else:
                print("   ✅ Cron job already exists")

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  Could not setup cron job automatically")
            print(f"   💡 Manually add to crontab: {cron_command}")

    def create_config_templates(self) -> None:
        """Create configuration templates"""
        print("📄 Creating configuration templates...")

        templates = {
            "vmess_template.json": {
                "v": "2",
                "ps": "Template Server",
                "add": "server.example.com",
                "port": "443",
                "id": "uuid-placeholder",
                "aid": "0",
                "scy": "auto",
                "net": "ws",
                "type": "none",
                "host": "server.example.com",
                "path": "/vmess",
                "tls": "tls",
                "sni": "server.example.com",
                "alpn": "h2,http/1.1",
            },
            "shadowsocks_template.json": {
                "server": "server.example.com",
                "server_port": 8388,
                "password": "password-placeholder",
                "method": "chacha20-ietf-poly1305",
                "plugin": "v2ray-plugin",
                "plugin_opts": "server;tls;host=server.example.com",
                "remarks": "SS Template",
                "timeout": 300,
            },
            "trojan_template.json": {
                "password": "password-placeholder",
                "remote_addr": "server.example.com",
                "remote_port": 443,
                "ssl": {
                    "enabled": True,
                    "sni": "server.example.com",
                    "alpn": ["h2", "http/1.1"],
                },
                "remarks": "Trojan Template",
            },
        }

        templates_dir = self.project_root / "templates"

        for filename, template in templates.items():
            template_file = templates_dir / filename
            with open(template_file, "w") as f:
                json.dump(template, f, indent=2)
            print(f"   ✅ {filename}")

    def setup_environment_file(self) -> None:
        """Create environment configuration file"""
        print("🌍 Creating environment file...")

        env_content = """# Free Proxy Configurations Environment
# Copy this file to .env and customize as needed

# Update interval (hours)
UPDATE_INTERVAL=6

# Log level (debug, info, warning, error)
LOG_LEVEL=info

# Maximum number of servers per protocol
MAX_SERVERS_PER_PROTOCOL=10

# Enable/disable specific protocols
ENABLE_VMESS=true
ENABLE_SHADOWSOCKS=true
ENABLE_TROJAN=true
ENABLE_HYSTERIA=true
ENABLE_TUIC=true
ENABLE_REALITY=true

# DNS servers
PRIMARY_DNS=1.1.1.1
SECONDARY_DNS=8.8.8.8

# Proxy sources (comma-separated URLs)
PROXY_SOURCES=https://api.proxyscrape.com/v2/,https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt

# Telegram bot token (optional, for notifications)
TELEGRAM_BOT_TOKEN=

# Telegram chat ID (optional, for notifications)
TELEGRAM_CHAT_ID=

# GitHub token (optional, for automatic updates)
GITHUB_TOKEN=
"""

        env_file = self.project_root / ".env.example"
        with open(env_file, "w") as f:
            f.write(env_content)

        print("   ✅ .env.example created")
        print("   💡 Copy to .env and customize as needed")

    def run_initial_tests(self) -> None:
        """Run initial tests to verify setup"""
        print("🧪 Running initial tests...")

        try:
            # Test configuration validation
            sys.path.append(str(self.project_root / "tests"))
            from config_validator import ConfigValidator

            validator = ConfigValidator()
            config_file = self.config_dir / "singbox.json"

            if config_file.exists():
                if validator.validate_singbox_config(str(config_file)):
                    print("   ✅ Configuration validation passed")
                else:
                    print("   ⚠️  Configuration validation has warnings")
                    print(validator.generate_report())
            else:
                print("   ⚠️  No configuration file to validate")

        except Exception as e:
            print(f"   ⚠️  Test failed: {e}")

    def display_next_steps(self) -> None:
        """Display next steps for the user"""
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. 📝 Review and customize .env file")
        print("2. 🔧 Configure your proxy client with subscription URLs:")
        print(f"   • Universal: file://{self.config_dir}/universal.txt")
        print(f"   • Sing-box: file://{self.config_dir}/singbox.json")
        print("3. 🚀 Start the auto-updater:")
        print(f"   python {self.project_root}/scripts/auto_updater.py")
        print("4. 🧪 Test your configuration:")
        print(f"   python {self.project_root}/tests/security_test.py")
        print("5. 📚 Read the documentation in the docs/ folder")
        print("\n🔒 Remember to test your setup and ensure your privacy is protected!")


def main():
    parser = argparse.ArgumentParser(description="Setup Free Proxy Configurations")
    parser.add_argument(
        "--skip-deps", action="store_true", help="Skip dependency installation"
    )
    parser.add_argument(
        "--skip-service", action="store_true", help="Skip systemd service creation"
    )
    parser.add_argument("--skip-cron", action="store_true", help="Skip cron job setup")
    parser.add_argument("--skip-tests", action="store_true", help="Skip initial tests")

    args = parser.parse_args()

    setup = ProxySetup()

    print("🚀 Starting Free Proxy Configurations Setup")
    print("=" * 50)

    # Check and install dependencies
    if not args.skip_deps:
        if not setup.check_dependencies():
            print("❌ Setup failed due to dependency issues")
            return 1

    # Create directories
    setup.create_directories()

    # Generate initial configurations
    setup.generate_initial_configs()

    # Create templates
    setup.create_config_templates()

    # Setup environment file
    setup.setup_environment_file()

    # Setup systemd service (Linux only)
    if not args.skip_service and sys.platform.startswith("linux"):
        setup.create_systemd_service()

    # Setup cron job
    if not args.skip_cron:
        setup.setup_cron_job()

    # Run initial tests
    if not args.skip_tests:
        setup.run_initial_tests()

    # Display next steps
    setup.display_next_steps()

    return 0


if __name__ == "__main__":
    exit(main())
