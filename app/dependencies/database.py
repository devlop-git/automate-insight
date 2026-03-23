from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        print("Database connected successfully")
        yield db
    finally:
        db.close()