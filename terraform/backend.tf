terraform {
  backend "gcs" {
    bucket = "directed-bongo-452118-g3-tfstate"
    prefix = "terraform/state"
  }
}
