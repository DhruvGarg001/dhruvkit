# Contributing to DhruvKit

Thank you for your interest in contributing to DhruvKit! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Adding New Templates](#adding-new-templates)
- [Adding New Add-ons](#adding-new-add-ons)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
- Check existing [issues](https://github.com/dhruvgarg001/dhruvkit/issues) to avoid duplicates
- Use the latest version of DhruvKit
- Test with a clean environment

When reporting a bug, include:
- Your operating system and Python version
- Steps to reproduce the issue
- Expected vs. actual behavior
- Any error messages or logs

### Suggesting Enhancements

We welcome feature requests! Please:
- Check if the feature has already been suggested
- Provide a clear description of the feature
- Explain why it would be useful
- Include examples of how it would work

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to your branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhruvgarg001/dhruvkit.git
   cd dhruvkit
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

4. **Install optional dependencies for testing**
   ```bash
   pip install -e .[fastapi,flask,mongodb,firebase]
   ```

## Pull Request Process

1. **Update documentation** - Ensure README.md and other docs reflect your changes
2. **Update CHANGELOG.md** - Add your changes under the "Unreleased" section
3. **Test thoroughly** - Test your changes with different templates and configurations
4. **Keep commits clean** - Use clear, descriptive commit messages
5. **One feature per PR** - Keep pull requests focused on a single feature or fix

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] Documentation has been updated
- [ ] CHANGELOG.md has been updated
- [ ] All commands work as expected (`dk new`, `dk init`, `dk add`, `dk docs`)
- [ ] No breaking changes (or clearly documented if necessary)

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write descriptive variable and function names
- Add docstrings to functions and classes

### File Organization

```
src/dhruvkit/
├── __init__.py           # Package initialization
├── cli.py                # Main CLI entry point
├── utils.py              # Utility functions
├── licenses.py           # License handling
├── commands/             # Command implementations
│   ├── __init__.py
│   ├── new.py
│   ├── init.py
│   ├── add.py
│   └── docs.py
├── templates/            # Template definitions
│   ├── __init__.py
│   ├── basic.py
│   ├── fastapi.py
│   └── flask.py
└── license_templates/    # License text files
    └── *.md
```

### Code Comments

- Use comments to explain complex logic
- Keep comments up-to-date with code changes
- Avoid obvious comments

## Adding New Templates

To add a new template:

1. **Create a new template file** in `src/dhruvkit/templates/`
   ```python
   # mytemplate.py
   MYTEMPLATE_TEMPLATE = {
       "name": "My Template",
       "description": "Description of the template",
       "files": {
           # Define your file structure
       }
   }
   ```

2. **Register the template** in `src/dhruvkit/templates/__init__.py`
   ```python
   from .mytemplate import MYTEMPLATE_TEMPLATE
   
   TEMPLATES = {
       "mytemplate": MYTEMPLATE_TEMPLATE,
       # ... other templates
   }
   ```

3. **Add tests** - Verify the template generates correctly
4. **Update documentation** - Add to README.md and docs command
5. **Add to optional dependencies** if needed in `pyproject.toml`

## Adding New Add-ons

To add a new add-on for a template:

1. **Define the add-on** in the template file
   ```python
   TEMPLATE_ADDONS = {
       "mytemplate": {
           "myaddon": {
               "description": "Description of the add-on",
               "files": {
                   # Additional files
               },
               "dependencies": ["package1", "package2"]
           }
       }
   }
   ```

2. **Ensure proper merging logic** - Test with other add-ons
3. **Update documentation** - Document the add-on usage
4. **Add examples** in the docs command

## Questions?

If you have questions, feel free to:
- Open an [issue](https://github.com/dhruvgarg001/dhruvkit/issues)
- Reach out to [Dhruv Garg](https://www.linkedin.com/in/dhruvgarg001/)

Thank you for contributing to DhruvKit! 🚀
