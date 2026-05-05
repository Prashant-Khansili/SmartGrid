#!/usr/bin/env python
"""
SmartGrid Dashboard - One-Click Launcher
This script automatically handles environment setup and launches the dashboard
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header():
    """Print welcome header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 50)
    print("  🚀 SmartGrid Dashboard Launcher")
    print("=" * 50)
    print(f"{Colors.ENDC}")


def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")


def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")


def print_info(msg):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")


def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")


def check_python():
    """Check if Python version is sufficient"""
    print_info("Checking Python version...")

    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
        print_error(
            f"Python 3.8+ required. Found Python {version_info.major}.{version_info.minor}"
        )
        return False

    print_success(
        f"Python {version_info.major}.{version_info.minor}.{version_info.micro} found"
    )
    return True


def check_venv():
    """Check if virtual environment exists"""
    print_info("Checking virtual environment...")

    venv_path = Path("venv")
    if not venv_path.exists():
        print_warning("Virtual environment not found. Creating...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print_success("Virtual environment created")
        except subprocess.CalledProcessError:
            print_error("Failed to create virtual environment")
            return False
    else:
        print_success("Virtual environment found")

    return True


def check_requirements():
    """Check if requirements are installed"""
    print_info("Checking dependencies...")

    required_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "plotly",
        "sklearn",
        "tensorflow",
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)

    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        print_info("Installing requirements.txt...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
            )
            print_success("Dependencies installed")
        except subprocess.CalledProcessError:
            print_error("Failed to install dependencies")
            return False
    else:
        print_success("All dependencies installed")

    return True


def check_structure():
    """Check if required directories exist"""
    print_info("Checking project structure...")

    required_dirs = ["dashboard", "src", "src/models", "src/data", "configs"]

    required_files = ["dashboard/app.py", "requirements.txt"]

    missing = []

    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(f"Directory: {dir_path}")

    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(f"File: {file_path}")

    if missing:
        print_error("Missing project files:")
        for item in missing:
            print(f"  - {item}")
        return False

    print_success("Project structure verified")
    return True


def create_directories():
    """Create necessary output directories"""
    print_info("Creating directories...")

    dirs_to_create = ["data/raw", "outputs/models", ".streamlit"]

    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print_success("Directories ready")


def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print_info("Launching dashboard...")
    print()
    print(f"{Colors.BOLD}{Colors.GREEN}")
    print("=" * 50)
    print("  Dashboard is starting...")
    print("=" * 50)
    print(f"{Colors.ENDC}")
    print()
    print_info("Opening browser at: http://localhost:8501")
    print_info("Press Ctrl+C to stop the dashboard")
    print()

    try:
        os.chdir("dashboard")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print_warning("\nDashboard stopped by user")
    except Exception as e:
        print_error(f"Failed to launch dashboard: {e}")
        return False

    return True


def main():
    """Main launcher function"""
    print_header()

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Step 1: Check Python
    if not check_python():
        print_error("Python check failed. Please install Python 3.8+")
        sys.exit(1)

    # Step 2: Check project structure
    if not check_structure():
        print_error("Project structure check failed.")
        print_info("Make sure you're in the SmartGrid root directory")
        sys.exit(1)

    # Step 3: Check/create virtual environment
    if not check_venv():
        print_error("Virtual environment check failed")
        sys.exit(1)

    # Step 4: Check/install requirements
    if not check_requirements():
        print_error("Dependency check failed")
        sys.exit(1)

    # Step 5: Create directories
    create_directories()

    # Step 6: Launch dashboard
    print()
    print_success("All checks passed! Ready to launch!")
    print()

    if not launch_dashboard():
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
