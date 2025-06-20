# Recurso que genera un archivo de configuración de red JSON en sistemas Windows usando PowerShell
resource "null_resource" "generate_config_windows" {
  # Este recurso solo se crea si el valor de os_type es windows
  count = var.os_type == "windows" ? 1 : 0

  # Fuerza la ejecución del recurso en cada apply
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    # Comando PowerShell que genera un archivo json que contiene la configuración de la red
    command = "ConvertTo-Json @{network_name='${var.network_name}'; cidr_block='${var.cidr_block}'; from_port=${var.from_port}; to_port=${var.to_port}; protocol='${var.protocol}'; allowed_ips=@(${join(", ", formatlist("'%s'", var.allowed_ips))})} | Out-File -Encoding utf8 ${var.file_name}"
    interpreter = ["PowerShell", "-Command"]
  }
}

# Recurso que genera un archivo de configuración de red JSON en sistemas Linux usando Bash
resource "null_resource" "generate_config_linux" {
  # Este recurso solo se crea si el valor de os_type es linux
  count = var.os_type == "linux" ? 1 : 0

  # Fuerza la ejecución del recurso en cada apply
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    # Comando Bash que genera un archivo json que contiene la configuración de la red
    command = "echo '{\"network_name\": \"${var.network_name}\", \"cidr_block\": \"${var.cidr_block}\", \"from_port\": ${var.from_port}, \"to_port\": ${var.to_port}, \"protocol\": \"${var.protocol}\", \"allowed_ips\": ${jsonencode(var.allowed_ips)}}' > ${var.file_name}"
    interpreter = ["/bin/bash", "-c"]
  }
}
