# MCP-Client-CLI Documentation

This directory contains the GitHub Pages documentation for the MCP-Client-CLI project, converted from the original ebook format.

## Structure

```
docs/
├── _config.yml          # Jekyll configuration
├── index.md             # Homepage
├── chapters.md          # Chapters index
├── _chapters/           # Chapter content
│   ├── chapter1.md
│   ├── chapter2.md
│   └── ...
├── _layouts/            # Jekyll layouts
│   ├── default.html
│   └── chapter.html
└── assets/
    └── css/
        └── style.scss   # Custom styling
```

## GitHub Pages Setup

To enable GitHub Pages for this repository:

1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch and "/docs" folder
5. Click "Save"

The documentation will be available at: `https://your-username.github.io/mcp-client-cli`

## Local Development

To run the documentation locally:

```bash
# Install Jekyll and dependencies
gem install bundler jekyll

# Navigate to docs directory
cd docs

# Create Gemfile if it doesn't exist
echo 'source "https://rubygems.org"' > Gemfile
echo 'gem "github-pages", group: :jekyll_plugins' >> Gemfile

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`

## Content Organization

- **Chapters**: All chapter content is in `_chapters/` with Jekyll front matter
- **Navigation**: Automatic chapter navigation and table of contents
- **Styling**: Custom CSS in `assets/css/style.scss`
- **Layouts**: Responsive layouts for different content types

## Features

- ✅ Responsive design
- ✅ Chapter navigation (previous/next)
- ✅ Table of contents
- ✅ Syntax highlighting
- ✅ Search engine optimization
- ✅ Mobile-friendly layout

## Customization

To customize the appearance:

1. Edit `_config.yml` for site-wide settings
2. Modify `assets/css/style.scss` for styling
3. Update layouts in `_layouts/` for structure changes

## Original Source

This documentation was converted from an ebook format with 12 chapters covering comprehensive MCP server testing with the mcp-client-cli tool. 