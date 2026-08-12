variable "project_id" {
  type        = string
  description = "directed-bongo-452118-g3"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "zone" {
  type        = string
  default     = "us-central1-b"
}

variable "machine_type" {
  type        = string
  default     = "c4-highcpu-2" 
}