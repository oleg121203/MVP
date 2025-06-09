/**
 * ProjectAnalyticsEngine - Core service for real-time HVAC project analytics
 * @module services/analytics/engine
 * @see VENTAI_ENTERPRISE_PLAN.md [P1.2-T3]
 */

import { RedisConnectionManager } from '../redis/connectionManager';
import { ProjectMetrics } from '../../interfaces/analytics';
import { WebSocketService } from '../websocket';
import * as metrics from 'prom-client';

const analyticsDuration = new metrics.Histogram({
  name: 'analytics_calculation_duration_seconds',
  help: 'Duration of analytics calculations in seconds',
  labelNames: ['projectId']
});

export class ProjectAnalyticsEngine {
  private redisManager: RedisConnectionManager;
  private batchSize = 10;

  constructor(redisManager: RedisConnectionManager) {
    this.redisManager = redisManager;
  }

  /**
   * Get real-time insights for a project
   * @param projectId - UUID of the project
   * @returns Promise<ProjectMetrics>
   */
  async getRealTimeInsights(projectId: string): Promise<ProjectMetrics> {
    const endTimer = analyticsDuration.startTimer({ projectId });
    try {
      const client = await this.redisManager.getConnection();
      try {
        // Check cache first
        const cachedMetrics = await client.get(`project:${projectId}:metrics`);
        if (cachedMetrics) {
          return RedisConnectionManager.deserialize(cachedMetrics);
        }
      } catch (error) {
        console.error('Redis cache error:', error);
      }

      // Calculate and cache if not found or error
      const metrics = await this.calculateAndCacheMetrics(projectId);
      const alerts = await this.getAlerts(projectId);
      await this.broadcastAlerts(projectId, alerts);
      return metrics;
    } finally {
      endTimer();
    }
  }

  /**
   * Calculate project metrics and cache results
   * @param projectId - UUID of the project
   */
  async calculateAndCacheMetrics(projectId: string): Promise<ProjectMetrics> {
    const metrics = this.generateMetrics(projectId);
    const client = await this.redisManager.getConnection();
    try {
      // Cache with 1 hour TTL
      await client.setEx(
        `project:${projectId}:metrics`,
        3600,
        RedisConnectionManager.serialize(metrics)
      );
      return metrics;
    } finally {
      this.redisManager.releaseConnection(client);
    }
  }

  /**
   * Batch calculate metrics for multiple projects
   * @param projectIds - Array of project UUIDs
   * @returns Promise<ProjectMetrics[]>
   */
  async batchCalculateMetrics(projectIds: string[]): Promise<ProjectMetrics[]> {
    const batchPromises = [];
    for (let i = 0; i < projectIds.length; i += this.batchSize) {
      const batch = projectIds.slice(i, i + this.batchSize);
      batchPromises.push(this.processBatch(batch));
    }
    return (await Promise.all(batchPromises)).flat();
  }

  /**
   * Process a batch of project IDs
   * @param projectIds - Array of project UUIDs
   * @returns Promise<ProjectMetrics[]>
   */
  private async processBatch(projectIds: string[]): Promise<ProjectMetrics[]> {
    const client = await this.redisManager.getConnection();
    try {
      const results = await Promise.all(
        projectIds.map(async projectId => {
          // Check cache first
          const cached = await client.get(`project:${projectId}:metrics`);
          return cached 
            ? RedisConnectionManager.deserialize(cached)
            : this.calculateAndCacheMetrics(projectId);
        })
      );
      return results;
    } finally {
      this.redisManager.releaseConnection(client);
    }
  }

  /**
   * Generate project metrics
   * @param projectId - UUID of the project
   * @returns ProjectMetrics
   */
  private generateMetrics(projectId: string): ProjectMetrics {
    return {
      projectId,
      costAnalysis: {
        currentSpend: 85000,
        projectedSpend: 100000,
        variance: -15,
        optimizationOpportunities: [
          {
            category: 'Material',
            item: 'Ductwork',
            currentCost: 12000,
            recommendedAlternative: 'Pre-insulated ducts',
            potentialSavings: 1800,
            impact: '15% cost reduction with same performance'
          },
          {
            category: 'Labor',
            item: 'HVAC installation',
            currentCost: 30000,
            recommendedAlternative: 'Hire local contractors',
            potentialSavings: 4500,
            impact: '15% cost reduction with same quality'
          }
        ]
      },
      timelineMetrics: {
        currentProgress: 92,
        projectedCompletion: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000),
        criticalPathItems: ['HVAC installation', 'Electrical work'],
        riskAssessment: {
          highRiskItems: 2,
          mediumRiskItems: 3,
          lowRiskItems: 5
        }
      },
      qualityMetrics: {
        complianceScore: 88,
        outstandingIssues: 4,
        lastInspectionDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
      },
      sustainabilityMetrics: {
        carbonFootprint: 1000,
        energyEfficiency: 80,
        waterUsage: 5000,
        wasteReduction: 20
      },
      lastUpdated: new Date()
    };
  }

  async getAlerts(projectId: string): Promise<Array<{
    timestamp: Date;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>> {
    const metrics = await this.getRealTimeInsights(projectId);
    const alerts: Array<{
      timestamp: Date;
      message: string;
      severity: 'low' | 'medium' | 'high';
    }> = [];

    // Cost variance alert
    if (metrics.costAnalysis.variance < -15) {
      alerts.push({
        timestamp: new Date(),
        message: `Cost variance exceeded threshold: ${metrics.costAnalysis.variance}%`,
        severity: 'high'
      });
    }

    // Risk assessment alerts
    if (metrics.timelineMetrics.riskAssessment?.highRiskItems >= 3) {
      alerts.push({
        timestamp: new Date(),
        message: `High risk items exceeded threshold: ${metrics.timelineMetrics.riskAssessment.highRiskItems}`,
        severity: 'high'
      });
    }

    // Quality alerts
    if (metrics.qualityMetrics.complianceScore < 70) {
      alerts.push({
        timestamp: new Date(),
        message: `Compliance score below threshold: ${metrics.qualityMetrics.complianceScore}`,
        severity: 'medium'
      });
    }

    return alerts;
  }

  private async broadcastAlerts(projectId: string, alerts: AlertItem[]): Promise<void> {
    if (WebSocketService.getInstance()) {
      WebSocketService.getInstance().broadcastAlerts(projectId, alerts);
    }
  }
}

type AlertItem = {
  timestamp: Date;
  message: string;
  severity: 'low' | 'medium' | 'high';
};
