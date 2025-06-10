import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { Progress } from '../ui/Progress';

interface MobileDevice {
  id: string;
  device_id: string;
  device_name: string;
  platform: string;
  user_name: string;
  user_role: string;
  is_active: boolean;
  last_sync: string;
}

interface FieldTask {
  id: string;
  title: string;
  description: string;
  status: string;
  progress: number;
  assigned_to: string;
  location: string;
  priority: string;
  due_date: string;
  photos?: string[];
  notes?: string;
}

interface ProjectSummary {
  id: string;
  name: string;
  status: string;
  progress: number;
  tasks_count: number;
  completed_tasks: number;
  location: string;
  estimated_completion: string;
}

interface AIInsight {
  id: string;
  type: string;
  title: string;
  description: string;
  confidence: number;
  priority: string;
  recommendations: string[];
}

const MobileFieldDashboard: React.FC = () => {
  const [devices, setDevices] = useState<MobileDevice[]>([]);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [fieldTasks, setFieldTasks] = useState<FieldTask[]>([]);
  const [aiInsights, setAIInsights] = useState<AIInsight[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'success' | 'error'>('idle');

  // Mock data for demonstration
  const mockDevices: MobileDevice[] = [
    {
      id: '1',
      device_id: 'DEVICE-001',
      device_name: 'iPad Pro - Field Team 1',
      platform: 'iOS',
      user_name: 'John Smith',
      user_role: 'Field Technician',
      is_active: true,
      last_sync: new Date(Date.now() - 5 * 60 * 1000).toISOString()
    },
    {
      id: '2',
      device_id: 'DEVICE-002',
      device_name: 'Samsung Galaxy Tab - Field Team 2',
      platform: 'Android',
      user_name: 'Maria Garcia',
      user_role: 'Senior Technician',
      is_active: true,
      last_sync: new Date(Date.now() - 2 * 60 * 1000).toISOString()
    }
  ];

  const mockProjects: ProjectSummary[] = [
    {
      id: 'proj-001',
      name: 'Office Complex HVAC Installation',
      status: 'In Progress',
      progress: 0.65,
      tasks_count: 12,
      completed_tasks: 8,
      location: 'Kiev, Ukraine',
      estimated_completion: '2025-06-20'
    },
    {
      id: 'proj-002',
      name: 'Residential Building Climate Control',
      status: 'In Progress',
      progress: 0.35,
      tasks_count: 8,
      completed_tasks: 3,
      location: 'Lviv, Ukraine',
      estimated_completion: '2025-06-25'
    }
  ];

  const mockFieldTasks: FieldTask[] = [
    {
      id: 'task-001',
      title: 'Install Main HVAC Unit',
      description: 'Install and configure the main HVAC unit on floor 3',
      status: 'In Progress',
      progress: 0.75,
      assigned_to: 'John Smith',
      location: 'Floor 3, Building A',
      priority: 'High',
      due_date: '2025-06-12',
      photos: ['/images/hvac-install-1.jpg', '/images/hvac-install-2.jpg'],
      notes: 'Unit positioning completed, working on electrical connections'
    },
    {
      id: 'task-002',
      title: 'Ductwork Inspection',
      description: 'Inspect and test all ductwork connections',
      status: 'Pending',
      progress: 0.0,
      assigned_to: 'Maria Garcia',
      location: 'All floors, Building A',
      priority: 'Medium',
      due_date: '2025-06-15'
    },
    {
      id: 'task-003',
      title: 'Temperature Sensor Calibration',
      description: 'Calibrate all temperature sensors and test readings',
      status: 'Completed',
      progress: 1.0,
      assigned_to: 'John Smith',
      location: 'All zones',
      priority: 'Medium',
      due_date: '2025-06-10'
    }
  ];

  const mockAIInsights: AIInsight[] = [
    {
      id: 'insight-001',
      type: 'efficiency',
      title: 'Energy Efficiency Optimization',
      description: 'AI analysis suggests adjusting HVAC settings could reduce energy consumption by 15%',
      confidence: 0.87,
      priority: 'High',
      recommendations: [
        'Reduce cooling temperature by 2°C during non-peak hours',
        'Implement zone-based temperature control',
        'Schedule maintenance for optimal performance'
      ]
    },
    {
      id: 'insight-002',
      type: 'maintenance',
      title: 'Predictive Maintenance Alert',
      description: 'System data indicates potential filter replacement needed in 2 weeks',
      confidence: 0.92,
      priority: 'Medium',
      recommendations: [
        'Schedule filter replacement for June 24th',
        'Order replacement filters now',
        'Check air quality sensors'
      ]
    }
  ];

  // Simulate data sync
  const performSync = async (deviceId?: string) => {
    setSyncStatus('syncing');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Update last sync time for device
      if (deviceId) {
        setDevices(prev => prev.map(device => 
          device.id === deviceId 
            ? { ...device, last_sync: new Date().toISOString() }
            : device
        ));
      }
      
      setSyncStatus('success');
      setTimeout(() => setSyncStatus('idle'), 3000);
    } catch (error) {
      setSyncStatus('error');
      setTimeout(() => setSyncStatus('idle'), 3000);
    }
  };

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return 'bg-green-500';
      case 'in progress': return 'bg-blue-500';
      case 'pending': return 'bg-yellow-500';
      case 'blocked': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  // Get priority color
  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  // Format time ago
  const formatTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return `${Math.floor(diffMins / 1440)}d ago`;
  };

  useEffect(() => {
    // Initialize with mock data
    setDevices(mockDevices);
    setProjects(mockProjects);
    setFieldTasks(mockFieldTasks);
    setAIInsights(mockAIInsights);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Mobile Field Management</h1>
          <p className="text-gray-600">Monitor field operations and mobile device status</p>
        </div>

        {/* Sync Status Bar */}
        {syncStatus !== 'idle' && (
          <div className={`mb-6 p-4 rounded-lg ${
            syncStatus === 'syncing' ? 'bg-blue-50 border-blue-200' :
            syncStatus === 'success' ? 'bg-green-50 border-green-200' :
            'bg-red-50 border-red-200'
          } border`}>
            <div className="flex items-center space-x-2">
              {syncStatus === 'syncing' && (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-blue-800">Syncing data...</span>
                </>
              )}
              {syncStatus === 'success' && (
                <>
                  <div className="h-4 w-4 bg-green-600 rounded-full"></div>
                  <span className="text-green-800">Sync completed successfully!</span>
                </>
              )}
              {syncStatus === 'error' && (
                <>
                  <div className="h-4 w-4 bg-red-600 rounded-full"></div>
                  <span className="text-red-800">Sync failed. Please try again.</span>
                </>
              )}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Mobile Devices */}
          <div className="xl:col-span-1">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>Mobile Devices ({devices.length})</CardTitle>
                  <Button
                    onClick={() => performSync()}
                    disabled={syncStatus === 'syncing'}
                    size="sm"
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    Sync All
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {devices.map((device) => (
                    <div key={device.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="font-semibold">{device.device_name}</h3>
                          <p className="text-sm text-gray-600">{device.user_name}</p>
                          <p className="text-xs text-gray-500">{device.user_role}</p>
                        </div>
                        <div className="flex flex-col items-end space-y-1">
                          <Badge className={device.is_active ? 'bg-green-500' : 'bg-gray-500'}>
                            {device.is_active ? 'Online' : 'Offline'}
                          </Badge>
                          <span className="text-xs text-gray-500">{device.platform}</span>
                        </div>
                      </div>
                      
                      <div className="text-xs text-gray-500 mb-2">
                        Last sync: {formatTimeAgo(device.last_sync)}
                      </div>
                      
                      <Button
                        onClick={() => performSync(device.id)}
                        disabled={syncStatus === 'syncing'}
                        variant="outline"
                        size="sm"
                        className="w-full"
                      >
                        Sync Device
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* AI Insights */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {aiInsights.map((insight) => (
                    <div key={insight.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-semibold text-sm">{insight.title}</h3>
                        <Badge className={getPriorityColor(insight.priority)}>
                          {insight.priority}
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                      
                      <div className="mb-2">
                        <div className="flex justify-between text-xs mb-1">
                          <span>Confidence</span>
                          <span>{Math.round(insight.confidence * 100)}%</span>
                        </div>
                        <Progress value={insight.confidence * 100} className="h-2" />
                      </div>
                      
                      <div className="text-xs">
                        <p className="font-medium mb-1">Recommendations:</p>
                        <ul className="space-y-1 text-gray-600">
                          {insight.recommendations.slice(0, 2).map((rec, idx) => (
                            <li key={idx}>• {rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Projects and Tasks */}
          <div className="xl:col-span-2">
            {/* Project Summary */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Project Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {projects.map((project) => (
                    <div 
                      key={project.id} 
                      className={`border rounded-lg p-4 cursor-pointer transition-all hover:shadow-md ${
                        selectedProject === project.id ? 'ring-2 ring-blue-500' : ''
                      }`}
                      onClick={() => setSelectedProject(
                        selectedProject === project.id ? null : project.id
                      )}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="font-semibold">{project.name}</h3>
                          <p className="text-sm text-gray-600">{project.location}</p>
                        </div>
                        <Badge className={getStatusColor(project.status)}>
                          {project.status}
                        </Badge>
                      </div>
                      
                      <div className="mb-3">
                        <div className="flex justify-between text-sm mb-1">
                          <span>Progress</span>
                          <span>{Math.round(project.progress * 100)}%</span>
                        </div>
                        <Progress value={project.progress * 100} className="w-full" />
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500">Tasks</p>
                          <p className="font-medium">
                            {project.completed_tasks}/{project.tasks_count}
                          </p>
                        </div>
                        <div>
                          <p className="text-gray-500">Due Date</p>
                          <p className="font-medium">
                            {new Date(project.estimated_completion).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Field Tasks */}
            <Card>
              <CardHeader>
                <CardTitle>Field Tasks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {fieldTasks.map((task) => (
                    <div key={task.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="font-semibold">{task.title}</h3>
                          <p className="text-sm text-gray-600 mb-1">{task.description}</p>
                          <p className="text-xs text-gray-500">
                            📍 {task.location} • Assigned to: {task.assigned_to}
                          </p>
                        </div>
                        <div className="flex flex-col items-end space-y-1">
                          <Badge className={getStatusColor(task.status)}>
                            {task.status}
                          </Badge>
                          <Badge className={getPriorityColor(task.priority)}>
                            {task.priority}
                          </Badge>
                        </div>
                      </div>
                      
                      <div className="mb-3">
                        <div className="flex justify-between text-sm mb-1">
                          <span>Progress</span>
                          <span>{Math.round(task.progress * 100)}%</span>
                        </div>
                        <Progress value={task.progress * 100} className="w-full" />
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500">Due Date</p>
                          <p className="font-medium">{new Date(task.due_date).toLocaleDateString()}</p>
                        </div>
                        {task.photos && task.photos.length > 0 && (
                          <div>
                            <p className="text-gray-500">Photos</p>
                            <p className="font-medium">{task.photos.length} attached</p>
                          </div>
                        )}
                      </div>
                      
                      {task.notes && (
                        <div className="mt-3 p-2 bg-gray-50 rounded text-sm">
                          <p className="font-medium text-gray-700">Notes:</p>
                          <p className="text-gray-600">{task.notes}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileFieldDashboard;
