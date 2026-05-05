#!/bin/bash

# SmartGrid Dashboard - Quick Setup Script for macOS/Linux
# This script automates the entire setup process

echo ""
echo "========================================"
echo "  SmartGrid Dashboard - Setup Script"
echo "  macOS/Linux"
echo "========================================"
echo ""

# 1. Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3.8+"
    exit 1
fi
python3 --version
echo "✅ Python found"

# 2. Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✅ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# 3. Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# 4. Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✅ pip upgraded"

# 5. Install dependencies
echo ""
echo "Installing dependencies (this may take 2-3 minutes)..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# 6. Verify installation
echo ""
echo "Verifying installation..."
python -c "import streamlit; import tensorflow; import sklearn; print('✅ All packages verified!')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some packages may not be installed correctly"
else
    echo "✅ Installation verified successfully"
fi

# 7. Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data/raw
mkdir -p outputs/models
echo "✅ Directories created"

# 8. Summary
echo ""
echo "========================================"
echo "  ✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Start dashboard:      cd dashboard"
echo "3. Run dashboard:        streamlit run app.py"
echo "4. Open browser:         http://localhost:8501"
echo ""
echo "For detailed instructions, see: SETUP_GUIDE.md"
echo ""

# Keep terminal open if run via GUI
read -p "Press Enter to close..."
