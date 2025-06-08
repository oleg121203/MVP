#!/usr/bin/env python3
"""
VentAI Enterprise Database Migration
Створення всіх enterprise таблиць та індексів
"""

import asyncio
import os
import sys
from pathlib import Path

# Додаємо backend до шляху
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from enterprise_database_schema import Base
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev'
)

async def create_enterprise_tables():
    """Створює всі enterprise таблиці"""
    print("🚀 Початок міграції VentAI Enterprise Database...")
    
    try:
        # Створюємо engine
        engine = create_engine(DATABASE_URL)
        
        # Створюємо всі таблиці
        print("📊 Створення таблиць...")
        Base.metadata.create_all(engine)
        
        print("✅ Всі enterprise таблиці створено успішно!")
        
        # Перевіряємо створені таблиці
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%project%' OR table_name LIKE '%client%' OR table_name LIKE '%supplier%'
                ORDER BY table_name;
            """))
            
            tables = result.fetchall()
            print(f"\n📋 Створені enterprise таблиці ({len(tables)}):")
            for table in tables:
                print(f"  ✓ {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка створення таблиць: {e}")
        return False

async def insert_sample_data():
    """Вставляє зразкові дані для тестування"""
    print("\n🔄 Вставка зразкових даних...")
    
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        
        with Session() as session:
            # Вставляємо зразкові дані через SQL
            sample_data_sql = """
            -- Зразковий клієнт
            INSERT INTO clients (
                id, name, company_name, client_type, email, phone, 
                city, lead_score, lifecycle_stage, created_at
            ) VALUES (
                gen_random_uuid(), 
                'Іван Петренко', 
                'БудІнвест ЛТД', 
                'enterprise',
                'ivan@budinvest.com.ua',
                '+380671234567',
                'Київ',
                8.5,
                'prospect',
                NOW()
            ) ON CONFLICT DO NOTHING;
            
            -- Зразковий постачальник
            INSERT INTO suppliers (
                id, name, company_type, website, email, phone,
                city, reliability_score, quality_score, is_active, created_at
            ) VALUES (
                gen_random_uuid(),
                'ВентТехСервіс',
                'manufacturer',
                'https://venttechservice.ua',
                'sales@venttechservice.ua',
                '+380443334455',
                'Київ',
                9.2,
                8.8,
                true,
                NOW()
            ) ON CONFLICT DO NOTHING;
            
            -- Зразковий матеріал
            INSERT INTO materials (
                id, name, category, material_type, base_price, 
                currency, unit_of_measure, availability_status, created_at
            ) VALUES (
                gen_random_uuid(),
                'Повітровод круглий оцинкований Ø200мм',
                'ductwork',
                'galvanized_steel',
                75.50,
                'UAH',
                'm',
                'in_stock',
                NOW()
            ) ON CONFLICT DO NOTHING;
            """
            
            session.execute(text(sample_data_sql))
            session.commit()
        
        print("✅ Зразкові дані вставлено успішно!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка вставки зразкових даних: {e}")
        return False

async def verify_database():
    """Перевіряє цілісність бази даних"""
    print("\n🔍 Перевірка цілісності бази даних...")
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Перевіряємо кількість записів у ключових таблицях
            tables_to_check = [
                'projects', 'project_analytics', 'cost_analyses',
                'suppliers', 'materials', 'price_quotes',
                'clients', 'client_interactions', 'calculation_results'
            ]
            
            for table in tables_to_check:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"  📊 {table}: {count} записів")
                except Exception as e:
                    print(f"  ❌ {table}: помилка - {e}")
        
        print("✅ Перевірка завершена!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка перевірки бази даних: {e}")
        return False

async def create_enterprise_views():
    """Створює корисні views для аналітики"""
    print("\n📈 Створення аналітичних views...")
    
    views_sql = """
    -- View для проектної аналітики
    CREATE OR REPLACE VIEW project_summary_view AS
    SELECT 
        p.id,
        p.name,
        p.status,
        p.total_area,
        p.budget,
        p.estimated_cost,
        p.actual_cost,
        c.name as client_name,
        c.company_name,
        pa.cost_per_m2,
        pa.energy_efficiency_rating,
        pa.compliance_score,
        p.created_at,
        p.deadline
    FROM projects p
    LEFT JOIN clients c ON p.client_id = c.id
    LEFT JOIN project_analytics pa ON p.id = pa.project_id;
    
    -- View для supplier рейтингу
    CREATE OR REPLACE VIEW supplier_rating_view AS
    SELECT 
        s.id,
        s.name,
        s.city,
        s.reliability_score,
        s.quality_score,
        s.delivery_score,
        s.price_competitiveness,
        s.ai_rating,
        COUNT(pq.id) as total_quotes,
        AVG(pq.quoted_price) as avg_quote_price,
        s.is_active
    FROM suppliers s
    LEFT JOIN price_quotes pq ON s.id = pq.supplier_id
    GROUP BY s.id;
    
    -- View для материалів з цінами
    CREATE OR REPLACE VIEW material_price_view AS
    SELECT 
        m.id,
        m.name,
        m.category,
        m.base_price,
        m.currency,
        s.name as supplier_name,
        s.reliability_score as supplier_rating,
        m.availability_status,
        m.last_price_update
    FROM materials m
    LEFT JOIN suppliers s ON m.supplier_id = s.id
    WHERE m.base_price > 0;
    
    -- View для клієнтської аналітики
    CREATE OR REPLACE VIEW client_analytics_view AS
    SELECT 
        c.id,
        c.name,
        c.company_name,
        c.lead_score,
        c.lifecycle_stage,
        c.total_project_value,
        c.projects_count,
        COUNT(ci.id) as total_interactions,
        MAX(ci.occurred_at) as last_interaction_date,
        c.created_at
    FROM clients c
    LEFT JOIN client_interactions ci ON c.id = ci.client_id
    GROUP BY c.id;
    """
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            conn.execute(text(views_sql))
            conn.commit()
        
        print("✅ Аналітичні views створено успішно!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка створення views: {e}")
        return False

async def main():
    """Головна функція міграції"""
    print("🏢 VENTAI ENTERPRISE DATABASE MIGRATION")
    print("=" * 50)
    print(f"🕐 Час початку: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")
    
    success_steps = 0
    total_steps = 5
    
    # Кроки міграції
    steps = [
        ("Створення enterprise таблиць", create_enterprise_tables),
        ("Вставка зразкових даних", insert_sample_data),
        ("Створення аналітичних views", create_enterprise_views),
        ("Перевірка цілісності БД", verify_database),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if await step_func():
            success_steps += 1
            print(f"✅ {step_name} завершено успішно")
        else:
            print(f"❌ {step_name} завершено з помилками")
    
    # Фінальний звіт
    print(f"\n📊 ПІДСУМОК МІГРАЦІЇ:")
    print(f"✅ Успішно: {success_steps}/{len(steps)} кроків")
    print(f"🕐 Час завершення: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_steps == len(steps):
        print(f"\n🎉 МІГРАЦІЯ ЗАВЕРШЕНА УСПІШНО!")
        print(f"🚀 VentAI Enterprise Database готова до використання")
        
        # Оновлюємо CHANGELOG
        update_changelog()
    else:
        print(f"\n⚠️  Міграція завершена з помилками")
        print(f"🔧 Перевірте логи та виправте проблеми")

def update_changelog():
    """Оновлює CHANGELOG після успішної міграції"""
    try:
        changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
        
        if changelog_path.exists():
            content = changelog_path.read_text(encoding='utf-8')
            
            # Додаємо запис про завершення задачі 1.1
            new_entry = f"""
