from app.database import SessionLocal
from app import models
from datetime import date

db = SessionLocal()

try:
    #---Clear existing data---
    db.query(models.Application).delete()
    db.query(models.User).delete()
    db.commit()
    print("Cleare existing data from User and Application tables")

    #---Create test users---
    users_data = [
        {"name": "Alice Smith", "email": "alice@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"},
        {"name": "Charlie Brown", "email": "charlie@example.com"}
    ]

    users = []
    for udata in users_data:
        user = models.User(name=udata["name"], email=udata["email"])
        db.add(user)
        db.commit()
        db.refresh(user)
        users.append(user)
        print(f"Created user: {user.name} with email {user.email}")

    #---Create applications for each user---
    applications_data = [
        {"company": "Acme Corp", "role": "Software Engineer", "status": "Applied", "date_applied": date(2026,3,1)},
        {"company": "Globex Inc", "role": "Backend Developer", "status": "Interviewing", "date_applied": date(2026,3,2)},
        {"company": "Initech", "role": "Full Stack Developer", "status": "Offered", "date_applied": date(2026,3,3)}
    ]

    for i, user in enumerate(users):
        for j, app_data in enumerate(applications_data):
            app = models.Application(
                company=app_data["company"],
                role=app_data["role"],
                status=app_data["status"],
                date_applied=app_data["date_applied"],
                user_id=user.id
            )
            db.add(app)
            db.commit()
            db.refresh(app)
            print(f"Created application {app.id} for {user.name} at {app.company}")

finally:
    db.close()
    print("Seeding complete!")