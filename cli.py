#!/usr/bin/env python3
"""
Agency Toolkit CLI - Professional automation for agencies

Built on Genesis Core architecture:
- 8 frozen core modules (never change)
- Extensions for domain logic (can evolve)
"""

import sys
from pathlib import Path
import click

from extensions.social_posts import generate_social_post, batch_generate_social_posts
from extensions.briefing_generator import generate_briefing, generate_briefing_from_csv, BriefingData
from extensions.folder_structure import (
    generate_folder_structure,
    generate_custom_structure,
    list_available_structures
)
from extensions.batch_processor import batch_process_with_callback


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Agency Toolkit - Professional automation built on Genesis Core.

    Commands:
      social     - Generate social media posts
      briefing   - Generate project briefings
      structure  - Generate folder structures
      batch      - Batch processing utilities
    """
    pass


# ============================================================================
# SOCIAL MEDIA COMMANDS
# ============================================================================

@cli.group()
def social():
    """Social media post generation."""
    pass


@social.command()
@click.argument('text')
@click.option('--style', default='modern', help='Visual style (modern, minimal, bold)')
@click.option('--color', default='#000000', help='Text color (hex)')
@click.option('--background', default='#FFFFFF', help='Background color (hex)')
@click.option('--output', type=click.Path(), help='Output directory')
def single(text, style, color, background, output):
    """Generate a single social media post."""
    output_dir = Path(output) if output else Path.cwd() / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        asset = generate_social_post(
            text=text,
            style=style,
            color=color,
            background=background,
            output_dir=output_dir
        )
        click.echo(f"✓ Social post generated: {asset.id}")
        if 'output_path' in asset.metadata:
            click.echo(f"  Saved to: {asset.metadata['output_path']}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@social.command()
@click.argument('csv_path', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), required=True, help='Output directory')
def batch(csv_path, output):
    """Generate social posts from CSV file.

    CSV format: text,style,color,background
    """
    csv_path = Path(csv_path)
    output_dir = Path(output)

    try:
        assets = batch_generate_social_posts(csv_path, output_dir)
        click.echo(f"✓ Generated {len(assets)} social posts")
        click.echo(f"  Output directory: {output_dir}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


# ============================================================================
# BRIEFING COMMANDS
# ============================================================================

@cli.group()
def briefing():
    """Project briefing generation."""
    pass


@briefing.command()
@click.option('--client', required=True, help='Client name')
@click.option('--project', required=True, help='Project name')
@click.option('--type', 'project_type', required=True, help='Project type')
@click.option('--goals', required=True, help='Goals (comma-separated)')
@click.option('--audience', required=True, help='Target audience')
@click.option('--timeline', required=True, help='Timeline')
@click.option('--budget', required=True, help='Budget')
@click.option('--deliverables', required=True, help='Deliverables (comma-separated)')
@click.option('--notes', default='', help='Additional notes')
@click.option('--output', type=click.Path(), help='Output directory')
@click.option('--format', type=click.Choice(['markdown', 'pdf']), default='markdown', help='Output format')
def single(client, project, project_type, goals, audience, timeline, budget, deliverables, notes, output, format):
    """Generate a single project briefing."""
    output_dir = Path(output) if output else Path.cwd() / 'output'

    # Parse comma-separated lists
    goals_list = [g.strip() for g in goals.split(',')]
    deliverables_list = [d.strip() for d in deliverables.split(',')]

    data = BriefingData(
        client_name=client,
        project_name=project,
        project_type=project_type,
        goals=goals_list,
        target_audience=audience,
        timeline=timeline,
        budget=budget,
        deliverables=deliverables_list,
        additional_notes=notes
    )

    try:
        asset = generate_briefing(data, output_dir, format)
        click.echo(f"✓ Briefing generated: {asset.id}")
        if 'output_path' in asset.metadata:
            click.echo(f"  Saved to: {asset.metadata['output_path']}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@briefing.command()
@click.argument('csv_path', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), required=True, help='Output directory')
@click.option('--format', type=click.Choice(['markdown', 'pdf']), default='markdown', help='Output format')
def batch(csv_path, output, format):
    """Generate briefings from CSV file.

    CSV format: client_name,project_name,project_type,goals,target_audience,timeline,budget,deliverables,additional_notes
    Note: goals and deliverables should be pipe-separated (|)
    """
    csv_path = Path(csv_path)
    output_dir = Path(output)

    try:
        assets = generate_briefing_from_csv(csv_path, output_dir, format)
        click.echo(f"✓ Generated {len(assets)} briefings")
        click.echo(f"  Output directory: {output_dir}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


# ============================================================================
# FOLDER STRUCTURE COMMANDS
# ============================================================================

@cli.group()
def structure():
    """Project folder structure generation."""
    pass


@structure.command()
def list():
    """List available folder structure templates."""
    structures = list_available_structures()
    click.echo("Available folder structures:\n")
    for key, name in structures.items():
        click.echo(f"  {key:20} - {name}")


@structure.command()
@click.argument('project_name')
@click.option('--type', 'structure_type', default='agency_standard',
              help='Structure type (use "structure list" to see options)')
@click.option('--path', type=click.Path(), default='.', help='Base path for creation')
@click.option('--no-readme', is_flag=True, help='Skip README.md creation')
def create(project_name, structure_type, path, no_readme):
    """Create a folder structure for a project."""
    base_path = Path(path)

    try:
        asset = generate_folder_structure(
            project_name=project_name,
            structure_type=structure_type,
            base_path=base_path,
            create_readme=not no_readme
        )
        click.echo(f"✓ Folder structure created: {asset.id}")
        if 'project_root' in asset.metadata:
            click.echo(f"  Location: {asset.metadata['project_root']}")
            click.echo(f"  Folders: {len(asset.metadata['created_folders'])}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@structure.command()
@click.argument('project_name')
@click.argument('folders', nargs=-1, required=True)
@click.option('--path', type=click.Path(), default='.', help='Base path for creation')
def custom(project_name, folders, path):
    """Create a custom folder structure.

    Example: agency-toolkit structure custom MyProject src tests docs
    """
    base_path = Path(path)

    try:
        asset = generate_custom_structure(
            project_name=project_name,
            folders=list(folders),
            base_path=base_path
        )
        click.echo(f"✓ Custom structure created: {asset.id}")
        if 'project_root' in asset.metadata:
            click.echo(f"  Location: {asset.metadata['project_root']}")
            click.echo(f"  Folders: {len(asset.metadata['created_folders'])}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


# ============================================================================
# BATCH PROCESSING COMMANDS
# ============================================================================

@cli.group()
def batch():
    """Batch processing utilities."""
    pass


@batch.command()
def info():
    """Show information about batch processing."""
    click.echo("""
Batch Processing Guide
======================

The batch processor can execute workflows on CSV data.

CSV Format:
-----------
Each row in the CSV is processed through the defined workflow.
Columns become dictionary keys passed to workflow steps.

Example CSV:
  name,email,status
  Alice,alice@example.com,active
  Bob,bob@example.com,pending

Error Handling:
---------------
- skip: Continue processing on errors (default)
- raise: Stop on first error
- log: Print errors but continue

For custom workflows, use the Python API:
  from extensions.batch_processor import define_batch_workflow
    """)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    cli()
