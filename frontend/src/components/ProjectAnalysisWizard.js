// src/components/ProjectAnalysisWizard.js
import React, { useState, useEffect } from 'react';
import { Button, Modal, Input } from './ui'; // Assuming these UI components are available
import { refineAnalysis } from '../services/apiService';
import { useToast } from '../context/ToastContext';
import { useLocalization } from '../context/LocalizationContext';
import './ProjectAnalysisWizard.css'; // CSS file for styling

const ProjectAnalysisWizard = ({ sessionId, questions, onRefine, onComplete, currentAnalysis }) => {
  const [userAnswers, setUserAnswers] = useState({});
  const [isRefining, setIsRefining] = useState(false);
  const { success, error, info, warning } = useToast(); // Added warning
  const { t } = useLocalization();

  // Automatically open modal when questions are present
  const isOpen = questions.length > 0;

  useEffect(() => {
    // Reset answers when questions change (new round of questions)
    // Initialize userAnswers with empty strings for all current questions
    const initialAnswers = {};
    questions.forEach((q) => {
      initialAnswers[q] = '';
    });
    setUserAnswers(initialAnswers);
  }, [questions]);

  const handleAnswerChange = (question, value) => {
    setUserAnswers((prev) => ({ ...prev, [question]: value }));
  };

  const handleSubmitAnswers = async () => {
    // Basic validation: Ensure all questions have an answer (not empty)
    const missingAnswers = questions.filter((q) => !userAnswers[q] || userAnswers[q].trim() === '');
    if (missingAnswers.length > 0) {
      warning(t('Please provide an answer for all questions.')); // Use translated warning
      return;
    }

    setIsRefining(true);
    try {
      // Call onRefine callback from parent, passing the answers
      await onRefine(userAnswers); // Parent component handles API call and state update
    } catch (err) {
      // Error handled by parent, but ensure UI reflects it
      error(t('Failed to submit answers: ') + (err.message || t('Unknown error'))); // Use translated error
    } finally {
      setIsRefining(false);
    }
  };

  // Prevent closing the modal while questions are pending
  const handleClose = () => {
    if (questions.length > 0) {
      info(t('Please answer the questions to complete the analysis.')); // Use translated info
      // Optionally, provide an option to cancel and lose progress
    } else {
      onComplete(); // If no questions, allow closing and signal completion
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title={t('Refine Project Details')}>
      <div className="refinement-wizard-content">
        <p className="mb-4 text-gray-700 dark:text-gray-300">
          {t(
            'The AI needs more information to fully understand your project. Please answer the following questions:'
          )}
        </p>
        {questions.map((q, index) => (
          <div key={index} className="form-group mb-4">
            <label
              htmlFor={`question-${index}`}
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              {q}
            </label>
            <Input
              type="text"
              id={`question-${index}`}
              value={userAnswers[q] || ''}
              onChange={(e) => handleAnswerChange(q, e.target.value)}
              placeholder={t('Your answer...')}
              className="w-full"
              disabled={isRefining}
            />
          </div>
        ))}
        <div className="flex justify-end gap-3 mt-6">
          <Button onClick={handleSubmitAnswers} disabled={isRefining}>
            {isRefining ? t('Submitting...') : t('Submit Answers')}
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default ProjectAnalysisWizard;
