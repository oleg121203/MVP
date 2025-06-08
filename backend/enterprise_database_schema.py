"""
VentAI Enterprise Database Schema
Розширена схема БД для enterprise аналітики та управління проектами
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text, JSON,
    ForeignKey, Table, Index, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid

Base = declarative_base()

# Many-to-many relationship tables
project_suppliers = Table(
    'project_suppliers',
    Base.metadata,
    Column('project_id', UUID(as_uuid=True), ForeignKey('projects.id')),
    Column('supplier_id', UUID(as_uuid=True), ForeignKey('suppliers.id'))
)

project_materials = Table(
    'project_materials',
    Base.metadata,
    Column('project_id', UUID(as_uuid=True), ForeignKey('projects.id')),
    Column('material_id', UUID(as_uuid=True), ForeignKey('materials.id'))
)

# === CORE PROJECT MANAGEMENT ===

class Project(Base):
    """Розширена модель проекту з enterprise функціями"""
    __tablename__ = 'projects'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'))
    
    # Project Details
    project_type = Column(String(100))  # office, residential, industrial, etc.
    total_area = Column(Float)  # m²
    total_volume = Column(Float)  # m³
    floors_count = Column(Integer)
    rooms_count = Column(Integer)
    
    # Financial Information
    budget = Column(Float)
    estimated_cost = Column(Float)
    actual_cost = Column(Float, default=0.0)
    profit_margin = Column(Float, default=0.15)  # 15% default
    
    # Project Status
    status = Column(String(50), default='planning')  # planning, design, execution, completed
    priority = Column(String(20), default='medium')  # low, medium, high, urgent
    progress_percentage = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(DateTime)
    deadline = Column(DateTime)
    completed_at = Column(DateTime)
    
    # AI Analysis Data
    ai_analysis_data = Column(JSON)  # Зберігає AI аналіз проекту
    optimization_suggestions = Column(JSON)  # AI рекомендації
    compliance_status = Column(JSON)  # Статус відповідності нормам
    
    # Relationships
    client = relationship("Client", back_populates="projects")
    analytics = relationship("ProjectAnalytics", back_populates="project", cascade="all, delete-orphan")
    cost_analyses = relationship("CostAnalysis", back_populates="project", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", secondary=project_suppliers, back_populates="projects")
    materials = relationship("Material", secondary=project_materials, back_populates="projects")
    calculations = relationship("CalculationResult", back_populates="project", cascade="all, delete-orphan")

# === ANALYTICS & KPI ===

class ProjectAnalytics(Base):
    """Аналітичні дані проекту в реальному часі"""
    __tablename__ = 'project_analytics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    
    # Performance Metrics
    energy_efficiency_rating = Column(Float)  # A++ to G scale (1.0 to 7.0)
    cost_per_m2 = Column(Float)
    time_to_completion_days = Column(Integer)
    quality_score = Column(Float)  # 0.0 to 10.0
    
    # Financial KPIs
    cost_variance = Column(Float)  # Відхилення від бюджету
    roi_percentage = Column(Float)  # Return on Investment
    savings_achieved = Column(Float)  # Досягнута економія
    
    # Operational KPIs  
    hvac_efficiency = Column(Float)
    air_quality_index = Column(Float)
    noise_level = Column(Float)  # dB
    compliance_score = Column(Float)  # % відповідності нормам
    
    # Market Analysis
    market_competitiveness = Column(Float)  # 1-10 рейтинг
    cost_vs_market_average = Column(Float)  # % відносно ринку
    
    # AI Insights
    ai_recommendations = Column(JSON)
    optimization_potential = Column(Float)  # % можливої оптимізації
    risk_factors = Column(JSON)  # Виявлені ризики
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="analytics")

# === FINANCIAL ANALYSIS ===

class CostAnalysis(Base):
    """Детальний аналіз витрат проекту"""
    __tablename__ = 'cost_analyses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    
    # Cost Breakdown
    materials_cost = Column(Float, default=0.0)
    labor_cost = Column(Float, default=0.0)
    equipment_cost = Column(Float, default=0.0)
    overhead_cost = Column(Float, default=0.0)
    profit_margin = Column(Float, default=0.0)
    
    # Detailed Categories
    ductwork_cost = Column(Float, default=0.0)
    insulation_cost = Column(Float, default=0.0)
    equipment_hvac_cost = Column(Float, default=0.0)
    electrical_cost = Column(Float, default=0.0)
    automation_cost = Column(Float, default=0.0)
    
    # Analysis Results
    total_estimated_cost = Column(Float)
    cost_per_m2 = Column(Float)
    cost_per_m3 = Column(Float)
    
    # Optimization Data
    potential_savings = Column(Float, default=0.0)
    optimized_cost = Column(Float)
    optimization_methods = Column(JSON)  # Методи оптимізації
    
    # AI Analysis
    ai_cost_breakdown = Column(JSON)
    market_comparison = Column(JSON)
    supplier_recommendations = Column(JSON)
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="cost_analyses")

# === SUPPLIER MANAGEMENT ===

class Supplier(Base):
    """База постачальників з AI рейтингом"""
    __tablename__ = 'suppliers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    company_type = Column(String(100))  # manufacturer, distributor, retailer
    website = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    
    # Address
    country = Column(String(100), default='Ukraine')
    city = Column(String(100))
    address = Column(Text)
    
    # Business Info
    years_in_business = Column(Integer)
    employee_count = Column(Integer)
    certifications = Column(ARRAY(String))
    specializations = Column(ARRAY(String))  # HVAC categories
    
    # Performance Metrics
    reliability_score = Column(Float, default=5.0)  # 1-10
    quality_score = Column(Float, default=5.0)
    delivery_score = Column(Float, default=5.0)
    price_competitiveness = Column(Float, default=5.0)
    
    # AI Analytics
    ai_rating = Column(Float)  # Overall AI-generated rating
    price_trend = Column(String(20))  # increasing, stable, decreasing
    recommendation_score = Column(Float)
    
    # Financial Data
    payment_terms = Column(String(100))
    currency = Column(String(10), default='UAH')
    min_order_amount = Column(Float)
    delivery_cost = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_order_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", secondary=project_suppliers, back_populates="suppliers")
    price_quotes = relationship("PriceQuote", back_populates="supplier", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="supplier")

# === MATERIALS & PRICING ===

class Material(Base):
    """Каталог матеріалів з аналітикою цін"""
    __tablename__ = 'materials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
    
    # Material Info
    name = Column(String(255), nullable=False)
    category = Column(String(100))  # ductwork, insulation, equipment, etc.
    subcategory = Column(String(100))
    material_type = Column(String(100))  # steel, aluminum, plastic, etc.
    
    # Specifications
    specifications = Column(JSON)  # Технічні характеристики
    dimensions = Column(JSON)  # Розміри
    weight = Column(Float)
    color = Column(String(50))
    finish = Column(String(100))
    
    # Standards & Compliance
    standards_compliance = Column(ARRAY(String))  # ДБН, ISO, EN стандарти
    fire_rating = Column(String(50))
    environmental_rating = Column(String(50))
    
    # Pricing
    base_price = Column(Float)
    currency = Column(String(10), default='UAH')
    unit_of_measure = Column(String(50))  # m, m², m³, kg, piece
    
    # AI Price Analysis
    price_history = Column(JSON)  # Історія цін
    price_trend = Column(String(20))  # up, down, stable
    predicted_price = Column(Float)  # AI прогноз ціни
    market_position = Column(String(20))  # premium, mid-range, budget
    
    # Performance Data
    popularity_score = Column(Float, default=0.0)
    quality_rating = Column(Float, default=5.0)
    availability_status = Column(String(50), default='in_stock')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_price_update = Column(DateTime)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="materials")
    projects = relationship("Project", secondary=project_materials, back_populates="materials")
    price_quotes = relationship("PriceQuote", back_populates="material", cascade="all, delete-orphan")

class PriceQuote(Base):
    """Цінові пропозиції від постачальників"""
    __tablename__ = 'price_quotes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey('materials.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    
    # Quote Details
    quoted_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float)
    currency = Column(String(10), default='UAH')
    
    # Terms
    delivery_time_days = Column(Integer)
    delivery_cost = Column(Float, default=0.0)
    payment_terms = Column(String(100))
    validity_period_days = Column(Integer, default=30)
    
    # Status
    status = Column(String(50), default='active')  # active, expired, accepted, rejected
    is_ai_generated = Column(Boolean, default=False)
    confidence_score = Column(Float)  # AI confidence in price accuracy
    
    # Additional Info
    notes = Column(Text)
    special_conditions = Column(JSON)
    
    # Timestamps
    quoted_at = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    responded_at = Column(DateTime)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="price_quotes")
    material = relationship("Material", back_populates="price_quotes")

# === CLIENT MANAGEMENT (CRM) ===

class Client(Base):
    """Клієнтська база з CRM функціями"""
    __tablename__ = 'clients'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Info
    name = Column(String(255), nullable=False)
    company_name = Column(String(255))
    client_type = Column(String(50))  # individual, small_business, enterprise, government
    industry = Column(String(100))
    
    # Contact Info
    email = Column(String(255))
    phone = Column(String(50))
    website = Column(String(255))
    
    # Address
    country = Column(String(100), default='Ukraine')
    city = Column(String(100))
    address = Column(Text)
    
    # Business Data
    annual_revenue = Column(Float)
    employee_count = Column(Integer)
    decision_maker = Column(String(255))
    
    # CRM Data
    lead_source = Column(String(100))  # website, referral, cold_email, etc.
    lead_score = Column(Float, default=0.0)  # AI-generated lead score
    lifecycle_stage = Column(String(50))  # lead, prospect, customer, churned
    
    # AI Analysis
    engagement_score = Column(Float, default=0.0)
    project_potential = Column(Float)  # Potential project value
    conversion_probability = Column(Float)
    preferred_communication = Column(String(50))
    
    # Relationship Data
    total_project_value = Column(Float, default=0.0)
    projects_count = Column(Integer, default=0)
    last_interaction = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_contact = Column(DateTime)
    
    # Relationships
    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")
    interactions = relationship("ClientInteraction", back_populates="client", cascade="all, delete-orphan")

class ClientInteraction(Base):
    """Історія взаємодії з клієнтами"""
    __tablename__ = 'client_interactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'), nullable=False)
    
    # Interaction Details
    interaction_type = Column(String(50))  # email, call, meeting, proposal
    direction = Column(String(20))  # inbound, outbound
    subject = Column(String(255))
    content = Column(Text)
    
    # AI Analysis
    sentiment = Column(String(20))  # positive, neutral, negative
    intent = Column(String(100))  # inquiry, complaint, purchase_intent, etc.
    ai_response_suggested = Column(Text)
    ai_follow_up_suggested = Column(Text)
    
    # Outcome
    outcome = Column(String(100))
    next_action = Column(String(255))
    priority = Column(String(20), default='medium')
    
    # Timestamps
    occurred_at = Column(DateTime, default=datetime.utcnow)
    follow_up_date = Column(DateTime)
    
    # Relationships
    client = relationship("Client", back_populates="interactions")

# === CALCULATION RESULTS ===

class CalculationResult(Base):
    """Результати розрахунків з аналітикою"""
    __tablename__ = 'calculation_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    
    # Calculation Info
    calculator_type = Column(String(100), nullable=False)
    calculation_name = Column(String(255))
    input_data = Column(JSON, nullable=False)
    results = Column(JSON, nullable=False)
    
    # AI Analysis
    ai_analysis = Column(JSON)
    optimization_suggestions = Column(JSON)
    confidence_score = Column(Float)
    
    # Performance Metrics
    calculation_time_ms = Column(Integer)
    accuracy_score = Column(Float)
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="calculations")

# === INDEXES FOR PERFORMANCE ===

# Project indexes
Index('idx_projects_status', Project.status)
Index('idx_projects_client', Project.client_id)
Index('idx_projects_created', Project.created_at)

# Analytics indexes  
Index('idx_analytics_project', ProjectAnalytics.project_id)
Index('idx_analytics_calculated', ProjectAnalytics.calculated_at)

# Supplier indexes
Index('idx_suppliers_rating', Supplier.ai_rating)
Index('idx_suppliers_active', Supplier.is_active)

# Material indexes
Index('idx_materials_category', Material.category)
Index('idx_materials_supplier', Material.supplier_id)
Index('idx_materials_price_updated', Material.last_price_update)

# Client indexes
Index('idx_clients_lead_score', Client.lead_score)
Index('idx_clients_lifecycle', Client.lifecycle_stage)

print("✅ VentAI Enterprise Database Schema створено успішно!")
print("📊 Таблиці: Projects, Analytics, Suppliers, Materials, Clients, CRM")
print("🚀 Готово для міграції бази даних")
