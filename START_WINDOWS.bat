@echo off
setlocal
cd /d "%~dp0"
title Haus Flora - Lokaler Start
echo Haus Flora - Einrichtung und Start
echo Voraussetzung: Python 3.11 oder neuer mit "Add python.exe to PATH".
echo.

if exist ".venv\Scripts\python.exe" goto environment_ready
py -3 -c "import sys; sys.exit(sys.version_info < (3, 11))" >nul 2>&1
if not errorlevel 1 goto create_with_launcher
python -c "import sys; sys.exit(sys.version_info < (3, 11))" >nul 2>&1
if errorlevel 1 goto missing_python
python -m venv .venv
if errorlevel 1 goto failed
goto environment_ready

:create_with_launcher
py -3 -m venv .venv
if errorlevel 1 goto failed

:environment_ready
".venv\Scripts\python.exe" -c "import sys; sys.exit(sys.version_info < (3, 11))"
if errorlevel 1 goto missing_python
echo [1/3] Abhaengigkeiten installieren oder pruefen...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo [2/3] Datenbank und Bilder vorbereiten...
".venv\Scripts\python.exe" scripts\start_local.py
if errorlevel 1 goto failed
echo.
echo [3/3] Website starten: http://127.0.0.1:8000/de/
echo Diese Adresse im Browser oeffnen. Zum Beenden Strg+C druecken.
echo Dieses Fenster waehrend der Nutzung geoeffnet lassen.
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
if errorlevel 1 goto failed
exit /b 0

:missing_python
echo.
echo Python 3.11 oder neuer wurde nicht gefunden.
echo Installiere Python von https://www.python.org/downloads/windows/
echo Setze bei der Installation den Haken "Add python.exe to PATH".
echo Starte danach diese Datei erneut.
echo Falls eine alte .venv existiert: umbenennen und erneut starten.
pause
exit /b 1

:failed
echo.
echo Einrichtung oder Start fehlgeschlagen. Siehe Fehlermeldung oben.
echo Fuer die Installation der Pakete ist eine Internetverbindung erforderlich.
pause
exit /b 1
