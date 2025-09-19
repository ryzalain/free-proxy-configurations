#!/bin/bash

# Free Proxy Configurations - GitHub Push Script
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 Pushing Free Proxy Configurations to GitHub..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "PROJECT_SUMMARY.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Prompt for GitHub username if not provided
if [ -z "$1" ]; then
    echo "📝 Please provide your GitHub username:"
    echo "Usage: ./push-to-github.sh YOUR_USERNAME"
    echo ""
    echo "Or run these commands manually:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/free-proxy-configurations.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    exit 1
fi

USERNAME=$1

echo "👤 GitHub Username: $USERNAME"
echo "📁 Repository: free-proxy-configurations"
echo ""

# Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/$USERNAME/free-proxy-configurations.git

# Rename branch to main
echo "🌿 Renaming branch to main..."
git branch -M main

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Successfully pushed to GitHub!"
    echo "🔗 Repository URL: https://github.com/$USERNAME/free-proxy-configurations"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Enable GitHub Actions (should auto-enable)"
    echo "3. Set up repository topics: proxy, vpn, privacy, security"
    echo "4. Star your repository to show it's active"
    echo "5. Share with the community!"
    echo ""
    echo "🔒 Your free proxy configurations are now live and will auto-update every 6 hours!"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "1. Repository exists on GitHub"
    echo "2. You have push permissions"
    echo "3. Your GitHub credentials are set up"
    echo ""
    echo "💡 You may need to authenticate with GitHub first:"
    echo "git config --global user.name 'Your Name'"
    echo "git config --global user.email 'your.email@example.com'"
fi