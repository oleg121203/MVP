"""
Task execution utilities for Omega System
"""
from typing import Dict, Any
import subprocess
from pathlib import Path
from .documentation import DocumentationHandler

class TaskExecutor:
    @staticmethod
    def implement(task: Dict[str, Any], force_mode: bool = True) -> None:
        """Execute task implementation"""
        # Implementation would vary based on task type
        if task.get('type') == 'frontend':
            TaskExecutor._implement_frontend(task, force_mode)
        elif task.get('type') == 'backend':
            TaskExecutor._implement_backend(task, force_mode)
        
    @staticmethod
    def _implement_frontend(task: Dict[str, Any], force_mode: bool) -> None:
        """Frontend-specific implementation"""
        # Example for Phase2.0-T7 (Frontend API Client)
        if task['id'] == 'Phase2.0-T7':
            # Create price client file
            Path("src/api/priceClient.ts").write_text(
                "// Auto-generated price API client\n"
                "import axios from 'axios';\n"
                "// Implementation would go here"
            )
            
            # Update price slice
            price_slice = Path("src/store/priceSlice.ts")
            if price_slice.exists():
                content = price_slice.read_text() + "\n// Updated by OmegaSystem"
                price_slice.write_text(content)
    
    @staticmethod
    def validate(task: Dict[str, Any], quality_gates: Dict[str, Any]) -> bool:
        """Run validation checks"""
        # Run tests
        test_result = subprocess.run(
            ["npm", "test"], 
            capture_output=True, 
            text=True
        )
        
        # Check coverage
        coverage_ok = "Coverage summary" in test_result.stdout \
            and f"{quality_gates['test_coverage']}%" in test_result.stdout
            
        # Check linting
        lint_result = subprocess.run(
            ["npm", "run", "lint"], 
            capture_output=True, 
            text=True
        )
        
        return coverage_ok and lint_result.returncode == 0
    
    @staticmethod
    def document(task: Dict[str, Any], phase: float) -> None:
        """Update changelogs using DocumentationHandler"""
        validation_stats = {
            "coverage": TaskExecutor._get_test_coverage(),
            "lint_score": TaskExecutor._get_lint_score()
        }
        
        DocumentationHandler.update_changelog(
            task=task,
            phase=phase,
            master_log_path=Path("CHANGELOG.md"),
            phase_dir=Path("docs/changelog"),
            validation_stats=validation_stats
        )
