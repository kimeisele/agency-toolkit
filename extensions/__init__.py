"""
Extensions - Domain-specific logic built on agency_core
======================================================

Extensions can change, iterate, and evolve.
They use the frozen core modules as building blocks.
"""

__version__ = "1.0.0"

from .social_posts import generate_social_post, batch_generate_social_posts
from .briefing_generator import generate_briefing, BriefingData
from .folder_structure import generate_folder_structure
from .batch_processor import process_csv_workflow

__all__ = [
    'generate_social_post',
    'batch_generate_social_posts',
    'generate_briefing',
    'BriefingData',
    'generate_folder_structure',
    'process_csv_workflow',
]
