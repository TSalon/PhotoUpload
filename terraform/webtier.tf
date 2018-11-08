resource "aws_iam_role" "webtier-role" {
    name = "webtier-role"
    assume_role_policy = "${file("assume-role-policy.json")}"
}

resource "aws_iam_instance_profile" "webtier-profile" {
    name = "webtier-profile"
    role = "${aws_iam_role.webtier-role.name}"
}

data "template_file" "pgpass" {
    template = "$${pg_host}:$${pg_port}:$${pg_dbname}:$${pg_username}:$${pg_password}"

    vars {
        pg_host = "${aws_db_instance.tsalon-db.address}"
        pg_port = "${aws_db_instance.tsalon-db.port}"
        pg_dbname = "${aws_db_instance.tsalon-db.name}"
        pg_username = "tsalonadmin"
        pg_password = "${var.db_password_admin}"
    }
}

data "template_file" "bootstrap-web" {
    template = "${file("bootstrap-web.tpl")}" 
    vars {
        username = "tsalon"
        password = "${var.web_ssh_password}"
    }
}

data "template_file" "bootstrap-tsalon" {
    template = "${file("bootstrap-tsalon.tpl")}" 
    vars {
        
    }
}

data "template_file" "django-settings-live" {
    template = "${file("settings-live.tpl.py")}" 
    vars {
        dbHost = "${aws_db_instance.tsalon-db.address}"
        dbPasswordTSalon = "${var.db_password_tsalon}"
        djangoSecretKey = "${var.django_secret_key}"
	    region = "${var.region}"
    }
}

resource "aws_instance" "tsalon-web" {
    ami = "${lookup(var.ec2ami, var.region)}"
    instance_type = "t2.micro"
    key_name = "${lookup(var.keypair, var.region)}"
    private_ip = "10.0.7.7"
    iam_instance_profile = "${aws_iam_instance_profile.webtier-profile.name}"
      
    tags {
        Name = "tsalon-web"    
    }

    provisioner "file" {
        source = "../web/scripts/"
        destination = "/home/admin"
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "admin"
        }  
    }

    provisioner "file" {
        content = "${data.template_file.bootstrap-web.rendered}"
        destination = "bootstrap-web.sh"
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "admin"
        }  
    }

    provisioner "remote-exec" {
        inline = [
            "chmod a+x bootstrap-web.sh",
            "./bootstrap-web.sh",
        ]
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "admin"
        }  
    }
    
    provisioner "file" {
        content = "${data.template_file.pgpass.rendered}"
        destination = ".pgpass"
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "tsalon"
        }  
    }

    provisioner "file" {
        content = "${data.template_file.bootstrap-tsalon.rendered}"
        destination = "bootstrap-tsalon.sh"
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "tsalon"
        }  
    }

    provisioner "remote-exec" {
        inline = [
            "chmod a+x bootstrap-tsalon.sh",
            "./bootstrap-tsalon.sh",
        ]
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "tsalon"
        }  
    }

        provisioner "file" {
        content = "${data.template_file.django-settings-live.rendered}"
        destination = "~/tsalon/web/site/tsalon/settingslive.py"
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "tsalon"
        }  
    }

    provisioner "remote-exec" {
        inline = [
            "sudo /etc/init.d/gu-tsalon stop",
            "sudo /etc/init.d/gu-tsalon start",
        ]
        connection {
            type = "ssh"
            agent = false
            private_key = "${file("${var.ec2_private_key}")}"
            user = "admin"
        }  
    }

}

resource "aws_eip" "web-tier-ip-address" {
    vpc = true
    associate_with_private_ip = "10.0.7.7"
}

resource "aws_eip_association" "eip-web-association" {
    instance_id = "${aws_instance.tsalon-web.id}"
    allocation_id = "${aws_eip.web-tier-ip-address.id}"
} 