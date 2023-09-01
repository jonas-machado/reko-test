import os
from dotenv import load_dotenv
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import UniqueConstraint
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


class Reference(Base):
    __tablename__ = "reference"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    instagram: Mapped[Optional[str]] = mapped_column(String(30), unique=True)
    country: Mapped[int] = mapped_column(Integer())
    tel: Mapped[int] = mapped_column(BigInteger())
    image: Mapped[str] = mapped_column(String(50))

    user: Mapped[List["User"]] = relationship(
        back_populates="reference", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Reference(id={self.id!r}, tel={self.tel!r}, email={self.email!r}, instagram={self.instagram!r}, country={self.country!r}, fullname={self.fullname!r}, image={self.image!r})"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(30))

    reference_id: Mapped[int] = mapped_column(ForeignKey("reference.id"))
    reference: Mapped["Reference"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, password={self.password!r}, reference_id={self.reference_id!r})"


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
