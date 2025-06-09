"""
Real-time documentation system for Omega Execution Core
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class DocumentationHandler:
    @staticmethod
    def update_changelog(
        task: Dict[str, Any],
        phase: float,
        master_log_path: Path,
        phase_dir: Path,
        validation_stats: Dict[str, Any]
    ) -> None:
        """Update both master changelog and phase-specific log"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create phase directory if needed
        phase_dir.mkdir(exist_ok=True)
        
        # Entry template
        entry = f"""
## [{task['id']}] {task['name']}
**Status:** ✅ AUTO-COMPLETED | ⏱️ {timestamp}
**Changes:**
- Created: `{task.get('created_files', [])}`
- Modified: `{task.get('modified_files', [])}`
**Validation:**
- Tests: {validation_stats.get('coverage', 0)}% coverage
- Lint: {validation_stats.get('lint_score', 0)}%"""
        
        # Update master changelog
        with open(master_log_path, "a") as f:
            f.write(entry)
            
        # Update phase log
        phase_file = phase_dir / f"phase{phase}.md"
        with open(phase_file, "a") as f:
            f.write(entry)
    
    @staticmethod
    def generate_commit_report(task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report of changes made"""
        return {
            "task_id": task["id"],
            "timestamp": datetime.utcnow().isoformat(),
            "changes": {
                "created": task.get("created_files", []),
                "modified": task.get("modified_files", [])
            }
        }
