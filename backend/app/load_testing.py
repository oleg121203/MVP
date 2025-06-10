import logging
from typing import Dict, Any, List, Optional
import subprocess
import json
import os
from datetime import datetime
import time
import threading
import requests
import statistics

logger = logging.getLogger(__name__)

class LoadTester:
    def __init__(self, config_path: str = 'load_test_config.json'):
        """
        Initialize load tester with configuration
        """
        self.config_path = config_path
        self.config = self.load_config()
        self.test_results = []
        self.is_running = False
        logger.info("Load tester initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load load testing configuration from file or create default if not exists
        """
        default_config = {
            "target_url": "http://localhost:8000",
            "endpoints": [
                {"path": "/api/v1/projects", "method": "GET", "weight": 40},
                {"path": "/api/v1/financials/transactions", "method": "GET", "weight": 30},
                {"path": "/api/v1/financials/forecast", "method": "POST", "weight": 20},
                {"path": "/api/v1/projects/summary", "method": "GET", "weight": 10}
            ],
            "concurrent_users": 100,
            "requests_per_user": 100,
            "ramp_up_time": 30,  # seconds
            "test_duration": 300,  # seconds
            "timeout": 5,  # seconds
            "auth_token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  # Replace with valid token
            "output_dir": "load_test_results",
            "last_test": None
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded load testing configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading load test config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default load test configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default load test config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved load testing configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving load test config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def run_load_test(self, test_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run a load test with configured parameters
        Returns test results summary
        """
        if self.is_running:
            return {"status": "error", "message": "Load test already in progress"}

        self.is_running = True
        start_time = datetime.now()
        test_name = test_name or start_time.strftime("load_test_%Y%m%d_%H%M%S")
        logger.info(f"Starting load test: {test_name}")

        try:
            # Create output directory
            output_dir = os.path.join(self.config['output_dir'], test_name)
            os.makedirs(output_dir, exist_ok=True)

            # Prepare test parameters
            concurrent_users = self.config['concurrent_users']
            requests_per_user = self.config['requests_per_user']
            ramp_up_time = self.config['ramp_up_time']
            test_duration = self.config['test_duration']
            target_url = self.config['target_url']
            timeout = self.config['timeout']
            auth_token = self.config['auth_token']

            # Reset results
            self.test_results = []
            threads = []

            # Calculate requests per endpoint based on weights
            total_weight = sum(ep['weight'] for ep in self.config['endpoints'])
            endpoint_requests = []
            total_requests = concurrent_users * requests_per_user
            for endpoint in self.config['endpoints']:
                weight_ratio = endpoint['weight'] / total_weight
                endpoint_total = int(total_requests * weight_ratio)
                per_user = max(1, endpoint_total // concurrent_users)
                endpoint_requests.append({
                    'path': endpoint['path'],
                    'method': endpoint['method'],
                    'count': per_user
                })

            def user_simulation(user_id: int):
                user_results = []
                session = requests.Session()
                session.headers.update({'Authorization': auth_token})

                # Ramp up delay
                delay = (ramp_up_time * user_id) / concurrent_users
                time.sleep(delay)

                start_time = time.time()
                while time.time() - start_time < test_duration:
                    for endpoint in endpoint_requests:
                        for _ in range(endpoint['count']):
                            if time.time() - start_time >= test_duration:
                                break
                            try:
                                url = f"{target_url}{endpoint['path']}"
                                start_req = time.time()
                                if endpoint['method'].upper() == 'GET':
                                    response = session.get(url, timeout=timeout)
                                elif endpoint['method'].upper() == 'POST':
                                    response = session.post(url, json={}, timeout=timeout)
                                else:
                                    continue

                                latency = (time.time() - start_req) * 1000  # Convert to ms
                                user_results.append({
                                    'endpoint': endpoint['path'],
                                    'method': endpoint['method'],
                                    'status_code': response.status_code,
                                    'latency_ms': latency,
                                    'timestamp': datetime.now().isoformat(),
                                    'user_id': user_id
                                })
                            except requests.exceptions.RequestException as e:
                                user_results.append({
                                    'endpoint': endpoint['path'],
                                    'method': endpoint['method'],
                                    'status_code': -1,
                                    'latency_ms': 0,
                                    'error': str(e),
                                    'timestamp': datetime.now().isoformat(),
                                    'user_id': user_id
                                })
                            # Small delay to prevent overwhelming server
                            time.sleep(0.1)

                self.test_results.extend(user_results)
                logger.info(f"User {user_id} completed simulation")

            # Start user simulation threads
            logger.info(f"Starting load test with {concurrent_users} concurrent users")
            for i in range(concurrent_users):
                t = threading.Thread(target=user_simulation, args=(i,))
                t.daemon = True
                threads.append(t)
                t.start()

            # Wait for test duration plus ramp up
            wait_time = test_duration + ramp_up_time + 10
            logger.info(f"Waiting for test completion (estimated {wait_time} seconds)")
            for t in threads:
                t.join(timeout=wait_time / concurrent_users)

            self.is_running = False
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Load test {test_name} completed in {duration:.2f} seconds")

            # Process and save results
            summary = self.process_results()
            summary['test_name'] = test_name
            summary['start_time'] = start_time.isoformat()
            summary['end_time'] = end_time.isoformat()
            summary['duration_seconds'] = duration
            summary['concurrent_users'] = concurrent_users
            summary['total_requests'] = len(self.test_results)

            # Save detailed results
            results_file = os.path.join(output_dir, 'detailed_results.json')
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2)

            # Save summary
            summary_file = os.path.join(output_dir, 'summary.json')
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)

            # Update last test in config
            self.config['last_test'] = {
                'name': test_name,
                'start_time': start_time.isoformat(),
                'duration': duration,
                'requests': len(self.test_results),
                'success_rate': summary['overall']['success_rate'],
                'avg_latency_ms': summary['overall']['average_latency_ms']
            }
            self.save_config()

            return summary
        except Exception as e:
            self.is_running = False
            logger.error(f"Error running load test: {e}")
            return {"status": "error", "message": str(e)}

    def process_results(self) -> Dict[str, Any]:
        """
        Process test results and generate summary statistics
        """
        if not self.test_results:
            return {"status": "error", "message": "No test results to process"}

        summary = {
            "overall": {
                "total_requests": len(self.test_results),
                "successful_requests": 0,
                "failed_requests": 0,
                "success_rate": 0.0,
                "average_latency_ms": 0.0,
                "median_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "status_codes": {},
                "errors": {}
            },
            "by_endpoint": {}
        }

        # Group results by endpoint
        endpoint_results = {}
        for result in self.test_results:
            key = f"{result['method']} {result['endpoint']}"
            if key not in endpoint_results:
                endpoint_results[key] = {
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                    "latencies": [],
                    "status_codes": {},
                    "errors": {}
                }

            ep = endpoint_results[key]
            ep['total_requests'] += 1
            status_code = result['status_code']
            ep['status_codes'][status_code] = ep['status_codes'].get(status_code, 0) + 1

            if status_code == 200 or status_code == 201:
                ep['successful_requests'] += 1
                ep['latencies'].append(result['latency_ms'])
            else:
                ep['failed_requests'] += 1
                if 'error' in result:
                    error_msg = result['error'][:100]  # Truncate long errors
                    ep['errors'][error_msg] = ep['errors'].get(error_msg, 0) + 1

        # Calculate statistics for each endpoint
        for key, ep in endpoint_results.items():
            latencies = ep['latencies']
            total = ep['total_requests']
            success = ep['successful_requests']
            failed = ep['failed_requests']

            summary['by_endpoint'][key] = {
                "total_requests": total,
                "successful_requests": success,
                "failed_requests": failed,
                "success_rate": (success / total * 100) if total > 0 else 0.0,
                "average_latency_ms": statistics.mean(latencies) if latencies else 0.0,
                "median_latency_ms": statistics.median(latencies) if latencies else 0.0,
                "p95_latency_ms": statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else (max(latencies) if latencies else 0.0),
                "p99_latency_ms": statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else (max(latencies) if latencies else 0.0),
                "status_codes": ep['status_codes'],
                "errors": ep['errors']
            }

        # Calculate overall statistics
        all_latencies = []
        overall = summary['overall']
        for result in self.test_results:
            status_code = result['status_code']
            overall['status_codes'][status_code] = overall['status_codes'].get(status_code, 0) + 1

            if status_code == 200 or status_code == 201:
                overall['successful_requests'] += 1
                all_latencies.append(result['latency_ms'])
            else:
                overall['failed_requests'] += 1
                if 'error' in result:
                    error_msg = result['error'][:100]
                    overall['errors'][error_msg] = overall['errors'].get(error_msg, 0) + 1

        overall['success_rate'] = (overall['successful_requests'] / overall['total_requests'] * 100) if overall['total_requests'] > 0 else 0.0
        overall['average_latency_ms'] = statistics.mean(all_latencies) if all_latencies else 0.0
        overall['median_latency_ms'] = statistics.median(all_latencies) if all_latencies else 0.0
        overall['p95_latency_ms'] = statistics.quantiles(all_latencies, n=20)[18] if len(all_latencies) >= 20 else (max(all_latencies) if all_latencies else 0.0)
        overall['p99_latency_ms'] = statistics.quantiles(all_latencies, n=100)[98] if len(all_latencies) >= 100 else (max(all_latencies) if all_latencies else 0.0)

        return summary

    def get_last_test_results(self) -> Dict[str, Any]:
        """
        Get results from the last test run
        """
        last_test = self.config.get('last_test')
        if not last_test:
            return {"status": "error", "message": "No previous test results found"}

        output_dir = os.path.join(self.config['output_dir'], last_test['name'])
        summary_file = os.path.join(output_dir, 'summary.json')

        if os.path.exists(summary_file):
            try:
                with open(summary_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading last test results: {e}")
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": f"Summary file not found at {summary_file}"}

    def get_test_status(self) -> Dict[str, Any]:
        """
        Get current status of load testing
        """
        return {
            "is_running": self.is_running,
            "last_test": self.config.get('last_test', {}),
            "current_results_count": len(self.test_results) if self.is_running else 0
        }

# Global load tester instance
load_tester = LoadTester()
