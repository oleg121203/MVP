import React, { useState } from 'react';
import { useLocalization } from '../context/LocalizationContext';
import { useTheme } from '../context/ThemeContext';

/**
 * Component for collecting user feedback on AI-generated results
 *
 * @param {Object} props Component properties
 * @param {string} props.responseId The unique ID of the AI response being rated
 * @param {string} props.taskType The type of AI task (document_analysis, project_chat, etc.)
 * @param {function} props.onFeedbackSubmit Callback function when feedback is submitted
 * @param {boolean} props.compact Whether to show a compact version of the widget
 * @param {boolean} props.showCommentField Whether to show the comment field initially
 */
const AIFeedbackWidget = ({
  responseId,
  taskType,
  onFeedbackSubmit,
  compact = false,
  showCommentField = false,
}) => {
  const { t } = useLocalization();
  const { theme } = useTheme();

  const [feedbackType, setFeedbackType] = useState(null);
  const [showComment, setShowComment] = useState(showCommentField);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleFeedbackClick = (type) => {
    setFeedbackType(type);

    // Show comment field for negative feedback or error reports
    if (type === 'negative' || type === 'error_report') {
      setShowComment(true);
    }
  };

  const handleSubmit = async () => {
    if (!feedbackType) return;

    setSubmitting(true);
    setError(null);

    try {
      const feedbackData = {
        response_id: responseId,
        feedback_type: feedbackType,
        comment: comment.trim() || null,
        task_type: taskType,
      };

      // Call API endpoint
      const response = await fetch('/api/ai/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      });

      if (!response.ok) {
        throw new Error(`Error submitting feedback: ${response.statusText}`);
      }

      setSubmitted(true);

      // Call callback if provided
      if (onFeedbackSubmit) {
        onFeedbackSubmit(feedbackData);
      }
    } catch (err) {
      console.error('Error submitting feedback:', err);
      setError(err.message || 'Failed to submit feedback');
    } finally {
      setSubmitting(false);
    }
  };

  // If feedback already submitted, show thank you message
  if (submitted) {
    return (
      <div className={`ai-feedback-widget ${compact ? 'compact' : ''} p-2 text-center`}>
        <p className="text-green-600 dark:text-green-400">{t('aiFeedback.thankYou')}</p>
      </div>
    );
  }

  return (
    <div
      className={`ai-feedback-widget ${compact ? 'compact' : ''} border border-gray-200 dark:border-gray-700 rounded-lg p-4 mt-4`}
    >
      <div className="text-center mb-2">
        <p className="text-sm text-gray-600 dark:text-gray-300">{t('aiFeedback.helpUsImprove')}</p>
      </div>

      <div className="flex justify-center space-x-2 mb-3">
        {/* Positive feedback button */}
        <button
          onClick={() => handleFeedbackClick('positive')}
          className={`px-3 py-1 rounded-full text-sm ${
            feedbackType === 'positive'
              ? 'bg-green-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-green-100 dark:hover:bg-green-900'
          }`}
        >
          👍 {t('aiFeedback.helpful')}
        </button>

        {/* Negative feedback button */}
        <button
          onClick={() => handleFeedbackClick('negative')}
          className={`px-3 py-1 rounded-full text-sm ${
            feedbackType === 'negative'
              ? 'bg-red-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-red-100 dark:hover:bg-red-900'
          }`}
        >
          👎 {t('aiFeedback.notHelpful')}
        </button>

        {!compact && (
          <button
            onClick={() => handleFeedbackClick('error_report')}
            className={`px-3 py-1 rounded-full text-sm ${
              feedbackType === 'error_report'
                ? 'bg-yellow-500 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-yellow-100 dark:hover:bg-yellow-900'
            }`}
          >
            🐞 {t('aiFeedback.reportError')}
          </button>
        )}
      </div>

      {/* Comment textarea */}
      {(showComment || !compact) && (
        <div className="mb-3">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder={
              feedbackType === 'error_report'
                ? t('aiFeedback.errorDescription')
                : t('aiFeedback.additionalFeedback')
            }
            className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            rows={3}
          />
        </div>
      )}

      {/* Submit button */}
      <div className="flex justify-end">
        <button
          onClick={handleSubmit}
          disabled={!feedbackType || submitting}
          className={`px-4 py-1 rounded-md text-sm ${
            !feedbackType || submitting
              ? 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
        >
          {submitting ? t('common.submitting') : t('common.submit')}
        </button>
      </div>

      {/* Error message */}
      {error && <div className="mt-2 text-center text-red-500 text-sm">{error}</div>}
    </div>
  );
};

export default AIFeedbackWidget;
