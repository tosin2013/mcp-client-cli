#!/bin/bash

# Quick Jekyll Test Script
# Fast validation without starting the server

set -e

echo "⚡ Quick Jekyll test for MCP-Client-CLI documentation..."

# Check if we're in the docs directory
if [ ! -f "_config.yml" ]; then
    echo "❌ Error: Run this from the docs/ directory"
    exit 1
fi

# Quick build test
echo "🔨 Testing Jekyll build..."
if bundle exec jekyll build --quiet; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi

# Quick validation
echo "🔍 Validating structure..."

# Check key files
if [ ! -f "_site/index.html" ]; then
    echo "❌ Missing index.html"
    exit 1
fi

# Count chapters
chapter_count=$(find _site/chapters -name "*.html" 2>/dev/null | wc -l)
if [ $chapter_count -lt 12 ]; then
    echo "❌ Expected 12 chapters, found $chapter_count"
    exit 1
fi

echo "✅ Found $chapter_count chapters"
echo "✅ Quick test passed! Ready for deployment."
echo ""
echo "💡 To run full local server: ./test-local.sh"
echo "🚀 To deploy: git add . && git commit -m 'Deploy docs' && git push" 