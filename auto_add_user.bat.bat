@echo off
title Flask Automation Script

REM Step 1: Reset CSV with header only
echo Name,Age,Email,Salary > C:\Users\sivabalaji.vm\Desktop\sample.csv

REM Step 2: Start Flask app
start cmd /k "py day3.1.py"

REM Step 3: Wait for Flask to boot
timeout /t 5 /nobreak >nul

REM Step 4: Upload CSV using curl
curl -X POST http://127.0.0.1:5000/upload_csv -F "file=@C:/Users/sivabalaji.vm/Desktop/sample.csv"

REM Step 5: Open Flask portal in browser
start http://127.0.0.1:5000/

REM Step 6: Keep adding NEW users every 3 seconds
setlocal enabledelayedexpansion
set /a counter=1

:loop
set /a age=20+(!random! %% 25)
set /a salary=50000+(!random! %% 50000)

REM Create a random name
for /f %%A in ('powershell -command "[guid]::NewGuid().ToString().Substring(0,8)"') do set uid=%%A

echo User!counter!,!age!,user!counter!_!uid!@mail.com,!salary! >> C:\Users\sivabalaji.vm\Desktop\sample.csv

set /a counter+=1
timeout /t 3 >nul
goto loop
