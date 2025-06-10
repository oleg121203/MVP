import logging
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Numeric, Index
from sqlalchemy.dialects.postgresql import RANGE
from sqlalchemy.sql import text
from typing import Dict, Any, List, Optional

from ...config import settings

logger = logging.getLogger(__name__)

class DatabasePartitioner:
    def __init__(self, db_url: str = settings.DATABASE_URL):
        """
        Initialize database partitioner with connection to PostgreSQL
        """
        self.engine = create_engine(db_url, echo=False)
        self.metadata = MetaData(bind=self.engine)
        self.conn = None
        logger.info("Database partitioner initialized")

    def connect(self):
        """
        Establish database connection
        """
        try:
            self.conn = self.engine.connect()
            logger.info("Database connection established for partitioning")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            self.conn = None
            return False

    def disconnect(self):
        """
        Close database connection
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
        self.conn = None

    def create_range_partition(self, 
                             parent_table_name: str, 
                             partition_name: str, 
                             start_value: Any, 
                             end_value: Any, 
                             column: str = 'created_at') -> bool:
        """
        Create a range partition for the specified parent table
        Args:
            parent_table_name: Name of the parent table
            partition_name: Name for the new partition
            start_value: Start value for the range (inclusive)
            end_value: End value for the range (exclusive)
            column: Column to partition on (default: 'created_at')
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.conn and not self.connect():
            return False

        try:
            # Create partition table inheriting from parent
            create_partition_sql = f"""
                CREATE TABLE IF NOT EXISTS {partition_name} 
                PARTITION OF {parent_table_name} 
                FOR VALUES FROM ('{start_value}') TO ('{end_value}');
            """
            self.conn.execute(text(create_partition_sql))

            # Create indexes on partition for performance
            create_index_sql = f"""
                CREATE INDEX IF NOT EXISTS {partition_name}_{column}_idx 
                ON {partition_name} ({column});
            """
            self.conn.execute(text(create_index_sql))

            logger.info(f"Created range partition {partition_name} for {parent_table_name}")
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating range partition {partition_name}: {e}")
            self.conn.rollback()
            return False

    def create_monthly_partitions(self, 
                                parent_table_name: str, 
                                start_date: str, 
                                months: int, 
                                column: str = 'created_at') -> List[str]:
        """
        Create monthly range partitions for the specified parent table
        Args:
            parent_table_name: Name of the parent table
            start_date: Start date in 'YYYY-MM-DD' format for first partition
            months: Number of monthly partitions to create
            column: Column to partition on (default: 'created_at')
        Returns:
            List[str]: List of created partition names
        """
        from datetime import datetime, timedelta
        
        created_partitions = []
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')

        for i in range(months):
            current_month = start_dt + timedelta(days=30 * i)
            next_month = start_dt + timedelta(days=30 * (i + 1))
            
            partition_name = f"{parent_table_name}_{current_month.strftime('%Y_%m')}"
            start_str = current_month.strftime('%Y-%m-01')
            end_str = next_month.strftime('%Y-%m-01')
            
            if self.create_range_partition(
                parent_table_name=parent_table_name,
                partition_name=partition_name,
                start_value=start_str,
                end_value=end_str,
                column=column
            ):
                created_partitions.append(partition_name)

        return created_partitions

    def create_partitioned_table(self, 
                               table_name: str, 
                               columns: List[Dict[str, Any]], 
                               partition_column: str = 'created_at') -> bool:
        """
        Create a new parent table for partitioning
        Args:
            table_name: Name of the parent table to create
            columns: List of column definitions with name, type, and optional constraints
            partition_column: Column to partition on
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.conn and not self.connect():
            return False

        try:
            # Define the table structure (without storage)
            table_args = []
            for col in columns:
                col_type = col['type']
                col_name = col['name']
                constraints = col.get('constraints', [])
                table_args.append(Column(col_name, col_type, *constraints))

            # Add index on partition column
            table_args.append(Index(f"{table_name}_{partition_column}_idx", partition_column))

            # Create parent table
            Table(table_name, self.metadata, *table_args, postgresql_partition_by=f'RANGE ({partition_column})')
            self.metadata.create_all(self.engine)

            logger.info(f"Created partitioned parent table {table_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating partitioned table {table_name}: {e}")
            return False

    def move_data_to_partition(self, 
                              parent_table_name: str, 
                              partition_name: str, 
                              condition: str) -> int:
        """
        Move existing data from parent table to a partition based on condition
        Args:
            parent_table_name: Name of the parent table
            partition_name: Name of the target partition
            condition: SQL condition to select rows to move (e.g., "created_at >= '2023-01-01' AND created_at < '2024-01-01'")
        Returns:
            int: Number of rows moved
        """
        if not self.conn and not self.connect():
            return 0

        try:
            # Begin transaction
            trans = self.conn.begin()
            
            # Select rows to move
            select_sql = f"""
                SELECT * FROM {parent_table_name}
                WHERE {condition}
            """
            rows = self.conn.execute(text(select_sql)).fetchall()
            row_count = len(rows)
            
            if row_count == 0:
                logger.info(f"No rows to move to partition {partition_name}")
                trans.commit()
                return 0
            
            # Insert into partition
            columns = rows[0].keys()
            col_names = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            insert_sql = f"""
                INSERT INTO {partition_name} ({col_names})
                VALUES ({placeholders})
            """
            
            for row in rows:
                self.conn.execute(text(insert_sql), row)
            
            # Delete from parent table (only if in parent, not already partitioned)
            delete_sql = f"""
                DELETE FROM ONLY {parent_table_name}
                WHERE {condition}
            """
            self.conn.execute(text(delete_sql))
            
            trans.commit()
            logger.info(f"Moved {row_count} rows to partition {partition_name}")
            return row_count
        except Exception as e:
            logger.error(f"Error moving data to partition {partition_name}: {e}")
            if 'trans' in locals():
                trans.rollback()
            return 0

    def get_partition_info(self, parent_table_name: str) -> Dict[str, Any]:
        """
        Get information about partitions for a given parent table
        Returns dictionary with partition details
        """
        if not self.conn and not self.connect():
            return {"status": "error", "message": "Database connection failed"}

        try:
            query = f"""
                SELECT 
                    nmsp_parent.nspname AS parent_schema,
                    parent.relname AS parent_table,
                    nmsp_child.nspname AS child_schema,
                    child.relname AS child_table,
                    pg_get_partkeydef(child.oid) AS partition_key,
                    pg_get_expr(child.relpartbound, child.oid) AS partition_bounds
                FROM pg_inherits
                    JOIN pg_class parent ON pg_inherits.inhparent = parent.oid
                    JOIN pg_class child ON pg_inherits.inhrelid = child.oid
                    JOIN pg_namespace nmsp_parent ON nmsp_parent.oid = parent.relnamespace
                    JOIN pg_namespace nmsp_child ON nmsp_child.oid = child.relnamespace
                WHERE parent.relname = '{parent_table_name}'
                ORDER BY child.relname;
            """
            
            result = self.conn.execute(text(query)).fetchall()
            
            partitions = []
            for row in result:
                partitions.append({
                    "child_table": row.child_table,
                    "schema": row.child_schema,
                    "partition_key": row.partition_key,
                    "bounds": row.partition_bounds
                })
            
            return {
                "status": "success",
                "parent_table": parent_table_name,
                "partition_count": len(partitions),
                "partitions": partitions
            }
        except Exception as e:
            logger.error(f"Error getting partition info for {parent_table_name}: {e}")
            return {"status": "error", "message": str(e)}

    def optimize_partitions(self, parent_table_name: str) -> Dict[str, Any]:
        """
        Optimize existing partitions by analyzing and creating appropriate indexes
        Returns optimization results
        """
        if not self.conn and not self.connect():
            return {"status": "error", "message": "Database connection failed"}

        partition_info = self.get_partition_info(parent_table_name)
        if partition_info["status"] != "success":
            return partition_info

        optimizations = []
        try:
            for partition in partition_info["partitions"]:
                child_table = partition["child_table"]
                
                # Analyze table to update statistics
                analyze_sql = f"ANALYZE {child_table};"
                self.conn.execute(text(analyze_sql))
                
                # Check for common query patterns and create indexes if beneficial
                # This is a simplified example - in production, you'd analyze query logs
                index_sql = f"""
                    CREATE INDEX IF NOT EXISTS {child_table}_common_query_idx
                    ON {child_table} (created_at DESC, id);
                """
                self.conn.execute(text(index_sql))
                
                optimizations.append({
                    "partition": child_table,
                    "action": "analyzed and indexed",
                    "index_created": f"{child_table}_common_query_idx"
                })
                logger.info(f"Optimized partition {child_table} with analysis and index")
            
            self.conn.commit()
            return {
                "status": "success",
                "message": f"Optimized {len(optimizations)} partitions for {parent_table_name}",
                "optimizations": optimizations
            }
        except Exception as e:
            logger.error(f"Error optimizing partitions for {parent_table_name}: {e}")
            self.conn.rollback()
            return {"status": "error", "message": str(e)}

# Global partitioner instance
db_partitioner = DatabasePartitioner()
