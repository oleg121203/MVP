-- Ініціалізація векторного розширення для Windsurf
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Створення схеми для Windsurf
CREATE SCHEMA IF NOT EXISTS windsurf;

-- Надання прав користувачу
GRANT ALL PRIVILEGES ON SCHEMA windsurf TO ventai_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA windsurf TO ventai_dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA windsurf TO ventai_dev;

-- Налаштування для українського пошуку
CREATE TEXT SEARCH CONFIGURATION ukrainian (COPY = simple);
