#!/usr/bin/env bash
# Ejecuta checkov sobre el directorio iac/ y guarda resultados en reports/checkov.json.

set -e

# Asegura que se trabaje desde el directorio raíz del repositorio
cd "$(git rev-parse --show-toplevel)"

echo "Iniciando escaneo de código estático con Checkov en iac/..."

# Crea directorio reports/ en raíz si no existe
mkdir --parents reports

# Ejecuta checkov en iac/ usando reglas personalizadas y guarda la salida en formato JSON
checkov --directory iac/ --external-checks-dir checkov/ --quiet --output json --soft-fail --output-file-path reports

mv reports/results_json.json reports/checkov.json

echo "Escaneo con Checkov completado. Resultados guardados en reports/checkov.json"

# Ejecuta un script para analizar el archivo JSON de configuración de red
bash scripts/validate_network_json.sh

echo "Validación de configuración de red completada."