import React, { useState } from 'react';
import Input from './ui/Input';
import Button from './ui/Button';
import { useLocalization } from '../context/LocalizationContext';

const ProjectForm = ({ onSave, onCancel, project = null, isLoading = false }) => {
  const { t } = useLocalization();
  const [name, setName] = useState(project?.name || '');
  const [description, setDescription] = useState(project?.description || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      onSave({ name, description });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <div>
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            {t('Project Name')}
          </label>
          <Input
            type="text"
            name="name"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={t('Example: Victoria Gardens Mall')}
            required
          />
        </div>
        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            {t('Description')}
          </label>
          <textarea
            name="description"
            id="description"
            rows="4"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border rounded-md focus:outline-none border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
            placeholder={t('Brief project description, purpose, or address')}
          ></textarea>
        </div>
      </div>
      <div className="mt-6 flex justify-end gap-3">
        <Button type="button" onClick={onCancel} variant="secondary">
          {t('Cancel')}
        </Button>
        <Button type="submit" variant="primary" disabled={isLoading}>
          {isLoading ? t('Saving...') : t('Save')}
        </Button>
      </div>
    </form>
  );
};

export default ProjectForm;
