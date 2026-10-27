@echo off
rem Inicia o Cadê Meu Trem? em http://127.0.0.1:8000 (somente nesta máquina, RNF05).
rem Na primeira vez, prepare o ambiente:
rem   python -m venv .venv
rem   .venv\Scripts\python -m pip install -r requirements.txt
rem Encerre com Ctrl+C.
cd /d "%~dp0.."
echo Abrindo em http://127.0.0.1:8000
.venv\Scripts\python -m flask --app app run --host 127.0.0.1 --port 8000
