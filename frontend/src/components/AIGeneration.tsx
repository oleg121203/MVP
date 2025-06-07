import React, { useState } from 'react';
import { apiClient, AITaskResponse } from '@/api/client';
import { useLoading } from '../context/LoadingContext';

interface TaskStatus {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  result?: string;
  error?: string;
}

export const AIGeneration: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [task, setTask] = useState<AITaskResponse | null>(null);
  const [error, setError] = useState('');
  const { withLoading } = useLoading();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setError('');

    try {
      await withLoading(async () => {
        const { id } = await apiClient.generateContent<{ id: string }>({ prompt });
        setTask({ id, status: 'pending' });

        const pollTask = async () => {
          try {
            const status = await apiClient.getTaskStatus<AITaskResponse>(id);
            setTask(status);

            if (status.status === 'processing') {
              setTimeout(pollTask, 1000);
            }
          } catch (err) {
            console.error('Polling error:', err);
            setTask((prev) => ({
              ...prev!,
              status: 'failed',
              error: 'Failed to check status',
            }));
          }
        };

        pollTask();
      });
    } catch (err) {
      setError('Failed to start generation');
      console.error(err);
    }
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg">
      <h2 className="text-xl font-semibold">AI Content Generation</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="prompt" className="block mb-2 font-medium">
            Your prompt:
          </label>
          <textarea
            id="prompt"
            className="w-full p-2 border rounded-md min-h-[100px]"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>

        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:bg-blue-300"
          disabled={!prompt.trim()}
        >
          Generate
        </button>
      </form>

      {error && <div className="text-red-500">{error}</div>}

      {task && (
        <div className="mt-4 p-3 border rounded-md">
          <div className="flex justify-between mb-2">
            <span>Task ID: {task.id}</span>
            <span
              className={`font-medium ${
                {
                  pending: 'text-yellow-500',
                  processing: 'text-blue-500',
                  completed: 'text-green-500',
                  failed: 'text-red-500',
                }[task.status]
              }`}
            >
              {task.status.toUpperCase()}
            </span>
          </div>

          {task.status === 'completed' && task.result && (
            <div className="mt-2 p-2 bg-gray-50 rounded">
              <h3 className="font-medium mb-1">Result:</h3>
              <p className="whitespace-pre-wrap">{task.result}</p>
            </div>
          )}

          {task.error && <div className="mt-2 text-red-500">{task.error}</div>}
        </div>
      )}
    </div>
  );
};
