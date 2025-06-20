#!/usr/bin/env bash
# Ejecuta bandit sobre el directorio src/ y guarda resultados en reports/bandit.json.

set -e

# Asegura que se trabaje desde el directorio raíz del repositorio
cd "$(git rev-parse --show-toplevel)"

echo "Iniciando escaneo de seguridad estático con Bandit..."

# Crea directorio reports/ en raíz si no existe
mkdir --parents reports

# Ejecuta bandit en src/ y guardar salida en formato JSON
# Escanea solo vulnerabilidades críticas con alta severidad y alta confianza
bandit --recursive src/ --format json --output reports/bandit.json --severity-level high --confidence-level high

echo "Escaneo con Bandit completado. Resultados guardados en reports/bandit.json"
