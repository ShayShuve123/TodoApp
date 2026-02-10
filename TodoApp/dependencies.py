from database import SessionLocal

def get_db():
    """Return a database connection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()