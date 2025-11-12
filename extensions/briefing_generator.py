"""
Briefing Generator Extension - Generate project briefings
Uses: core.asset_entity, core.content_transform, core.asset_io
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional
from agency_core import asset_entity, asset_io, content_transform, job_identity, template_schema


@dataclass
class BriefingData:
    """Data structure for project briefing."""
    client_name: str
    project_name: str
    project_type: str
    goals: List[str]
    target_audience: str
    timeline: str
    budget: str
    deliverables: List[str]
    additional_notes: str = ""


def setup_briefing_template():
    """Define briefing template."""
    template_schema.define_template(
        name="project_briefing",
        fields=[
            {"name": "client_name", "type": str, "required": True},
            {"name": "project_name", "type": str, "required": True},
            {"name": "project_type", "type": str, "required": True},
            {"name": "goals", "type": list, "required": True},
            {"name": "target_audience", "type": str, "required": True},
            {"name": "timeline", "type": str, "required": True},
            {"name": "budget", "type": str, "required": True},
            {"name": "deliverables", "type": list, "required": True},
            {"name": "additional_notes", "type": str, "required": False, "default": ""},
        ],
        description="Project briefing template"
    )


def register_briefing_transforms():
    """Register transforms for briefings."""

    def briefing_to_markdown(data: dict) -> str:
        """Convert briefing data to markdown."""
        md = f"""# Project Briefing: {data['project_name']}

## Client
**{data['client_name']}**

## Project Overview
- **Type**: {data['project_type']}
- **Timeline**: {data['timeline']}
- **Budget**: {data['budget']}

## Goals
"""
        for goal in data['goals']:
            md += f"- {goal}\n"

        md += f"""
## Target Audience
{data['target_audience']}

## Deliverables
"""
        for deliverable in data['deliverables']:
            md += f"- {deliverable}\n"

        if data.get('additional_notes'):
            md += f"""
## Additional Notes
{data['additional_notes']}
"""

        return md

    def markdown_to_pdf_placeholder(markdown: str) -> bytes:
        """
        Convert markdown to PDF (placeholder).
        In production, use fpdf, weasyprint, or pandoc.
        """
        # This is a placeholder - real implementation would generate PDF
        return markdown.encode('utf-8')

    content_transform.define_transform(
        name="briefing_to_markdown",
        source_type="briefing_data",
        target_type="markdown",
        func=briefing_to_markdown
    )

    content_transform.define_transform(
        name="markdown_to_pdf",
        source_type="markdown",
        target_type="pdf",
        func=markdown_to_pdf_placeholder
    )


# Initialize on import
setup_briefing_template()
register_briefing_transforms()


def generate_briefing(
    data: BriefingData,
    output_dir: Optional[Path] = None,
    format: str = "markdown"
) -> asset_entity.Asset:
    """
    Generate a project briefing.

    Args:
        data: Briefing data
        output_dir: Output directory for briefing file
        format: Output format (markdown, pdf)

    Returns:
        Asset entity representing the briefing
    """
    # Create job for tracking
    job = job_identity.create_job(
        name="briefing_generation",
        params=asdict(data)
    )

    try:
        # Validate data
        data_dict = asdict(data)
        validation = template_schema.validate_template_data("project_briefing", data_dict)
        if not validation['valid']:
            raise ValueError(f"Invalid briefing data: {validation['errors']}")

        # Create asset entity
        briefing = asset_entity.create_asset("project_briefing", data_dict)

        # Generate markdown
        markdown_content = content_transform.apply_transform("briefing_to_markdown", data_dict)

        # Write file
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            if format == "markdown":
                output_path = output_dir / f"{data.project_name.replace(' ', '_')}_briefing.md"
                asset_io.write_file(output_path, markdown_content)
            elif format == "pdf":
                pdf_bytes = content_transform.apply_transform("markdown_to_pdf", markdown_content)
                output_path = output_dir / f"{data.project_name.replace(' ', '_')}_briefing.pdf"
                asset_io.write_pdf(output_path, pdf_bytes)
            else:
                raise ValueError(f"Unsupported format: {format}")

            briefing.metadata['output_path'] = str(output_path)

        # Log success
        job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"asset_id": briefing.id}
        )

        return briefing

    except Exception as e:
        job_identity.log_job_execution(
            job.id,
            status="failed",
            error=str(e)
        )
        raise


def generate_briefing_from_csv(csv_path: Path, output_dir: Path, format: str = "markdown") -> List[asset_entity.Asset]:
    """
    Generate multiple briefings from CSV file.

    CSV format:
    client_name,project_name,project_type,goals,target_audience,timeline,budget,deliverables,additional_notes

    Note: goals and deliverables should be pipe-separated (|)
    """
    rows = asset_io.read_csv(csv_path)

    assets = []
    for row in rows:
        # Parse pipe-separated lists
        goals = row.get('goals', '').split('|') if row.get('goals') else []
        deliverables = row.get('deliverables', '').split('|') if row.get('deliverables') else []

        data = BriefingData(
            client_name=row['client_name'],
            project_name=row['project_name'],
            project_type=row['project_type'],
            goals=goals,
            target_audience=row['target_audience'],
            timeline=row['timeline'],
            budget=row['budget'],
            deliverables=deliverables,
            additional_notes=row.get('additional_notes', '')
        )

        asset = generate_briefing(data, output_dir, format)
        assets.append(asset)

    return assets
