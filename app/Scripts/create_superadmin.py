from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

admin = db.query(User).filter(
    User.email == "admin@gmail.com"
).first()

if admin:
    admin.role = "superadmin"
    db.commit()
    print("Superadmin created")
else:
    print("User not found")

db.close()