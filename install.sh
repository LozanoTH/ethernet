#!/bin/bash

# --- CONFIGURACIÓN ---
INTERFACE="wlan0"
PORT=8080
REPO_URL="https://github.com/LozanoTH/ethernet" # Ajustar si es necesario

# --- 1. COMPROBACIÓN DE ACTUALIZACIONES ---
if [ -d ".git" ]; then
    echo "[*] Comprobando actualizaciones en GitHub..."
    git fetch origin &>/dev/null
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u})
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[!] Nueva versión detectada. Actualizando código..."
        git pull origin main
        echo "[+] Actualización completada. Reiniciando script..."
        exec bash "$0" "$@"
        exit
    fi
fi

# --- 2. COMPROBACIÓN DE ROOT ---
echo "[*] Verificando privilegios de Root..."
if [[ $(id -u) -ne 0 ]]; then
    # Intentar detectar si estamos en Termux para sugerir tsu/su
    if [ -d "/data/data/com.termux" ]; then
        echo "[!] Error: Se requiere Root para acceder a la tarjeta WiFi."
        echo "[*] Reintentando con 'su'..."
        exec su -c "env PATH=$PATH:/system/bin:/system/xbin bash $0 $@"
        exit
    else
        echo "[!] Error: Este script debe ejecutarse como root (sudo)."
        exit 1
    fi
fi

# --- 3. COMPROBACIÓN DE PAQUETES ---
echo "[*] Verificando dependencias..."
REQUIRED_PKGS=("python" "wpa-supplicant" "pixiewps" "iw" "openssl")
MISSING_PKGS=()

for pkg in "${REQUIRED_PKGS[@]}"; do
    if ! command -v "$pkg" &>/dev/null && ! pkg list-installed "$pkg" &>/dev/null; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "[!] Faltan paquetes: ${MISSING_PKGS[*]}"
    echo "[*] Instalando dependencias necesarias..."
    pkg install -y root-repo
    pkg install -y "${MISSING_PKGS[@]}"
else
    echo "[+] Todas las dependencias están instaladas."
fi

# --- 4. EJECUCIÓN DEL SCRIPT ---
echo "[+] Iniciando WPS Auditor App..."
echo "[*] Interfaz: $INTERFACE | Puerto Web: $PORT"
echo "------------------------------------------"

# Usamos el comando de entorno específico para Android/Termux
env PATH=$PATH:/system/bin:/system/xbin python3 wps.py -i "$INTERFACE" -W --web-port "$PORT"
