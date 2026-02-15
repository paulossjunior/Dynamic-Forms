import os

# Use /tmp for SQLite in serverless environments (read-only allowed only in /tmp)
# But ideally, use a real DATABASE_URL (Postgres)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/sql_app.db")

connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
