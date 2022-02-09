@echo off
REM 声明采用UTF-8编码
chcp 65001
setlocal enabledelayedexpansion
set count=10000
cd ../datasets/JPEGImages
for /f "delims=" %%i in ('dir /b *.jpg,*.png,*.bmp,*.jpeg,*.gif') do call:Rename "%%~i"
pause
exit
 
:Rename
set /a count+=1
if /i "%~1"=="!count:~1!%~x1" goto :eof
if exist "!count:~1!%~x1" goto Rename
echo rename：%1 !count:~1!
ren "%~1" "!count:~1!%~x1"
goto :eof