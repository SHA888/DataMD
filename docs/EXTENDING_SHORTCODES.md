# Extending DataMD with New Shortcode Handlers

This guide explains how to extend DataMD by adding new shortcode handlers for additional file formats and data sources.

## Table of Contents
1. [Understanding the Architecture](#understanding-the-architecture)
2. [Creating a New Shortcode Handler](#creating-a-new-shortcode-handler)
3. [Implementing the Handler Function](#implementing-the-handler-function)
4. [Adding Input Sanitization](#adding-input-sanitization)
5. [Integrating with Caching](#integrating-with-caching)
6. [Adding Configuration Options](#adding-configuration-options)
7. [Registering the Handler](#registering-the-handler)
8. [Testing the Handler](#testing-the-handler)
9. [Documentation](#documentation)
10. [Example Implementation](#example-implementation)

## Understanding the Architecture

DataMD uses a modular architecture where each shortcode handler is implemented as a conditional branch in the [DataMDPreprocessor.run()](file:///home/kade/DataMD/python_implementation/datamd_ext.py#L203-L542) method in [datamd_ext.py](file:///home/kade/DataMD/python_implementation/datamd_ext.py). The processor:

1. Parses shortcode patterns using regular expressions
2. Resolves file paths securely
3. Sanitizes input parameters
4. Processes the data
5. Caches results when appropriate
6. Returns formatted output

## Creating a New Shortcode Handler

To add a new shortcode handler, you'll need to:

1. Determine the shortcode syntax
2. Implement the processing logic
3. Add input validation and sanitization
4. Integrate with caching
5. Register the handler in the main processing loop

## Implementing the Handler Function

Let's walk through implementing a new shortcode handler. For this example, we'll create a handler for processing XML files.

### 1. Define the Shortcode Syntax

First, decide on the syntax for your shortcode:
```
{{ xml "data.xml" "xpath_expression" }}
```

### 2. Add the Handler Code

Add a new conditional branch in the [DataMDPreprocessor.run()](file:///home/kade/DataMD/python_implementation/datamd_ext.py#L203-L542) method:

```python
elif cmd == "xml":
    # Check if XML processing is enabled (optional)
    if not config.is_feature_enabled("xml_processing"):
        new_lines.append("Error: XML processing is disabled")
        continue

    # Get XPath expression if provided
    xpath_expr = sanitize_string_input(
        args[0] if args else "/", max_length=1000
    )

    # Try to get from cache first
    cache_key = f"xml:{secure_path}:{xpath_expr}"
    result = cache_manager.get(str(secure_path), xpath=xpath_expr)

    if result is None:
        try:
            import xml.etree.ElementTree as ET

            # Parse XML file
            tree = ET.parse(secure_path)
            root = tree.getroot()

            # Apply XPath expression if provided
            if xpath_expr and xpath_expr != "/":
                elements = root.findall(xpath_expr)
            else:
                elements = [root]

            # Convert to markdown table or text
            if elements:
                # Simple conversion to text for this example
                result = "\n".join([ET.tostring(elem, encoding="unicode") for elem in elements])
            else:
                result = "No elements found"

            # Cache the result
            cache_manager.set(str(secure_path), result, xpath=xpath_expr)
        except Exception as e:
            result = f"Error processing XML file: {str(e)}"

    new_lines.append(result)
```

## Adding Input Sanitization

All input parameters should be sanitized to prevent security vulnerabilities. Use the existing sanitization functions or create new ones as needed:

```python
def sanitize_xpath_expression(xpath):
    """
    Sanitize XPath expression to prevent injection attacks.

    Args:
        xpath (str): The XPath expression to sanitize

    Returns:
        str: Sanitized XPath expression
    """
    if not xpath:
        return "/"

    # Remove potentially dangerous characters
    dangerous_chars = [";", "--", "/*", "*/", "DROP", "DELETE", "UPDATE"]
    sanitized = xpath
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    # Limit length
    return sanitize_string_input(sanitized, max_length=1000)
```

## Integrating with Caching

DataMD uses a caching mechanism to avoid reprocessing the same files. Always integrate your handler with caching:

```python
# Try to get from cache first
cache_key = f"your_shortcode:{secure_path}:{param1}:{param2}"
result = cache_manager.get(str(secure_path), param1=param1, param2=param2)

if result is None:
    # Process the data
    result = your_processing_function(secure_path, param1, param2)

    # Cache the result
    cache_manager.set(str(secure_path), result, param1=param1, param2=param2)

new_lines.append(result)
```

## Adding Configuration Options

For handlers that need configuration options, add them to the configuration system:

1. Add default values to [config.py](file:///home/kade/DataMD/python_implementation/config.py):
```python
DEFAULTS = {
    "features": {
        "xml_processing": True,
        # ... other features
    },
    "processing": {
        "default_xml_xpath": "/",
        # ... other processing defaults
    }
}
```

2. Add getter methods:
```python
def is_xml_processing_enabled(self):
    """Check if XML processing is enabled."""
    return self.get("features.xml_processing", True)

def get_default_xml_xpath(self):
    """Get default XPath expression for XML processing."""
    return self.get("processing.default_xml_xpath", "/")
```

## Registering the Handler

The handler is automatically registered by adding it to the conditional chain in the [run()](file:///home/kade/DataMD/python_implementation/datamd_ext.py#L203-L542) method. Make sure to add it in alphabetical order for maintainability.

## Testing the Handler

Create comprehensive tests for your new handler:

1. Unit tests for the processing function
2. Integration tests for the shortcode
3. Edge case tests for error conditions

Example test structure:
```python
def test_xml_shortcode_basic():
    """Test basic XML shortcode processing."""
    # Create test XML file
    # Process with DataMD
    # Verify output

def test_xml_shortcode_with_xpath():
    """Test XML shortcode with XPath expression."""
    # Create test XML file with known structure
    # Process with XPath expression
    # Verify correct elements are extracted

def test_xml_shortcode_error_handling():
    """Test XML shortcode error handling."""
    # Test with invalid XML file
    # Test with invalid XPath expression
    # Verify appropriate error messages
```

## Documentation

Document your new shortcode in the syntax reference:

1. Add to [SYNTAX.md](file:///home/kade/DataMD/docs/SYNTAX.md)
2. Add example to [examples/](file:///home/kade/DataMD/examples/) directory
3. Update README.md if it's a major feature

## Example Implementation

Here's a complete example of adding a YAML shortcode handler:

### 1. Add to [datamd_ext.py](file:///home/kade/DataMD/python_implementation/datamd_ext.py):

```python
# Add import at the top
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None

# Add to the conditional chain in run() method
elif cmd == "yaml":
    # Check if YAML processing is enabled
    if not config.is_feature_enabled("yaml_processing"):
        new_lines.append("Error: YAML processing is disabled")
        continue

    # Check if PyYAML is available
    if not YAML_AVAILABLE:
        new_lines.append("Error: PyYAML not available for YAML processing")
        continue

    # Get key path if provided
    key_path = sanitize_string_input(
        " ".join(args) if args else "", max_length=1000
    )

    # Try to get from cache first
    cache_key = f"yaml:{secure_path}:{key_path}"
    result = cache_manager.get(str(secure_path), key_path=key_path)

    if result is None:
        try:
            with open(secure_path, 'r') as f:
                data = yaml.safe_load(f)

            # Extract specific key if path provided
            if key_path:
                keys = key_path.split('.')
                value = data
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = f"Key '{key_path}' not found"
                        break
                result = str(value)
            else:
                # Convert entire YAML to JSON format for display
                result = "```json\n" + json.dumps(data, indent=2) + "\n```"

            # Cache the result
            cache_manager.set(str(secure_path), result, key_path=key_path)
        except Exception as e:
            result = f"Error processing YAML file: {str(e)}"

    new_lines.append(result)
```

### 2. Add configuration support in [config.py](file:///home/kade/DataMD/python_implementation/config.py):

```python
# In DEFAULTS
"features": {
    "yaml_processing": True,
    # ... other features
}

# Add getter method
def is_yaml_processing_enabled(self):
    """Check if YAML processing is enabled."""
    return self.get("features.yaml_processing", True)
```

### 3. Add input sanitization function:

```python
def sanitize_key_path(key_path):
    """
    Sanitize key path to prevent injection attacks.

    Args:
        key_path (str): The key path to sanitize

    Returns:
        str: Sanitized key path
    """
    if not key_path:
        return ""

    # Allow alphanumeric characters, dots, underscores, and hyphens
    import re
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', key_path)
    return sanitize_string_input(sanitized, max_length=1000)
```

### 4. Add to [SYNTAX.md](file:///home/kade/DataMD/docs/SYNTAX.md):

```markdown
### YAML Files
```
{{ yaml "config/settings.yaml" }}
{{ yaml "data.yaml" "database.host" }}
```
```

### 5. Create an example in [examples/yaml_example.dmd](file:///home/kade/DataMD/examples/yaml_example.dmd):

```markdown
---
title: "YAML Processing Example"
engine: jupyter
format: html
---

# YAML Processing Example

This example demonstrates the YAML processing feature in DataMD.

## Full YAML File
{{ yaml "config/app.yaml" }}

## Specific Key
{{ yaml "config/app.yaml" "database.host" }}

## Nested Key
{{ yaml "config/app.yaml" "logging.level" }}
```

## Best Practices

1. **Security First**: Always validate and sanitize inputs
2. **Error Handling**: Provide clear error messages for users
3. **Caching**: Use the caching mechanism to improve performance
4. **Configuration**: Make features configurable when appropriate
5. **Documentation**: Document syntax and provide examples
6. **Testing**: Create comprehensive tests for all functionality
7. **Performance**: Consider memory usage for large files
8. **Dependencies**: Handle missing dependencies gracefully

## Conclusion

Extending DataMD with new shortcode handlers is straightforward when following the established patterns. By leveraging the existing infrastructure for security, caching, and configuration, you can quickly add support for new file formats and data sources while maintaining consistency with the rest of the system.
