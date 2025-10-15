"""Data models for AI Project Orchestrator."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class Status(Enum):
    """Initiative validation status."""
    READY = "ready"
    BLOCKED = "blocked"
    WARNING = "warning"


@dataclass
class Initiative:
    """Represents an initiative with its metadata and status."""
    id: str
    name: str
    directory: Path
    status: Status
    task_count: int = 0
    completed_count: int = 0
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    summary_status: Optional[str] = None
    current_task: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    target_date: Optional[str] = None
    estimated_hours: Optional[int] = None

    @property
    def progress_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.task_count == 0:
            return 0.0
        return (self.completed_count / self.task_count) * 100

    @property
    def is_active(self) -> bool:
        """Check if initiative is actively being worked on."""
        return bool(self.started_at and not self.ended_at)

    @property
    def is_completed(self) -> bool:
        """Check if initiative is completed."""
        return bool(self.ended_at)

    @property
    def is_not_started(self) -> bool:
        """Check if initiative hasn't been started yet."""
        return not self.started_at and not self.ended_at

    @property
    def is_cancelled(self) -> bool:
        """Check if initiative is cancelled."""
        return "cancelled" in (self.summary_status or "").lower()


@dataclass
class Task:
    """Represents a task within an initiative."""
    id: str
    title: str
    status: str  # 'pending', 'in_progress', 'completed'
    group: int = 0
    description: str = ""
    dependencies: List[str] = field(default_factory=list)

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == 'completed'

    @property
    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == 'in_progress'

    @property
    def is_pending(self) -> bool:
        """Check if task is pending."""
        return self.status == 'pending'

