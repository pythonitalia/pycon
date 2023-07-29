locals {
  is_prod                = terraform.workspace == "production"
  db_connection_pycon_be = var.enable_proxy ? "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_proxy.proxy[0].endpoint}:${data.aws_db_instance.database.port}/pycon" : "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/pycon"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

data "aws_db_proxy" "proxy" {
  count = var.enable_proxy ? 1 : 0
  name  = "pythonit-${terraform.workspace}-database-proxy"
}

data "aws_elasticache_cluster" "redis" {
  cluster_id = "production-pretix"
}

resource "aws_ecs_cluster" "temporal" {
  name = "${terraform.workspace}-temporal"
}

data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.temporal.name
  }
}

data "aws_iam_instance_profile" "instance" {
  name = "${terraform.workspace}-pretix-instance-profile"
}

resource "aws_instance" "temporal" {
  ami               = "ami-0d24d62eae192fc54"
  instance_type     = "t3.small"
  subnet_id         = data.aws_subnet.private.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.instance.id,
    data.aws_security_group.rds.id
  ]
  source_dest_check    = false
  user_data            = data.template_file.user_data.rendered
  iam_instance_profile = data.aws_iam_instance_profile.instance.name
  key_name             = "pretix"

  tags = {
    Name = "${terraform.workspace}-temporal-instance"
  }

  root_block_device {
    volume_size = 30
  }
}


resource "aws_ecs_task_definition" "temporal_service" {
  family = "${terraform.workspace}-temporal"
  container_definitions = jsonencode([
    {
      name      = "temporal"
      image     = "temporalio/auto-setup:1.21.2.0"
      cpu       = 512
      memory    = 512
      essential = true
      environment = [
        {
          name  = "DB"
          value = "postgres"
        },
        {
          name  = "DB_PORT",
          value = "5432"
        },
        {
          name  = "POSTGRES_USER"
          value = data.aws_db_instance.database.master_username
        },
        {
          name  = "POSTGRES_PWD"
          value = module.common_secrets.value.database_password
        },
        {
          name  = "POSTGRES_DB"
          value = "temporal"
        },
        {
          name  = "POSTGRES_SEEDS"
          value = var.enable_proxy ? data.aws_db_proxy.proxy[0].endpoint : data.aws_db_instance.database.address
        },
      ]
      portMappings = [
        {
          containerPort = 7233
          hostPort      = 7233
          protocol      = "tcp"
        }
      ]
      mountPoints    = []
      systemControls = []
    },
    {
      name   = "temporal-ui",
      image  = "temporalio/ui:2.16.2"
      cpu    = 512
      memory = 512
      environment = [
        {
          name  = "TEMPORAL_ADDRESS",
          value = "172.17.0.1:7233"
        }
      ],
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
          protocol      = "tcp"
        }
      ]
    },
    # {
    #   name   = "pycon-backend-worker",
    #   cpu    = 512
    #   memory = 512
    #   image  = local.pycon_be_image_uri
    #   environment = [
    #     {
    #       name  = "DJANGO_SETTINGS_MODULE",
    #       value = "pycon.settings.prod"
    #     },
    #     {
    #       name  = "TEMPORAL_ADDRESS",
    #       value = "172.17.0.1:7233"
    #     },
    #     {
    #       name  = "DATABASE_URL"
    #       value = local.db_connection_pycon_be
    #     },
    #     {
    #       name = "DEBUG",
    #       value = "False"
    #     },
    #     {
    #       name = "SECRET_KEY",
    #       value = module.pycon_be_secrets.value.secret_key
    #     },
    #     {
    #       name = "CACHE_URL",
    #       value = local.is_prod ? "redis://${data.aws_elasticache_cluster.redis.cache_nodes.0.address}/8" : "locmemcache://snowflake"
    #     }
    #   ]
    # }
  ])

  requires_compatibilities = []
  tags                     = {}
}


resource "aws_ecs_service" "temporal" {
  name                               = "${terraform.workspace}-temporal-service"
  cluster                            = aws_ecs_cluster.temporal.id
  task_definition                    = aws_ecs_task_definition.temporal_service.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
