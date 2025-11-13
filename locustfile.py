from locust import HttpUser, task, between
import io

class FileStorageUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def health(self):
        self.client.get("/health")

    @task(3)
    def list_files(self):
        self.client.get("/files")

    @task(5)
    def upload_file(self):
        files = {"file": ("locust.txt", io.BytesIO(b"locust load test"), "text/plain")}
        self.client.post("/files", files=files)
