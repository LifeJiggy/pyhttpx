# Contributing to pyhttpx

Thank you for your interest in contributing to pyhttpx! We welcome contributions from the community and are grateful for any help you can provide.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.6 or higher
- Git
- A GitHub account
- Basic knowledge of Python and HTTP protocols

### Quick Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/pyhttpx.git
   cd pyhttpx
   ```
3. **Set up the development environment**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # if available
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Installing Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (if you plan to run tests)
pip install pytest black flake8 mypy

# Or install everything at once
pip install requests beautifulsoup4 mmh3 colorama pytest black flake8 mypy
```

### Setting Up Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

```bash
pip install pre-commit
pre-commit install
```

### Running the Tool Locally

```bash
# Basic test
python pyhttpx.py -u example.com -sc -title

# Test with verbose output
python pyhttpx.py -u example.com -v -sc -title -cl -rt
```

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Found a bug? Let us know!
- **✨ Feature Requests**: Have an idea for a new feature?
- **📖 Documentation**: Help improve our docs
- **🧪 Tests**: Write tests to ensure code quality
- **💻 Code**: Submit fixes, features, or improvements

### Finding Issues to Work On

1. Check our [GitHub Issues](https://github.com/LifeJiggy/pyhttpx/issues) page
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to indicate you're working on it

### Reporting Bugs

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to reproduce**: Step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, etc.
- **Logs/Screenshots**: If applicable

### Feature Requests

For feature requests, please:

- Check if the feature already exists or is planned
- Describe the use case and why it's needed
- Provide examples of how it would work
- Consider the impact on existing functionality

## 📝 Development Guidelines

### Code Style

We follow PEP 8 guidelines with some modifications:

- Use 4 spaces for indentation
- Line length: 88 characters (Black default)
- Use descriptive variable names
- Add docstrings to functions and classes
- Use type hints where possible

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format code
black pyhttpx.py

# Check formatting
black --check pyhttpx.py
```

### Linting

Use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 pyhttpx.py

# With specific rules
flake8 --max-line-length=88 --extend-ignore=E203,W503 pyhttpx.py
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for static type checking:

```bash
# Run type checker
mypy pyhttpx.py
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat: add support for custom HTTP methods
fix: resolve redirect handling issue
docs: update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest test_pyhttpx.py

# Run with coverage
pytest --cov=pyhttpx --cov-report=html

# Run tests in verbose mode
pytest -v
```

### Writing Tests

When adding new features, please include tests:

```python
import pytest
from pyhttpx import HTTPProber, ProbeResult

def test_new_feature():
    """Test description"""
    # Arrange
    args = create_test_args()
    prober = HTTPProber(args)

    # Act
    result = prober.probe_url("http://example.com")

    # Assert
    assert result.probe_status == True
    assert result.status_code == 200
```

### Test Coverage

Aim for high test coverage, especially for:
- Core probing functionality
- Error handling
- Edge cases
- Different output formats

## 📤 Submitting Changes

### Pull Request Process

1. **Ensure your code follows our guidelines**:
   - Code is formatted with Black
   - Passes linting checks
   - Includes tests if applicable
   - Updates documentation

2. **Update documentation** if needed:
   - README.md for user-facing changes
   - Code comments for internal changes

3. **Create a pull request**:
   - Use a descriptive title
   - Reference any related issues
   - Provide a clear description of changes
   - Include screenshots for UI changes

4. **Respond to feedback**:
   - Address review comments
   - Make requested changes
   - Keep the PR updated

### PR Template

Please use this template for pull requests:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

## 🌍 Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Documentation**: Check our wiki for detailed guides

### Communication

- Be respectful and constructive in all interactions
- Use clear, descriptive language
- Provide context for your questions
- Help others when you can

### Recognition

Contributors will be recognized in:
- GitHub's contributor insights
- Release notes for significant contributions
- Special mentions in documentation

## 📄 License

By contributing to pyhttpx, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Your contributions help make pyhttpx better for everyone. We appreciate your time and effort!

---

**Happy contributing! 🎉**