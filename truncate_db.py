from app.database import SessionLocal
from app import models

db = SessionLocal()

#Delete all rowes
db.query(models.Application).delete()
db.query(models.User).delete()
db.commit()
db.close

print("Deleted all rows from User and Application tables")
