# Changelog

All notable changes to the MCP Testing Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-05-28

### Fixed
- Fixed validation inconsistency in error responses where the framework was returning `"type": "error"` but expecting `"type": "text"` according to its Pydantic schema
- Added new standardized error handler module to ensure all error responses comply with the MCP specification
- Implemented backward compatibility for detecting error responses during migration

### Added
- New `error_handler.py` module with functions for creating standardized error responses:
  - `create_error_response()`: Creates responses with `"type": "text"` and JSON-formatted error messages
  - `format_validation_error()`: Specifically formats validation errors
  - `format_tool_error()`: Specifically formats tool execution errors
  - `is_error_response()`: Detects error responses in various formats
  - `standardize_response()`: Converts non-compliant responses to the correct format
- Comprehensive test suite for the new error handling functionality

## [1.0.1] - 2025-04-15

### Added
- Initial public release of the MCP Testing Framework
- Comprehensive testing capabilities for MCP servers
- Support for functional, security, and performance testing
- Automated issue detection and remediation
- Integration with CI/CD pipelines
