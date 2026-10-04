from app.core.database import SessionLocal
from app.models.user import User
import os


db = SessionLocal()


admin = User(
    username="admin",
    email="admin@gmail.com",
    password=os.getenv("ADMIN_PASSWORD"),
    role="super_admin",
)


db.add(admin)

db.commit()


print("Super admin created")
