#!/bin/bash

# Local Jekyll Testing Script for MCP-Client-CLI Documentation
# This script validates that the Jekyll site builds and runs correctly

set -e  # Exit on any error

echo "🚀 Starting local Jekyll testing for MCP-Client-CLI documentation..."
echo ""

# Check if we're in the docs directory
if [ ! -f "_config.yml" ]; then
    echo "❌ Error: _config.yml not found. Please run this script from the docs/ directory."
    exit 1
fi

# Check if Ruby and Bundler are installed
echo "🔍 Checking prerequisites..."
if ! command -v ruby &> /dev/null; then
    echo "❌ Error: Ruby is not installed. Please install Ruby first."
    echo "   Visit: https://www.ruby-lang.org/en/downloads/"
    exit 1
fi

if ! command -v bundle &> /dev/null; then
    echo "❌ Error: Bundler is not installed. Installing bundler..."
    gem install bundler
fi

echo "✅ Ruby and Bundler are available"

# Install dependencies
echo ""
echo "📦 Installing Jekyll dependencies..."
if [ ! -f "Gemfile.lock" ]; then
    echo "   First time setup - this may take a few minutes..."
fi

bundle install

echo "✅ Dependencies installed successfully"

# Build the site
echo ""
echo "🔨 Building Jekyll site..."
bundle exec jekyll build

if [ $? -eq 0 ]; then
    echo "✅ Site built successfully"
else
    echo "❌ Build failed - check the errors above"
    exit 1
fi

# Validate the build
echo ""
echo "🔍 Validating build output..."

# Check if key files exist
if [ ! -f "_site/index.html" ]; then
    echo "❌ Error: index.html not generated"
    exit 1
fi

if [ ! -d "_site/chapters" ]; then
    echo "❌ Error: chapters directory not generated"
    exit 1
fi

# Count chapter files
chapter_count=$(find _site/chapters -name "*.html" | wc -l)
if [ $chapter_count -lt 12 ]; then
    echo "❌ Error: Expected 12 chapters, found $chapter_count"
    exit 1
fi

echo "✅ Found $chapter_count chapter files"
echo "✅ Build validation passed"

# Start local server
echo ""
echo "🌐 Starting local Jekyll server..."
echo "   Site will be available at: http://localhost:4000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Check if port 4000 is already in use
if lsof -Pi :4000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Warning: Port 4000 is already in use"
    echo "   Trying alternative port 4001..."
    bundle exec jekyll serve --port 4001 --host 0.0.0.0
else
    bundle exec jekyll serve --host 0.0.0.0
fi 