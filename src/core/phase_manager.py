"""
Phase transition and task hierarchy management for Omega Execution Core
"""
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class PhaseManager:
    @staticmethod
    def parse_hierarchy(
        master_plan_path: Path,
        progress_log_path: Path,
        phase_files: List[Path],
        mode: str = "strict_sequential"
    ) -> Optional[Dict[str, Any]]:
        """Parse task hierarchy from plan files"""
        if not master_plan_path.exists():
            return None
            
        content = master_plan_path.read_text()
        
        # Detect current phase from phase files
        current_phase = PhaseManager._detect_current_phase(phase_files)
        if not current_phase:
            return None
            
        # Parse all tasks for current phase
        tasks = PhaseManager._parse_phase_tasks(content, current_phase)
        
        # Filter out completed tasks
        return next(
            (t for t in tasks 
             if not PhaseManager._is_task_completed(t['id'], progress_log_path)),
            None
        )
    
    @staticmethod
    def _detect_current_phase(phase_files: List[Path]) -> Optional[float]:
        """Detect current phase from phase changelog files"""
        # Implementation would analyze phase files
        return 2.0  # Default for now
    
    @staticmethod
    def _parse_phase_tasks(content: str, phase: float) -> List[Dict[str, Any]]:
        """Parse all tasks for given phase from markdown"""
        tasks = []
        
        # Find phase section
        phase_section = re.search(
            rf"### ФАЗА {phase}:.*?\n((?:\n.*?)+?)(?=### ФАЗA|""", 
            content, 
            re.DOTALL
        )
        
        if not phase_section:
            return tasks
            
        # Parse all task blocks in phase
        task_blocks = re.finditer(
            r"#### \*\*Завдання .*?\*\*\n((?:\n.*?)+?)(?=#### |### |""",
            phase_section.group(1)
        )
        
        for block in task_blocks:
            # Extract task ID
            task_id_match = re.search(r"Phase.*?\-T\d+", block.group(0))
            if not task_id_match:
                continue
                
            # Determine task type
            task_type = "frontend" if "frontend" in block.group(0).lower() else "backend"
            
            # Check completion status
            status_match = re.search(r"\- \[(x| )\]", block.group(0))
            completed = status_match.group(1) == "x" if status_match else False
            
            tasks.append({
                "id": task_id_match.group(0),
                "name": block.group(0).split("\n")[0].strip("#* "),
                "type": task_type,
                "completed": completed
            })
            
        return tasks
    
    @staticmethod
    def _is_task_completed(task_id: str, progress_log_path: Path) -> bool:
        """Check if task is marked completed in progress log"""
        if not progress_log_path.exists():
            return False
            
        content = progress_log_path.read_text()
        return f"[{task_id}]" in content and "COMPLETED" in content
    
    @staticmethod
    def check_phase_completion(plan_path: Path, phase: float) -> bool:
        """Verify 100% completion of phase tasks"""
        if not plan_path.exists():
            return False
            
        content = plan_path.read_text()
        
        # Find phase section
        phase_section = re.search(
            rf"### ФАЗА {phase}:.*?\n((?:\n.*?)+?)(?=### ФАЗA|""", 
            content, 
            re.DOTALL
        )
        
        if not phase_section:
            return False
            
        # Check all tasks are completed (no [ ] markers)
        return "[ ]" not in phase_section.group(1) and "[x]" in phase_section.group(1)
    
    @staticmethod
    def initialize_phase(phase: float) -> None:
        """Prepare system for new phase"""
        # Would create phase directory, update config etc.
        pass
