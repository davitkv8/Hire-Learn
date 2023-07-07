provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "example_vpc" {
  cidr_block = "10.0.0.0/16"
 tags = {
     Name = "example-vpc"
   }
}

resource "aws_internet_gateway" "example_igw" {
  vpc_id = aws_vpc.example_vpc.id

  tags = {
    Name = "example-igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.example_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.example_igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table_association" "public_subnet1" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet2" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet3" {
  subnet_id      = aws_subnet.subnet3.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_subnet" "subnet1" {
  vpc_id     = aws_vpc.example_vpc.id
  cidr_block = "10.0.1.0/24"

    tags = {
      Name = "subnet1"
    }
}

resource "aws_subnet" "subnet2" {
  vpc_id     = aws_vpc.example_vpc.id
  cidr_block = "10.0.2.0/24"

   tags = {
      Name = "subnet2"
    }
}

resource "aws_subnet" "subnet3" {
  vpc_id     = aws_vpc.example_vpc.id
  cidr_block = "10.0.3.0/24"

  tags = {
    Name = "subnet3"
  }
}

resource "aws_security_group" "traffic_sg" {
  name        = "traffic_sg"
  description = "traffic security group"
  vpc_id      = aws_vpc.example_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
      Name = "traffic-sg"
    }
}

resource "aws_eip" "dev_eip" {
  vpc      = true
  instance = aws_instance.dev.id
}

resource "aws_eip" "prod_eip" {
  vpc      = true
  instance = aws_instance.prod.id
}

resource "aws_eip" "staging_eip" {
  vpc      = true
  instance = aws_instance.staging.id
}

resource "aws_instance" "dev" {
  ami                    = "ami-06b09bfacae1453cb"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.subnet1.id
  vpc_security_group_ids = [aws_security_group.traffic_sg.id]
    associate_public_ip_address = true

    tags = {
      Name        = "dev-instance"
      Environment = "dev"
    }
}

resource "aws_instance" "prod" {
  ami                    = "ami-06b09bfacae1453cb"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.subnet2.id
  vpc_security_group_ids = [aws_security_group.traffic_sg.id]
    associate_public_ip_address = true

    tags = {
      Name        = "prod-instance"
      Environment = "prod"
    }

    user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install docker -y
              sudo yum install docker -y
              sudo usermod -a -G docker ec2-user
              sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              sudo systemctl start docker
              sudo yum install nginx
              sudo systemctl start nginx
              sudo systemctl enable nginx
              sudo yum install git -y
              docker login ghcr.io -u davitkv8 -p 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
              EOF

}

resource "aws_instance" "staging" {
  ami                    = "ami-06b09bfacae1453cb"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.subnet3.id
  vpc_security_group_ids = [aws_security_group.traffic_sg.id]
  associate_public_ip_address = true
   tags = {
      Name        = "staging-instance"
      Environment = "staging"
    }
}
variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"  # Update with your desired region if needed
}