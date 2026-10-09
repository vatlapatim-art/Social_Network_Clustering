import subprocess
import sys
import os

def main():
    print("SOCIAL NETWORK COMMUNITY DETECTION - LAUNCHER")
    print("===========================================")
    print("Checking dependencies...")
    try:
        import streamlit
        print("Streamlit found. Launching application...")
        # Use subprocess to run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except ImportError:
        print("Error: Required dependencies are not installed.")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
