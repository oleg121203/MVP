import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import os
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests

logger = logging.getLogger(__name__)

class FinancialReporting:
    def __init__(self, config_path: str = 'financial_reporting_config.json', reports_dir: str = 'financial_reports'):
        """
        Initialize Financial Reporting module for automated report generation
        """
        self.config_path = config_path
        self.reports_dir = reports_dir
        self.config = self.load_config()
        os.makedirs(self.reports_dir, exist_ok=True)
        logger.info("Financial Reporting module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load financial reporting configuration from file or create default if not exists
        """
        default_config = {
            "report_templates": {
                "monthly_financial_summary": {
                    "name": "Monthly Financial Summary",
                    "frequency": "monthly",
                    "data_sources": ["financial_transactions", "project_data", "budget_forecasts"],
                    "metrics": ["total_revenue", "total_expenses", "net_profit", "budget_variance", "top_projects_by_cost"],
                    "output_formats": ["pdf", "excel"],
                    "distribution_list": ["finance_team", "executives"]
                },
                "quarterly_performance": {
                    "name": "Quarterly Performance Report",
                    "frequency": "quarterly",
                    "data_sources": ["financial_transactions", "project_data", "kpi_metrics"],
                    "metrics": ["quarterly_revenue", "quarterly_expenses", "profit_margin", "project_completion_rate", "roi_analysis"],
                    "output_formats": ["pdf", "ppt"],
                    "distribution_list": ["board_members", "executives"]
                },
                "project_cost_analysis": {
                    "name": "Project Cost Analysis",
                    "frequency": "on_demand",
                    "data_sources": ["project_data", "financial_transactions"],
                    "metrics": ["project_budget", "actual_cost", "cost_variance", "cost_breakdown_by_category", "forecasted_completion_cost"],
                    "output_formats": ["pdf", "excel"],
                    "distribution_list": ["project_managers", "finance_team"]
                }
            },
            "email_settings": {
                "smtp_server": "smtp.example.com",
                "smtp_port": 587,
                "smtp_username": "reports@example.com",
                "smtp_password": "your_password_here",
                "from_address": "reports@example.com"
            },
            "distribution_groups": {
                "finance_team": ["finance1@example.com", "finance2@example.com"],
                "executives": ["exec1@example.com", "exec2@example.com"],
                "board_members": ["board1@example.com", "board2@example.com"],
                "project_managers": ["pm1@example.com", "pm2@example.com"]
            },
            "data_api_endpoint": "http://localhost:8000/api/v1",
            "last_report_generation": {}
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded financial reporting configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading reporting config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default reporting configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default reporting config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved financial reporting configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving reporting config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def fetch_data(self, source: str, time_range: Dict[str, str] = None) -> pd.DataFrame:
        """
        Fetch data from configured API endpoints
        Args:
            source: Data source identifier (e.g., 'financial_transactions', 'project_data')
            time_range: Dictionary with 'start_date' and 'end_date' in 'YYYY-MM-DD' format
        Returns:
            DataFrame with fetched data or empty DataFrame on error
        """
        try:
            api_endpoint = f"{self.config['data_api_endpoint']}/{source.replace('_', '/')}"
            headers = {'Authorization': 'Bearer your_token_here'}  # Replace with actual token mechanism
            params = {}
            if time_range and time_range.get('start_date') and time_range.get('end_date'):
                params['start_date'] = time_range['start_date']
                params['end_date'] = time_range['end_date']

            response = requests.get(api_endpoint, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict) and 'results' in data:
                    return pd.DataFrame(data['results'])
                else:
                    return pd.DataFrame([data])
            else:
                logger.error(f"Failed to fetch data from {source}: Status {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching data from {source}: {e}")
            return pd.DataFrame()

    def generate_report(self, report_type: str, time_period: Dict[str, str] = None, 
                       project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a financial report of specified type
        Args:
            report_type: Type of report to generate (key in report_templates)
            time_period: Dictionary with 'start_date' and 'end_date' for the report period
            project_id: Optional project ID for project-specific reports
        Returns:
            Dictionary with report generation status and file paths if successful
        """
        try:
            if report_type not in self.config['report_templates']:
                return {"status": "error", "message": f"Unknown report type: {report_type}"}

            template = self.config['report_templates'][report_type]
            report_name = template['name']
            logger.info(f"Generating report: {report_name}")

            # Determine time period if not provided
            if not time_period:
                now = datetime.now()
                if template['frequency'] == 'monthly':
                    start_date = (now.replace(day=1) - timedelta(days=30)).strftime('%Y-%m-%d')
                    end_date = now.strftime('%Y-%m-%d')
                elif template['frequency'] == 'quarterly':
                    start_date = (now - timedelta(days=90)).strftime('%Y-%m-%d')
                    end_date = now.strftime('%Y-%m-%d')
                else:  # Default to monthly for on_demand
                    start_date = (now.replace(day=1) - timedelta(days=30)).strftime('%Y-%m-%d')
                    end_date = now.strftime('%Y-%m-%d')
                time_period = {'start_date': start_date, 'end_date': end_date}

            # Fetch required data
            data_sets = {}
            for source in template['data_sources']:
                data_sets[source] = self.fetch_data(source, time_period)
                logger.info(f"Fetched data for {source}: {len(data_sets[source])} records")

            # Calculate metrics
            metrics_data = self.calculate_metrics(data_sets, template['metrics'], time_period, project_id)

            # Generate report files in requested formats
            output_files = []
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_base_name = f"{report_type}_{timestamp}"
            for format_type in template['output_formats']:
                output_path = os.path.join(self.reports_dir, report_base_name + f'.{format_type}')
                # This is a placeholder - in a full implementation, you'd use proper libraries
                # to generate PDF, Excel, PPT etc. Here we'll simulate with a text file
                with open(output_path, 'w') as f:
                    f.write(f"Report: {report_name}\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n")
                    f.write(f"Period: {time_period['start_date']} to {time_period['end_date']}\n")
                    if project_id:
                        f.write(f"Project ID: {project_id}\n")
                    f.write("\nMetrics:\n")
                    for metric, value in metrics_data.items():
                        f.write(f"{metric}: {value}\n")
                output_files.append(output_path)
                logger.info(f"Generated {format_type} report at {output_path}")

            # Update last generation time
            self.config['last_report_generation'][report_type] = datetime.now().isoformat()
            self.save_config()

            return {
                "status": "success",
                "report_type": report_type,
                "report_name": report_name,
                "generated_files": output_files,
                "time_period": time_period,
                "project_id": project_id if project_id else "N/A",
                "metrics_summary": metrics_data
            }
        except Exception as e:
            logger.error(f"Error generating report {report_type}: {e}")
            return {"status": "error", "message": str(e)}

    def calculate_metrics(self, data_sets: Dict[str, pd.DataFrame], metrics: List[str], 
                         time_period: Dict[str, str], project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate requested metrics from the provided data sets
        Args:
            data_sets: Dictionary of data source names to DataFrames
            metrics: List of metric names to calculate
            time_period: Dictionary with start_date and end_date for filtering
            project_id: Optional project ID for filtering
        Returns:
            Dictionary of metric names to calculated values
        """
        try:
            results = {}
            financial_data = data_sets.get('financial_transactions', pd.DataFrame())
            project_data = data_sets.get('project_data', pd.DataFrame())
            forecast_data = data_sets.get('budget_forecasts', pd.DataFrame())

            # Filter by project if specified
            if project_id:
                if not financial_data.empty and 'project_id' in financial_data.columns:
                    financial_data = financial_data[financial_data['project_id'] == project_id]
                if not project_data.empty and 'id' in project_data.columns:
                    project_data = project_data[project_data['id'] == project_id]

            for metric in metrics:
                try:
                    if metric == 'total_revenue' and not financial_data.empty:
                        revenue = financial_data[financial_data['transaction_type'] == 'revenue']['amount'].sum()
                        results[metric] = round(revenue, 2)
                    elif metric == 'total_expenses' and not financial_data.empty:
                        expenses = financial_data[financial_data['transaction_type'] == 'expense']['amount'].sum()
                        results[metric] = round(expenses, 2)
                    elif metric == 'net_profit' and not financial_data.empty:
                        revenue = financial_data[financial_data['transaction_type'] == 'revenue']['amount'].sum()
                        expenses = financial_data[financial_data['transaction_type'] == 'expense']['amount'].sum()
                        results[metric] = round(revenue - expenses, 2)
                    elif metric == 'budget_variance' and not financial_data.empty and not forecast_data.empty:
                        actual_expenses = financial_data[financial_data['transaction_type'] == 'expense']['amount'].sum()
                        budgeted = forecast_data['budgeted_expense'].sum() if 'budgeted_expense' in forecast_data.columns else 0
                        results[metric] = round(actual_expenses - budgeted, 2)
                    elif metric == 'top_projects_by_cost' and not financial_data.empty:
                        project_costs = financial_data.groupby('project_id')['amount'].sum().sort_values(ascending=False).head(5)
                        results[metric] = project_costs.to_dict()
                    elif metric == 'quarterly_revenue' and not financial_data.empty:
                        financial_data['date'] = pd.to_datetime(financial_data['date'])
                        financial_data.set_index('date', inplace=True)
                        revenue = financial_data[financial_data['transaction_type'] == 'revenue'].resample('Q')['amount'].sum()
                        results[metric] = revenue.to_dict()
                    elif metric == 'quarterly_expenses' and not financial_data.empty:
                        financial_data['date'] = pd.to_datetime(financial_data['date'])
                        financial_data.set_index('date', inplace=True)
                        expenses = financial_data[financial_data['transaction_type'] == 'expense'].resample('Q')['amount'].sum()
                        results[metric] = expenses.to_dict()
                    elif metric == 'profit_margin' and not financial_data.empty:
                        revenue = financial_data[financial_data['transaction_type'] == 'revenue']['amount'].sum()
                        expenses = financial_data[financial_data['transaction_type'] == 'expense']['amount'].sum()
                        results[metric] = round((revenue - expenses) / revenue * 100, 2) if revenue > 0 else 0.0
                    elif metric == 'project_completion_rate' and not project_data.empty:
                        completed = len(project_data[project_data['status'] == 'completed'])
                        total = len(project_data)
                        results[metric] = round(completed / total * 100, 2) if total > 0 else 0.0
                    elif metric == 'roi_analysis' and not financial_data.empty and not project_data.empty:
                        project_costs = financial_data.groupby('project_id')['amount'].sum()
                        roi_data = {}
                        for pid, cost in project_costs.items():
                            project = project_data[project_data['id'] == pid]
                            if not project.empty and 'revenue_generated' in project.columns:
                                revenue = project['revenue_generated'].iloc[0]
                                roi = ((revenue - cost) / cost * 100) if cost > 0 else 0.0
                                roi_data[pid] = round(roi, 2)
                        results[metric] = roi_data
                    elif metric == 'project_budget' and not project_data.empty and project_id:
                        results[metric] = float(project_data['budget'].iloc[0]) if 'budget' in project_data.columns else 0.0
                    elif metric == 'actual_cost' and not financial_data.empty and project_id:
                        results[metric] = round(financial_data['amount'].sum(), 2)
                    elif metric == 'cost_variance' and not financial_data.empty and not project_data.empty and project_id:
                        actual = financial_data['amount'].sum()
                        budget = float(project_data['budget'].iloc[0]) if 'budget' in project_data.columns else 0.0
                        results[metric] = round(actual - budget, 2)
                    elif metric == 'cost_breakdown_by_category' and not financial_data.empty and project_id:
                        breakdown = financial_data.groupby('category')['amount'].sum().to_dict()
                        results[metric] = {k: round(v, 2) for k, v in breakdown.items()}
                    elif metric == 'forecasted_completion_cost' and not financial_data.empty and project_id:
                        # Simplified forecast - in reality, you'd integrate with predictive analytics
                        actual = financial_data['amount'].sum()
                        progress = float(project_data['completion_percentage'].iloc[0]) if 'completion_percentage' in project_data.columns else 50.0
                        results[metric] = round(actual / (progress / 100), 2) if progress > 0 else actual * 2
                    else:
                        results[metric] = "Not calculated - insufficient data or unsupported metric"
                except Exception as e:
                    logger.error(f"Error calculating metric {metric}: {e}")
                    results[metric] = f"Error: {str(e)}"

            return results
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return {metric: f"Error: {str(e)}" for metric in metrics}

    def distribute_report(self, report_files: List[str], distribution_lists: List[str]) -> Dict[str, Any]:
        """
        Distribute generated reports to specified distribution lists via email
        Args:
            report_files: List of file paths to attach to the email
            distribution_lists: List of distribution group names to send to
        Returns:
            Dictionary with distribution status
        """
        try:
            email_settings = self.config['email_settings']
            recipients = []
            for dist_list in distribution_lists:
                if dist_list in self.config['distribution_groups']:
                    recipients.extend(self.config['distribution_groups'][dist_list])
                else:
                    logger.warning(f"Distribution list {dist_list} not found in config")

            if not recipients:
                return {"status": "error", "message": "No valid recipients found for distribution"}

            if not report_files:
                return {"status": "error", "message": "No report files provided for distribution"}

            # Prepare email
            msg = MIMEMultipart()
            msg['From'] = email_settings['from_address']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"Financial Report - {datetime.now().strftime('%Y-%m-%d')}"

            body = f"Dear recipients,\n\nPlease find attached the latest financial report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nBest regards,\nVentAI Reporting System"
            msg.attach(MIMEText(body, 'plain'))

            # Attach files
            for file_path in report_files:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)
                else:
                    logger.warning(f"Report file not found for attachment: {file_path}")

            # Send email
            with smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port']) as server:
                server.starttls()
                server.login(email_settings['smtp_username'], email_settings['smtp_password'])
                server.send_message(msg)

            logger.info(f"Report distributed to {len(recipients)} recipients: {', '.join(recipients)}")
            return {
                "status": "success",
                "message": f"Report distributed to {len(recipients)} recipients",
                "recipients": recipients,
                "attached_files": report_files
            }
        except Exception as e:
            logger.error(f"Error distributing report: {e}")
            return {"status": "error", "message": str(e)}

    def schedule_reports(self, report_types: List[str] = None) -> Dict[str, Any]:
        """
        Check configuration and schedule automatic report generation based on frequency
        Args:
            report_types: Optional list of report types to schedule, if None, checks all
        Returns:
            Dictionary with scheduling status
        """
        try:
            if report_types is None:
                report_types = list(self.config['report_templates'].keys())

            scheduled = []
            for rtype in report_types:
                if rtype not in self.config['report_templates']:
                    logger.warning(f"Report type {rtype} not found in templates")
                    continue

                template = self.config['report_templates'][rtype]
                frequency = template['frequency']
                last_gen_str = self.config['last_report_generation'].get(rtype)

                should_generate = False
                now = datetime.now()

                if frequency == 'monthly':
                    if not last_gen_str:
                        should_generate = True
                    else:
                        last_gen = datetime.fromisoformat(last_gen_str)
                        if last_gen.month != now.month or last_gen.year != now.year:
                            should_generate = True
                elif frequency == 'quarterly':
                    if not last_gen_str:
                        should_generate = True
                    else:
                        last_gen = datetime.fromisoformat(last_gen_str)
                        last_quarter = (last_gen.month - 1) // 3
                        current_quarter = (now.month - 1) // 3
                        if last_quarter != current_quarter or last_gen.year != now.year:
                            should_generate = True
                elif frequency == 'on_demand':
                    should_generate = False

                if should_generate:
                    logger.info(f"Scheduling report generation for {rtype} based on {frequency} frequency")
                    result = self.generate_report(rtype)
                    if result['status'] == 'success':
                        dist_result = self.distribute_report(
                            result['generated_files'],
                            template['distribution_list']
                        )
                        scheduled.append({
                            "report_type": rtype,
                            "generated": True,
                            "distributed": dist_result['status'] == 'success',
                            "report_files": result.get('generated_files', []),
                            "distribution_status": dist_result.get('message', 'Not distributed')
                        })
                    else:
                        scheduled.append({
                            "report_type": rtype,
                            "generated": False,
                            "distributed": False,
                            "error": result.get('message', 'Unknown error')
                        })
                else:
                    scheduled.append({
                        "report_type": rtype,
                        "generated": False,
                        "distributed": False,
                        "reason": "Not due for generation based on frequency"
                    })

            return {
                "status": "success",
                "message": f"Checked scheduling for {len(report_types)} report types",
                "scheduled_reports": scheduled
            }
        except Exception as e:
            logger.error(f"Error scheduling reports: {e}")
            return {"status": "error", "message": str(e)}

    def get_reporting_status(self) -> Dict[str, Any]:
        """
        Get current status of financial reporting system
        """
        return {
            "report_templates": {k: v['name'] for k, v in self.config['report_templates'].items()},
            "last_report_generation": self.config['last_report_generation'],
            "distribution_groups": {k: len(v) for k, v in self.config['distribution_groups'].items()},
            "reports_directory": self.reports_dir
        }

# Global financial reporting instance
financial_reporter = FinancialReporting()
