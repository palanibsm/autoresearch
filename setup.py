#!/usr/bin/env python3
"""
Interactive setup wizard for Database Query Optimizer PoC
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_section(text):
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}\n")

def check_docker():
    """Check if Docker is installed"""
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        print("✅ Docker found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not found")
        print("   Install from: https://www.docker.com/products/docker-desktop")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} found")
        return True
    else:
        print(f"❌ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def setup_env_file():
    """Create and configure .env file"""
    env_path = Path("backend/.env")
    example_path = Path("backend/.env.example")

    if env_path.exists():
        print("⚠️  .env file already exists")
        overwrite = input("   Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            return False

    # Copy from example
    if example_path.exists():
        with open(example_path) as f:
            content = f.read()
        with open(env_path, 'w') as f:
            f.write(content)
        print(f"✅ Created {env_path}")
    else:
        # Create basic .env
        env_content = """# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banking_db
DB_USER=banking_user
DB_PASSWORD=banking_pass

# Anthropic Claude API Key (Required)
ANTHROPIC_API_KEY=

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_path}")

    # Prompt for API key
    print("\n" + "─" * 60)
    print("Configure Anthropic API Key")
    print("─" * 60)
    print("\nHow to get your API key:")
    print("  1. Go to: https://console.anthropic.com")
    print("  2. Login or create account")
    print("  3. Navigate to 'API Keys' section")
    print("  4. Copy your API key (starts with 'sk-ant-')")

    api_key = input("\nEnter your Anthropic API key (or press Enter to skip): ").strip()

    if api_key:
        with open(env_path, 'r') as f:
            content = f.read()
        content = content.replace('ANTHROPIC_API_KEY=', f'ANTHROPIC_API_KEY={api_key}')
        with open(env_path, 'w') as f:
            f.write(content)
        print("✅ API key configured")
    else:
        print("⚠️  API key not configured. You can add it later in backend/.env")

    return True

def install_dependencies():
    """Install Python dependencies"""
    print_section("Installing Python Dependencies")

    backend_dir = Path("backend")
    requirements_file = backend_dir / "requirements.txt"

    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False

    print("Installing packages...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            cwd=str(backend_dir)
        )
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def start_docker():
    """Start Docker containers"""
    print_section("Starting PostgreSQL (Docker)")

    print("Starting containers...")
    try:
        subprocess.run(
            ["docker-compose", "up", "-d"],
            check=True,
            capture_output=True
        )
        print("✅ Docker containers started")

        # Wait for database
        print("\nWaiting for database to be ready...")
        for i in range(30):
            try:
                subprocess.run(
                    ["docker-compose", "exec", "-T", "postgres", "pg_isready", "-U", "banking_user"],
                    check=True,
                    capture_output=True,
                    timeout=2
                )
                print("✅ Database is ready!")
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                if i < 29:
                    print(f"   Waiting... ({i+1}/30)")

        print("⚠️  Database took too long to start")
        return True  # Container is running, might just need more time

    except subprocess.CalledProcessError as e:
        print(f"❌ Docker startup failed: {e}")
        return False

def summary():
    """Print setup summary"""
    print_header("Setup Complete! 🎉")

    print("Next steps:")
    print("  1. Start PostgreSQL (if not already running):")
    print("     docker-compose up")
    print("")
    print("  2. Start Flask backend:")
    print("     cd backend")
    print("     python app.py")
    print("")
    print("  3. Open in browser:")
    print("     http://localhost:5000")
    print("")
    print("For more information, see:")
    print("  • README.md - Comprehensive documentation")
    print("  • QUICKSTART.md - Quick start guide")
    print("")

def main():
    print_header("Database Query Optimizer - Setup Wizard")

    print("Checking prerequisites...")
    print()

    checks = {
        "Python": check_python(),
        "Docker": check_docker(),
    }

    print()
    if not all(checks.values()):
        print("❌ Please install missing prerequisites and try again")
        return False

    print("✅ All prerequisites found!\n")

    # Setup
    if not setup_env_file():
        return False

    if not install_dependencies():
        return False

    if not start_docker():
        print("⚠️  Docker setup had issues, but you can still try to run")

    summary()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
