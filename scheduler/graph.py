from scheduler.models import Job

class JobGraph:
    def __init__(self):
        self.jobs: dict[str, Job] = {}

    def add_job(self, job: Job) -> None:
        self.jobs[job.name] = job

    