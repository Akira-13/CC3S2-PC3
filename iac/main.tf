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
