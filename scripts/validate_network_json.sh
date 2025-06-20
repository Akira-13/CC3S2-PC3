#!/usr/bin/env bash

# Valida el contenido del archivo network_config.json generado por Terraform

set -e

# Ruta del archivo JSON a validar 
JSON_FILE="iac/network_config.json"
# Ruta del archivo de reporte
REPORT_FILE="reports/network_validation_report.json"

mkdir -p reports

# Si el archivo no existe, se registra el error y se detiene
if [ ! -f "$JSON_FILE" ]; then
  echo "{\"error\": \"Archivo no encontrado: $JSON_FILE\"}" > "$REPORT_FILE"
  echo "Archivo no encontrado: $JSON_FILE."
  exit 0
fi

# Extraer valores del JSON
CIDR=$(jq -r '.cidr_block' "$JSON_FILE")
PORT=$(jq '.from_port' "$JSON_FILE")
TO_PORT=$(jq '.to_port' "$JSON_FILE")
NAME=$(jq -r '.network_name' "$JSON_FILE")
PROTOCOL=$(jq -r '.protocol' "$JSON_FILE")
ALLOWED_IPS=$(jq -r '.allowed_ips[]' "$JSON_FILE")

# Inicializar listas para errores y advertencias
ERRORS=()
WARNINGS=()

HIGH_RISK_PORTS=(21 23 69 109 110 137 138 139 143 445)

# Validación 1: detectar CIDR abierto
if [[ "$CIDR" == "0.0.0.0/0" ]]; then
  ERRORS+=("CIDR abierto detectado: $CIDR")
fi

# Recorrer todos los puertos del rango para aplicar validaciones
for p in $(seq "$PORT" "$TO_PORT"); do
  # Validación 2: puertos menores a 1024
  if [ "$p" -lt 1024 ]; then
    WARNINGS+=("Puerto inseguro (<1024): $p")
  fi

  # Validación 3: puertos de alto riesgo
  for risky in "${HIGH_RISK_PORTS[@]}"; do
    if [ "$p" -eq "$risky" ]; then
      ERRORS+=("Puerto de alto riesgo detectado: $p")
    fi
  done
done

# Validación 4: rango de puertos muy amplio
if [ "$((TO_PORT - PORT))" -gt 100 ]; then
  WARNINGS+=("Rango de puertos amplio: de $PORT a $TO_PORT")
fi

# Validación 5: nombre de red por defecto
if [[ "$NAME" == "dummy-network" ]]; then
  WARNINGS+=("Nombre de red por defecto usado: $NAME")
fi

# Validación 6: uso de protocolo permisivo
if [[ "$PROTOCOL" == "all" ]]; then
  WARNINGS+=("Protocolo permisivo: $PROTOCOL")
fi

# Validación 6: IPs peligrosas en la lista de allowed_ips
for ip in $ALLOWED_IPS; do
  if [[ "$ip" == "0.0.0.0/0" ]]; then
    ERRORS+=("IP peligrosa permitida: $ip")
  fi
done

# Generar archivo de reporte en JSON
{
  echo "{"
  echo "  \"archivo_analizado\": \"$JSON_FILE\","
  echo "  \"errores\": ["
  for ((i = 0; i < ${#ERRORS[@]}; i++)); do
    echo "    \"${ERRORS[$i]}\"$( [[ $i -lt $((${#ERRORS[@]} - 1)) ]] && echo , )"
  done
  echo "  ],"
  echo "  \"advertencias\": ["
  for ((i = 0; i < ${#WARNINGS[@]}; i++)); do
    echo "    \"${WARNINGS[$i]}\"$( [[ $i -lt $((${#WARNINGS[@]} - 1)) ]] && echo , )"
  done
  echo "  ]"
  echo "}"
} > "$REPORT_FILE"

echo "Resultado en $REPORT_FILE"

