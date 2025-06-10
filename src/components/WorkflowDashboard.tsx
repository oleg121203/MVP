import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { Progress } from '../ui/Progress';

interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  task_count: number;
  estimated_duration: number;
}

interface WorkflowInstance {
  id: string;
  name: string;
  status: string;
  progress: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

interface WorkflowTask {
  id: string;
  name: string;
  status: string;
  priority: number;
  estimated_duration: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
}

interface WorkflowDetail {
  id: string;
  name: string;
  status: string;
  progress: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  tasks: WorkflowTask[];
}

const WorkflowDashboard: React.FC = () => {
  const [templates, setTemplates] = useState<{ [key: string]: WorkflowTemplate }>({});
  const [activeWorkflows, setActiveWorkflows] = useState<WorkflowInstance[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<WorkflowDetail | null>(null);
  const [loading, setLoading] = useState(false);

  // Fetch workflow templates
  const fetchTemplates = async () => {
    try {
      const response = await fetch('/api/workflow/templates');
      const data = await response.json();
      if (data.success) {
        setTemplates(data.templates);
      }
    } catch (error) {
      console.error('Failed to fetch templates:', error);
    }
  };

  // Fetch active workflows
  const fetchActiveWorkflows = async () => {
    try {
      const response = await fetch('/api/workflow/list');
      const data = await response.json();
      setActiveWorkflows(data);
    } catch (error) {
      console.error('Failed to fetch workflows:', error);
    }
  };

  // Create new workflow from template
  const createWorkflow = async (templateId: string) => {
    setLoading(true);
    try {
      const workflowId = `workflow_${Date.now()}`;
      const response = await fetch('/api/workflow/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_id: templateId,
          workflow_id: workflowId,
          context: {
            project_name: `HVAC Project ${Date.now()}`,
            client_id: `CLIENT-${Date.now()}`,
            project_type: 'commercial'
          }
        })
      });
      
      const data = await response.json();
      if (data.success) {
        // Start execution
        await fetch(`/api/workflow/execute/${workflowId}`, {
          method: 'POST'
        });
        
        // Refresh workflows list
        fetchActiveWorkflows();
      }
    } catch (error) {
      console.error('Failed to create workflow:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get workflow details
  const getWorkflowDetails = async (workflowId: string) => {
    try {
      const response = await fetch(`/api/workflow/status/${workflowId}`);
      const data = await response.json();
      setSelectedWorkflow(data);
    } catch (error) {
      console.error('Failed to fetch workflow details:', error);
    }
  };

  // Cancel workflow
  const cancelWorkflow = async (workflowId: string) => {
    try {
      await fetch(`/api/workflow/cancel/${workflowId}`, {
        method: 'POST'
      });
      fetchActiveWorkflows();
      if (selectedWorkflow?.id === workflowId) {
        setSelectedWorkflow(null);
      }
    } catch (error) {
      console.error('Failed to cancel workflow:', error);
    }
  };

  // Status color mapping
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return 'bg-green-500';
      case 'running': return 'bg-blue-500';
      case 'failed': return 'bg-red-500';
      case 'cancelled': return 'bg-gray-500';
      default: return 'bg-yellow-500';
    }
  };

  // Priority color mapping
  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1: return 'bg-red-500 text-white';
      case 2: return 'bg-yellow-500 text-black';
      default: return 'bg-green-500 text-white';
    }
  };

  useEffect(() => {
    fetchTemplates();
    fetchActiveWorkflows();
    
    // Refresh active workflows every 10 seconds
    const interval = setInterval(fetchActiveWorkflows, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Workflow Automation</h1>
          <p className="text-gray-600">Manage and monitor automated HVAC project workflows</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Templates Section */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Workflow Templates</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(templates).map(([id, template]) => (
                    <div key={id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <h3 className="font-semibold text-lg mb-2">{template.name}</h3>
                      <p className="text-gray-600 text-sm mb-3">{template.description}</p>
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-sm text-gray-500">
                          {template.task_count} tasks • {template.estimated_duration}min
                        </span>
                      </div>
                      <Button
                        onClick={() => createWorkflow(id)}
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                      >
                        {loading ? 'Creating...' : 'Start Workflow'}
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Active Workflows Section */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Active Workflows ({activeWorkflows.length})</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {activeWorkflows.length === 0 ? (
                    <div className="text-center py-8 text-gray-500">
                      No active workflows. Start a workflow from the templates.
                    </div>
                  ) : (
                    activeWorkflows.map((workflow) => (
                      <div key={workflow.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <h3 className="font-semibold text-lg">{workflow.name}</h3>
                            <p className="text-gray-500 text-sm">ID: {workflow.id}</p>
                            <p className="text-gray-500 text-sm">
                              Created: {new Date(workflow.created_at).toLocaleString()}
                            </p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getStatusColor(workflow.status)}>
                              {workflow.status}
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="mb-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span>Progress</span>
                            <span>{Math.round(workflow.progress * 100)}%</span>
                          </div>
                          <Progress value={workflow.progress * 100} className="w-full" />
                        </div>

                        <div className="flex space-x-2">
                          <Button
                            onClick={() => getWorkflowDetails(workflow.id)}
                            variant="outline"
                            size="sm"
                          >
                            View Details
                          </Button>
                          {workflow.status === 'RUNNING' && (
                            <Button
                              onClick={() => cancelWorkflow(workflow.id)}
                              variant="outline"
                              size="sm"
                              className="text-red-600 border-red-600 hover:bg-red-50"
                            >
                              Cancel
                            </Button>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Workflow Details Modal/Panel */}
        {selectedWorkflow && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-2xl font-bold">{selectedWorkflow.name}</h2>
                    <p className="text-gray-600">Workflow Details</p>
                  </div>
                  <Button
                    onClick={() => setSelectedWorkflow(null)}
                    variant="outline"
                    size="sm"
                  >
                    Close
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-2">Status</h3>
                    <Badge className={getStatusColor(selectedWorkflow.status)}>
                      {selectedWorkflow.status}
                    </Badge>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-2">Progress</h3>
                    <div className="flex items-center space-x-2">
                      <Progress value={selectedWorkflow.progress * 100} className="flex-1" />
                      <span className="text-sm font-medium">
                        {Math.round(selectedWorkflow.progress * 100)}%
                      </span>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold mb-2">Tasks</h3>
                    <p className="text-lg">{selectedWorkflow.tasks.length}</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-4">Tasks</h3>
                  <div className="space-y-3">
                    {selectedWorkflow.tasks.map((task) => (
                      <div key={task.id} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h4 className="font-semibold">{task.name}</h4>
                            <p className="text-gray-500 text-sm">ID: {task.id}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge className={getPriorityColor(task.priority)}>
                              Priority {task.priority}
                            </Badge>
                            <Badge className={getStatusColor(task.status)}>
                              {task.status}
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="text-sm text-gray-600 mb-2">
                          Estimated: {task.estimated_duration} minutes
                        </div>
                        
                        {task.started_at && (
                          <div className="text-sm text-gray-600">
                            Started: {new Date(task.started_at).toLocaleString()}
                          </div>
                        )}
                        
                        {task.completed_at && (
                          <div className="text-sm text-gray-600">
                            Completed: {new Date(task.completed_at).toLocaleString()}
                          </div>
                        )}
                        
                        {task.error_message && (
                          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                            Error: {task.error_message}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkflowDashboard;
