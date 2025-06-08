#!/usr/bin/env bash
# Ejecuta shellcheck sobre los scripts bash y guarda los resultados en shellcheck_report.txt

set -e

# Asegura que se trabaje desde el directorio raíz del repositorio
cd "$(git rev-parse --show-toplevel)"

echo "🔹 Iniciando escaneo de scripts Bash con Shellcheck..."

# Crear carpeta reports si no existe
mkdir -p reports

# Encontrar todos los scripts .sh y escanearlos
# La salida de shellcheck se encuentra en reports/shellcheck_report.json
find . -type f -name "*.sh" -exec shellcheck --format=json1 {} + > reports/shellcheck_report.json

echo "✅ Escaneo de Shellcheck completado. Resultados guardados en reports/shellcheck_report.json"
