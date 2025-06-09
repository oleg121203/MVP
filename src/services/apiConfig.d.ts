interface ApiConfig {
  FASTAPI_BASE_URL: string;
  DJANGO_BASE_URL: string;
  LOGIN_ENDPOINT: string;
  AI_DASHBOARD_ENDPOINT: string;
}

declare const config: ApiConfig;
export default config;
