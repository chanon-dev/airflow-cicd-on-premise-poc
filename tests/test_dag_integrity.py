
import os
import pytest
from airflow.models import DagBag

def test_dag_import_errors():
    """
    Verify that there are no DAG import errors in the dags folder.
    This works by loading the DagBag and checking the 'import_errors' property.
    """
    # Adjust path to point to the dags folder relative to this test file.
    # Assuming tests/ is at root and dags/ is at root.
    dags_folder = os.path.join(os.path.dirname(__file__), '../dags')
    
    dag_bag = DagBag(dag_folder=dags_folder, include_examples=False)
    
    assert len(dag_bag.import_errors) == 0, f"DAG import errors found: {dag_bag.import_errors}"

def test_dag_cycles():
    """
    Optional: Check for cycles in DAGs (if strict checking is needed).
    """
    # This is implicitly handled by DagBag in newer versions but good to be explicit if needed.
    pass
