from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5) 

    @task
    def view_matches(self):
        self.client.get("/index")