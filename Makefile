# Free Proxy Configurations Makefile

.PHONY: help install setup test lint security clean update validate docs

# Default target
help:
	@echo "🚀 Free Proxy Configurations - Available Commands:"
	@echo ""
	@echo "📦 Setup and Installation:"
	@echo "  install     - Install Python dependencies"
	@echo "  setup       - Run initial setup script"
	@echo "  clean       - Clean generated files and caches"
	@echo ""
	@echo "⚙️  Configuration Management:"
	@echo "  generate    - Generate proxy configurations"
	@echo "  update      - Update proxy configurations"
	@echo "  validate    - Validate all configurations"
	@echo ""
	@echo "🧪 Testing and Quality:"
	@echo "  test        - Run all tests"
	@echo "  test-unit   - Run unit tests only"
	@echo "  test-security - Run security tests"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black and isort"
	@echo "  security    - Run security scans"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs        - Generate documentation"
	@echo "  docs-serve  - Serve documentation locally"
	@echo ""
	@echo "🔧 Development:"
	@echo "  dev-install - Install development dependencies"
	@echo "  pre-commit  - Install pre-commit hooks"
	@echo "  check       - Run all checks (lint, test, security)"

# Installation and Setup
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

dev-install: install
	@echo "🔧 Installing development dependencies..."
	pip install -r requirements-dev.txt || pip install pytest pytest-cov flake8 black isort mypy bandit safety pre-commit

setup: install
	@echo "⚙️  Running initial setup..."
	python scripts/setup.py --skip-service --skip-cron

pre-commit: dev-install
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install

# Configuration Management
generate:
	@echo "⚙️  Generating proxy configurations..."
	python scripts/proxy_generator.py

update:
	@echo "🔄 Updating proxy configurations..."
	python scripts/auto_updater.py --once

validate:
	@echo "✅ Validating configurations..."
	@if [ -f configs/singbox.json ]; then \
		python tests/config_validator.py configs/singbox.json --type singbox; \
	else \
		echo "⚠️  No Sing-box config found, generating..."; \
		make generate; \
		python tests/config_validator.py configs/singbox.json --type singbox; \
	fi
	@if [ -f configs/universal.txt ]; then \
		python tests/config_validator.py configs/universal.txt --type subscription; \
	fi

# Testing
test: dev-install
	@echo "🧪 Running all tests..."
	pytest tests/ -v --cov=scripts --cov-report=term-missing

test-unit: dev-install
	@echo "🧪 Running unit tests..."
	pytest tests/ -v -k "not integration"

test-security:
	@echo "🔒 Running security tests..."
	python tests/security_test.py

test-integration: generate
	@echo "🔗 Running integration tests..."
	python tests/config_validator.py configs/singbox.json --type singbox --test-connectivity

# Code Quality
lint: dev-install
	@echo "🔍 Running linting..."
	flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	mypy scripts/ --ignore-missing-imports

format: dev-install
	@echo "🎨 Formatting code..."
	black scripts/ tests/
	isort scripts/ tests/

security: dev-install
	@echo "🔒 Running security scans..."
	bandit -r scripts/ -ll
	safety check

check: lint test security
	@echo "✅ All checks completed!"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation is already available in the docs/ directory"
	@echo "Available documents:"
	@ls -la docs/

docs-serve:
	@echo "🌐 Serving documentation locally..."
	@if command -v python3 -m http.server >/dev/null 2>&1; then \
		echo "📖 Documentation available at http://localhost:8000"; \
		python3 -m http.server 8000; \
	else \
		echo "❌ Python HTTP server not available"; \
	fi

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f bandit-report.json safety-report.json
	@echo "✅ Cleanup completed!"

# Development Workflows
dev-setup: dev-install pre-commit setup
	@echo "🚀 Development environment ready!"

ci-test: install test lint security validate
	@echo "🤖 CI tests completed!"

release-check: clean format lint test security validate
	@echo "🚀 Release checks completed!"

# Docker targets
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t free-proxy-configs .

docker-run: docker-build
	@echo "🐳 Running Docker container..."
	docker run -p 8080:8080 free-proxy-configs

# Monitoring and Status
status:
	@echo "📊 System Status:"
	@echo "=================="
	@if [ -f configs/status.json ]; then \
		echo "📄 Configuration Status:"; \
		cat configs/status.json | python -m json.tool; \
	else \
		echo "⚠️  No status file found"; \
	fi
	@echo ""
	@echo "📁 Available Configurations:"
	@ls -la configs/ 2>/dev/null || echo "⚠️  No configs directory found"

health-check:
	@echo "🏥 Health Check:"
	@echo "================"
	@echo "🐍 Python version: $(shell python --version)"
	@echo "📦 Dependencies:"
	@pip list | grep -E "(requests|pyyaml|jsonschema)" || echo "⚠️  Some dependencies missing"
	@echo "📁 Directory structure:"
	@ls -la | grep -E "(scripts|tests|configs|docs)" || echo "⚠️  Some directories missing"
	@echo "⚙️  Configuration validation:"
	@make validate 2>/dev/null || echo "⚠️  Configuration validation failed"

# Backup and Restore
backup:
	@echo "💾 Creating backup..."
	@mkdir -p backups
	@tar -czf backups/backup-$(shell date +%Y%m%d-%H%M%S).tar.gz configs/ logs/ .env 2>/dev/null || true
	@echo "✅ Backup created in backups/ directory"

restore:
	@echo "📥 Available backups:"
	@ls -la backups/ 2>/dev/null || echo "⚠️  No backups found"
	@echo "To restore, extract a backup file to the project directory"

# Update project
update-project:
	@echo "🔄 Updating project from repository..."
	git pull origin main
	make install
	make generate
	@echo "✅ Project updated!"

# Performance testing
benchmark:
	@echo "⚡ Running performance benchmarks..."
	@echo "Testing configuration generation speed..."
	@time python scripts/proxy_generator.py
	@echo "Testing validation speed..."
	@time make validate

# Help for specific commands
help-setup:
	@echo "📦 Setup Command Help:"
	@echo "======================"
	@echo "The setup command will:"
	@echo "  1. Install Python dependencies"
	@echo "  2. Create necessary directories"
	@echo "  3. Generate initial configurations"
	@echo "  4. Create configuration templates"
	@echo "  5. Set up environment files"
	@echo ""
	@echo "Usage: make setup"

help-test:
	@echo "🧪 Testing Command Help:"
	@echo "========================"
	@echo "Available test commands:"
	@echo "  test         - Run all tests with coverage"
	@echo "  test-unit    - Run only unit tests"
	@echo "  test-security - Run security-specific tests"
	@echo "  test-integration - Run integration tests"
	@echo ""
	@echo "Usage: make test"

help-dev:
	@echo "🔧 Development Help:"
	@echo "==================="
	@echo "Development workflow:"
	@echo "  1. make dev-setup    - Set up development environment"
	@echo "  2. make format       - Format code before committing"
	@echo "  3. make check        - Run all quality checks"
	@echo "  4. make test         - Run tests"
	@echo "  5. git commit        - Commit changes"
	@echo ""
	@echo "Pre-commit hooks will automatically run formatting and basic checks."