# 🤝 Contributing to Free Proxy Configurations

Thank you for your interest in contributing to this project! This guide will help you get started with contributing to our free proxy configurations repository.

## 🎯 Ways to Contribute

### 1. 🐛 Bug Reports
- Report configuration issues
- Document connectivity problems
- Identify security vulnerabilities
- Report documentation errors

### 2. 💡 Feature Requests
- Suggest new protocols
- Request client support
- Propose security improvements
- Recommend new features

### 3. 🔧 Code Contributions
- Fix bugs in scripts
- Add new protocol support
- Improve configuration generators
- Enhance security features

### 4. 📚 Documentation
- Improve tutorials
- Add client guides
- Translate documentation
- Create video tutorials

### 5. 🧪 Testing
- Test configurations
- Validate security
- Performance testing
- Cross-platform testing

## 🚀 Getting Started

### Prerequisites

**Required Software:**
```bash
# Python 3.8+
python3 --version

# Git
git --version

# Required Python packages
pip install -r requirements.txt
```

**Optional Tools:**
```bash
# For testing
pip install pytest pytest-cov

# For linting
pip install flake8 black isort

# For security testing
pip install bandit safety
```

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/free-proxies.git
   cd free-proxies
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 📝 Development Guidelines

### Code Style

**Python Code:**
```python
# Use Black for formatting
black scripts/ tests/

# Use isort for imports
isort scripts/ tests/

# Follow PEP 8
flake8 scripts/ tests/
```

**Configuration Files:**
```json
{
  "format": "Use 2-space indentation",
  "naming": "Use descriptive names",
  "comments": "Add comments for complex logic"
}
```

### Commit Messages

**Format:**
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(generator): add Hysteria protocol support"
git commit -m "fix(validator): handle invalid UUID format"
git commit -m "docs(tutorial): add iOS setup instructions"
```

### Branch Naming

**Convention:**
```
type/short-description
```

**Examples:**
```bash
git checkout -b feat/hysteria-support
git checkout -b fix/dns-leak-issue
git checkout -b docs/android-guide
```

## 🔒 Security Guidelines

### Security-First Approach

1. **Never commit sensitive data**
   - No real passwords or keys
   - Use placeholder values
   - Check with `git diff` before committing

2. **Validate all inputs**
   - Sanitize user inputs
   - Validate configuration formats
   - Check for injection attacks

3. **Use secure defaults**
   - Strong encryption methods
   - Secure TLS configurations
   - Safe DNS settings

### Security Review Process

**Before Submitting:**
```bash
# Run security checks
bandit -r scripts/
safety check

# Test configurations
python tests/security_test.py
python tests/config_validator.py config.json
```

## 🧪 Testing

### Running Tests

**Unit Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_generator.py
```

**Integration Tests:**
```bash
# Test configuration generation
python scripts/proxy_generator.py

# Test configuration validation
python tests/config_validator.py configs/singbox.json

# Test security
python tests/security_test.py
```

**Manual Testing:**
```bash
# Test proxy connectivity
curl -x socks5://127.0.0.1:1080 https://httpbin.org/ip

# Test DNS resolution
nslookup google.com 127.0.0.1

# Test speed
speedtest-cli --proxy socks5://127.0.0.1:1080
```

### Writing Tests

**Test Structure:**
```python
import pytest
from scripts.proxy_generator import ProxyGenerator

class TestProxyGenerator:
    def setup_method(self):
        self.generator = ProxyGenerator()
    
    def test_generate_vmess_config(self):
        server = {"host": "test.com", "country": "US", "city": "NYC"}
        config = self.generator.generate_vmess_config(server)
        
        assert "server" in config
        assert config["server"] == "test.com"
        assert "uuid" in config
    
    def test_invalid_server_data(self):
        with pytest.raises(ValueError):
            self.generator.generate_vmess_config({})
```

## 📋 Pull Request Process

### Before Creating PR

1. **Update your fork**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feat/your-feature
   ```

3. **Make changes and test**
   ```bash
   # Make your changes
   # Run tests
   pytest
   # Run security checks
   bandit -r scripts/
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Creating the PR

