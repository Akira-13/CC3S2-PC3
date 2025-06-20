import subprocess
import os
import re
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CURRENT_REPORT = "reports/scheduled_reports/security_report_scheduled.md"
PREVIOUS_REPORT = "reports/scheduled_reports/prev_security_report_scheduled.md"


def run_scans():
    # Ejecutar run_all_scans.sh
    print("Ejecutando escaneos...")
    subprocess.run(
        ["bash", "scripts/run_all_scans_scheduled.sh"],
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
        check=True,
    )


def count_vulnerabilities(report_path):
    # Contar las lineas que empiecen con "- **Archivo**"
    if not os.path.exists(report_path):
        return 0

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Contar líneas que representen hallazgos
    return len(re.findall(r"^- \*\*Archivo\*\*", content, re.MULTILINE))


def notify_difference(prev, current):
    # Compara número de vulnerabilidades e imprime resultado.
    print(f"Vulnerabilidades anteriores: {prev}")
    print(f"Vulnerabilidades actuales: {current}")

    if current > prev:
        print("! Aumentó el número de vulnerabilidades !")
    elif current < prev:
        print("Disminuyó el número de vulnerabilidades.")
    else:
        print("No hubo cambios en el número de vulnerabilidades.")


def main():
    if os.path.exists(CURRENT_REPORT):
        print("Encontrado reporte previo. Guardando copia como reporte anterior...")
        os.replace(CURRENT_REPORT, PREVIOUS_REPORT)
    else:
        # En caso no exista reporte, se limita a generarlo
        print(
            "No se encontró un reporte previo. Se generará uno nuevo por primera vez."
        )

    run_scans()

    if os.path.exists(PREVIOUS_REPORT):
        # Compara número de vulnerabalidades entre reporte antiguo y nuevo
        previous = count_vulnerabilities(PREVIOUS_REPORT)
        current = count_vulnerabilities(CURRENT_REPORT)
        notify_difference(previous, current)
    else:
        print("Reporte generado por primera vez. No hay comparación previa.")
        print(
            "Ejecuta este script o espera a siguiente ejecución para realizar comparación."
        )


if __name__ == "__main__":
    main()

    print("\nPara programar este script diariamente con cron, ejecuta:")
    print("crontab -e")
    print("Y añade una línea como esta:")
    print(f"0 9 * * * /usr/bin/python3 {os.path.abspath(__file__)}")
    print("Esto ejecuta el script a las 9000 horas todos los días.")
