
@echo off
echo Starting all services...

:: Start client.py
start cmd /k "cd /d %~dp0client_socket && python client.py"


echo All services started.
