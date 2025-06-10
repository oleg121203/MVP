import logging
from typing import Dict, Any, List, Optional
import subprocess
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class ScalingManager:
    def __init__(self, config_path: str = 'scaling_config.json'):
        """
        Initialize scaling manager with configuration
        """
        self.config_path = config_path
        self.config = self.load_config()
        self.supported_providers = ['docker', 'kubernetes']
        logger.info("Scaling manager initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load scaling configuration from file or create default if not exists
        """
        default_config = {
            "provider": "docker",
            "min_instances": 1,
            "max_instances": 5,
            "target_cpu_usage": 70.0,
            "target_memory_usage": 80.0,
            "scaling_cooldown": 300,  # seconds
            "health_check_endpoint": "/health",
            "health_check_interval": 30,  # seconds
            "health_check_timeout": 5,  # seconds
            "instance_template": {
                "cpu": 1,
                "memory": "512MB",
                "image": "ventai-app:latest"
            },
            "last_scaling_action": None
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded scaling configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading scaling config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default scaling configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default scaling config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved scaling configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving scaling config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def get_current_instance_count(self) -> int:
        """
        Get current number of running instances based on provider
        """
        provider = self.config.get('provider', 'docker')
        if provider not in self.supported_providers:
            logger.error(f"Unsupported scaling provider: {provider}")
            return 0

        try:
            if provider == 'docker':
                cmd = "docker ps -q --filter name=ventai-app | wc -l"
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                count = int(result.stdout.strip())
                logger.info(f"Current Docker instance count: {count}")
                return count
            elif provider == 'kubernetes':
                cmd = "kubectl get pods -l app=ventai-app -o json | jq '.items | length'"
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                count = int(result.stdout.strip())
                logger.info(f"Current Kubernetes pod count: {count}")
                return count
            return 0
        except Exception as e:
            logger.error(f"Error getting instance count: {e}")
            return 0

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics (CPU, memory) for running instances
        Returns average metrics across all instances
        """
        provider = self.config.get('provider', 'docker')
        if provider not in self.supported_providers:
            return {"status": "error", "message": f"Unsupported provider: {provider}"}

        try:
            if provider == 'docker':
                # Get all container IDs
                cmd_ids = "docker ps -q --filter name=ventai-app"
                result_ids = subprocess.run(cmd_ids, shell=True, check=True, capture_output=True, text=True)
                container_ids = result_ids.stdout.strip().split('\n')
                if not container_ids or container_ids == ['']:
                    return {"status": "error", "message": "No running containers found"}

                total_cpu = 0.0
                total_mem = 0.0
                count = len(container_ids)

                for cid in container_ids:
                    # Get container stats
                    cmd_stats = f"docker stats --no-stream --format '{{{{.CPUPerc}}}}|{{{{.MemPerc}}}}' {cid}"
                    result_stats = subprocess.run(cmd_stats, shell=True, check=True, capture_output=True, text=True)
                    stats = result_stats.stdout.strip().split('|')
                    if len(stats) == 2:
                        cpu = float(stats[0].replace('%', ''))
                        mem = float(stats[1].replace('%', ''))
                        total_cpu += cpu
                        total_mem += mem

                avg_cpu = total_cpu / count if count > 0 else 0.0
                avg_mem = total_mem / count if count > 0 else 0.0

                return {
                    "status": "success",
                    "instance_count": count,
                    "average_cpu_usage": round(avg_cpu, 1),
                    "average_memory_usage": round(avg_mem, 1),
                    "provider": provider
                }
            elif provider == 'kubernetes':
                # Use kubectl top or metrics-server if available
                cmd = "kubectl top pod -l app=ventai-app --sort-by=cpu --format=json"
                try:
                    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                    data = json.loads(result.stdout)
                    pods = data.get('items', [])
                    count = len(pods)

                    if count == 0:
                        return {"status": "error", "message": "No running pods found"}

                    total_cpu = 0.0
                    total_mem = 0.0

                    for pod in pods:
                        cpu_str = pod.get('cpu', '0m').replace('m', '')
                        mem_str = pod.get('memory', '0Mi').replace('Mi', '')
                        try:
                            cpu = float(cpu_str) / 1000.0  # Convert millicores to cores
                            mem = float(mem_str) / 1024.0  # Convert Mi to GiB (assuming 80% of 1GiB limit as usage %)
                            total_cpu += cpu
                            total_mem += mem
                        except ValueError:
                            continue

                    avg_cpu = (total_cpu / count) * 100 if count > 0 else 0.0  # Rough % assuming 1 core limit
                    avg_mem = (total_mem / count) * 100 if count > 0 else 0.0  # Rough % assuming 1GiB limit

                    return {
                        "status": "success",
                        "instance_count": count,
                        "average_cpu_usage": round(avg_cpu, 1),
                        "average_memory_usage": round(avg_mem, 1),
                        "provider": provider
                    }
                except Exception as e:
                    logger.error(f"Error getting Kubernetes metrics: {e}")
                    return {"status": "error", "message": str(e)}
            return {"status": "error", "message": "Provider not implemented"}
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"status": "error", "message": str(e)}

    def scale_instances(self, target_count: int) -> Dict[str, Any]:
        """
        Scale to target number of instances
        Returns result of scaling operation
        """
        provider = self.config.get('provider', 'docker')
        if provider not in self.supported_providers:
            return {"status": "error", "message": f"Unsupported provider: {provider}"}

        current_count = self.get_current_instance_count()
        target_count = max(self.config['min_instances'], min(self.config['max_instances'], target_count))

        if current_count == target_count:
            return {
                "status": "no_change",
                "message": f"Current instance count {current_count} already matches target {target_count}",
                "current_count": current_count,
                "target_count": target_count
            }

        # Check cooldown period
        last_action_str = self.config.get('last_scaling_action')
        if last_action_str:
            try:
                last_action_time = datetime.fromisoformat(last_action_str)
                elapsed = (datetime.now() - last_action_time).total_seconds()
                if elapsed < self.config['scaling_cooldown']:
                    return {
                        "status": "cooldown",
                        "message": f"Scaling cooldown in effect. {int(self.config['scaling_cooldown'] - elapsed)} seconds remaining",
                        "current_count": current_count,
                        "target_count": target_count
                    }
            except ValueError:
                logger.error(f"Invalid last_scaling_action format: {last_action_str}")

        try:
            if provider == 'docker':
                if target_count > current_count:
                    # Scale up
                    for i in range(target_count - current_count):
                        container_name = f"ventai-app-{current_count + i + 1}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        cpu = self.config['instance_template']['cpu']
                        mem = self.config['instance_template']['memory']
                        image = self.config['instance_template']['image']
                        cmd = f"docker run -d --name {container_name} --memory='{mem}' --cpus='{cpu}' {image}"
                        subprocess.run(cmd, shell=True, check=True)
                        logger.info(f"Started new container {container_name}")
                else:
                    # Scale down
                    containers_to_remove = current_count - target_count
                    # Get list of containers to stop
                    cmd_list = f"docker ps --filter name=ventai-app --format '{{{{.Names}}}}' | tail -n {containers_to_remove}"
                    result = subprocess.run(cmd_list, shell=True, check=True, capture_output=True, text=True)
                    container_names = result.stdout.strip().split('\n')
                    
                    for name in container_names:
                        if name:
                            cmd_stop = f"docker stop {name}"
                            cmd_rm = f"docker rm {name}"
                            subprocess.run(cmd_stop, shell=True, check=True)
                            subprocess.run(cmd_rm, shell=True, check=True)
                            logger.info(f"Stopped and removed container {name}")

                # Update last scaling action time
                self.config['last_scaling_action'] = datetime.now().isoformat()
                self.save_config()

                return {
                    "status": "success",
                    "message": f"Scaled from {current_count} to {target_count} instances",
                    "current_count": self.get_current_instance_count(),
                    "target_count": target_count,
                    "provider": provider
                }
            elif provider == 'kubernetes':
                # Use kubectl to scale deployment
                cmd = f"kubectl scale deployment ventai-app --replicas={target_count}"
                subprocess.run(cmd, shell=True, check=True)
                logger.info(f"Scaled Kubernetes deployment to {target_count} replicas")

                # Update last scaling action time
                self.config['last_scaling_action'] = datetime.now().isoformat()
                self.save_config()

                return {
                    "status": "success",
                    "message": f"Scaled from {current_count} to {target_count} replicas",
                    "current_count": self.get_current_instance_count(),
                    "target_count": target_count,
                    "provider": provider
                }
            return {"status": "error", "message": "Provider not implemented"}
        except Exception as e:
            logger.error(f"Error scaling instances: {e}")
            return {"status": "error", "message": str(e), "current_count": current_count, "target_count": target_count}

    def autoscale_based_on_metrics(self) -> Dict[str, Any]:
        """
        Automatically scale based on current system metrics
        Returns result of autoscaling decision
        """
        metrics = self.get_system_metrics()
        if metrics['status'] != 'success':
            return metrics

        current_count = metrics['instance_count']
        cpu_usage = metrics['average_cpu_usage']
        mem_usage = metrics['average_memory_usage']
        target_cpu = self.config['target_cpu_usage']
        target_mem = self.config['target_memory_usage']

        # Simple scaling logic based on CPU and memory thresholds
        if cpu_usage > target_cpu * 1.2 or mem_usage > target_mem * 1.2:
            # Scale up if over threshold by 20%
            target_count = min(self.config['max_instances'], current_count + 1)
            logger.info(f"Scaling up due to high resource usage. CPU: {cpu_usage}%, Memory: {mem_usage}%")
            return self.scale_instances(target_count)
        elif cpu_usage < target_cpu * 0.5 and mem_usage < target_mem * 0.5 and current_count > self.config['min_instances']:
            # Scale down if under threshold by 50% and above min instances
            target_count = max(self.config['min_instances'], current_count - 1)
            logger.info(f"Scaling down due to low resource usage. CPU: {cpu_usage}%, Memory: {mem_usage}%")
            return self.scale_instances(target_count)
        else:
            return {
                "status": "no_change",
                "message": f"Resource usage within target range. CPU: {cpu_usage}%, Memory: {mem_usage}%",
                "current_count": current_count,
                "target_cpu": target_cpu,
                "target_memory": target_mem
            }

    def check_instance_health(self) -> Dict[str, Any]:
        """
        Check health of running instances
        Returns health status of instances
        """
        provider = self.config.get('provider', 'docker')
        if provider not in self.supported_providers:
            return {"status": "error", "message": f"Unsupported provider: {provider}"}

        health_endpoint = self.config.get('health_check_endpoint', '/health')
        interval = self.config.get('health_check_interval', 30)
        timeout = self.config.get('health_check_timeout', 5)

        try:
            if provider == 'docker':
                cmd = "docker ps --filter name=ventai-app --format '{{.Names}}|{{.Ports}}'"
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                containers = result.stdout.strip().split('\n')
                if not containers or containers == ['']:
                    return {"status": "error", "message": "No running containers found"}

                health_status = []
                unhealthy_containers = []

                for container in containers:
                    if not container:
                        continue
                    parts = container.split('|')
                    if len(parts) < 2:
                        continue
                    name = parts[0]
                    port_info = parts[1]
                    # Extract port if available
                    port = None
                    if '->' in port_info:
                        port_str = port_info.split('->')[0].split(':')[-1]
                        try:
                            port = int(port_str)
                        except ValueError:
                            pass
                    
                    if port:
                        # Try to hit health endpoint
                        import requests
                        try:
                            response = requests.get(f"http://localhost:{port}{health_endpoint}", timeout=timeout)
                            if response.status_code == 200:
                                health_status.append({"name": name, "status": "healthy", "port": port})
                            else:
                                health_status.append({"name": name, "status": "unhealthy", "port": port, "reason": f"Status code {response.status_code}"})
                                unhealthy_containers.append(name)
                        except requests.RequestException as e:
                            health_status.append({"name": name, "status": "unhealthy", "port": port, "reason": str(e)})
                            unhealthy_containers.append(name)
                    else:
                        health_status.append({"name": name, "status": "unknown", "port": None, "reason": "Port not found"})
                        unhealthy_containers.append(name)

                # Restart unhealthy containers
                for name in unhealthy_containers:
                    try:
                        cmd_restart = f"docker restart {name}"
                        subprocess.run(cmd_restart, shell=True, check=True)
                        logger.info(f"Restarted unhealthy container {name}")
                        # Update status
                        for status in health_status:
                            if status['name'] == name:
                                status['action'] = 'restarted'
                    except Exception as e:
                        logger.error(f"Error restarting container {name}: {e}")
                        for status in health_status:
                            if status['name'] == name:
                                status['action'] = f'failed to restart: {str(e)}'

                return {
                    "status": "success",
                    "message": f"Health check completed for {len(health_status)} containers",
                    "instance_count": len(health_status),
                    "healthy_count": sum(1 for s in health_status if s['status'] == 'healthy'),
                    "unhealthy_count": len(unhealthy_containers),
                    "details": health_status,
                    "provider": provider
                }
            elif provider == 'kubernetes':
                # Use kubectl to check pod health
                cmd = "kubectl get pods -l app=ventai-app -o json"
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                data = json.loads(result.stdout)
                pods = data.get('items', [])

                if not pods:
                    return {"status": "error", "message": "No running pods found"}

                health_status = []
                unhealthy_pods = []

                for pod in pods:
                    name = pod['metadata']['name']
                    status = pod['status']['phase']
                    conditions = pod['status'].get('conditions', [])
                    ready_condition = next((c for c in conditions if c['type'] == 'Ready'), None)
                    
                    if status == 'Running' and ready_condition and ready_condition['status'] == 'True':
                        health_status.append({"name": name, "status": "healthy", "phase": status})
                    else:
                        health_status.append({"name": name, "status": "unhealthy", "phase": status, "reason": "Not ready"})
                        unhealthy_pods.append(name)

                # Restart unhealthy pods by deleting them (Kubernetes will recreate)
                for name in unhealthy_pods:
                    try:
                        cmd_delete = f"kubectl delete pod {name}"
                        subprocess.run(cmd_delete, shell=True, check=True)
                        logger.info(f"Deleted unhealthy pod {name} for restart")
                        for status in health_status:
                            if status['name'] == name:
                                status['action'] = 'deleted for restart'
                    except Exception as e:
                        logger.error(f"Error deleting pod {name}: {e}")
                        for status in health_status:
                            if status['name'] == name:
                                status['action'] = f'failed to delete: {str(e)}'

                return {
                    "status": "success",
                    "message": f"Health check completed for {len(health_status)} pods",
                    "instance_count": len(health_status),
                    "healthy_count": sum(1 for s in health_status if s['status'] == 'healthy'),
                    "unhealthy_count": len(unhealthy_pods),
                    "details": health_status,
                    "provider": provider
                }
            return {"status": "error", "message": "Provider not implemented"}
        except Exception as e:
            logger.error(f"Error checking instance health: {e}")
            return {"status": "error", "message": str(e)}

    def configure_autoscaling(self, enable: bool = True) -> Dict[str, Any]:
        """
        Enable or disable autoscaling
        Returns configuration status
        """
        # For simplicity, this could be expanded to set up cron jobs or a separate monitoring service
        update = {"autoscaling_enabled": enable}
        if self.update_config(update):
            return {
                "status": "success",
                "message": f"Autoscaling {'enabled' if enable else 'disabled'}",
                "autoscaling_enabled": enable
            }
        else:
            return {"status": "error", "message": "Failed to update configuration"}

    def get_scaling_status(self) -> Dict[str, Any]:
        """
        Get current scaling status including metrics and configuration
        """
        metrics = self.get_system_metrics()
        if metrics['status'] != 'success':
            metrics = {"instance_count": self.get_current_instance_count(), "average_cpu_usage": "N/A", "average_memory_usage": "N/A"}

        last_action_str = self.config.get('last_scaling_action')
        cooldown_remaining = 0
        if last_action_str:
            try:
                last_action_time = datetime.fromisoformat(last_action_str)
                elapsed = (datetime.now() - last_action_time).total_seconds()
                cooldown_remaining = max(0, self.config['scaling_cooldown'] - elapsed)
            except ValueError:
                cooldown_remaining = "Invalid timestamp"

        return {
            "status": "success",
            "scaling_enabled": self.config.get('autoscaling_enabled', False),
            "provider": self.config.get('provider', 'docker'),
            "instance_count": metrics.get('instance_count', 0),
            "average_cpu_usage": metrics.get('average_cpu_usage', 'N/A'),
            "average_memory_usage": metrics.get('average_memory_usage', 'N/A'),
            "min_instances": self.config.get('min_instances', 1),
            "max_instances": self.config.get('max_instances', 5),
            "target_cpu_usage": self.config.get('target_cpu_usage', 70.0),
            "target_memory_usage": self.config.get('target_memory_usage', 80.0),
            "last_scaling_action": last_action_str if last_action_str else "Never",
            "cooldown_remaining": round(cooldown_remaining, 0) if isinstance(cooldown_remaining, (int, float)) else cooldown_remaining
        }

# Global scaling manager instance
scaling_manager = ScalingManager()
