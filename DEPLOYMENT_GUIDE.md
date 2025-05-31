# 📚 MCP-Client-CLI Documentation Deployment Guide

## 🎯 Overview

This guide covers local testing and automated deployment of the MCP-Client-CLI documentation to GitHub Pages at `https://tosin2013.github.io/mcp-client-cli`.

## 🧪 Local Testing

### Prerequisites

Before testing locally, ensure you have:

```bash
# Check Ruby version (3.0+ recommended)
ruby --version

# Check if Bundler is installed
bundle --version

# If Bundler is not installed
gem install bundler
```

### Quick Test (Recommended)

For fast validation without starting a server:

```bash
cd docs
bundle install  # First time only
./quick-test.sh
```

This will:
- ✅ Validate Jekyll builds correctly
- ✅ Check all 12 chapters are generated
- ✅ Verify site structure
- ⚡ Complete in under 30 seconds

### Full Local Server Test

To test the complete user experience:

```bash
cd docs
./test-local.sh
```

This will:
- 🔍 Check all prerequisites
- 📦 Install dependencies
- 🔨 Build the site
- 🔍 Validate structure
- 🌐 Start local server at `http://localhost:4000`

**Expected Output:**
```
🚀 Starting local Jekyll testing for MCP-Client-CLI documentation...
✅ Ruby and Bundler are available
📦 Installing Jekyll dependencies...
✅ Dependencies installed successfully
🔨 Building Jekyll site...
✅ Site built successfully
🔍 Validating build output...
✅ Found 12 chapter files
✅ Build validation passed
🌐 Starting local Jekyll server...
   Site will be available at: http://localhost:4000
```

### Manual Testing

If you prefer manual control:

```bash
cd docs

# Install dependencies
bundle install

# Build site
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve

# Open in browser
open http://localhost:4000
```

## 🚀 Automated Deployment

### GitHub Actions Setup

The repository includes automated deployment via GitHub Actions:

**File:** `.github/workflows/deploy-docs.yml`

**Features:**
- ✅ Automatic deployment on push to `main`/`master`
- ✅ Parallel build and test jobs
- ✅ Link validation
- ✅ Structure validation
- ✅ Deployment notifications

### Enabling GitHub Pages

1. **Push your changes:**
   ```bash
   git add .
   git commit -m "Add GitHub Pages documentation"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - The workflow will automatically deploy

3. **Access your site:**
   ```
   https://tosin2013.github.io/mcp-client-cli
   ```

### Manual Deployment Trigger

You can manually trigger deployment:

1. Go to **Actions** tab in your repository
2. Select **Deploy Documentation to GitHub Pages**
3. Click **Run workflow**
4. Choose branch and click **Run workflow**

## 🔧 Troubleshooting

### Common Issues

#### Local Testing Issues

**1. Ruby Version Error**
```bash
# Error: Ruby version too old
rbenv install 3.1.0
rbenv global 3.1.0
```

**2. Bundle Install Fails**
```bash
# Clear bundle cache and retry
bundle clean --force
rm Gemfile.lock
bundle install
```

**3. Port 4000 Already in Use**
```bash
# Kill existing process
lsof -ti:4000 | xargs kill -9

# Or use different port
bundle exec jekyll serve --port 4001
```

**4. Site Not Building**
```bash
# Check for syntax errors
bundle exec jekyll build --verbose
```

#### GitHub Actions Issues

**1. Workflow Not Triggering**
- Ensure you're pushing to `main` or `master` branch
- Check that changes are in `docs/` directory
- Verify workflow file is in `.github/workflows/`

**2. Build Failing**
- Check **Actions** tab for detailed logs
- Common issues:
  - Invalid YAML front matter
  - Missing dependencies
  - Liquid template errors

**3. Pages Not Updating**
- Wait 5-10 minutes after successful deployment
- Check **Settings** → **Pages** for status
- Clear browser cache

### Validation Commands

```bash
# Test site structure
cd docs
find _site -name "*.html" | wc -l  # Should be 14+ files

# Check for broken internal links
bundle exec jekyll build
bundle exec htmlproofer _site --disable-external

# Validate YAML front matter
ruby -ryaml -e "puts YAML.load_file('_chapters/chapter1.md')"
```

## 📊 Monitoring Deployment

### GitHub Actions Dashboard

Monitor deployment status:
1. Go to **Actions** tab
2. View recent workflow runs
3. Check build/test/deploy status

### Site Analytics

Once deployed, you can add:
- Google Analytics
- GitHub Pages analytics
- Custom monitoring

### Performance Monitoring

```bash
# Test site performance
lighthouse https://tosin2013.github.io/mcp-client-cli

# Check mobile responsiveness
curl -A "Mobile" https://tosin2013.github.io/mcp-client-cli
```

## 🔄 Maintenance Workflow

### Regular Updates

1. **Update content:**
   ```bash
   # Edit chapters in docs/_chapters/
   cd docs
   ./quick-test.sh  # Validate changes
   ```

2. **Test locally:**
   ```bash
   ./test-local.sh  # Full testing
   ```

3. **Deploy:**
   ```bash
   git add .
   git commit -m "Update documentation"
   git push origin main
   ```

### Adding New Chapters

1. **Create new chapter:**
   ```bash
   cp docs/_chapters/chapter1.md docs/_chapters/chapter13.md
   ```

2. **Update front matter:**
   ```yaml
   ---
   layout: chapter
   title: "New Chapter Title"
   chapter_number: 13
   description: "Chapter description"
   ---
   ```

3. **Test and deploy:**
   ```bash
   cd docs
   ./quick-test.sh
   git add . && git commit -m "Add chapter 13" && git push
   ```

## 🎯 Success Metrics

### Deployment Success Indicators

- ✅ GitHub Actions workflow completes successfully
- ✅ Site loads at `https://tosin2013.github.io/mcp-client-cli`
- ✅ All 12 chapters are accessible
- ✅ Navigation works between chapters
- ✅ Mobile responsiveness works
- ✅ Search engines can index the site

### Testing Checklist

Before each deployment:

- [ ] Local build succeeds
- [ ] All chapters load correctly
- [ ] Navigation links work
- [ ] Mobile layout is responsive
- [ ] Code syntax highlighting works
- [ ] External links are valid
- [ ] Images load correctly (if any)

## 📞 Support

If you encounter issues:

1. **Check the logs** in GitHub Actions
2. **Validate locally** using test scripts
3. **Review documentation** in `docs/README.md`
4. **Check Jekyll documentation** at https://jekyllrb.com/

Your comprehensive MCP-Client-CLI documentation is now ready for professional deployment! 🚀 