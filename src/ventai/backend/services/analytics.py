import json
import pandas as pd
import redis
from datetime import datetime, timezone
from typing import Dict, Any

class ProjectAnalyticsEngine:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6380):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        
    def calculate_metrics(self, project_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate key performance metrics from project data"""
        metrics = {
            'completion_rate': project_data['completed_tasks'] / project_data['total_tasks'],
            'budget_utilization': project_data['spent_budget'] / project_data['total_budget'],
            'time_efficiency': project_data['completed_tasks'] / project_data['elapsed_days'],
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Publish to Redis channel
        self.redis.publish(f'project:{project_data["id"]}:metrics', json.dumps(metrics))
        return metrics
    
    def generate_insights(self, metrics: Dict[str, float], historical_data: pd.DataFrame) -> str:
        """Generate AI-powered insights from metrics and historical data"""
        insights = []
        
        if metrics['completion_rate'] < 0.5:
            insights.append("Project is behind schedule - consider reallocating resources")
        
        if metrics['budget_utilization'] > 0.8:
            insights.append("Budget consumption high - review expenses")
            
        if len(insights) > 0:
            return '\n'.join(insights)
        else:
            return "Project is on track with no major issues detected"
    
    def _publish_metrics(self, project_id: int, metrics: Dict[str, float]):
        """Publish metrics to Redis for real-time updates"""
        payload = {
            'project_id': project_id,
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.redis.publish(f'project_analytics:{project_id}', json.dumps(payload))
