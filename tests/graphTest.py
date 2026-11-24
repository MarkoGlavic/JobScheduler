import pytest
from scheduler.graph import JobGraph
from scheduler.models import Job

def test_cycle():
    g = JobGraph()
    g.add_job(Job("a", 5, 1, depends_on=["b"]))
    g.add_job(Job("b", 5, 1, depends_on=["a"]))
    with pytest.raises(ValueError, match = "Cycle in graph"):
        g.validate()

def test_duplicate():
    g = JobGraph()
    g.add_job(Job("a", 5, 1, depends_on=["b"]))
    with pytest.raises(ValueError, match ="Job with name already exists"):
        g.add_job(Job("a", 5, 1, depends_on=["b"]))




def test_missing_dependency():
    g = JobGraph()
    g.add_job(Job("a", 5, 1, depends_on=["fsdaiohfdaoiu"]))
    with pytest.raises(ValueError, match="Depending job doesnt exist"):
        g.validate()

def test_diamond_is_valid():
    g = JobGraph()
    g.add_job(Job("a", 5, 1))
    g.add_job(Job("b", 5, 1, depends_on=["a"]))
    g.add_job(Job("c", 5, 1, depends_on=["a"]))
    g.add_job(Job("d", 5, 1, depends_on=["b", "c"]))
    g.validate() 

def test_order_is_valid():
    g = JobGraph()
    g.add_job(Job("a", 5, 1))
    g.add_job(Job("b", 5, 1, depends_on=["a"]))
    g.add_job(Job("c", 5, 1, depends_on=["a"]))
    g.add_job(Job("d", 5, 1, depends_on=["b", "c"]))

    order = g.topological_order()

    assert sorted(order) == ["a", "b", "c", "d"]
    pos = {name: i for i, name in enumerate(order)}
    for job in g.jobs.values():
        for dep in job.depends_on:
            assert pos[dep] < pos[job.name]

def test_order_raises_on_cycle():
    g = JobGraph()
    g.add_job(Job("a", 5, 1, depends_on=["b"]))
    g.add_job(Job("b", 5, 1, depends_on=["a"]))
    with pytest.raises(ValueError, match="Cycle in graph"):
        g.topological_order()