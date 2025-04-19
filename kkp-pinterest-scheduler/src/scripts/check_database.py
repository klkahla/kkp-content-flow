from models.pin import Session, Pin
from utils.logger import logger
from sqlalchemy import func

def check_database():
    session = Session()
    try:
        # Get total count
        total_pins = session.query(Pin).count()
        logger.info(f"Total pins in database: {total_pins}")

        # Get most recent pins
        recent_pins = session.query(Pin).order_by(Pin.created_at.desc()).limit(5).all()
        logger.info("\nMost recent pins:")
        for pin in recent_pins:
            logger.info(f"Title: {pin.title}")
            logger.info(f"Board: {pin.board_id}")
            logger.info(f"Created at: {pin.created_at}")
            logger.info("---")

        # Get pins by board
        board_counts = session.query(Pin.board_id, func.count(Pin.id)).\
            group_by(Pin.board_id).all()
        logger.info("\nPins per board:")
        for board_id, count in board_counts:
            logger.info(f"Board {board_id}: {count} pins")

    except Exception as e:
        logger.error(f"Error checking database: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    check_database() 