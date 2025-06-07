// API Response Types

export interface AnalysisResults {
  compliance_status: string;
  compliance_issues?: string[];
  recommendations?: {
    optimal_system_type?: string;
    energy_savings_potential?: number;
    priority_actions?: string[];
  };
}

export interface ProjectInsights {
  analysis: string;
  optimization: string;
  compliance: string;
}

export interface AuthResponse {
  access_token: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  reply: string;
}

export interface ApiError {
  message: string;
  code?: string;
}
