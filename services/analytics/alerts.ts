import { ProjectMetrics } from '../../interfaces/analytics';

interface RedisConnectionManager {
  set(key: string, value: string, ttl: number): Promise<void>;
}

interface WebhookClient {
  send(payload: unknown): Promise<void>;
}

interface EmailNotification {
  to: string;
  subject: string;
  body: string;
}

interface NotificationService {
  sendEmail(notification: EmailNotification): Promise<void>;
}

export class PerformanceAlertService {
  private redis: RedisConnectionManager;
  private webhookClient: WebhookClient;
  private notificationService: NotificationService;
  private alertThresholds = {
    costVariance: -15, // percentage
    highRiskItems: 3,
    complianceScore: 70,
    carbonFootprint: 10000 // kgCO2
  };

  constructor(
    redis: RedisConnectionManager, 
    webhookClient: WebhookClient,
    notificationService: NotificationService
  ) {
    this.redis = redis;
    this.webhookClient = webhookClient;
    this.notificationService = notificationService;
  }

  async checkForAlerts(metrics: ProjectMetrics): Promise<void> {
    const alerts: string[] = [];

    // Cost variance alert
    if (metrics.costAnalysis.variance < this.alertThresholds.costVariance) {
      alerts.push(`Cost variance exceeded threshold: ${metrics.costAnalysis.variance}% (Threshold: ${this.alertThresholds.costVariance}%)`);
    }

    // Risk assessment alerts
    if (metrics.timelineMetrics.riskAssessment?.highRiskItems >= this.alertThresholds.highRiskItems) {
      alerts.push(`High risk items exceeded threshold: ${metrics.timelineMetrics.riskAssessment.highRiskItems} (Threshold: ${this.alertThresholds.highRiskItems})`);
    }

    // Quality alerts
    if (metrics.qualityMetrics.complianceScore < this.alertThresholds.complianceScore) {
      alerts.push(`Compliance score below threshold: ${metrics.qualityMetrics.complianceScore} (Threshold: ${this.alertThresholds.complianceScore})`);
    }

    // Sustainability alerts
    if (metrics.sustainabilityMetrics?.carbonFootprint && 
        metrics.sustainabilityMetrics.carbonFootprint > this.alertThresholds.carbonFootprint) {
      alerts.push(`Carbon footprint exceeded threshold: ${metrics.sustainabilityMetrics.carbonFootprint}kg (Threshold: ${this.alertThresholds.carbonFootprint}kg)`);
    }

    // Optimization opportunity alerts
    if (metrics.costAnalysis.optimizationOpportunities.length > 0) {
      const totalSavings = metrics.costAnalysis.optimizationOpportunities
        .reduce((sum: number, opp: { potentialSavings: number }) => sum + opp.potentialSavings, 0);
      
      if (totalSavings > 10000) { // $10,000 threshold
        alerts.push(`Significant optimization opportunities available: Total potential savings $${totalSavings.toLocaleString()}`);
      }
    }

    // Process alerts if any found
    if (alerts.length > 0) {
      await this.processAlerts(metrics.projectId, alerts);
    }
  }

  private async processAlerts(projectId: string, alerts: string[]): Promise<void> {
    // Store in Redis for dashboard display
    await this.redis.set(`alerts:${projectId}`, JSON.stringify({
      timestamp: new Date(),
      alerts
    }), 3600); // 1 hour TTL

    // Send webhook notification
    await this.webhookClient.send({
      event: 'performance_alert',
      projectId,
      alerts,
      timestamp: new Date().toISOString()
    });

    // Email critical alerts
    if (alerts.some(a => a.includes('High risk') || a.includes('Compliance score'))) {
      await this.notificationService.sendEmail({
        to: 'project-managers@ventai.com',
        subject: `Critical Performance Alerts - Project ${projectId}`,
        body: alerts.join('\n\n')
      });
    }
  }
}
