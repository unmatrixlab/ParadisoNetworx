@echo off
title Lanzador Nexus AI - WSL Ubuntu
echo ==========================================
echo    INICIANDO ECOSISTEMA DE IA (WSL)
echo ==========================================

:: 1. Lanzar Streamlit en una NUEVA ventana de Ubuntu
echo [OK] Abriendo terminal de Ubuntu para Streamlit...
start wsl -d Ubuntu bash -ic "streamlit run /home/ico/ia2.py --server.enableCORS=false --server.enableXsrfProtection=false; exec bash"

:: 2. Esperar a que el servidor de Ubuntu levante
echo Esperando 7 segundos para asegurar que la web cargue...
timeout /t 7

:: 3. Iniciar el Tunel de Cloudflare en esta misma ventana
echo [OK] Abriendo el puente hacia Internet...
cd %USERPROFILE%\Downloads
.\cloudflared-windows-amd64.exe tunnel --url http://localhost:8501

pause
