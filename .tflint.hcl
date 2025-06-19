# Plugin nativo de Terraform activado
plugin "terraform" {
  enabled = true
}

# Plugin personalizado activado
# Este plugin verifica que los tags sigan un determinado formato regex
plugin "tflint-ruleset" {
  enabled = true
  version = "0.1.0"
  source = "github.com/aclj20/tflint-tag-format-validator"
}


# Reglas del plugin nativo habilitadas

# Regla que verifica que se declare la versión requerida de Terraform
rule "terraform_required_version" {
  enabled = true
}

# Regla que verifica que se declare el bloque required_providers
rule "terraform_required_providers" {
  enabled = true
}




