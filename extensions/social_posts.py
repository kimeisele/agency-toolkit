"""
Social Posts Extension - Generate social media posts
Uses: core.asset_entity, core.content_transform, core.asset_io
"""

from pathlib import Path
from typing import Dict, List, Optional
from agency_core import asset_entity, asset_io, content_transform, job_identity, template_schema


def setup_social_post_template():
    """Define social post template."""
    template_schema.define_template(
        name="social_post",
        fields=[
            {"name": "text", "type": str, "required": True},
            {"name": "style", "type": str, "required": False, "default": "modern"},
            {"name": "color", "type": str, "required": False, "default": "#000000"},
            {"name": "background", "type": str, "required": False, "default": "#FFFFFF"},
        ],
        description="Social media post template"
    )


def register_social_transforms():
    """Register transforms for social posts."""

    def text_to_simple_image(data: Dict) -> bytes:
        """
        Simple text-to-image transform (placeholder).
        In production, use PIL/Pillow or external service.
        """
        # This is a placeholder - real implementation would use PIL
        text = data.get('text', '')
        style = data.get('style', 'modern')
        color = data.get('color', '#000000')

        # For now, return a simple representation
        content = f"Social Post Image\n\nText: {text}\nStyle: {style}\nColor: {color}"
        return content.encode('utf-8')

    content_transform.define_transform(
        name="text_to_social_image",
        source_type="social_post_data",
        target_type="image_bytes",
        func=text_to_simple_image
    )


# Initialize on import
setup_social_post_template()
register_social_transforms()


def generate_social_post(
    text: str,
    style: str = "modern",
    color: str = "#000000",
    background: str = "#FFFFFF",
    output_dir: Optional[Path] = None
) -> asset_entity.Asset:
    """
    Generate a social media post.

    Args:
        text: Post text
        style: Visual style (modern, minimal, bold)
        color: Text color
        background: Background color
        output_dir: Output directory for image file

    Returns:
        Asset entity representing the social post
    """
    # Create job for tracking
    job = job_identity.create_job(
        name="social_post_generation",
        params={"text": text, "style": style, "color": color}
    )

    try:
        # Validate data against template
        data = {
            "text": text,
            "style": style,
            "color": color,
            "background": background
        }

        validation = template_schema.validate_template_data("social_post", data)
        if not validation['valid']:
            raise ValueError(f"Invalid data: {validation['errors']}")

        # Create asset entity
        post = asset_entity.create_asset("social_post", data)

        # Apply transform to generate image
        image_bytes = content_transform.apply_transform("text_to_social_image", data)

        # Write image file
        if output_dir:
            output_path = Path(output_dir) / f"{post.id}.png"
            asset_io.write_image(output_path, image_bytes)
            post.metadata['output_path'] = str(output_path)

        # Log success
        job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"asset_id": post.id}
        )

        return post

    except Exception as e:
        job_identity.log_job_execution(
            job.id,
            status="failed",
            error=str(e)
        )
        raise


def batch_generate_social_posts(csv_path: Path, output_dir: Path) -> List[asset_entity.Asset]:
    """
    Batch generate social posts from CSV file.

    CSV format:
    text,style,color,background

    Args:
        csv_path: Path to CSV file
        output_dir: Output directory for images

    Returns:
        List of generated assets
    """
    rows = asset_io.read_csv(csv_path)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = []
    for row in rows:
        asset = generate_social_post(
            text=row.get('text', ''),
            style=row.get('style', 'modern'),
            color=row.get('color', '#000000'),
            background=row.get('background', '#FFFFFF'),
            output_dir=output_dir
        )
        assets.append(asset)

    return assets
