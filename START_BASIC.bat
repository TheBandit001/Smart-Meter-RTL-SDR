@echo off
cd /d C:\nbpower

:: Start rtl_tcp with 912 MHz frequency in a new window
start "RTL_TCP" cmd /c "rtl_tcp -f 912000000"

:: Wait 5 seconds for rtl_tcp to start
timeout /t 5 /nobreak >nul

:: Start rtlamr in this window (Change 64259716  to your Meter ID, Not the Bill Meter you see on your bill)
rtlamr -filterid=64259716

pause
