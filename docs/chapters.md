---
layout: default
title: Chapters
description: Complete list of all chapters in the MCP-Client-CLI Technical Documentation
---

# Chapters

This comprehensive guide is organized into 12 chapters, each covering different aspects of MCP server testing with the mcp-client-cli tool.

{% assign sorted_chapters = site.chapters | sort: 'chapter_number' %}

<div class="chapters-grid">
{% for chapter in sorted_chapters %}
<div class="chapter-card">
    <h3><a href="{{ chapter.url | relative_url }}">Chapter {{ chapter.chapter_number }}: {{ chapter.title }}</a></h3>
    {% if chapter.description %}
    <p class="chapter-description">{{ chapter.description }}</p>
    {% endif %}
    <a href="{{ chapter.url | relative_url }}" class="read-more">Read Chapter →</a>
</div>
{% endfor %}
</div>

## Reading Guide

### For Beginners
Start with these chapters to get up and running:
1. [Chapter 1: Introduction to MCP and the MCP-Client-CLI]({{ '/chapters/chapter1/' | relative_url }})
2. [Chapter 3: Setting Up the MCP-Client-CLI]({{ '/chapters/chapter3/' | relative_url }})
3. [Chapter 4: Basic Usage and Commands]({{ '/chapters/chapter4/' | relative_url }})

### For Advanced Users
Jump to these chapters for advanced topics:
- [Chapter 6: Advanced Testing Capabilities]({{ '/chapters/chapter6/' | relative_url }})
- [Chapter 7: AI-Driven Configuration System]({{ '/chapters/chapter7/' | relative_url }})
- [Chapter 8: CI/CD Integration]({{ '/chapters/chapter8/' | relative_url }})

### For Troubleshooting
When you encounter issues:
- [Chapter 10: Troubleshooting and Best Practices]({{ '/chapters/chapter10/' | relative_url }})
- [Chapter 11: Case Studies and Real-World Examples]({{ '/chapters/chapter11/' | relative_url }})

## External References

This documentation includes over 150 external references to authoritative sources, providing additional context and validation for the techniques described. 