import { useAuth } from './context/AuthContext';
import { LoginForm } from './components/LoginForm';
import { ProjectList } from './components/ProjectList';
import { AIGeneration } from './components/AIGeneration';
import { ErrorNotifications } from './components/ErrorNotifications';
import { LoadingIndicator } from './components/LoadingIndicator';

export default function App() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <LoadingIndicator />
      <ErrorNotifications />
      {isAuthenticated ? (
        <div className="max-w-4xl mx-auto space-y-8">
          <ProjectList />
          <AIGeneration />
        </div>
      ) : (
        <LoginForm />
      )}
    </div>
  );
}
