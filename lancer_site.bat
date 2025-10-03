@echo off
cd /d %~dp0
waitress-serve --port=8080 app:app
