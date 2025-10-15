"""AI Project Orchestrator (AIPO) - Modular CLI Tool.

Validates swarm configurations and initiative readiness.
Provides modular commands for project management.
"""

__version__ = "2.1.0"

from .models import Initiative, Status, Task
from .core import validate_initiative, get_all_initiatives, categorize_initiatives
from .utils import Colors, create_progress_bar, extract_tasks

__all__ = [
    'Initiative',
    'Status',
    'Task',
    'validate_initiative',
    'get_all_initiatives',
    'categorize_initiatives',
    'Colors',
    'create_progress_bar',
    'extract_tasks',
]

