resource "aws_db_instance" "tsalon-db" {
    allocated_storage = 20
    allow_major_version_upgrade = false
    apply_immediately = true
    auto_minor_version_upgrade = true
    backup_retention_period = 7
    backup_window = "05:37-06:37"
    storage_type = "gp2"
    engine = "postgres"
    engine_version = "10.3"
    final_snapshot_identifier = "tsalon-snapshot-final"
    identifier = "tsalon-db"
    instance_class = "db.t2.micro"
    name = "tsalon"
    username = "tsalonadmin"
    password = "${var.db_password_admin}"
    publicly_accessible = false
    multi_az = false
    skip_final_snapshot = false
}