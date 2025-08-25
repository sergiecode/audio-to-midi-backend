"""
Setup script for Audio to MIDI Backend
Created by Sergie Code

This script helps set up the development environment.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Required: Python 3.8 or higher")
        return False

def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    if platform.system() == "Windows":
        command = "python -m venv venv"
    else:
        command = "python3 -m venv venv"
    
    return run_command(command, "Creating virtual environment")

def activate_and_install():
    """Install dependencies in virtual environment."""
    if platform.system() == "Windows":
        pip_command = "venv\\Scripts\\pip"
    else:
        pip_command = "venv/bin/pip"
    
    commands = [
        (f"{pip_command} install --upgrade pip", "Upgrading pip"),
        (f"{pip_command} install -r requirements.txt", "Installing dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['uploads', 'output', 'logs', 'models']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")
    
    return True

def test_installation():
    """Test if the installation works."""
    print("🧪 Testing installation...")
    
    if platform.system() == "Windows":
        python_command = "venv\\Scripts\\python"
    else:
        python_command = "venv/bin/python"
    
    test_command = f"{python_command} -c \"from src.transcription.transcriber import AudioTranscriber; print('✅ Import test passed')\""
    
    return run_command(test_command, "Testing imports")

def print_next_steps():
    """Print instructions for next steps."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Start the server:")
    print("   python app.py")
    
    print("\n3. Test the API:")
    print("   python example_usage.py")
    
    print("\n4. Open your browser and go to:")
    print("   http://localhost:5000/health")
    
    print("\n📖 Read the README.md for detailed instructions!")
    print("\n🎵 Happy coding! - Sergie Code")

def main():
    """Main setup function."""
    print("🎵 Audio to MIDI Backend - Setup Script")
    print("Created by Sergie Code\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not activate_and_install():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("⚠️ Installation test failed, but basic setup is complete")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
