import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Esta función extrae los errores relacionados con etiquetas obligatorias de TFLint.
def get_tflint_tag_errors(tflint_file):
    tag_errors = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint["issues"]:
            if (
                "missing tag" in entry["message"]
                or "Attribute validation error for tag" in entry["message"]
            ):
                tag_errors.append(
                    {
                        "file": entry["range"]["filename"],
                        "line": entry["range"]["start"]["line"],
                        "message": entry["message"],
                    }
                )
    return tag_errors


# Esta función extrae los problemas de seguridad detectados por Bandit.
def get_bandit_issues(bandit_file, severity="HIGH"):
    issues = []

    with open(bandit_file) as f:
        json_bandit = json.load(f)
        for result in json_bandit.get("results", []):
            if isinstance(severity, list):
                if result["issue_severity"] in severity:
                    issues.append(
                        {
                            "file": result["filename"],
                            "line": result["line_number"],
                            "test_id": result["test_id"],
                            "issue_text": result["issue_text"],
                        }
                    )
            if result["issue_severity"] == severity:
                issues.append(
                    {
                        "file": result["filename"],
                        "line": result["line_number"],
                        "test_id": result["test_id"],
                        "issue_text": result["issue_text"],
                    }
                )
    return issues


# Esta función extrae los problemas de seguridad detectados por TFLint.
def get_tflint_issues(tflint_file):
    rules_violated = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint["issues"]:
            rule_info = entry.get("rule")
            if rule_info:
                rules_violated.append(
                    {
                        "file": entry["range"]["filename"],
                        "line": entry["range"]["start"]["line"],
                        "severity": rule_info.get("severity", "0"),
                        "message": entry["message"],
                        "rule_name": rule_info.get("name"),
                        "description": rule_info.get("description", "N/A"),
                        "link": rule_info.get("link", "N/A"),
                    }
                )
    return rules_violated


# Esta función extrae los problemas de Checkov relacionados con etiquetas obligatorias.
def get_checkov_missing_tags(findings_file):
    missing_tags_issues = []

    filter = (
        "mandatory tag"  
    )

    with open(findings_file) as f:
        json_checkov = json.load(f)
        failed_checks = json_checkov.get("results", {}).get("failed_checks", [])

        for entry in failed_checks:
            # Filtra solo los resultados correspondientes al ruleset personalizado
            if entry.get("check_id", "").startswith("CKV_CUSTOM"):
                missing_tags_issues.append({
                    "file": entry["file_path"],
                    "start_line": entry["file_line_range"][0],
                    "end_line": entry["file_line_range"][1],
                    "resource": entry["resource"],
                    "check_id": entry["check_id"],
                    "severity": entry["severity"],
                    "message": entry["check_name"],
                    "guideline": entry["guideline"]
                })
    
    return missing_tags_issues

# Esta función extrae los problemas detectados en la configuración de red simulada
def get_network_json_issues(network_report_file):
    network_issues = []

    with open(network_report_file) as f:
        report = json.load(f)

        # Procesar los errores reportados 
        for error in report.get("errores", []):
            network_issues.append({
                "file": report.get("archivo_analizado", "unknown"),
                "type": "error",
                "message": error
            })

        # Procesar las advertencias reportadas
        for warning in report.get("advertencias", []):
            network_issues.append({
                "file": report.get("archivo_analizado", "unknown"),
                "type": "warning",
                "message": warning
            })

    return network_issues

