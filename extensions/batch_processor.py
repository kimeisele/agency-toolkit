"""
Batch Processor Extension - Process CSV files with workflows
Uses: core.asset_io, core.workflow_process
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from agency_core import asset_io, workflow_process, job_identity


def process_csv_workflow(
    csv_path: Path,
    workflow_name: str,
    output_dir: Optional[Path] = None
) -> List[Any]:
    """
    Process CSV file through a workflow.

    Args:
        csv_path: Path to CSV file
        workflow_name: Name of registered workflow
        output_dir: Optional output directory for results

    Returns:
        List of workflow results
    """
    # Create job for tracking
    job = job_identity.create_job(
        name="batch_csv_processing",
        params={
            "csv_path": str(csv_path),
            "workflow_name": workflow_name
        }
    )

    try:
        # Read CSV
        rows = asset_io.read_csv(csv_path)

        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for i, row in enumerate(rows):
            # Execute workflow for each row
            result = workflow_process.execute_workflow(workflow_name, row)
            results.append(result)

        # Log success
        job_identity.log_job_execution(
            job.id,
            status="completed",
            result={"rows_processed": len(results)}
        )

        return results

    except Exception as e:
        job_identity.log_job_execution(
            job.id,
            status="failed",
            error=str(e)
        )
        raise


def define_batch_workflow(
    name: str,
    steps: List[Dict[str, Callable]],
    description: str = ""
) -> None:
    """
    Define a batch processing workflow.

    Args:
        name: Workflow name
        steps: List of step definitions with 'name' and 'func'
        description: Workflow description
    """
    workflow_process.define_workflow(
        name=name,
        steps=steps,
        description=description
    )


def batch_process_with_callback(
    csv_path: Path,
    process_func: Callable[[Dict], Any],
    output_dir: Optional[Path] = None,
    error_handling: str = "skip"  # skip, raise, log
) -> Dict[str, Any]:
    """
    Process CSV with a custom callback function.

    Args:
        csv_path: Path to CSV file
        process_func: Function to process each row
        output_dir: Optional output directory
        error_handling: How to handle errors (skip, raise, log)

    Returns:
        Dict with results and errors
    """
    job = job_identity.create_job(
        name="batch_callback_processing",
        params={"csv_path": str(csv_path)}
    )

    rows = asset_io.read_csv(csv_path)

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    errors = []

    for i, row in enumerate(rows):
        try:
            result = process_func(row)
            results.append(result)
        except Exception as e:
            error_info = {
                "row_index": i,
                "row_data": row,
                "error": str(e)
            }
            errors.append(error_info)

            if error_handling == "raise":
                raise
            elif error_handling == "log":
                print(f"Error processing row {i}: {e}")

    # Log completion
    status = "completed" if not errors else "completed_with_errors"
    job_identity.log_job_execution(
        job.id,
        status=status,
        result={
            "total_rows": len(rows),
            "successful": len(results),
            "errors": len(errors)
        }
    )

    return {
        "results": results,
        "errors": errors,
        "total": len(rows),
        "successful": len(results),
        "failed": len(errors)
    }
