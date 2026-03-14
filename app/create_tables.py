from .database import engine, Base
from .models import User, Application

Base.metadata.create_all(bind=engine)
print("✅ Tables created in the database")