# Genera un informe de seguridad en formato Markdown.
def generate_security_report(
    bandit_issues, tflint_tag_issues, tflint_issues, checkov_missing_tags, network_json_issues, output_file
):
    with open(output_file, "w") as f:
        f.write("# Security Report\n\n")

        # Listar las vulnerabilidades Bandit
        f.write("### Bandit - Vulnerabilidades nivel ERROR\n\n")
        if not bandit_issues:
            f.write("No se encontraron vulnerabilidades de nivel high.\n")
        else:
            for issue in bandit_issues:
                f.write(
                    f"- **Archivo**: `{issue['file']}` - Linea: {issue['line']} - ID: `{issue['test_id']}`\n\n"
                )
                f.write(f"  - {issue['issue_text']}\n\n")
        
        # Listar las reglas violadas halladas con TFLint
        f.write("### TFLint - Reglas violadas\n\n")
        if not tflint_issues:
            f.write("No se encontraron reglas violadas en TFLint.\n\n")
        else:
            for rule in tflint_issues:
                f.write(
                    f"- **Archivo**: `{rule['file']}` - Linea: {rule['line']} - Severidad: `{rule['severity']}`\n"
                )
                f.write(f"  - **Regla**: `{rule['rule_name']}`\n")
                f.write(f"  - {rule['message']}\n")
                f.write(f"  - {rule['description']}\n")
                if rule["link"]:
                    f.write(f"  - [Ver mas]({rule['link']})\n")
                f.write("\n")
        
        # Listar específicamente los errores de tags obligatorios
        f.write("#### Errores de tags obligatorios\n\n")
        if not tflint_tag_issues:
            f.write("No se encontraron errores relacionados con tags obligatorios.\n\n")
        else:
            for error in tflint_tag_issues:
                f.write(f"- **Archivo**: `{error['file']}` - Linea: {error['line']}\n")
                f.write(f"  - {error['message']}\n\n")
        
        # Listar lo hallado con checkov
        f.write("## Checkov - Recursos sin etiquetas obligatorias\n\n")
        if not checkov_missing_tags:
            f.write(" No se encontraron recursos sin etiquetas obligatorias.\n\n")
        else:
            for entry in checkov_missing_tags:
                f.write(
                    f"- **Archivo**: `{entry['file']}` ({entry['start_line']} - {entry['end_line']})\n"
                )
                f.write(f"  - Recurso: `{entry['resource']}`\n")
                f.write(f"  - Severidad: `{entry['severity']}`\n")
                f.write(
                    f"  - Mensaje: {entry['message']} (Check: `{entry['check_id']}`)\n"
                )
                if entry["guideline"]:
                    f.write(f"  - [Guía]({entry['guideline']})\n")
                f.write("\n")

        # Listar los errores y advertencias hallados en la configuración de red
        f.write("### Configuracion de red local\n\n")
        if not network_json_issues:
            f.write(" No se detectaron problemas de configuración de red en network_config.json.\n\n")
        else:
            for issue in network_json_issues:
                f.write(f"- **Archivo**: `{issue['file']}` - Tipo: `{issue['type']}`\n")
                f.write(f"  - {issue['message']}\n\n")

def generate_security_dashboard(
    bandit_issues, tflint_tag_issues, tflint_issues, checkov_missing_tags, graphic_file
):
    enviroment = Environment(
        loader=FileSystemLoader("templates"), autoescape=select_autoescape()
    )
    template = enviroment.get_template("security_report_template.html")

    html_file = template.render(
        bandit_issues=bandit_issues,
        tflint_issues=tflint_issues,
        checkov_issues=checkov_missing_tags,
        tflint_tag_issues=tflint_tag_issues,
        svg_file=graphic_file,
    )

    output_file = "reports/dashboard.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_file)
    pass


if __name__ == "__main__":
    tflint_tag_issues = get_tflint_tag_errors("reports/tflint_iac.json")
    tflint_issues = get_tflint_issues("reports/tflint_iac.json")
    bandit_issues = get_bandit_issues("reports/bandit.json")
    checkov_missing_tags = get_checkov_missing_tags("reports/checkov.json")
    network_issues = get_network_json_issues("reports/network_validation_report.json")

    generate_security_report(
        bandit_issues,
        tflint_tag_issues,
        tflint_issues,
        checkov_missing_tags,
        network_issues,
        "reports/security_report.md",
    )

    generate_security_dashboard(
        bandit_issues, tflint_tag_issues, tflint_issues, 
        checkov_missing_tags, "summary_chart.svg"
    )