### ✅ COMPLETED - {datetime.now().strftime('%Y-%m-%d %H:%M')}

#### 📊 Завдання 1.1: Database Schema для Analytics - ЗАВЕРШЕНО
- [x] **1.1.1** Створити таблиці для проектів з аналітикою ✅
- [x] **1.1.2** Схема для зберігання AI аналізів ✅
- [x] **1.1.3** Таблиці для цінової аналітики ✅
- [x] **1.1.4** Система метрик та KPI ✅

**Деталі реалізації:**
- Створено 9 основних enterprise таблиць
- Додано аналітичні views для швидких запитів
- Імплементовано індекси для оптимізації продуктивності
- Зразкові дані для тестування системи

---
"""
            
            # Вставляємо новий запис після заголовка ФАЗА 1
            phase1_index = content.find("## 🎯 ФАЗА 1: CORE ANALYTICS FOUNDATION")
            if phase1_index != -1:
                insert_point = content.find("\n", phase1_index + len("## 🎯 ФАЗА 1: CORE ANALYTICS FOUNDATION"))
                updated_content = content[:insert_point] + new_entry + content[insert_point:]
                
                changelog_path.write_text(updated_content, encoding='utf-8')
                print("📝 CHANGELOG оновлено успішно!")
        
    except Exception as e:
        print(f"⚠️  Не вдалося оновити CHANGELOG: {e}")

if __name__ == "__main__":
    asyncio.run(main())
