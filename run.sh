#!/bin/bash

# Banking Management System - Quick Start Script

echo "🏦 Banking Management System"
echo "============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Start the application
echo "🚀 Starting application..."
echo ""
echo "Access the application at: http://localhost:5000"
echo ""
echo "Default Admin:"
echo "  Username: admin"
echo "  Password: password"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
