import json

def get_tflint_tag_errors(tflint_file):
    tag_errors = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint:
            if entry["type"] == "ERROR" and ("missing tag" in entry["message"] or "Attribute validation error for tag" in entry["message"]):
                tag_errors.append({
                    "file": entry["range"]["filename"],
                    "line": entry["range"]["start"]["line"],
                    "message": entry["message"]
                })

    return tag_errors

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

def get_tflint_issues(tflint_file):
    rules_violated = []

    with open(tflint_file) as f:
        json_tflint = json.load(f)
        for entry in json_tflint:
            rule_info = entry.get("rule")
            if rule_info:
                rules_violated.append({
                    "file": entry["range"]["filename"],
                    "line": entry["range"]["start"]["line"],
                    "severity": entry["type"],
                    "message": entry["message"],
                    "rule_name": rule_info.get("name"),
                    "description": rule_info.get("description"),
                    "link": rule_info.get("link")
                })

    return rules_violated

def get_checkov_missing_tags(findings_file):
    missing_tags_issues = []
    filter = "mandatory tag" # Esto puede ser cambiado en futuras versiones, dependiendo del sprint 2.
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

if __name__ == "__main__":
    tflint_tag_issues = get_tflint_tag_errors("reports/tflint.json")
    tflint_issues = get_tflint_issues("reports/tflint.json")
    bandit_issues = get_bandit_issues("reports/bandit.json")
    #checkov_missing_tags = get_checkov_missing_tags("reports/checkov.json")





