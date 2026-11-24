from dataclasses import dataclass, field


@dataclass
class Job:
    name: str
    duration_min: int
    resource_cost: int
    depends_on: list[str] = field(default_factory=list)