/*
Este archivo crea 3 recursos dummy usando el recurso null_resource,
cada recurso incluye las etiquetas obligatorias definidas en mandatory_tags
*/

resource "null_resource" "dummy1" {
  # Asigna las etiquetas obligatorias como triggers del recurso
  triggers = local.mandatory_tags
}

resource "null_resource" "dummy2" {
  triggers = local.mandatory_tags
}

resource "null_resource" "dummy3" {
  triggers = local.mandatory_tags
}

# Recurso dummy temporal que se excluye del chequeo de etiquetas obligatorias y formato

resource "null_resource" "dummy_temp" {
  #checkov:skip=CKV_CUSTOM_1:Recurso temporal sin etiquetas completas
  #checkov:skip=CKV_CUSTOM_2:Recurso de prueba sin necesidad de etiquetas formateadas
  triggers = {
    Owner = "Ariana-Lopez"
    Env  = "dev"
  }
}

# Recurso dummy con etiquetas mal formateadas que se excluye solo del chequeo de formato

resource "null_resource" "dummy_invalid_format" {
  #checkov:skip=CKV_CUSTOM_2:Recurso de prueba sin necesidad de etiquetas formateadas
  triggers = {
    Name  = "InvalidDummy!"   
    Owner = "ArianaLopez"       
    Env   = "DEV"                
  }
}

# Módulo que simula una configuración de red y genera un archivo JSON con sus valores
module "network_dummy" {
  source        = "./network_dummy"

  # Nombre lógico de la red simulada
  network_name  = "test-network"

  # Rango CIDR asignado a la red
  cidr_block    = "10.0.0.0/16"

  # Puerto abierto para simular acceso
  from_port     = 22
  to_port       = 22

  # Nombre del archivo JSON que se generará
  file_name     = "network_config.json"

  # Tipo de sistema operativo para determinar el comando correcto
  os_type = var.os_type
}
