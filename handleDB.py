import os
from dotenv import load_dotenv
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

load_dotenv()

dialect = os.getenv("DIALECT")
driver = os.getenv("DRIVER")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

# Replace with your database details
DATABASE_URI = (
    dialect
    + "+"
    + driver
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


# Example: Define a model
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    instagram: Mapped[Optional[str]]
    country: Mapped[str]
    tel: Mapped[str]
    image: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# Example: Create tables (if not already created)
Base.metadata.create_all(engine)

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
