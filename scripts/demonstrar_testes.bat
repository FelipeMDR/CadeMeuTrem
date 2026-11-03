@echo off
rem Executa os testes Selenium com o Chrome visivel, em ritmo de demonstracao: cada campo ou botao
rem e destacado antes de ser usado, o texto e digitado letra por letra e cada pagina fica na tela
rem por um instante. O canto da pagina mostra o cenario em execucao.
rem
rem Exemplos:
rem   scripts\demonstrar_testes.bat                                     todos os cenarios
rem   scripts\demonstrar_testes.bat tests\selenium\test_ct01_pessoas.py  so o CT01
rem   scripts\demonstrar_testes.bat -k rfs01                            so os cenarios do RFS01
rem
rem Para mudar o ritmo, defina antes a pausa em segundos (padrao 0.8): set PAUSA_SELENIUM=1.5
setlocal
cd /d "%~dp0.."
set MOSTRAR_NAVEGADOR=1
.venv\Scripts\python -m pytest -v %*
