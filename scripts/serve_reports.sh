#!/usr/bin/env bash
# Lanza un servidor HTTP local para visualizar los reportes de seguridad y abre el navegador en la vista principal.
# Los reportes de seguridad son generados por src/security_checker.py

set -e

# Asegurarse de estar en la raíz del proyecto
cd "$(git rev-parse --show-toplevel)"

REPORT_DIR="reports"
REPORT_FILE="dashboard.html"
PORT=8000
URL="http://localhost:${PORT}/${REPORT_FILE}"

# Verificar si el archivo a servir existe
if [ ! -f "${REPORT_DIR}/${REPORT_FILE}" ]; then
    echo "! No se encontró ${REPORT_DIR}/${REPORT_FILE}. Asegúrate de haber generado el reporte."
    exit 1
fi

echo "Sirviendo directorio ${REPORT_DIR} en http://localhost:${PORT}/"
echo "Abriendo navegador en ${URL}"

# Abrir navegador si se detecta entorno gráfico
if command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open "$URL" >/dev/null 2>&1 &
elif command -v start >/dev/null 2>&1; then
    # Windows
    start "$URL"
else
    echo "! No se detectó navegador gráfico. Puedes abrir manualmente: $URL"
fi

# Lanzar servidor HTTP
cd "$REPORT_DIR"
if command -v python3 >/dev/null 2>&1; then
    # Prioridad a python3
    python3 -m http.server "$PORT"
elif command -v python >/dev/null 2>&1; then
    # python en su defecto
    python -m SimpleHTTPServer "$PORT"
else
    echo "! No se encontró ni python3 ni python. Instala Python para servir los reportes."
    exit 1
fi