1. **Push to your fork**
   ```bash
   git push origin feat/your-feature
   ```

2. **Create PR on GitHub**
   - Use the PR template
   - Provide clear description
   - Link related issues
   - Add screenshots if applicable

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement
- [ ] Performance optimization

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data included

## Related Issues
Fixes #123
Related to #456

## Screenshots (if applicable)
[Add screenshots here]
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs
   - Security scans complete
   - Tests pass

2. **Code Review**
   - Maintainer reviews code
   - Feedback provided
   - Changes requested if needed

3. **Approval and Merge**
   - PR approved by maintainer
   - Merged into main branch
   - Branch deleted

## 🏷️ Adding New Protocols

### Protocol Implementation Checklist

1. **Research Protocol**
   - [ ] Understand protocol specifications
   - [ ] Identify security features
   - [ ] Check client compatibility

2. **Implement Generator**
   ```python
   def generate_new_protocol_config(self, server: Dict) -> Dict:
       """Generate configuration for new protocol"""
       config = {
           "type": "new_protocol",
           "server": server["host"],
           "server_port": server["ports"]["new_protocol"],
           # Add protocol-specific fields
       }
       return config
   ```

3. **Add Validation**
   ```python
   def _validate_new_protocol(self, index: int, config: Dict) -> None:
       """Validate new protocol configuration"""
       required_fields = ['server', 'server_port']
       
       for field in required_fields:
           if field not in config:
               self.errors.append(f"New protocol outbound {index}: missing '{field}'")
   ```

4. **Update Documentation**
   - Add protocol description
   - Include security notes
   - Provide client setup instructions

5. **Add Tests**
   ```python
   def test_generate_new_protocol_config(self):
       server = {"host": "test.com", "ports": {"new_protocol": 443}}
       config = self.generator.generate_new_protocol_config(server)
       
       assert config["type"] == "new_protocol"
       assert config["server"] == "test.com"
   ```

## 📚 Documentation Standards

### Writing Guidelines

1. **Clear and Concise**
   - Use simple language
   - Avoid jargon
   - Provide examples

2. **Structure**
   - Use headings and subheadings
   - Include table of contents
   - Add navigation links

3. **Code Examples**
   ```markdown
   # Always include language specification
   ```json
   {
     "example": "configuration"
   }
   ```

   ```bash
   # Include comments for complex commands
   curl -x socks5://127.0.0.1:1080 https://httpbin.org/ip
   ```

4. **Screenshots**
   - Use consistent styling
   - Highlight important areas
   - Keep file sizes reasonable

### Documentation Types

**Tutorials:**
- Step-by-step instructions
- Beginner-friendly
- Include troubleshooting

**Guides:**
- Topic-specific information
- More detailed than tutorials
- For experienced users

**Reference:**
- Technical specifications
- API documentation
- Configuration options

## 🌍 Internationalization

### Adding Translations

1. **Create language directory**
   ```
   docs/
   ├── en/          # English (default)
   ├── zh/          # Chinese
   ├── es/          # Spanish
   └── fr/          # French
   ```

2. **Translate key documents**
   - README.md
   - Beginner guide
   - Client setup guides

3. **Maintain consistency**
   - Use same structure
   - Keep technical terms consistent
   - Update all languages when content changes

## 🎖️ Recognition

### Contributors

All contributors are recognized in:
- README.md contributors section
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

### Contribution Types

- 🐛 Bug reports and fixes
- 💡 Feature suggestions and implementations
- 📚 Documentation improvements
- 🌍 Translations
- 🧪 Testing and validation
- 🔒 Security improvements

## 📞 Getting Help

### Communication Channels

1. **GitHub Discussions**
   - General questions
   - Feature discussions
   - Community support

2. **Issues**
   - Bug reports
   - Feature requests
   - Technical problems

3. **Discord/Telegram**
   - Real-time chat
   - Quick questions
   - Community interaction

### Mentorship

New contributors can request mentorship:
- Pair programming sessions
- Code review guidance
- Project orientation
- Best practices training

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

🎉 **Thank you for contributing!** Your efforts help make internet privacy accessible to everyone. Every contribution, no matter how small, makes a difference.