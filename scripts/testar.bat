@echo off
rem Executa os testes Selenium (CT01, CT02 e CT13). Na primeira vez, prepare o ambiente:
rem   python -m venv .venv
rem   .venv\Scripts\python -m pip install -r requirements.txt
cd /d "%~dp0.."
.venv\Scripts\python -m pytest tests\selenium -v %*
