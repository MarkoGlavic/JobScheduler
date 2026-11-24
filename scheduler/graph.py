from scheduler.models import Job
from collections import defaultdict, deque 


class JobGraph:
    def __init__(self):
        self.jobs: dict[str, Job] = {}

    def add_job(self, job: Job) -> None:
        if job.name in self.jobs:
            raise ValueError("Job with name already exists")
        self.jobs[job.name] = job

    def validate(self) -> None:
        self.job_exists()
        self.topological_order()

    def job_exists(self) -> None:
        for job in self.jobs.values():
            for dep in job.depends_on:
                if dep not in self.jobs:
                    raise ValueError("Depending job doesnt exist")
        

    def topological_order(self) -> list[str]:
        self.job_exists()
        indegree = {name: len(job.depends_on) for name, job in self.jobs.items()}
        adj = defaultdict(list)
        for job in self.jobs.values():
            for dep in job.depends_on:
                adj[dep].append(job.name)

        q = deque(name for name, deg in indegree.items() if deg == 0)
        order = []

        while q:
            node = q.popleft()
            order.append(node)
            for nei in adj[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        if len(order) != len(self.jobs):
            raise ValueError("Cycle in graph")
        return order