import os
import json
import matplotlib.pyplot as plt


# Extractores específicos
# Se evita hardcodear a la lógica principal
def extract_bandit_issues(data):
    return len(data.get("results", []))


def extract_checkov_issues(data):
    return len(data.get("results", {}).get("failed_checks", []))


def extract_shellcheck_issues(data):
    return len(data.get("comments", []))


def extract_tflint_issues(data):
    return len(data.get("issues", []))


TOOLS = {
    "Bandit": ("bandit.json", extract_bandit_issues),
    "Checkov": ("checkov.json", extract_checkov_issues),
    "Shellcheck": ("shellcheck.json", extract_shellcheck_issues),
    "TFLint": ("tflint_iac.json", extract_tflint_issues),
}


# Funcion para generar reportes
# Se separan las herramientas del generador del grafico para separar responsabilidades
def generate_security_report_chart(
    output_path="reports/summary_chart.svg", report_dir="reports/"
):
    issue_counts = {}

    for tool_name, (filename, extractor) in TOOLS.items():
        file_path = os.path.join(report_dir, filename)

        # Si la herramienta no existe, se omite
        if not os.path.exists(file_path):
            continue

        with open(file_path, "r") as file:
            data = json.load(file)

        # Estraer errores
        try:
            issue_counts[tool_name] = extractor(data)
        except Exception as e:
            print(f"No se pudo extraer errores de {tool_name}: {e}")

    if not issue_counts:
        return

    # Hacer gráfico tarta/pie
    labels = list(issue_counts.keys())
    sizes = list(issue_counts.values())

    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.savefig(output_path, format='svg')


generate_security_report_chart()
