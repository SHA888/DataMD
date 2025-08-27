# Contributing to Data Markdown (DataMD)

Thank you for your interest in contributing to Data Markdown (DataMD)! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 🐛 Bug Reports
- Use the bug report template
- Include sample .dmd files that reproduce the issue
- Provide environment details (OS, Python version, etc.)

### 💡 Feature Requests
- Use the feature request template
- Describe real-world use cases
- Consider implementation complexity

### 📝 Documentation
- Improve README, SYNTAX.md, or examples
- Add use case tutorials
- Fix typos or unclear explanations

### 🔧 Code Contributions
- Add support for new file formats
- Improve error handling
- Optimize performance
- Add tests

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/SHA888/DataMD.git
   cd DataMD
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```

3. **Install Quarto** (optional)
   - Download from https://quarto.org

4. **Install Tesseract OCR**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-spa tesseract-ocr-fra

   # macOS
   brew install tesseract tesseract-lang

   # Windows - download from GitHub releases
   ```

## Testing Your Changes

### Test with Python-only (primary)
```bash
python python_implementation/process_dmd.py example.dmd
python python_implementation/process_dmd.py simple_example.dmd
```

### Test with Quarto (optional)
```bash
cp example.dmd example.qmd
cp simple_example.dmd simple_example.qmd
quarto render example.qmd
quarto render simple_example.qmd
```

### Run Tests
```bash
pytest tests/
```

## Adding New File Format Support

1. **Update the Lua filter** (`datamd.lua`)
   - Add new shortcode handling
   - Include error handling

2. **Update Python extension** (`python_implementation/datamd_ext.py`)
   - Add processing logic
   - Handle exceptions gracefully

3. **Add tests**
   - Create test files in `tests/data/`
   - Add test cases in `tests/test_formats.py`

4. **Update documentation**
   - Add syntax to `SYNTAX.md`
   - Include examples in README
   - Update requirements if needed

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Include error handling
- Keep functions focused and small

## Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issues when applicable
- Keep commits atomic (one logical change per commit)

Examples:
```
Add support for YAML file processing
Fix CSV parsing with custom separators
Update documentation for video embedding
Remove deprecated PDF extraction method
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the development setup
   - Test thoroughly
   - Update documentation

3. **Submit pull request**
   - Use the PR template
   - Link related issues
   - Describe changes clearly
   - Include test results

4. **Code review**
   - Address feedback promptly
   - Make requested changes
   - Ensure CI passes

## Community Guidelines

- Be respectful and inclusive
- Help newcomers get started
- Share knowledge and best practices
- Focus on constructive feedback
- Celebrate contributions of all sizes

## Getting Help

- Open an issue for questions
- Check existing issues and discussions
- Join community discussions
- Review documentation and examples

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make Data Markdown (DataMD) better for everyone! 🚀
