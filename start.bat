@echo off
echo ====================================
echo        CORE-SE PROJECT STARTUP
echo ====================================
echo.

REM Set the root directory
set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

echo Starting CORE-SE Application...
echo Root directory: %ROOT_DIR%
echo.

REM Start Backend (Python FastAPI)
echo [1/3] Starting Backend Server...
echo --------------------------------
start "CORE Backend" cmd /k "cd /d "%ROOT_DIR%backend" && (if exist core_env\Scripts\activate.bat (echo Activating virtual environment... && call core_env\Scripts\activate.bat && echo Environment activated.) else (echo Using system Python.)) && echo Starting FastAPI server on http://127.0.0.1:8000 && python start_backend.py"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

REM Start FDS Data Engine
echo [2/3] Starting FDS Data Engine...
echo -----------------------------------
start "FDS Data Engine" cmd /k "cd /d "%ROOT_DIR%backend\fds" && (if exist ..\core_env\Scripts\activate.bat (echo Activating virtual environment... && call ..\core_env\Scripts\activate.bat && echo Environment activated.) else (echo Using system Python.)) && echo Starting FDS Data Engine on http://localhost:8001 && python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

REM Wait a moment for data engine to initialize
timeout /t 4 /nobreak >nul

REM Start Frontend (Next.js)
echo [3/3] Starting Frontend Server...
echo ---------------------------------
start "CORE Frontend" cmd /k "cd /d "%ROOT_DIR%frontend" && echo Checking dependencies... && npm install --legacy-peer-deps --silent && echo Starting Next.js development server... && npm run dev"

echo.
echo ====================================
echo   CORE-SE Application Started!
echo ====================================
echo.
echo Backend:     http://localhost:8000
echo Data Engine: http://localhost:8001
echo Frontend:    http://localhost:3000 (or next available port)
echo.
echo All three services are starting in separate windows.
echo Check each window for the exact URLs and status.
echo Wait a moment for them to fully initialize.
echo.
echo The FDS Data Engine provides requirements impact analysis
echo and connects to the frontend for advanced analytics.
echo.
echo Press any key to close this window...
pause >nul
