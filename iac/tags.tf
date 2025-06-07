/*
Este archivo define las etiquetas que se asignan a los recursos Terraform 
*/

locals { 
    /*
    mandatory_tags agrupa las etiquetas obligatorias (Name, Owner, Env) 
    para asegurar que siempre existan en los recursos
    */
    mandatory_tags = { 
        Name = var.name, 
        Owner = var.owner, 
        Env = var.env 
    } 
}
