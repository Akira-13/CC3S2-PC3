// CIDR block define el rango de direcciones IP de la red simulada
variable "cidr_block" {
  type        = string
  description = "CIDR block de la red dummy"
  default     = "10.0.0.0/16"
}

// Nombre lógico de la red simulada
variable "network_name" {
  type        = string
  description = "Nombre de la red dummy"
  default     = "dummy-network"
}

// Puerto de inicio permitido por la regla de red simulada
variable "from_port" {
  type        = number
  description = "Puerto de inicio"
  default     = 22
}

// Puerto final permitido 
variable "to_port" {
  type        = number
  description = "Puerto final"
  default     = 22
}

// Protocolo de red simulado
variable "protocol" {
  type        = string
  default     = "tcp"
}

// Lista de IPs permitidas por la regla de red
variable "allowed_ips" {
  type        = list(string)
  default     = ["0.0.0.0/0"]
}


// Nombre del archivo de salida donde se escribirá el JSON con esta configuración
variable "file_name" {
  type        = string
  description = "Nombre del archivo JSON que se va a generar"
  default     = "network_config.json"
}

// Sistema operativo del entorno donde se ejecuta Terraform
variable "os_type" {
  type    = string
  default = "windows" 
}
