variable "home_ip" {
    type = "string"
}
 
variable "work_ip" {
    type = "string"
}

variable "region" {
    type = "string"
    default = "eu-west-1"
}

variable "ec2ami" {
    type = "map"
    default = {
        "eu-west-2" = "ami-02d7859cef54f67bb"
    }
}

variable "keypair" {
    type = "map"
    default = {
        "eu-west-2" = "tsalon-ireland"
    }
}

variable "ec2_private_key" {
    type = "string"
}

variable "db_password_admin" {
    type = "string"
}

variable "db_password_tsalon" {
    type = "string"
}

variable "web_ssh_password" {
    type = "string"
}

variable "django_secret_key" {
    type = "string"
}