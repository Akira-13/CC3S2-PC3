#!/usr/bin/env bash

# La ejecucion se detiene si ocurre un error
set -e

# Muestra un mensaje de error si ocurre alguno
trap 'echo "[ERROR] Error durante la ejecución de run_all_scans.sh"' ERR

# Crea la carpeta de reportes si no existe
mkdir -p reports
echo "[INFO] Carpeta de reportes creada"

# Inicia el escaneo de seguridad con Bandit, TFLint y Checkov secuencialmente

echo "[SCAN] Escaneo con Bandit iniciado"
bash scripts/scan_bandit.sh

echo "[SCAN] Escaneo con TFLint iniciado"
bash scripts/scan_tflint.sh

echo "[PRETTIFY] Formateando archivo JSON TFLint"
python util/prettify_json.py

echo "[SCAN] Escaneo con Checkov iniciado"
bash scripts/scan_checkov.sh

# Genera el reporte final ejecutando el script en python
python src/security_checker.py
echo "[REPORT] Reporte final generado"