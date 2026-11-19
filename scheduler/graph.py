from scheduler.models import Job
from collections import defaultdict, deque 


class JobGraph:
    def __init__(self):
        self.jobs: dict[str, Job] = {}

    def add_job(self, job: Job) -> None:
        self.jobs[job.name] = job

    def validate(self) -> None:
        self.job_exists()
        self.check_cycles()

    def job_exists(self) -> None:
        for job in self.jobs.values():
            for dep in job.depends_on:
                if dep not in self.jobs:
                    raise ValueError("Depending job doesnt exist")
        

    def check_cycles(self) -> None:
        indegree = {name: len(job.depends_on) for name, job in self.jobs.items()}
        adj = defaultdict(list)
        for job in self.jobs.values():
            for dep in job.depends_on:
                adj[dep].append(job.name)

        q = deque()
        for job in self.jobs.values():
            if len(job.depends_on) == 0:
                q.append(job.name)

        done = 0

        while q:
            node = q.popleft()
            done+=1

            for nei in adj[node]:
                indegree[nei] -=1
                if indegree[nei] == 0:
                    q.append(nei)

        if done != len(self.jobs):
            raise ValueError("Cycle in graph")


