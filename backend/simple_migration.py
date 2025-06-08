#!/usr/bin/env python3
"""
Simple Enterprise Database Migration
Створення enterprise таблиць для VentAI Platform
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'ventai_dev',
    'user': 'ventai_dev',
    'password': 'ventai_dev_password'
}

def create_enterprise_tables():
    """Створює всі enterprise таблиці"""
    
    # SQL for creating tables
    CREATE_TABLES_SQL = """
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Projects table with AI analytics
    CREATE TABLE IF NOT EXISTS projects (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        description TEXT,
        client_id UUID,
        
        -- AI Analysis Fields
        ai_analysis_status VARCHAR(50) DEFAULT 'pending',
        ai_optimization_score FLOAT DEFAULT 0.0,
        ai_recommendations JSONB,
        ai_cost_predictions JSONB,
        ai_risk_assessment JSONB,
        
        -- Project Metadata
        total_budget FLOAT,
        estimated_savings FLOAT DEFAULT 0.0,
        actual_savings FLOAT DEFAULT 0.0,
        project_type VARCHAR(100),
        status VARCHAR(50) DEFAULT 'planning',
        priority VARCHAR(20) DEFAULT 'medium',
        
        -- File Management
        uploaded_files JSONB,
        calculation_results JSONB,
        
        -- Timestamps
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW(),
        deadline TIMESTAMP,
        completed_at TIMESTAMP
    );
    
    -- Project Analytics table
    CREATE TABLE IF NOT EXISTS project_analytics (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        project_id UUID NOT NULL,
        
        -- KPI Metrics
        completion_percentage FLOAT DEFAULT 0.0,
        budget_utilization FLOAT DEFAULT 0.0,
        timeline_adherence FLOAT DEFAULT 100.0,
        quality_score FLOAT DEFAULT 0.0,
        efficiency_rating FLOAT DEFAULT 0.0,
        
        -- AI Analytics
        ai_performance_score FLOAT,
        ai_trend_analysis JSONB,
        ai_bottlenecks JSONB,
        ai_suggestions JSONB,
        
        -- Real-time Data
        daily_progress JSONB,
        weekly_summary JSONB,
        monthly_trends JSONB,
        
        -- Risk Analytics
        risk_level VARCHAR(20) DEFAULT 'low',
        risk_factors JSONB,
        mitigation_strategies JSONB,
        
        -- Timestamps
        analysis_date TIMESTAMP DEFAULT NOW(),
        last_updated TIMESTAMP DEFAULT NOW()
    );
    
    -- Cost Analysis table
    CREATE TABLE IF NOT EXISTS cost_analysis (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        project_id UUID NOT NULL,
        
        -- Cost Breakdown
        material_costs JSONB,
        labor_costs JSONB,
        equipment_costs JSONB,
        overhead_costs JSONB,
        total_estimated_cost FLOAT,
        total_actual_cost FLOAT DEFAULT 0.0,
        
        -- AI Cost Intelligence
        ai_cost_optimization JSONB,
        ai_alternative_materials JSONB,
        ai_supplier_recommendations JSONB,
        ai_cost_forecast JSONB,
        
        -- Savings Analysis
        potential_savings FLOAT DEFAULT 0.0,
        realized_savings FLOAT DEFAULT 0.0,
        roi_percentage FLOAT DEFAULT 0.0,
        payback_period_months INTEGER,
        
        -- Market Analysis
        market_price_comparison JSONB,
        price_trend_analysis JSONB,
        competitor_pricing JSONB,
        
        -- Timestamps
        analysis_date TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Suppliers table
    CREATE TABLE IF NOT EXISTS suppliers (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        contact_info JSONB,
        business_details JSONB,
        
        -- AI Performance Analytics
        ai_reliability_score FLOAT DEFAULT 0.0,
        ai_quality_rating FLOAT DEFAULT 0.0,
        ai_price_competitiveness FLOAT DEFAULT 0.0,
        ai_delivery_performance FLOAT DEFAULT 0.0,
        ai_overall_score FLOAT DEFAULT 0.0,
        
        -- Performance Metrics
        on_time_delivery_rate FLOAT DEFAULT 0.0,
        quality_rejection_rate FLOAT DEFAULT 0.0,
        price_stability_index FLOAT DEFAULT 0.0,
        response_time_hours FLOAT,
        
        -- Business Information
        specialties TEXT[],
        certifications JSONB,
        coverage_areas TEXT[],
        minimum_order_value FLOAT,
        payment_terms VARCHAR(100),
        
        -- AI Insights
        ai_strengths JSONB,
        ai_weaknesses JSONB,
        ai_recommendations JSONB,
        
        -- Status
        status VARCHAR(50) DEFAULT 'active',
        last_interaction TIMESTAMP,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Materials table
    CREATE TABLE IF NOT EXISTS materials (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        category VARCHAR(100),
        subcategory VARCHAR(100),
        
        -- Technical Specifications
        specifications JSONB,
        technical_parameters JSONB,
        quality_standards JSONB,
        
        -- Price Analytics
        current_market_price FLOAT,
        price_history JSONB,
        price_trend_direction VARCHAR(20),
        price_volatility_index FLOAT,
        
        -- AI Price Intelligence
        ai_price_forecast JSONB,
        ai_price_alerts JSONB,
        ai_alternative_materials JSONB,
        ai_market_analysis JSONB,
        
        -- Supplier Information
        primary_suppliers TEXT[],
        supplier_count INTEGER DEFAULT 0,
        avg_delivery_time INTEGER,
        
        -- Usage Analytics
        popularity_score FLOAT DEFAULT 0.0,
        usage_frequency INTEGER DEFAULT 0,
        last_used_date TIMESTAMP,
        
        -- Timestamps
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Price Quotes table
    CREATE TABLE IF NOT EXISTS price_quotes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        material_id UUID NOT NULL,
        supplier_id UUID NOT NULL,
        project_id UUID,
        
        -- Quote Details
        unit_price FLOAT NOT NULL,
        quantity FLOAT NOT NULL,
        total_price FLOAT NOT NULL,
        currency VARCHAR(10) DEFAULT 'UAH',
        
        -- Terms and Conditions
        delivery_time_days INTEGER,
        payment_terms VARCHAR(100),
        warranty_period VARCHAR(50),
        special_conditions TEXT,
        
        -- AI Analysis
        ai_price_rating FLOAT,
        ai_deal_quality VARCHAR(20),
        ai_negotiation_tips JSONB,
        ai_risk_factors JSONB,
        
        -- Quote Status
        status VARCHAR(50) DEFAULT 'pending',
        valid_until TIMESTAMP,
        response_time FLOAT,
        
        -- Timestamps
        quote_date TIMESTAMP DEFAULT NOW(),
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Clients table
    CREATE TABLE IF NOT EXISTS clients (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        company_name VARCHAR(255),
        contact_person VARCHAR(255),
        
        -- Contact Information
        email VARCHAR(255),
        phone VARCHAR(50),
        address JSONB,
        website VARCHAR(255),
        
        -- Business Information
        industry VARCHAR(100),
        company_size VARCHAR(50),
        annual_revenue FLOAT,
        business_type VARCHAR(100),
        
        -- AI Lead Scoring
        ai_lead_score FLOAT DEFAULT 0.0,
        ai_conversion_probability FLOAT DEFAULT 0.0,
        ai_customer_value_prediction FLOAT DEFAULT 0.0,
        ai_engagement_level VARCHAR(20),
        ai_personas JSONB,
        
        -- Interaction Analytics
        total_interactions INTEGER DEFAULT 0,
        last_interaction_date TIMESTAMP,
        preferred_communication VARCHAR(50),
        response_rate FLOAT DEFAULT 0.0,
        
        -- Business Metrics
        total_project_value FLOAT DEFAULT 0.0,
        average_project_size FLOAT DEFAULT 0.0,
        customer_lifetime_value FLOAT DEFAULT 0.0,
        
        -- Status and Classifications
        status VARCHAR(50) DEFAULT 'prospect',
        source VARCHAR(100),
        tags TEXT[],
        
        -- Timestamps
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Client Interactions table
    CREATE TABLE IF NOT EXISTS client_interactions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        client_id UUID NOT NULL,
        
        -- Interaction Details
        interaction_type VARCHAR(50),
        subject VARCHAR(500),
        content TEXT,
        direction VARCHAR(20),
        
        -- AI Analysis
        ai_sentiment_score FLOAT,
        ai_intent_classification VARCHAR(100),
        ai_urgency_level VARCHAR(20),
        ai_follow_up_suggestions JSONB,
        ai_extracted_requirements JSONB,
        
        -- Email Specific
        email_thread_id VARCHAR(255),
        auto_response_sent BOOLEAN DEFAULT FALSE,
        ai_response_quality FLOAT,
        human_review_required BOOLEAN DEFAULT FALSE,
        
        -- Metadata
        interaction_duration INTEGER,
        attachments JSONB,
        participants JSONB,
        
        -- Timestamps
        interaction_date TIMESTAMP DEFAULT NOW(),
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    -- Calculation Results table
    CREATE TABLE IF NOT EXISTS calculation_results (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        project_id UUID,
        
        -- Calculator Information
        calculator_type VARCHAR(100) NOT NULL,
        input_parameters JSONB NOT NULL,
        calculation_results JSONB NOT NULL,
        
        -- AI Analysis of Results
        ai_result_analysis JSONB,
        ai_optimization_suggestions JSONB,
        ai_alternative_approaches JSONB,
        ai_accuracy_confidence FLOAT,
        
        -- Validation
        is_validated BOOLEAN DEFAULT FALSE,
        validation_notes TEXT,
        accuracy_rating FLOAT,
        
        -- Usage Statistics
        calculation_time_ms INTEGER,
        user_rating FLOAT,
        
        -- Timestamps
        calculated_at TIMESTAMP DEFAULT NOW(),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    
    # Create indexes for performance
    CREATE_INDEXES_SQL = """
    -- Performance indexes
    CREATE INDEX IF NOT EXISTS idx_projects_client ON projects(client_id);
    CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
    CREATE INDEX IF NOT EXISTS idx_projects_created ON projects(created_at);
    CREATE INDEX IF NOT EXISTS idx_analytics_project ON project_analytics(project_id);
    CREATE INDEX IF NOT EXISTS idx_analytics_date ON project_analytics(analysis_date);
    CREATE INDEX IF NOT EXISTS idx_cost_analysis_project ON cost_analysis(project_id);
    CREATE INDEX IF NOT EXISTS idx_suppliers_score ON suppliers(ai_overall_score);
    CREATE INDEX IF NOT EXISTS idx_materials_category ON materials(category);
    CREATE INDEX IF NOT EXISTS idx_materials_price ON materials(current_market_price);
    CREATE INDEX IF NOT EXISTS idx_quotes_material_supplier ON price_quotes(material_id, supplier_id);
    CREATE INDEX IF NOT EXISTS idx_clients_score ON clients(ai_lead_score);
    CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status);
    CREATE INDEX IF NOT EXISTS idx_interactions_client ON client_interactions(client_id);
    CREATE INDEX IF NOT EXISTS idx_interactions_date ON client_interactions(interaction_date);
    CREATE INDEX IF NOT EXISTS idx_calculations_project ON calculation_results(project_id);
    CREATE INDEX IF NOT EXISTS idx_calculations_type ON calculation_results(calculator_type);
    """
    
    try:
        # Connect to database
        print("🔌 Підключення до enterprise бази даних...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create tables
        print("📊 Створення enterprise таблиць...")
        cursor.execute(CREATE_TABLES_SQL)
        
        # Create indexes
        print("🔍 Створення індексів для продуктивності...")
        cursor.execute(CREATE_INDEXES_SQL)
        
        # Verify tables created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        print(f"\n✅ Успішно створено {len(table_names)} enterprise таблиць:")
        for table in table_names:
            print(f"   📋 {table}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Enterprise база даних готова!")
        print("🚀 Можна починати розробку аналітичних сервісів")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка створення таблиць: {e}")
        return False

if __name__ == "__main__":
    create_enterprise_tables()
