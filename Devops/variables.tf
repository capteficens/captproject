variable "aws_region" {
  default = "us-east-1"
}

variable "availability_zone" {
  default = "us-east-1a"
}

variable "ami_id" {
  description = "AMI ID (Amazon Linux 2)"
  default     = "ami-0c02fb55956c7d316"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "SSH Key Pair Name"
  default     = "projectcapt" # Replace this with your actual key
}

