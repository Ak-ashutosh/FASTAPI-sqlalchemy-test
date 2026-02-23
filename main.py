from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# -----------------------------
# DATABASE CONFIG
# -----------------------------

DATABASE_URL = "postgresql+psycopg2://postgres:qwerty@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# -----------------------------
# MODEL (Table)
# -----------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Create tables in PostgreSQL
Base.metadata.create_all(bind=engine)


# -----------------------------
# FASTAPI APP
# -----------------------------

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# ROUTES
# -----------------------------

@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL working 🚀"}


@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user