import React, { useState, useEffect, lazy, Suspense } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { useTranslation } from 'react-i18next';

// Lazy loaded components
const ProjectChatInterface = lazy(() => import('../components/ProjectChatInterface'));
const AnalyticsDashboard = lazy(() => import('../components/AnalyticsDashboard'));

// ... (rest of the code remains the same)

      {/* Project Chat Section */}
      <React.Suspense fallback={<div>Loading Chat...</div>}> 
        <ProjectChatInterface projectId={id} />
      </React.Suspense>

      {/* Analytics Dashboard Section */}
      <div style={themedStyles.card}>
        <div style={themedStyles.sectionHeader}>
          <h3 style={themedStyles.sectionHeading}>{t('Analytics Dashboard')}</h3>
        </div>
        <React.Suspense fallback={<div>Loading Dashboard...</div>}>
          <AnalyticsDashboard projectId={id} />
        </React.Suspense>
      </div>
    </div>
// ... (rest of the code remains the same)