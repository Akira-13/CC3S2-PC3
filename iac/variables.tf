/*
Este archivo define las variables necesarias para los recursos Terraform,  
contiene variables para el nombre, dueño y entorno del recurso
*/
variable "name" {
    type = string
    description = "Nombre del recurso"
    default = "dummy-resource"
}

variable "owner" {
    type = string
    description = "Dueño del recurso"
    default = "admin"
}

variable "env" {
    type = string
    description = "Entorno del recurso"
    default = "dev"
}