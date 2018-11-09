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

variable "zones" {
    type = "map"
    default = {
      "eu-west-1" = "eu-west-1a"
    }
}

variable "zones_secondary" {
    type = "map"
    default = {
      "eu-west-1" = "eu-west-1b"
    }
}

variable "ec2ami" {
    type = "map"
    default = {
        "eu-west-1" = "ami-05cdaf7e7b6c76277"
    }
}

variable "keypair" {
    type = "map"
    default = {
        "eu-west-1" = "tsalon-ireland"
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