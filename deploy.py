#!/usr/bin/env python3
"""
🚀 LingoDash Deployment Script
Deploy to Streamlit Cloud with one command
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_prerequisites():
    """Check if git is configured and repository is ready"""
    print("🔍 Checking prerequisites...")
    
    # Check if git is installed
    if not run_command("git --version", "Checking git installation"):
        return False
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository. Initializing...")
        if not run_command("git init", "Initializing git repository"):
            return False
    
    return True

def validate_files():
    """Validate that all required files exist"""
    required_files = [
        "streamlit_app.py",
        "requirements.txt", 
        ".streamlit/config.toml",
        "data/languages.csv",
        "data/competitors.csv", 
        "data/phases.csv",
        "data/projection.csv"
    ]
    
    print("📋 Validating required files...")
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def deploy_to_streamlit_cloud():
    """Main deployment process"""
    print("\n🌐 LingoDash Deployment to Streamlit Cloud")
    print("=" * 50)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        return False
    
    # Step 2: Validate files
    if not validate_files():
        return False
    
    # Step 3: Add all files to git
    print("\n📦 Preparing files for deployment...")
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Step 4: Check if there are changes to commit
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  No changes to commit - repository is up to date")
    else:
        # Step 5: Commit changes
        commit_message = "🚀 Deploy LingoDash v1.0 - Strategic Multilingual Expansion Dashboard"
        if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
            return False
    
    # Step 6: Check if remote origin exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("\n⚠️  No remote origin found.")
        print("📋 Next steps:")
        print("1. Create a repository on GitHub")
        print("2. Add remote origin:")
        print("   git remote add origin https://github.com/YOUR_USERNAME/lingopass.git")
        print("3. Push to GitHub:")
        print("   git push -u origin main")
        print("4. Deploy on https://share.streamlit.io")
        return True
    
    # Step 7: Push to GitHub
    if not run_command("git push origin main", "Pushing to GitHub"):
        # Try to set upstream if it fails
        if not run_command("git push -u origin main", "Setting upstream and pushing"):
            return False
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Go to https://share.streamlit.io")
    print("2. Sign in with your GitHub account")
    print("3. Click 'New app'")
    print("4. Select your repository")
    print("5. Set main file path: streamlit_app.py")
    print("6. Click 'Deploy!'")
    
    print("\n🔗 Your app will be available at:")
    print("   https://YOUR_USERNAME-lingopass-streamlit-app-xxx.streamlit.app")
    
    return True

if __name__ == "__main__":
    success = deploy_to_streamlit_cloud()
    sys.exit(0 if success else 1) 