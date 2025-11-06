#!/bin/bash

# ML Setup Script for Resume Analysis System
# This script installs required ML dependencies

echo "=================================="
echo "🤖 ML Dependencies Installation"
echo "=================================="
echo ""

# Navigate to Python directory
cd "$(dirname "$0")"

echo "📦 Installing Python ML packages..."
echo ""

# Try different installation methods
if command -v pip3 &> /dev/null; then
    echo "Using pip3..."
    pip3 install sentence-transformers torch scikit-learn numpy
elif command -v pip &> /dev/null; then
    echo "Using pip..."
    pip install sentence-transformers torch scikit-learn numpy
else
    echo "❌ Error: pip or pip3 not found!"
    echo "Please install Python and pip first."
    exit 1
fi

# Check installation
echo ""
echo "✅ Verifying installation..."
python3 -c "
try:
    from sentence_transformers import SentenceTransformer
    import torch
    import numpy as np
    print('✅ All ML libraries installed successfully!')
    print('📥 Downloading pre-trained model (first time only, ~420MB)...')
    model = SentenceTransformer('all-mpnet-base-v2')
    print('✅ Model ready!')
    print('')
    print('🎉 Setup complete! You can now use ML-based analysis.')
except Exception as e:
    print(f'❌ Error: {e}')
    print('Installation may have failed. Try manual installation.')
    exit(1)
"

echo ""
echo "=================================="
echo "✅ Installation Complete!"
echo "=================================="
echo ""
echo "To start the Python service:"
echo "  cd backend/python"
echo "  python3 app.py"
echo ""
