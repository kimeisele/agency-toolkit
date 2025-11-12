"""
Tests for frozen core modules.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from agency_core import (
    asset_io, asset_storage, template_schema, asset_entity,
    content_transform, workflow_process, rule_validation, job_identity
)


class TestAssetIO:
    """Test asset_io module."""

    def test_read_write_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.txt"
            content = "Hello World"

            asset_io.write_file(path, content)
            assert asset_io.read_file(path) == content

    def test_read_write_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.json"
            data = {"name": "test", "value": 123}

            asset_io.write_json(path, data)
            assert asset_io.read_json(path) == data

    def test_read_write_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.csv"
            data = [
                {"name": "Alice", "age": "30"},
                {"name": "Bob", "age": "25"}
            ]

            asset_io.write_csv(path, data)
            result = asset_io.read_csv(path)
            assert result == data


class TestAssetStorage:
    """Test asset_storage module."""

    def test_store_retrieve(self):
        asset_storage.clear_storage()
        asset_storage.store_asset("test_key", {"data": "value"})
        assert asset_storage.retrieve_asset("test_key") == {"data": "value"}

    def test_list_assets(self):
        asset_storage.clear_storage()
        asset_storage.store_asset("test_1", "value1")
        asset_storage.store_asset("test_2", "value2")
        asset_storage.store_asset("other_1", "value3")

        all_keys = asset_storage.list_assets()
        assert len(all_keys) == 3

        test_keys = asset_storage.list_assets(prefix="test_")
        assert len(test_keys) == 2


class TestTemplateSchema:
    """Test template_schema module."""

    def test_define_and_validate_template(self):
        template_schema.define_template(
            name="test_template",
            fields=[
                {"name": "field1", "type": str, "required": True},
                {"name": "field2", "type": int, "required": False}
            ]
        )

        # Valid data
        result = template_schema.validate_template_data(
            "test_template",
            {"field1": "value", "field2": 123}
        )
        assert result['valid'] is True

        # Invalid data (missing required field)
        result = template_schema.validate_template_data(
            "test_template",
            {"field2": 123}
        )
        assert result['valid'] is False
        assert len(result['errors']) > 0


class TestAssetEntity:
    """Test asset_entity module."""

    def test_create_asset(self):
        asset = asset_entity.create_asset(
            "test_type",
            {"name": "test", "value": 123}
        )

        assert asset.type == "test_type"
        assert asset.data["name"] == "test"
        assert asset.id is not None

    def test_update_asset(self):
        asset = asset_entity.create_asset("test", {"value": 1})
        updated = asset_entity.update_asset(asset.id, {"value": 2})

        assert updated.data["value"] == 2

    def test_list_by_type(self):
        asset_entity.create_asset("type_a", {})
        asset_entity.create_asset("type_a", {})
        asset_entity.create_asset("type_b", {})

        type_a_assets = asset_entity.list_assets_by_type("type_a")
        assert len([a for a in type_a_assets if a.type == "type_a"]) >= 2


class TestContentTransform:
    """Test content_transform module."""

    def test_define_and_apply_transform(self):
        def uppercase_transform(data):
            return data.upper()

        content_transform.define_transform(
            name="test_uppercase",
            source_type="string",
            target_type="string",
            func=uppercase_transform
        )

        result = content_transform.apply_transform("test_uppercase", "hello")
        assert result == "HELLO"


class TestWorkflowProcess:
    """Test workflow_process module."""

    def test_define_and_execute_workflow(self):
        def step1(data):
            return data + 1

        def step2(data):
            return data * 2

        workflow_process.define_workflow(
            name="test_workflow",
            steps=[
                {"name": "add_one", "func": step1},
                {"name": "multiply_two", "func": step2}
            ]
        )

        result = workflow_process.execute_workflow("test_workflow", 5)
        assert result == 12  # (5 + 1) * 2


class TestRuleValidation:
    """Test rule_validation module."""

    def test_define_and_validate_rule(self):
        def check_positive(data):
            from agency_core.rule_validation import ValidationResult
            if data > 0:
                return ValidationResult(valid=True, errors=[])
            else:
                return ValidationResult(valid=False, errors=["Value must be positive"])

        rule_validation.define_rule(
            name="test_positive",
            check=check_positive
        )

        # Valid data
        result = rule_validation.validate_asset(10, ["test_positive"])
        assert result.valid is True

        # Invalid data
        result = rule_validation.validate_asset(-5, ["test_positive"])
        assert result.valid is False
        assert len(result.errors) > 0


class TestJobIdentity:
    """Test job_identity module."""

    def test_create_and_log_job(self):
        job = job_identity.create_job(
            name="test_job",
            params={"param1": "value1"}
        )

        assert job.name == "test_job"
        assert job.id is not None

        # Log execution
        success = job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"output": "success"}
        )
        assert success is True

        # Retrieve job
        retrieved = job_identity.get_job(job.id)
        assert retrieved is not None
        assert len(retrieved.executions) == 1
        assert retrieved.executions[0].status == "completed"
