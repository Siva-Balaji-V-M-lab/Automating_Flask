@echo off
setlocal enabledelayedexpansion

:: Prompt user details
set /p name=Enter Name: 
set /p age=Enter Age: 
set /p email=Enter Email: 

:: Append to CSV
echo %name%,%age%,%email% >> "%USERPROFILE%\Desktop\sample.csv"

echo User added successfully!
pause
