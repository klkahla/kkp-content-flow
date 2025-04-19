from config.settings import DATABASE_URL
from sqlalchemy import create_engine
from utils.logger import logger

def test_connection():
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Try to connect
        with engine.connect() as connection:
            logger.info("Successfully connected to the database!")
            
            # Try to create a test table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    test_column VARCHAR(255)
                )
            """)
            logger.info("Successfully created test table!")
            
            # Clean up
            connection.execute("DROP TABLE test_table")
            logger.info("Successfully cleaned up test table!")
            
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection() 