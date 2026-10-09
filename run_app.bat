@echo off
echo ===================================================
echo   SOCIAL NETWORK COMMUNITY DETECTION
echo ===================================================
echo Installing/Upgrading requirements if needed...
python -m pip install -r requirements.txt
echo Starting the Streamlit application...
python -m streamlit run app.py
pause
