# 🔍 Universal Data Pattern Identifier and Formatter

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange.svg)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-green.svg)]()

> **An intelligent data formatting tool that uses Google's Gemini AI to automatically identify patterns in your data and generate precise regex patterns for extraction and formatting.**

## 🌟 Features

- 🤖 **AI-Powered Pattern Recognition**: Leverages Google Gemini AI to analyze and understand complex data patterns
- 📊 **Multi-Format Support**: Works with both `.txt` and `.csv` files
- 🎯 **Intelligent Regex Generation**: Automatically creates precise regex patterns based on your data structure
- ⚡ **Batch Processing**: Process entire files with thousands of records efficiently
- 🔧 **Fallback Mechanisms**: Smart fallback pattern generation when API is unavailable
- 📝 **Interactive CLI**: User-friendly command-line interface with step-by-step guidance
- 🧪 **Pattern Testing**: Built-in testing to verify regex patterns before full processing
- 💾 **Flexible Output**: Save results in multiple formats (TXT, CSV)

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Install Dependencies

```bash
pip install google-generativeai
```

### Clone Repository

```bash
git clone https://github.com/yourusername/data-pattern-formatter.git
cd data-pattern-formatter
```

## ⚡ Quick Start

1. **Set up your API key** in the script:
   ```python
   API_KEY = "your-gemini-api-key-here"
   ```

2. **Run the application**:
   ```bash
   python data_pattern_formatter.py
   ```

3. **Choose your mode**:
   - **Option 1**: Analyze data and get AI-generated regex patterns
   - **Option 2**: Apply regex patterns to format your entire dataset

## 📖 Usage

### Mode 1: Pattern Recognition 🔍

Perfect for when you have messy data and need to identify the underlying pattern:

```
Input File: user_data.txt
Content: 
John Doe|john.doe@email.com|555-1234|25
Jane Smith|jane.smith@email.com|555-5678|30
Bob Johnson|bob.j@email.com|555-9012|28

Expected Format: [name]|[email]|[phone]|[age]

Generated Pattern: ([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)
```

### Mode 2: Data Formatting ⚙️

Use this mode when you have a regex pattern and want to format your entire dataset:

```
Input: Raw data file (any format)
Pattern: Your regex pattern
Output: Cleanly formatted data with consistent structure
```

## 🔧 Configuration

### API Configuration

```python
class DataPatternFormatter:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
```

### Generation Settings

```python
generation_config = {
    "temperature": 0.1,      # Low temperature for consistent results
    "max_output_tokens": 150 # Limit output length
}
```

## 💡 Examples

### Example 1: Processing Log Files

**Input Data:**
```
2024-01-15 10:30:45 ERROR Database connection failed
2024-01-15 10:31:02 INFO User login successful
2024-01-15 10:31:15 WARN Memory usage high
```

**Expected Format:** `[date]|[time]|[level]|[message]`

**Generated Pattern:** `(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)`

### Example 2: Processing Contact Information

**Input Data:**
```
Smith, John, john.smith@email.com, (555) 123-4567
Doe, Jane, jane.doe@email.com, (555) 987-6543
```

**Expected Format:** `[lastname]|[firstname]|[email]|[phone]`

**Generated Pattern:** `([^,]+),\s*([^,]+),\s*([^,]+),\s*(.*)`

### Example 3: Processing Product Data

**Input Data:**
```
PRD001:Laptop:$999.99:Electronics
PRD002:Mouse:$29.99:Accessories
PRD003:Keyboard:$79.99:Accessories
```

**Expected Format:** `[id]|[name]|[price]|[category]`

**Generated Pattern:** `([^:]+):([^:]+):([^:]+):([^:]+)`

## 📚 API Reference

### Core Methods

#### `read_file(file_path: str) -> List[str]`
Reads data from TXT or CSV files.

**Parameters:**
- `file_path`: Path to the input file

**Returns:**
- List of strings containing file data

#### `get_regex_pattern_from_gemini(sample_data: List[str], expected_format: str) -> str`
Generates regex pattern using Gemini AI.

**Parameters:**
- `sample_data`: Sample of your data for analysis
- `expected_format`: Desired output format specification

**Returns:**
- Regex pattern string

#### `apply_regex_pattern(data: List[str], regex_pattern: str) -> List[str]`
Applies regex pattern to format data.

**Parameters:**
- `data`: Input data to process
- `regex_pattern`: Regex pattern to apply

**Returns:**
- Formatted data as list of strings

#### `save_output(data: List[str], output_path: str)`
Saves formatted data to file.

**Parameters:**
- `data`: Formatted data to save
- `output_path`: Output file path

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **API Key Invalid** | Verify your Gemini API key at [ai.google.dev](https://ai.google.dev/) |
| **File Not Found** | Check file path and ensure file exists |
| **Regex Pattern Fails** | Use Pattern Testing mode to verify before processing |
| **Empty Output** | Check if your data matches the expected pattern |
| **Encoding Issues** | Ensure your files are UTF-8 encoded |

### Error Codes

- `FileNotFoundError`: Input file doesn't exist
- `ValueError`: Unsupported file format
- `re.error`: Invalid regex pattern
- `Exception`: General API or processing error

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Data    │───▶│  Gemini AI API   │───▶│ Regex Pattern   │
│  (TXT/CSV)      │    │   Analysis       │    │  Generation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Formatted Data  │◀───│   Data Processing│◀───│ Pattern Application│
│   Output        │    │   & Validation   │    │   & Extraction  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings for all functions
- Include type hints where applicable
- Write comprehensive tests

## 📝 Changelog

### Version 1.0.0
- Initial release with Gemini AI integration
- Support for TXT and CSV files
- Interactive CLI interface
- Pattern testing functionality
- Fallback pattern generation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- 📧 **Email**: support@yourproject.com
- 💬 **Issues**: [GitHub Issues](https://github.com/yourusername/data-pattern-formatter/issues)
- 📖 **Documentation**: [Wiki](https://github.com/yourusername/data-pattern-formatter/wiki)

## ⭐ Acknowledgments

- Google Gemini AI team for the powerful language model
- Python community for excellent libraries
- Contributors and users for feedback and improvements

---

<div align="center">

**Made with ❤️ for data professionals**

[![Stars](https://img.shields.io/github/stars/yourusername/data-pattern-formatter?style=social)](https://github.com/yourusername/data-pattern-formatter/stargazers)
[![Forks](https://img.shields.io/github/forks/yourusername/data-pattern-formatter?style=social)](https://github.com/yourusername/data-pattern-formatter/network/members)

</div>