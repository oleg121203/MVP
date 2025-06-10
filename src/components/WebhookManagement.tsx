import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';

interface WebhookEndpoint {
  id: string;
  name: string;
  url: string;
  event_types: string[];
  is_active: boolean;
  retry_count: number;
  timeout_seconds: number;
  created_at: string;
}

interface WebhookStats {
  total_endpoints: number;
  active_endpoints: number;
  total_deliveries: number;
  successful_deliveries: number;
  failed_deliveries: number;
  average_response_time: number;
}

interface CreateWebhookForm {
  name: string;
  url: string;
  event_types: string[];
  secret_key: string;
  retry_count: number;
  timeout_seconds: number;
}

const WebhookManagement: React.FC = () => {
  const [webhooks, setWebhooks] = useState<WebhookEndpoint[]>([]);
  const [stats, setStats] = useState<WebhookStats | null>(null);
  const [availableEvents, setAvailableEvents] = useState<string[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [testingWebhook, setTestingWebhook] = useState<string | null>(null);
  const [createForm, setCreateForm] = useState<CreateWebhookForm>({
    name: '',
    url: '',
    event_types: [],
    secret_key: '',
    retry_count: 3,
    timeout_seconds: 30
  });

  // Fetch webhooks
  const fetchWebhooks = async () => {
    try {
      const response = await fetch('/api/webhooks/endpoints');
      if (response.ok) {
        const data = await response.json();
        setWebhooks(data);
      }
    } catch (error) {
      console.error('Failed to fetch webhooks:', error);
    }
  };

  // Fetch webhook statistics
  const fetchStats = async () => {
    try {
      const response = await fetch('/api/webhooks/stats');
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Failed to fetch webhook stats:', error);
    }
  };

  // Fetch available event types
  const fetchEventTypes = async () => {
    try {
      const response = await fetch('/api/webhooks/events/types');
      if (response.ok) {
        const data = await response.json();
        setAvailableEvents(data);
      }
    } catch (error) {
      console.error('Failed to fetch event types:', error);
    }
  };

  // Create new webhook
  const createWebhook = async () => {
    try {
      const response = await fetch('/api/webhooks/endpoints', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(createForm)
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setShowCreateForm(false);
          setCreateForm({
            name: '',
            url: '',
            event_types: [],
            secret_key: '',
            retry_count: 3,
            timeout_seconds: 30
          });
          fetchWebhooks();
          fetchStats();
        }
      }
    } catch (error) {
      console.error('Failed to create webhook:', error);
    }
  };

  // Delete webhook
  const deleteWebhook = async (webhookId: string) => {
    if (!confirm('Are you sure you want to delete this webhook?')) return;

    try {
      const response = await fetch(`/api/webhooks/endpoints/${webhookId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchWebhooks();
        fetchStats();
      }
    } catch (error) {
      console.error('Failed to delete webhook:', error);
    }
  };

  // Test webhook
  const testWebhook = async (webhookId: string) => {
    setTestingWebhook(webhookId);
    try {
      const response = await fetch('/api/webhooks/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          endpoint_id: webhookId,
          event_type: 'project.created',
          test_data: {
            id: 'test-project-123',
            name: 'Test HVAC Project',
            status: 'created',
            client_id: 'test-client',
            timestamp: new Date().toISOString()
          }
        })
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.success ? 'Test webhook sent successfully!' : 'Failed to send test webhook');
      }
    } catch (error) {
      console.error('Failed to test webhook:', error);
      alert('Failed to send test webhook');
    } finally {
      setTestingWebhook(null);
    }
  };

  // Handle form input changes
  const handleFormChange = (field: keyof CreateWebhookForm, value: any) => {
    setCreateForm(prev => ({ ...prev, [field]: value }));
  };

  // Toggle event type selection
  const toggleEventType = (eventType: string) => {
    setCreateForm(prev => ({
      ...prev,
      event_types: prev.event_types.includes(eventType)
        ? prev.event_types.filter(et => et !== eventType)
        : [...prev.event_types, eventType]
    }));
  };

  // Format event type for display
  const formatEventType = (eventType: string) => {
    return eventType.split('.').map(part => 
      part.charAt(0).toUpperCase() + part.slice(1)
    ).join(' ');
  };

  useEffect(() => {
    fetchWebhooks();
    fetchStats();
    fetchEventTypes();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Webhook Management</h1>
              <p className="text-gray-600">Manage external integrations and webhook endpoints</p>
            </div>
            <Button
              onClick={() => setShowCreateForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              Add Webhook
            </Button>
          </div>
        </div>

        {/* Statistics Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-blue-600">{stats.total_endpoints}</div>
                <div className="text-sm text-gray-600">Total Endpoints</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-green-600">{stats.active_endpoints}</div>
                <div className="text-sm text-gray-600">Active Endpoints</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-purple-600">{stats.total_deliveries}</div>
                <div className="text-sm text-gray-600">Total Deliveries</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-green-600">{stats.successful_deliveries}</div>
                <div className="text-sm text-gray-600">Successful</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-red-600">{stats.failed_deliveries}</div>
                <div className="text-sm text-gray-600">Failed</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Webhooks List */}
        <Card>
          <CardHeader>
            <CardTitle>Webhook Endpoints ({webhooks.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {webhooks.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No webhook endpoints configured. Create your first webhook to get started.
              </div>
            ) : (
              <div className="space-y-4">
                {webhooks.map((webhook) => (
                  <div key={webhook.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-semibold text-lg">{webhook.name}</h3>
                        <p className="text-gray-600 text-sm">{webhook.url}</p>
                        <p className="text-gray-500 text-xs">
                          Created: {new Date(webhook.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={webhook.is_active ? 'bg-green-500' : 'bg-gray-500'}>
                          {webhook.is_active ? 'Active' : 'Inactive'}
                        </Badge>
                      </div>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-700 mb-2">Event Types:</p>
                      <div className="flex flex-wrap gap-2">
                        {webhook.event_types.map((eventType) => (
                          <Badge key={eventType} variant="outline" className="text-xs">
                            {formatEventType(eventType)}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 text-sm">
                      <div>
                        <span className="text-gray-500">Retry Count:</span>
                        <span className="ml-2 font-medium">{webhook.retry_count}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Timeout:</span>
                        <span className="ml-2 font-medium">{webhook.timeout_seconds}s</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Status:</span>
                        <span className={`ml-2 font-medium ${webhook.is_active ? 'text-green-600' : 'text-gray-600'}`}>
                          {webhook.is_active ? 'Enabled' : 'Disabled'}
                        </span>
                      </div>
                    </div>

                    <div className="flex space-x-2">
                      <Button
                        onClick={() => testWebhook(webhook.id)}
                        disabled={testingWebhook === webhook.id}
                        variant="outline"
                        size="sm"
                      >
                        {testingWebhook === webhook.id ? 'Testing...' : 'Test'}
                      </Button>
                      <Button
                        onClick={() => deleteWebhook(webhook.id)}
                        variant="outline"
                        size="sm"
                        className="text-red-600 border-red-600 hover:bg-red-50"
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Create Webhook Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-2xl font-bold">Create Webhook Endpoint</h2>
                  <Button
                    onClick={() => setShowCreateForm(false)}
                    variant="outline"
                    size="sm"
                  >
                    Cancel
                  </Button>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Name
                    </label>
                    <input
                      type="text"
                      value={createForm.name}
                      onChange={(e) => handleFormChange('name', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                      placeholder="My Integration Webhook"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      URL
                    </label>
                    <input
                      type="url"
                      value={createForm.url}
                      onChange={(e) => handleFormChange('url', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                      placeholder="https://api.example.com/webhooks/ventai"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Secret Key (Optional)
                    </label>
                    <input
                      type="password"
                      value={createForm.secret_key}
                      onChange={(e) => handleFormChange('secret_key', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                      placeholder="webhook_secret_key_123"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Retry Count
                      </label>
                      <input
                        type="number"
                        min="0"
                        max="10"
                        value={createForm.retry_count}
                        onChange={(e) => handleFormChange('retry_count', parseInt(e.target.value))}
                        className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Timeout (seconds)
                      </label>
                      <input
                        type="number"
                        min="5"
                        max="300"
                        value={createForm.timeout_seconds}
                        onChange={(e) => handleFormChange('timeout_seconds', parseInt(e.target.value))}
                        className="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Event Types
                    </label>
                    <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto border border-gray-300 rounded-md p-3">
                      {availableEvents.map((eventType) => (
                        <label key={eventType} className="flex items-center space-x-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={createForm.event_types.includes(eventType)}
                            onChange={() => toggleEventType(eventType)}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm">{formatEventType(eventType)}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="flex space-x-3 pt-4">
                    <Button
                      onClick={createWebhook}
                      disabled={!createForm.name || !createForm.url || createForm.event_types.length === 0}
                      className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                      Create Webhook
                    </Button>
                    <Button
                      onClick={() => setShowCreateForm(false)}
                      variant="outline"
                    >
                      Cancel
                    </Button>
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

export default WebhookManagement;
