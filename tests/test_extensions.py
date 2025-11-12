"""
Tests for extension modules.
"""

import pytest
from pathlib import Path
import tempfile

from extensions.social_posts import generate_social_post
from extensions.briefing_generator import generate_briefing, BriefingData
from extensions.folder_structure import generate_folder_structure, list_available_structures


class TestSocialPosts:
    """Test social_posts extension."""

    def test_generate_social_post(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            asset = generate_social_post(
                text="Test post",
                style="modern",
                output_dir=Path(tmpdir)
            )

            assert asset.type == "social_post"
            assert asset.data["text"] == "Test post"
            assert "output_path" in asset.metadata


class TestBriefingGenerator:
    """Test briefing_generator extension."""

    def test_generate_briefing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data = BriefingData(
                client_name="Test Client",
                project_name="Test Project",
                project_type="Web Development",
                goals=["Goal 1", "Goal 2"],
                target_audience="Test audience",
                timeline="3 months",
                budget="$10,000",
                deliverables=["Deliverable 1", "Deliverable 2"]
            )

            asset = generate_briefing(data, output_dir=Path(tmpdir), format="markdown")

            assert asset.type == "project_briefing"
            assert asset.data["project_name"] == "Test Project"
            assert "output_path" in asset.metadata

            # Check file was created
            output_path = Path(asset.metadata["output_path"])
            assert output_path.exists()


class TestFolderStructure:
    """Test folder_structure extension."""

    def test_list_structures(self):
        structures = list_available_structures()
        assert len(structures) > 0
        assert "agency_standard" in structures

    def test_generate_folder_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            asset = generate_folder_structure(
                project_name="Test Project",
                structure_type="agency_standard",
                base_path=Path(tmpdir)
            )

            assert asset.type == "folder_structure"
            assert "project_root" in asset.metadata

            # Check folders were created
            project_root = Path(asset.metadata["project_root"])
            assert project_root.exists()
            assert (project_root / "README.md").exists()
