"""
Setup Script for Free Proxy Configurations
Automates the initial setup and configuration
"""

import argparse
import json
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
        