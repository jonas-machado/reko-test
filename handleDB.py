from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

load_dotenv()

dialect = os.getenv("DIALECT")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

# Replace with your database details
DATABASE_URI = (
    dialect
    + "://"
    + username
    + ":"
    + password
    + "@"
    + host
    + ":"
    + port
    + "/"
    + database_name
)

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a session factory
Session = sessionmaker(bind=engine)

# Example: Define a model


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    instagram: Mapped[Optional[str]]
    country: Mapped[int]
    tel: Mapped[int]     
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# Example: Create tables (if not already created)
# Base.metadata.create_all(engine)

# # Example: Use the session
# session = Session()

# # Add data to the database
# new_user = User(username='john_doe')
# session.add(new_user)
# session.commit()

# # Query data
# users = session.query(User).all()
# for user in users:
#     print(user.username)

# # Close the session
# session.close()
