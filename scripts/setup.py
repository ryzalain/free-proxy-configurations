"""
Setup Script for Free Proxy Configurations
Automates the initial setup and configuration of the project.
"""

import json
import platform
import subprocess
import sys
from pathlib import Path


class ProxySetup:
    """Handles the automated setup process for the project."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "configs"
        self.logs_dir = self.project_root / "logs"
        self.scripts_dir = self.project_root / "scripts"

    def check_dependencies(self) -> bool:
        """Check for and install required Python packages."""
        print("🔍 Checking dependencies...")
        required = [
            "requests", "pyyaml", "jsonschema", "cryptography",
            "schedule", "python-dotenv", "jinja2", "click", "rich",
        ]
        missing = [pkg for pkg in required if not self._is_installed(pkg)]

        if not missing:
            print("✅ All dependencies are already installed.")
            return True

        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", *missing]
            )
            print("✅ Dependencies installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. "
                  "Please install them manually.")
            return False

    def _is_installed(self, package_name: str) -> bool:
        """Check if a package is installed."""
        try:
            __import__(package_name.replace("-", "_"))
            return True
        except ImportError:
            return False

    def create_directories(self) -> None:
        """Create necessary project directories."""
        print("📁 Creating directories...")
        dirs_to_create = [
            self.config_dir,
            self.logs_dir,
            self.project_root / "templates",
            self.project_root / "backups",
        ]
        for directory in dirs_to_create:
            directory.mkdir(exist_ok=True)
            print(f"   ✅ Created or already exists: "
                  f"{directory.relative_to(self.project_root)}")

    def generate_initial_configs(self) -> None:
        """Generate initial configuration files using the proxy_generator."""
        print("⚙️  Generating initial configurations...")
        # Temporarily add scripts directory to the path for local import
        sys.path.insert(0, str(self.scripts_dir))
        try:
            from proxy_generator import ProxyGenerator
            generator = ProxyGenerator()

            # A map of filenames to their generator functions for cleaner code
            configs_to_generate = {
                "singbox.json": generator.generate_singbox_config,
                "universal.txt": generator.export_universal_subscription,
                "shadowsocks.txt": generator.export_shadowsocks_subscription,
                "v2ray.txt": generator.export_vmess_subscription,
            }

            for filename, func in configs_to_generate.items():
                content = func()
                out_path = self.config_dir / filename
                with out_path.open("w", encoding="utf-8") as f:
                    if isinstance(content, dict):
                        json.dump(content, f, indent=2)
                    else:
                        f.write(content)
                print(f"   ✅ Generated {filename}")

        except ImportError:
            print(f"   ❌ Error: Could not import ProxyGenerator from "
                  f"{self.scripts_dir}.")
        except Exception as e:
            print(f"   ❌ Failed to generate configurations: {e}")
        finally:
            # Clean up the path modification
            if str(self.scripts_dir) in sys.path:
                sys.path.remove(str(self.scripts_dir))

    def create_systemd_service(self) -> None:
        """Generate a systemd service file for the auto-updater."""
        print("🔧 Creating systemd service file...")
        if platform.system() != "Linux":
            print("   ⚠️  Skipping: Systemd is only available on Linux.")
            return

        updater_script_path = self.scripts_dir / "auto_updater.py"
        service_content = f"""[Unit]
Description=Free Proxy Configurations Auto-Updater
After=network.target

[Service]
ExecStart={sys.executable} {updater_script_path}
WorkingDirectory={self.project_root}
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
        service_file = self.project_root / "proxy-updater.service"
        service_file.write_text(service_content, encoding="utf-8")

        print("   ✅ Service file 'proxy-updater.service' "
              "created in project root.")
        print("   💡 To install, run with sudo:")
        print(f"      sudo cp {service_file} /etc/systemd/system/")
        print("      sudo systemctl enable --now proxy-updater.service")


def main():
    """Run the complete setup process."""
    setup = ProxySetup()
    if setup.check_dependencies():
        setup.create_directories()
        setup.generate_initial_configs()
        setup.create_systemd_service()
        print("\n🎉 Setup complete!")


if __name__ == "__main__":
    main()
