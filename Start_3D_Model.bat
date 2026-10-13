@echo off
title First-Floor 3D Massing Model Launcher
echo ===================================================================
echo   FIRST-FLOOR ARCHITECTURAL 3D MASSING MODEL
echo   Source CAD Plan: 1446 x 2048 px
echo   26 Apartment Blocks + 5 Structural Cores
echo ===================================================================
echo.
echo [1/2] Opening application in your default web browser...
start "" "http://localhost:8080/index.html"
echo.
echo [2/2] Starting local HTTP server on port 8080...
echo Server running at: http://localhost:8080
echo (Keep this window open while viewing the model. Press Ctrl+C to stop.)
echo.
python -m http.server 8080
pause
