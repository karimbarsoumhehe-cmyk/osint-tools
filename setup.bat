@echo off
title Installation des dependances
echo ======================================
echo Installation des modules Python...
echo ======================================

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ======================================
echo Installation terminee.
echo ======================================
pause