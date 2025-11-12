"""
Folder Structure Extension - Generate project folder structures
Uses: core.asset_io, core.asset_entity
"""

from pathlib import Path
from typing import Dict, List, Optional
from agency_core import asset_entity, asset_io, job_identity


# Predefined folder structures
FOLDER_STRUCTURES = {
    "agency_standard": {
        "name": "Agency Standard",
        "structure": [
            "01_brief",
            "02_research",
            "03_concepts",
            "04_design",
            "05_final_delivery",
            "06_assets",
            "06_assets/logos",
            "06_assets/images",
            "06_assets/fonts",
            "07_archive",
        ]
    },
    "social_media": {
        "name": "Social Media Campaign",
        "structure": [
            "01_brief_strategy",
            "02_content_calendar",
            "03_graphics",
            "03_graphics/posts",
            "03_graphics/stories",
            "03_graphics/ads",
            "04_copy",
            "05_final_exports",
            "06_analytics",
        ]
    },
    "web_project": {
        "name": "Web Project",
        "structure": [
            "01_brief",
            "02_research_ux",
            "03_wireframes",
            "04_design_mockups",
            "05_assets",
            "05_assets/images",
            "05_assets/icons",
            "05_assets/fonts",
            "06_development_handoff",
            "07_final_delivery",
        ]
    },
    "branding": {
        "name": "Branding Project",
        "structure": [
            "01_brief_research",
            "02_moodboards",
            "03_concepts",
            "04_logo_design",
            "05_brand_guidelines",
            "06_applications",
            "06_applications/business_cards",
            "06_applications/letterhead",
            "06_applications/social_media",
            "07_final_delivery",
        ]
    }
}


def generate_folder_structure(
    project_name: str,
    structure_type: str = "agency_standard",
    base_path: Optional[Path] = None,
    create_readme: bool = True
) -> asset_entity.Asset:
    """
    Generate a folder structure for a project.

    Args:
        project_name: Name of the project (will be root folder)
        structure_type: Type of structure (agency_standard, social_media, web_project, branding)
        base_path: Base path where to create the structure
        create_readme: Whether to create README.md in root

    Returns:
        Asset entity representing the folder structure
    """
    # Create job for tracking
    job = job_identity.create_job(
        name="folder_structure_generation",
        params={
            "project_name": project_name,
            "structure_type": structure_type
        }
    )

    try:
        # Get structure definition
        if structure_type not in FOLDER_STRUCTURES:
            raise ValueError(
                f"Unknown structure type: {structure_type}. "
                f"Available: {', '.join(FOLDER_STRUCTURES.keys())}"
            )

        structure_def = FOLDER_STRUCTURES[structure_type]

        # Create asset entity
        structure_asset = asset_entity.create_asset(
            "folder_structure",
            {
                "project_name": project_name,
                "structure_type": structure_type,
                "folders": structure_def['structure']
            }
        )

        # Create folders if base_path provided
        if base_path:
            base_path = Path(base_path)
            project_root = base_path / project_name.replace(' ', '_')

            created_folders = []
            for folder in structure_def['structure']:
                folder_path = project_root / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                created_folders.append(str(folder_path))

            # Create README if requested
            if create_readme:
                readme_content = f"""# {project_name}

Project Type: **{structure_def['name']}**

## Folder Structure

"""
                for folder in structure_def['structure']:
                    indent = "  " * (folder.count('/'))
                    folder_name = folder.split('/')[-1]
                    readme_content += f"{indent}- `{folder_name}/`\n"

                readme_content += """
## Usage

This folder structure follows agency best practices for organized project management.

- Keep all project files organized in their respective folders
- Use clear naming conventions for files
- Archive old versions in the `archive` folder
"""

                readme_path = project_root / "README.md"
                asset_io.write_file(readme_path, readme_content)

            structure_asset.metadata['created_folders'] = created_folders
            structure_asset.metadata['project_root'] = str(project_root)

        # Log success
        job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"asset_id": structure_asset.id}
        )

        return structure_asset

    except Exception as e:
        job_identity.log_job_execution(
            job.id,
            status="failed",
            error=str(e)
        )
        raise


def list_available_structures() -> Dict[str, str]:
    """List all available folder structure types."""
    return {key: val['name'] for key, val in FOLDER_STRUCTURES.items()}


def generate_custom_structure(
    project_name: str,
    folders: List[str],
    base_path: Optional[Path] = None
) -> asset_entity.Asset:
    """
    Generate a custom folder structure.

    Args:
        project_name: Name of the project
        folders: List of folder paths (e.g., ["docs", "src/components", "tests"])
        base_path: Base path where to create the structure

    Returns:
        Asset entity representing the folder structure
    """
    job = job_identity.create_job(
        name="custom_folder_structure",
        params={"project_name": project_name, "folders": folders}
    )

    try:
        structure_asset = asset_entity.create_asset(
            "custom_folder_structure",
            {
                "project_name": project_name,
                "folders": folders
            }
        )

        if base_path:
            base_path = Path(base_path)
            project_root = base_path / project_name.replace(' ', '_')

            created_folders = []
            for folder in folders:
                folder_path = project_root / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                created_folders.append(str(folder_path))

            structure_asset.metadata['created_folders'] = created_folders
            structure_asset.metadata['project_root'] = str(project_root)

        job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"asset_id": structure_asset.id}
        )

        return structure_asset

    except Exception as e:
        job_identity.log_job_execution(
            job.id,
            status="failed",
            error=str(e)
        )
        raise
