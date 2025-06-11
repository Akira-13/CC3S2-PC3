import json

# Esta función extrae los errores relacionados con etiquetas obligatorias de TFLint.
def get_tflint_tag_errors(tflint_file):
    tag_errors = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint["issues"]:  
            if "missing tag" in entry["message"] or "Attribute validation error for tag" in entry["message"]:
                tag_errors.append({
                    "file": entry["range"]["filename"],
                    "line": entry["range"]["start"]["line"],
                    "message": entry["message"]
                })

    return tag_errors

# Esta función extrae los problemas de seguridad detectados por Bandit.
def get_bandit_issues(bandit_file, severity = "HIGH"):
    issues = []
  
    with open(bandit_file) as f:
        json_bandit = json.load(f)
        for result in json_bandit.get("results", []):
            if isinstance(severity, list):
                if result["issue_severity"] in severity:
                    issues.append({
                        "file": result["filename"],
                        "line": result["line_number"],
                        "test_id": result["test_id"],
                        "issue_text": result["issue_text"]
                    })
            if result["issue_severity"] == severity:
                issues.append({
                    "file": result["filename"],
                    "line": result["line_number"],
                    "test_id": result["test_id"],
                    "issue_text": result["issue_text"]
                })

    return issues

# Esta función extrae los problemas de seguridad detectados por TFLint.
def get_tflint_issues(tflint_file):
    rules_violated = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint["issues"]:
            rule_info = entry.get("rule")
            if rule_info:
                rules_violated.append({
                    "file": entry["range"]["filename"],
                    "line": entry["range"]["start"]["line"],
                    "severity": rule_info.get("severity", "0"), 
                    "message": entry["message"],
                    "rule_name": rule_info.get("name"),
                    "description": rule_info.get("description", "N/A"),  
                    "link": rule_info.get("link", "N/A")  
                })

    return rules_violated

# Esta función extrae los problemas de Checkov relacionados con etiquetas obligatorias.
# El filtro cambiará en el sprint 2.
def get_checkov_missing_tags(findings_file):
    missing_tags_issues = []
    filter = "mandatory tag" # TODO cambiar cuando se implemente el ruleset en el sprint 2
    with open(findings_file) as f:
        json_checkov = json.load(f)
        failed_checks = json_checkov.get("results", {}).get("failed_checks", [])

        for entry in failed_checks:
            if filter in entry.get("check_name", "").lower():
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

# Genera un informe de seguridad en formato Markdown.
def generar_security_report(bandit_issues, tflint_tag_issues, tflint_issues, checkov_missing_tags, output_file):
    with open(output_file, 'w') as f:
        f.write("# Security Report\n\n")

        # Listar las vulnerabilidades Bandit
        f.write("### Bandit - Vulnerabilidades nivel ERROR\n\n")
        if not bandit_issues:
            f.write("No se encontraron vulnerabilidades de nivel high.\n")
        else:
            for issue in bandit_issues:
                f.write(f"- **Archivo**: `{issue['file']}` - Linea: {issue['line']} - ID: `{issue['test_id']}`\n\n")
                f.write(f"  - {issue['issue_text']}\n\n")

        # Listar las reglas violadas halladas con TFLint
        f.write("### TFLint - Reglas violadas\n\n")
        if not tflint_issues:
            f.write("No se encontraron reglas violadas en TFLint.\n\n")
        else:
            for rule in tflint_issues:
                f.write(f"- **Archivo**: `{rule['file']}` - Linea: {rule['line']} - Severidad: `{rule['severity']}`\n")
                f.write(f"  - **Regla**: `{rule['rule_name']}`\n")
                f.write(f"  - {rule['message']}\n")
                f.write(f"  - {rule['description']}\n")
                if rule['link']:
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

        #Listar lo hallado con checkov
        f.write("## Checkov - Recursos sin etiquetas obligatorias\n\n")
        if not checkov_missing_tags:
            f.write(" No se encontraron recursos sin etiquetas obligatorias.\n\n")
        else:
            for entry in checkov_missing_tags:
                f.write(f"- **Archivo**: `{entry['file']}` ({entry['start_line']} - {entry['end_line']})\n")
                f.write(f"  - Recurso: `{entry['resource']}`\n")
                f.write(f"  - Severidad: `{entry['severity']}`\n")
                f.write(f"  - Mensaje: {entry['message']} (Check: `{entry['check_id']}`)\n")
                if entry['guideline']:
                    f.write(f"  - [Guía]({entry['guideline']})\n")
                f.write("\n")


if __name__ == "__main__":
    tflint_tag_issues = get_tflint_tag_errors("reports/tflint_iac.json")
    tflint_issues = get_tflint_issues("reports/tflint_iac.json")
    bandit_issues = get_bandit_issues("reports/bandit.json")
    checkov_missing_tags = get_checkov_missing_tags("reports/checkov.json")

    generar_security_report(
        bandit_issues,
        tflint_tag_issues,
        tflint_issues,
        checkov_missing_tags,
        "reports/security_report.md"
    )
