"""
Job Identity - Track job execution and identity
FROZEN MODULE - Pure stdlib
"""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class JobExecution:
    """Job execution log entry."""
    timestamp: datetime
    status: str  # started, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Job:
    """Job definition and tracking."""
    id: str
    name: str
    params: Dict[str, Any]
    created_at: datetime
    executions: List[JobExecution] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['created_at'] = self.created_at.isoformat()
        result['executions'] = [
            {
                'timestamp': e.timestamp.isoformat(),
                'status': e.status,
                'result': e.result,
                'error': e.error,
                'metadata': e.metadata
            }
            for e in self.executions
        ]
        return result


class JobRegistry:
    """Registry for jobs."""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def create(self, name: str, params: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Job:
        """Create a new job."""
        job = Job(
            id=str(uuid.uuid4()),
            name=name,
            params=params,
            created_at=datetime.utcnow(),
            metadata=metadata or {}
        )
        self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def log_execution(
        self,
        job_id: str,
        status: str,
        result: Optional[Any] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log a job execution."""
        job = self._jobs.get(job_id)
        if not job:
            return False

        execution = JobExecution(
            timestamp=datetime.utcnow(),
            status=status,
            result=result,
            error=error,
            metadata=metadata or {}
        )
        job.executions.append(execution)
        return True

    def list_all(self) -> List[Job]:
        """List all jobs."""
        return list(self._jobs.values())

    def list_by_name(self, name: str) -> List[Job]:
        """List jobs by name."""
        return [j for j in self._jobs.values() if j.name == name]


# Global registry
_registry = JobRegistry()


def create_job(name: str, params: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Job:
    """Create a new job."""
    return _registry.create(name, params, metadata)


def get_job(job_id: str) -> Optional[Job]:
    """Get job by ID."""
    return _registry.get(job_id)


def log_job_execution(
    job_id: str,
    status: str,
    result: Optional[Any] = None,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Log a job execution."""
    return _registry.log_execution(job_id, status, result, error, metadata)


def list_jobs(name: Optional[str] = None) -> List[Job]:
    """List all jobs, optionally filtered by name."""
    if name:
        return _registry.list_by_name(name)
    return _registry.list_all()
