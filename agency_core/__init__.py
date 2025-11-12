"""
Agency Core - Frozen Foundation
================================

8 stable modules that NEVER change:
- asset_io: File operations
- asset_storage: Key-value storage
- template_schema: Data structures
- asset_entity: CRUD operations
- content_transform: Data transformations
- workflow_process: Multi-step workflows
- rule_validation: Validation rules
- job_identity: Job tracking
"""

__version__ = "1.0.0"

from .asset_io import read_file, write_file, read_image, write_image, read_csv, write_pdf
from .asset_storage import store_asset, retrieve_asset, list_assets, delete_asset
from .template_schema import define_template, validate_template_data, get_template
from .asset_entity import create_asset, update_asset, get_asset, list_assets_by_type, delete_asset_entity
from .content_transform import define_transform, apply_transform, list_transforms
from .workflow_process import define_workflow, execute_workflow, get_workflow
from .rule_validation import define_rule, validate_asset, list_rules
from .job_identity import create_job, log_job_execution, get_job, list_jobs

__all__ = [
    # IO
    'read_file', 'write_file', 'read_image', 'write_image', 'read_csv', 'write_pdf',
    # Storage
    'store_asset', 'retrieve_asset', 'list_assets', 'delete_asset',
    # Schema
    'define_template', 'validate_template_data', 'get_template',
    # Entity
    'create_asset', 'update_asset', 'get_asset', 'list_assets_by_type', 'delete_asset_entity',
    # Transform
    'define_transform', 'apply_transform', 'list_transforms',
    # Process
    'define_workflow', 'execute_workflow', 'get_workflow',
    # Validation
    'define_rule', 'validate_asset', 'list_rules',
    # Identity
    'create_job', 'log_job_execution', 'get_job', 'list_jobs',
]
