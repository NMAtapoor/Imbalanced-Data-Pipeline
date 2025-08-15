import subprocess
import sys
import os
from pathlib import Path

"""
End-to-End (E2E) Tests for ETL Pipeline

These tests validate the complete ETL pipeline execution from start to finish,
testing the system as a whole rather than individual components.

Test Coverage:
1. Complete Pipeline Execution: Verifies the entire ETL workflow runs successfully
   from script invocation through data processing and output generation
2. Environment Handling: Tests proper environment setup and configuration loading
3. Output Validation: Confirms expected data files and logs are created
4. Error Handling: Validates graceful failure and proper error reporting
5. Process Integration: Tests subprocess execution and exit code handling

E2E Tests focus on:
- Real script execution via subprocess (not function calls)
- Complete system workflow validation
- Environment isolation and configuration
- Actual file system outputs and logging
- Production-like execution scenarios

This differs from other test types by:
- Testing the complete system end-to-end
- Using subprocess execution (not direct function calls)
- Validating real file outputs and system state
- Testing deployment-ready script execution
- Focusing on user-facing functionality

Note: These tests require actual database and file system access,
making them slower but providing the highest confidence in system functionality.
"""


def test_full_etl_pipeline_success():
    """E2E test: Complete ETL pipeline execution with output validation"""
    # Set test environment and log directory
    env = os.environ.copy()
    env["ENV"] = "test"
    
    # Get directories
    project_root = Path(__file__).parent.parent.parent
    test_logs_dir = Path(__file__).parent.parent / "logs"
    test_logs_dir.mkdir(exist_ok=True)
    env["LOG_BASE_PATH"] = str(test_logs_dir)
    
    # Run the ETL pipeline script
    result = subprocess.run(
        [sys.executable, "scripts/run_etl.py", "test"],
        cwd=str(project_root),
        env=env,
        capture_output=True,
        text=True,
    )

    # Verify pipeline executed successfully
    assert result.returncode == 0, f"ETL pipeline failed: {result.stderr}"
    
    # Verify log file was created and contains expected stages
    log_file = test_logs_dir / "logs" / "etl_pipeline.log"
    assert log_file.exists(), f"ETL pipeline log file not created at {log_file}"
    
    log_content = log_file.read_text()
    assert "Starting ETL pipeline" in log_content
    assert "Beginning data extraction phase" in log_content
    assert "Data extraction phase completed" in log_content
    assert "Beginning the data transformation phase" in log_content
    assert "Data transformation phase completed" in log_content
    assert "ETL pipeline completed successfully" in log_content
    
    # Verify processed data files were created
    processed_dir = project_root / "data" / "processed"
    assert (processed_dir / "cleaned_transactions.csv").exists()
    assert (processed_dir / "cleaned_customers.csv").exists()


def test_etl_pipeline_invalid_environment():
    """E2E test: ETL pipeline handles invalid environment gracefully"""
    env = os.environ.copy()
    
    project_root = Path(__file__).parent.parent.parent
    test_logs_dir = Path(__file__).parent.parent / "logs"
    test_logs_dir.mkdir(exist_ok=True)
    env["LOG_BASE_PATH"] = str(test_logs_dir)
    
    # Run with invalid environment argument (should fail)
    result = subprocess.run(
        [sys.executable, "scripts/run_etl.py", "invalid_env"],
        cwd=str(project_root),
        env=env,
        capture_output=True,
        text=True,
    )

    # Verify pipeline failed gracefully
    assert result.returncode == 1, f"Expected pipeline to fail with invalid env, got return code {result.returncode}"
    assert "Please provide an environment" in result.stderr or "Please provide an environment" in result.stdout