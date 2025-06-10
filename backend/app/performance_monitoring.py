import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class PerformanceMonitoring:
    def __init__(self, monitoring_dir: str = 'monitoring_data', config_path: str = 'monitoring_config.json'):
        """
        Initialize AI-Driven Performance Monitoring and Reporting
        """
        self.monitoring_dir = monitoring_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.metrics = {}
        self.reports = []
        os.makedirs(self.monitoring_dir, exist_ok=True)
        logger.info("Performance Monitoring module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load monitoring configuration from file or create default if not exists
        """
        default_config = {
            "monitoring": {
                "enabled": True,
                "monitoring_modes": ["real_time", "batch", "hybrid"],
                "default_mode": "real_time",
                "monitoring_frequency": "hourly",
                "monitoring_time": "00:00",
                "target_areas": [
                    "system_performance",
                    "user_activity",
                    "ai_operations",
                    "business_metrics",
                    "cost_analysis"
                ],
                "monitoring_levels": {
                    "system_performance": "real_time",
                    "user_activity": "real_time",
                    "ai_operations": "hybrid",
                    "business_metrics": "batch",
                    "cost_analysis": "batch"
                }
            },
            "metrics": {
                "enabled": True,
                "metric_types": ["performance", "usage", "health", "financial", "custom"],
                "default_metric": "performance",
                "metric_validation": True
            },
            "data_collection": {
                "enabled": True,
                "collection_types": ["log", "sensor", "api", "database", "user_input"],
                "default_collection": "log",
                "collection_validation": True
            },
            "analysis": {
                "enabled": True,
                "analysis_types": ["statistical", "predictive", "diagnostic", "prescriptive"],
                "default_analysis": "statistical",
                "analysis_validation": True
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "trend", "anomaly", "forecast"],
                "default_report": "summary",
                "report_frequency": "daily",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard", "mobile"],
                "recipients": ["operations_team", "it_admin", "executives"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["threshold", "anomaly", "trend", "predictive"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "cpu_usage": 80,
                    "memory_usage": 85,
                    "disk_io": 75,
                    "network_latency": 200,
                    "error_rate": 5,
                    "response_time": 500,
                    "throughput": 1000,
                    "user_satisfaction": 80,
                    "cost_overrun": 110
                }
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "switch_to_manual", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded monitoring configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading monitoring config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default monitoring configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default monitoring config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved monitoring configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving monitoring config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_metric(self, metric_id: str, metric_name: str, description: str, target_area: str, metric_type: Optional[str] = None, collection_method: Optional[str] = None, analysis_type: Optional[str] = None, thresholds: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new performance metric
        Args:
            metric_id: Unique identifier for the metric
            metric_name: Name of the metric
            description: Detailed description of the metric
            target_area: Target area for monitoring
            metric_type: Type of metric ('performance', 'usage', etc.)
            collection_method: Method of data collection ('log', 'sensor', etc.)
            analysis_type: Type of analysis ('statistical', 'predictive', etc.)
            thresholds: Thresholds for alerts
        Returns:
            Dictionary with metric definition status
        """
        try:
            if not self.config['monitoring']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Monitoring is disabled"
                }

            if metric_id in self.metrics:
                return {
                    "status": "error",
                    "message": f"Metric with ID {metric_id} already exists"
                }

            if target_area not in self.config['monitoring']['target_areas']:
                return {
                    "status": "error",
                    "message": f"Invalid target area: {target_area}. Must be one of {self.config['monitoring']['target_areas']}"
                }

            metric_type = metric_type or self.config['metrics']['default_metric']
            if metric_type not in self.config['metrics']['metric_types']:
                return {
                    "status": "error",
                    "message": f"Invalid metric type: {metric_type}. Must be one of {self.config['metrics']['metric_types']}"
                }

            collection_method = collection_method or self.config['data_collection']['default_collection']
            if collection_method not in self.config['data_collection']['collection_types']:
                return {
                    "status": "error",
                    "message": f"Invalid collection method: {collection_method}. Must be one of {self.config['data_collection']['collection_types']}"
                }

            analysis_type = analysis_type or self.config['analysis']['default_analysis']
            if analysis_type not in self.config['analysis']['analysis_types']:
                return {
                    "status": "error",
                    "message": f"Invalid analysis type: {analysis_type}. Must be one of {self.config['analysis']['analysis_types']}"
                }

            metric_info = {
                "metric_id": metric_id,
                "metric_name": metric_name,
                "description": description,
                "target_area": target_area,
                "metric_type": metric_type,
                "collection_method": collection_method,
                "analysis_type": analysis_type,
                "thresholds": thresholds or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.metrics[metric_id] = metric_info

            # Save metric to file
            metric_file = os.path.join(self.monitoring_dir, f"metric_{metric_id}.json")
            try:
                with open(metric_file, 'w') as f:
                    json.dump(metric_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving metric data for {metric_id}: {e}")

            logger.info(f"Defined performance metric {metric_id} - {metric_name} for {target_area}")
            return {
                "status": "success",
                "metric_id": metric_id,
                "metric_name": metric_name,
                "target_area": target_area,
                "metric_type": metric_type,
                "collection_method": collection_method,
                "analysis_type": analysis_type,
                "thresholds": thresholds or {},
                "created_at": metric_info['created_at'],
                "version": metric_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining metric {metric_id}: {e}")
            return {"status": "error", "message": str(e)}

    def collect_data(self, metric_id: str, data_source: str, data_value: Any, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Collect data for a specific metric
        Args:
            metric_id: ID of metric to collect data for
            data_source: Source of the data
            data_value: Collected data value
            timestamp: Timestamp of data collection (ISO format), defaults to now
        Returns:
            Dictionary with data collection status
        """
        try:
            if not self.config['monitoring']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Monitoring is disabled",
                    "collection_id": "N/A"
                }

            if metric_id not in self.metrics:
                return {
                    "status": "error",
                    "message": f"Metric {metric_id} not found",
                    "collection_id": "N/A"
                }

            metric_info = self.metrics[metric_id]
            timestamp = timestamp or datetime.now().isoformat()
            collection_id = f"coll_{metric_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            data_point = {
                "collection_id": collection_id,
                "metric_id": metric_id,
                "metric_name": metric_info['metric_name'],
                "target_area": metric_info['target_area'],
                "data_source": data_source,
                "data_value": data_value,
                "timestamp": timestamp
            }

            # Save data point
            data_file = os.path.join(self.monitoring_dir, f"data_{metric_id}.json")
            data_list = []
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r') as f:
                        data_list = json.load(f)
                except Exception as e:
                    logger.warning(f"Error loading data for {metric_id}: {e}")

            data_list.append(data_point)

            try:
                with open(data_file, 'w') as f:
                    json.dump(data_list, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving data for {metric_id}: {e}")

            logger.info(f"Collected data for metric {metric_id} from {data_source}")
            return {
                "status": "success",
                "collection_id": collection_id,
                "metric_id": metric_id,
                "metric_name": metric_info['metric_name'],
                "target_area": metric_info['target_area'],
                "data_source": data_source,
                "data_value": data_value,
                "timestamp": timestamp
            }
        except Exception as e:
            logger.error(f"Error collecting data for metric {metric_id}: {e}")
            return {"status": "error", "message": str(e), "collection_id": "N/A"}

    def analyze_data(self, metric_id: str, analysis_type: Optional[str] = None, time_range: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Analyze collected data for a metric
        Args:
            metric_id: ID of metric to analyze
            analysis_type: Type of analysis to perform
            time_range: Time range for analysis {'start': ISO_TIMESTAMP, 'end': ISO_TIMESTAMP}
        Returns:
            Dictionary with analysis results
        """
        try:
            if not self.config['monitoring']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Monitoring is disabled",
                    "analysis_id": "N/A"
                }

            if metric_id not in self.metrics:
                return {
                    "status": "error",
                    "message": f"Metric {metric_id} not found",
                    "analysis_id": "N/A"
                }

            metric_info = self.metrics[metric_id]
            analysis_type = analysis_type or metric_info['analysis_type']

            if analysis_type not in self.config['analysis']['analysis_types']:
                return {
                    "status": "error",
                    "message": f"Invalid analysis type: {analysis_type}. Must be one of {self.config['analysis']['analysis_types']}",
                    "analysis_id": "N/A"
                }

            analysis_id = f"anal_{metric_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Load data for analysis
            data_file = os.path.join(self.monitoring_dir, f"data_{metric_id}.json")
            data_list = []
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r') as f:
                        data_list = json.load(f)
                except Exception as e:
                    logger.warning(f"Error loading data for analysis {metric_id}: {e}")

            # Filter by time range if provided
            if time_range and 'start' in time_range and 'end' in time_range:
                start_time = time_range['start']
                end_time = time_range['end']
                data_list = [d for d in data_list if start_time <= d['timestamp'] <= end_time]

            # Simulated analysis - in real system, would apply statistical or ML models
            analysis_start = datetime.now()
            analysis_info = {
                "analysis_id": analysis_id,
                "metric_id": metric_id,
                "metric_name": metric_info['metric_name'],
                "target_area": metric_info['target_area'],
                "analysis_type": analysis_type,
                "time_range": time_range or {},
                "start_time": analysis_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "running",
                "results": {},
                "insights": [],
                "alerts": []
            }

            # Simulate analysis results based on analysis type
            data_count = len(data_list)
            if data_count > 0:
                if analysis_type == "statistical":
                    # Simulate basic statistical analysis
                    values = [float(d['data_value']) for d in data_list if isinstance(d['data_value'], (int, float))]
                    analysis_info['results'] = {
                        "data_points": len(values),
                        "mean": sum(values) / len(values) if values else 0,
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0
                    }
                    analysis_info['insights'].append(f"Analyzed {len(values)} data points for {metric_info['metric_name']}")
                elif analysis_type == "predictive":
                    # Simulate predictive analysis
                    analysis_info['results'] = {
                        "data_points": data_count,
                        "forecast": "stable",
                        "confidence": random.uniform(0.7, 0.95)
                    }
                    analysis_info['insights'].append(f"Generated forecast for {metric_info['metric_name']}")
                elif analysis_type == "diagnostic":
                    # Simulate diagnostic analysis
                    analysis_info['results'] = {
                        "data_points": data_count,
                        "issues_detected": random.randint(0, 2),
                        "primary_cause": "usage patterns"
                    }
                    analysis_info['insights'].append(f"Diagnosed performance issues for {metric_info['metric_name']}")
                else:  # prescriptive
                    # Simulate prescriptive analysis
                    analysis_info['results'] = {
                        "data_points": data_count,
                        "recommendations": random.randint(1, 3)
                    }
                    analysis_info['insights'].append(f"Generated recommendations for {metric_info['metric_name']}")

                # Check for alerts based on thresholds
                thresholds = metric_info.get('thresholds', {})
                if thresholds and analysis_type in ["statistical", "diagnostic"]:
                    mean_value = analysis_info['results'].get('mean', 0)
                    for threshold_name, threshold_value in thresholds.items():
                        if threshold_name in self.config['alerts']['thresholds'] and mean_value > threshold_value:
                            analysis_info['alerts'].append({
                                "alert_type": "threshold",
                                "metric": threshold_name,
                                "value": mean_value,
                                "threshold": threshold_value,
                                "message": f"{threshold_name} exceeded threshold: {mean_value} > {threshold_value}"
                            })
            else:
                analysis_info['results'] = {"data_points": 0, "message": "No data available for analysis"}

            analysis_end = datetime.now()
            analysis_info['end_time'] = analysis_end.isoformat()
            analysis_info['duration_seconds'] = (analysis_end - analysis_start).total_seconds()
            analysis_info['status'] = "completed"

            # Save analysis results
            analysis_file = os.path.join(self.monitoring_dir, f"analysis_{analysis_id}.json")
            try:
                with open(analysis_file, 'w') as f:
                    json.dump(analysis_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving analysis data for {analysis_id}: {e}")

            logger.info(f"Performed {analysis_type} analysis for metric {metric_id}, status: {analysis_info['status']}")
            return {
                "status": "success",
                "analysis_id": analysis_id,
                "metric_id": metric_id,
                "metric_name": metric_info['metric_name'],
                "target_area": metric_info['target_area'],
                "analysis_type": analysis_type,
                "start_time": analysis_info['start_time'],
                "end_time": analysis_info['end_time'],
                "duration_seconds": analysis_info['duration_seconds'],
                "analysis_status": analysis_info['status'],
                "data_points": analysis_info['results'].get('data_points', 0),
                "insights_count": len(analysis_info['insights']),
                "alerts_count": len(analysis_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error analyzing data for metric {metric_id}: {e}")
            return {"status": "error", "message": str(e), "analysis_id": "N/A"}

    def generate_report(self, report_type: str, time_range: Dict[str, str], target_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a performance report
        Args:
            report_type: Type of report to generate ('summary', 'detailed', etc.)
            time_range: Time range for report {'start': ISO_TIMESTAMP, 'end': ISO_TIMESTAMP}
            target_areas: Target areas to include in report, defaults to all
        Returns:
            Dictionary with report generation status
        """
        try:
            if not self.config['monitoring']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Monitoring is disabled",
                    "report_id": "N/A"
                }

            if report_type not in self.config['reporting']['report_types']:
                return {
                    "status": "error",
                    "message": f"Invalid report type: {report_type}. Must be one of {self.config['reporting']['report_types']}",
                    "report_id": "N/A"
                }

            if 'start' not in time_range or 'end' not in time_range:
                return {
                    "status": "error",
                    "message": "Time range must include 'start' and 'end' timestamps",
                    "report_id": "N/A"
                }

            target_areas = target_areas or self.config['monitoring']['target_areas']
            invalid_areas = [a for a in target_areas if a not in self.config['monitoring']['target_areas']]
            if invalid_areas:
                return {
                    "status": "error",
                    "message": f"Invalid target areas: {invalid_areas}. Must be subset of {self.config['monitoring']['target_areas']}",
                    "report_id": "N/A"
                }

            report_id = f"report_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated report generation - in real system, would aggregate analysis results
            generation_start = datetime.now()
            report_info = {
                "report_id": report_id,
                "report_type": report_type,
                "time_range": time_range,
                "target_areas": target_areas,
                "start_time": generation_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "generating",
                "contents": {
                    "metrics_covered": [],
                    "key_findings": [],
                    "recommendations": [],
                    "alerts_summary": []
                }
            }

            # Simulate report contents based on report type and target areas
            metrics_by_area = {area: [] for area in target_areas}
            for metric_id, metric_info in self.metrics.items():
                if metric_info['target_area'] in target_areas:
                    metrics_by_area[metric_info['target_area']].append({
                        "metric_id": metric_id,
                        "metric_name": metric_info['metric_name'],
                        "status": "monitored"
                    })
                    report_info['contents']['metrics_covered'].append(metric_id)

            if report_type == "summary":
                for area in target_areas:
                    if metrics_by_area[area]:
                        report_info['contents']['key_findings'].append(f"Monitored {len(metrics_by_area[area])} metrics in {area}")
                report_info['contents']['recommendations'].append("Continue monitoring key performance indicators")
            elif report_type == "detailed":
                for area in target_areas:
                    if metrics_by_area[area]:
                        report_info['contents']['key_findings'].append(f"Detailed analysis of {len(metrics_by_area[area])} metrics in {area} shows stable performance")
                report_info['contents']['recommendations'].append("Review detailed metrics for potential optimization opportunities")
            elif report_type == "trend":
                for area in target_areas:
                    if metrics_by_area[area]:
                        report_info['contents']['key_findings'].append(f"Trend analysis for {area} indicates consistent performance")
                report_info['contents']['recommendations'].append("Maintain current operational parameters based on trend stability")
            elif report_type == "anomaly":
                for area in target_areas:
                    if metrics_by_area[area] and random.random() < 0.3:  # Simulate occasional anomalies
                        report_info['contents']['key_findings'].append(f"Anomaly detected in {area} metrics")
                        report_info['contents']['alerts_summary'].append(f"Investigate unusual patterns in {area}")
                if not report_info['contents']['alerts_summary']:
                    report_info['contents']['key_findings'].append("No significant anomalies detected in monitored areas")
            else:  # forecast
                for area in target_areas:
                    if metrics_by_area[area]:
                        report_info['contents']['key_findings'].append(f"Forecast for {area} predicts stable performance")
                report_info['contents']['recommendations'].append("Prepare for forecasted operational demands")

            generation_end = datetime.now()
            report_info['end_time'] = generation_end.isoformat()
            report_info['duration_seconds'] = (generation_end - generation_start).total_seconds()
            report_info['status'] = "completed"

            # Save report
            report_file = os.path.join(self.monitoring_dir, f"report_{report_id}.json")
            try:
                with open(report_file, 'w') as f:
                    json.dump(report_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving report data for {report_id}: {e}")

            # Add to reports list
            self.reports.append({
                "report_id": report_id,
                "report_type": report_type,
                "time_range": time_range,
                "target_areas": target_areas,
                "generated_at": generation_end.isoformat(),
                "status": report_info['status']
            })

            logger.info(f"Generated {report_type} report {report_id}, status: {report_info['status']}")
            return {
                "status": "success",
                "report_id": report_id,
                "report_type": report_type,
                "time_range": time_range,
                "target_areas": target_areas,
                "start_time": report_info['start_time'],
                "end_time": report_info['end_time'],
                "duration_seconds": report_info['duration_seconds'],
                "report_status": report_info['status'],
                "metrics_covered_count": len(report_info['contents']['metrics_covered']),
                "key_findings_count": len(report_info['contents']['key_findings']),
                "recommendations_count": len(report_info['contents']['recommendations']),
                "alerts_count": len(report_info['contents']['alerts_summary'])
            }
        except Exception as e:
            logger.error(f"Error generating {report_type} report: {e}")
            return {"status": "error", "message": str(e), "report_id": "N/A"}

    def get_monitoring_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current monitoring status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'metrics', 'reports')
        Returns:
            Dictionary with monitoring status information
        """
        try:
            metrics_summary = {
                "total_metrics": len(self.metrics),
                "metrics_by_area": {},
                "metrics_by_type": {}
            }

            for m in self.metrics.values():
                metrics_summary['metrics_by_area'][m['target_area']] = metrics_summary['metrics_by_area'].get(m['target_area'], 0) + 1
                metrics_summary['metrics_by_type'][m['metric_type']] = metrics_summary['metrics_by_type'].get(m['metric_type'], 0) + 1

            reports_summary = {
                "total_reports": len(self.reports),
                "reports_by_type": {},
                "recent_reports": sorted(
                    [
                        {
                            "report_id": r['report_id'],
                            "report_type": r['report_type'],
                            "generated_at": r['generated_at'],
                            "status": r['status']
                        }
                        for r in self.reports
                    ],
                    key=lambda x: x['generated_at'],
                    reverse=True
                )[:5]
            }

            for r in self.reports:
                reports_summary['reports_by_type'][r['report_type']] = reports_summary['reports_by_type'].get(r['report_type'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "monitoring_enabled": self.config['monitoring']['enabled'],
                    "default_mode": self.config['monitoring']['default_mode'],
                    "target_areas": self.config['monitoring']['target_areas'],
                    "metrics_summary": {
                        "total_metrics": metrics_summary['total_metrics']
                    },
                    "reports_summary": {
                        "total_reports": reports_summary['total_reports']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "monitoring": {
                        "enabled": self.config['monitoring']['enabled'],
                        "monitoring_modes": self.config['monitoring']['monitoring_modes'],
                        "default_mode": self.config['monitoring']['default_mode'],
                        "monitoring_frequency": self.config['monitoring']['monitoring_frequency'],
                        "monitoring_time": self.config['monitoring']['monitoring_time'],
                        "target_areas": self.config['monitoring']['target_areas'],
                        "monitoring_levels": self.config['monitoring']['monitoring_levels']
                    },
                    "metrics": {
                        "enabled": self.config['metrics']['enabled'],
                        "metric_types": self.config['metrics']['metric_types'],
                        "default_metric": self.config['metrics']['default_metric'],
                        "metric_validation": self.config['metrics']['metric_validation']
                    },
                    "data_collection": {
                        "enabled": self.config['data_collection']['enabled'],
                        "collection_types": self.config['data_collection']['collection_types'],
                        "default_collection": self.config['data_collection']['default_collection'],
                        "collection_validation": self.config['data_collection']['collection_validation']
                    },
                    "analysis": {
                        "enabled": self.config['analysis']['enabled'],
                        "analysis_types": self.config['analysis']['analysis_types'],
                        "default_analysis": self.config['analysis']['default_analysis'],
                        "analysis_validation": self.config['analysis']['analysis_validation']
                    },
                    "reporting": {
                        "enabled": self.config['reporting']['enabled'],
                        "report_types": self.config['reporting']['report_types'],
                        "default_report": self.config['reporting']['default_report'],
                        "report_frequency": self.config['reporting']['report_frequency'],
                        "report_time": self.config['reporting']['report_time'],
                        "distribution_channels": self.config['reporting']['distribution_channels'],
                        "recipients": self.config['reporting']['recipients']
                    },
                    "alerts": {
                        "enabled": self.config['alerts']['enabled'],
                        "alert_types": self.config['alerts']['alert_types'],
                        "alert_channels": self.config['alerts']['alert_channels'],
                        "alert_escalation": self.config['alerts']['alert_escalation'],
                        "thresholds": self.config['alerts']['thresholds']
                    },
                    "metrics_summary": metrics_summary,
                    "reports_summary": reports_summary
                }
            elif scope == "metrics":
                return {
                    "status": "success",
                    "metrics_summary": metrics_summary,
                    "metrics": [
                        {
                            "metric_id": mid,
                            "metric_name": m['metric_name'],
                            "description": m['description'],
                            "target_area": m['target_area'],
                            "metric_type": m['metric_type'],
                            "collection_method": m['collection_method'],
                            "analysis_type": m['analysis_type'],
                            "thresholds": m['thresholds'],
                            "status": m['status'],
                            "version": m['version'],
                            "created_at": m['created_at'],
                            "updated_at": m['updated_at']
                        }
                        for mid, m in self.metrics.items()
                    ]
                }
            elif scope == "reports":
                return {
                    "status": "success",
                    "reports_summary": reports_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting monitoring status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global performance monitoring instance
monitoring = PerformanceMonitoring()
