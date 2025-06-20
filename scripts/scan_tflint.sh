#!/usr/bin/env bash
# Ejecuta tfling sobre los módulos del directorio iac/ y guarda resultados en reports/tflint.json.

set -e

# Asegura que se trabaje desde el directorio raíz del repositorio
cd "$(git rev-parse --show-toplevel)"

ROOT_DIR=$(pwd)

echo "Iniciando escaneo de TFLint..."

# Crear carpeta reports si no existe
mkdir -p reports


# Ejecutar tflint con salida JSON
# Se recorre cada módulo
find iac/ -type d | while read -r dir; do
  if [ -f "$dir/main.tf" ]; then

  # Extrae el nombre del módulo
  module_name=$(basename "$dir")

  # Crear un archivo de salida único para cada módulo
  output_file="$ROOT_DIR/reports/tflint_${module_name}.json"

    (
      cd "$dir"
      # Inicializar terraform (por completitud se deshabilita backend en caso tuviera)
      terraform init -backend=false -input=false -no-color > /dev/null 2>&1
      # Ejecutar tflint y guardar salida
      tflint --format json --force > "$output_file"
    )
  fi
done

echo "Escaneo con TFLint completado. Resultados guardados en reports/tflint_<modulo>.json"
