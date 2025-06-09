"""
VENTAI ENTERPRISE - OMEGA EXECUTION CORE
Autonomous task execution engine for VentAI Enterprise platform
"""
import json
from typing import Dict, Any
from pathlib import Path
from .task_executor import TaskExecutor
from .phase_manager import PhaseManager
from .emergency import EmergencyProtocols
from .tech_stack import TechStackManager
import datetime

class OmegaSystem:
    def __init__(self):
        self._load_config()
        self.current_phase = self._detect_current_phase()
        self.failsafe = False
        
    def _load_config(self):
        """Load configuration from omega_config.json"""
        config_path = Path(__file__).parent / "omega_config.json"
        with open(config_path) as f:
            config = json.load(f)
        self.config = config
        self.quality_gates = config["quality_gates"]
        self.plan_path = Path(config["paths"]["master_plan"])
        self.changelog_path = Path(config["paths"]["changelog"])
        self.retry_policy = config["retry_policy"]
    
    def _detect_current_phase(self) -> float:
        """Detect current phase from config"""
        return float(self.config.get('current_phase', 2.0))
        
    def execute(self):
        """Main execution loop"""
        while not self.failsafe:
            task = self._fetch_next_task()
            if not task:
                if self._verify_completion():
                    self._safe_shutdown()
                continue
                
            self._process_task(task)
            self._update_system_state()
            
    def _fetch_next_task(self) -> Dict[str, Any]:
        """Use PhaseManager to parse task hierarchy"""
        return PhaseManager.parse_hierarchy(
            master_plan_path=self.plan_path,
            progress_log_path=self.changelog_path,
            phase_files=[Path(f"docs/changelog/phase{self.current_phase}.md")],
            mode="strict_sequential"
        )
        
    def _handle_failure(self, task: Dict[str, Any], exception: Exception) -> None:
        """Handle failure using appropriate emergency protocol"""
        error_type = str(exception)
        
        if "cascading" in error_type.lower():
            EmergencyProtocols.handle_cascading_failure(task, self.current_phase)
        elif "dependency" in error_type.lower():
            EmergencyProtocols.handle_dependency_issues(task)
        elif "validation" in error_type.lower():
            EmergencyProtocols.handle_validation_failure(task)
            
        # Create autoticket and mark skipped
        self._create_autoticket(task, error_type)
        self._mark_skipped(task)
        
    def _create_autoticket(self, task: Dict[str, Any], error: str) -> None:
        """Generate automatic ticket for failed task"""
        ticket = {
            "task_id": task["id"],
            "phase": self.current_phase,
            "error": error,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        tickets_dir = Path("reports/tickets")
        tickets_dir.mkdir(exist_ok=True)
        
        ticket_path = tickets_dir / f"{task['id']}.json"
        ticket_path.write_text(json.dumps(ticket, indent=2))
        
    def _mark_skipped(self, task: Dict[str, Any]) -> None:
        """Mark task as skipped in changelog"""
        entry = f"\n## [{task['id']}] {task['name']} - SKIPPED\n"
        
        with open(self.changelog_path, "a") as f:
            f.write(entry)
            
    def _process_task(self, task: Dict[str, Any]) -> None:
        """Handle task execution with retries"""
        if task.get('completed', False):
            self._document(task)
            return
            
        for attempt in range(self.retry_policy["max_attempts"]):
            try:
                self._implement(task)
                self._validate(task)
                self._document(task)
                return
            except Exception as e:
                if attempt == self.retry_policy["max_attempts"] - 1:
                    self._handle_failure(task, e)
                continue
                
    def _implement(self, task: Dict[str, Any]) -> None:
        """Execute implementation with tech stack"""
        tech_stack = TechStackManager.get_dependencies(task.get("type", ""))
        TaskExecutor.implement(
            task, 
            force_mode=True,
            tech_stack=tech_stack
        )
        
    def _validate(self, task: Dict[str, Any]) -> None:
        """Verify task implementation meets all standards"""
        # Verify dependencies first
        if not TechStackManager.verify_dependencies(task.get("type", "")):
            raise ValueError("Dependency validation failed")
            
        # Then verify implementation quality
        if not TaskExecutor.validate(task, self.quality_gates):
            raise ValueError("Quality validation failed")
            
    def _document(self, task: Dict[str, Any]) -> None:
        """Update documentation with task status"""
        status = "COMPLETED" if not task.get('skipped', False) else "SKIPPED"
        
        entry = (
            f"\n## [{task['id']}] {task['name']} - {status}\n"
            f"**Phase:** {self.current_phase}\n"
            f"**Timestamp:** {datetime.datetime.utcnow().isoformat()}\n"
        )
        
        if status == "COMPLETED":
            entry += (
                f"**Validation:**\n"
                f"- Test Coverage: {self._get_test_coverage()}%\n"
                f"- Lint Score: {self._get_lint_score()}/100\n"
            )
            
        with open(self.changelog_path, "a") as f:
            f.write(entry)
            
    def _get_test_coverage(self) -> float:
        # TO DO: implement test coverage calculation
        pass
        
    def _get_lint_score(self) -> float:
        # TO DO: implement lint score calculation
        pass
        
    def _update_system_state(self) -> None:
        """Check if phase completed"""
        pass  # Would implement phase transition logic
        
    def _verify_completion(self) -> bool:
        """Check if all tasks completed"""
        return False  # Would implement completion check
        
    def _safe_shutdown(self) -> None:
        """Validate shutdown conditions"""
        if self._verify_completion():
            self.failsafe = True
            
    def _check_phase_completion(self) -> bool:
        """Delegate to PhaseManager"""
        return PhaseManager.check_phase_completion(self.plan_path, self.current_phase)
        
    def _initialize_phase(self, phase: float) -> None:
        """Delegate to PhaseManager"""
        PhaseManager.initialize_phase(phase)
        
if __name__ == "__main__":
    OmegaSystem().execute()  # Immortal execution core
