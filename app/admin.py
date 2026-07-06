from app.core.database import SessionLocal
from app.models.user import User


db = SessionLocal()



admin = User(

username="admin",

email="admin@gmail.com",

password="your_hashed_password",

role="super_admin"

)


db.add(admin)

db.commit()


print("Super admin created")