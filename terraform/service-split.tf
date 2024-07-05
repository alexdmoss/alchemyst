resource "google_cloud_run_v2_service" "frontend" {

  name     = "${var.app_name}-frontend"
  project  = var.gcp_project_id
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {

    containers {

      name = "frontend"
      image = var.frontend_image_tag
      # depends_on = ["backend"]

      ports {
        container_port = var.frontend_port
      }

      resources {
        startup_cpu_boost = true
        cpu_idle = true
      }

      startup_probe {
        initial_delay_seconds = 30
        timeout_seconds       = 1
        period_seconds        = 3
        failure_threshold     = 1
        http_get {
          path = "/health"
        }
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
      }

    }

    timeout = "10s"

    scaling {
      min_instance_count = 1
      max_instance_count = 2
    }

    service_account = data.google_service_account.runtime.email

  }

}

resource "google_cloud_run_v2_service" "backend" {

  name     = "${var.app_name}-backend"
  project  = var.gcp_project_id
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {

    containers {

      name = "backend"
      image = var.backend_image_tag

      ports {
        container_port = var.backend_port
      }

      env {
        name = "DATA_STORE_NAMESPACE"
        value = "Alchemyst"
      }

      env {
        name = "DATA_STORE_PROJECT"
        value = var.gcp_project_id
      }

      env {
        name = "GOOGLE_CLOUD_PROJECT"
        value = var.gcp_project_id
      }

      resources {
        startup_cpu_boost = true
        cpu_idle = true
      }

      startup_probe {
        initial_delay_seconds = 60
        timeout_seconds       = 10
        period_seconds        = 30
        failure_threshold     = 5
        http_get {
          path = "/health"
        }
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
      }

    }

    timeout = "10s"

    scaling {
      min_instance_count = 1
      max_instance_count = 2
    }

    service_account = data.google_service_account.runtime.email

  }

}

resource "google_cloud_run_v2_service_iam_member" "allow-public-access-frontend" {
  location = google_cloud_run_v2_service.frontend.location
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
