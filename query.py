from sqlalchemy import select
from sqlalchemy.orm import lazyload
from sqlalchemy.orm import joinedload
from handleDB import Reference
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

dialect = os.getenv("DIALECT")
driver = os.getenv("DRIVER")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

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
session = Session(engine)

# set children to load lazily
# stmt = select(Reference).options(lazyload(Reference.user))


# set children to load eagerly with a join
stmt = (
    select(Reference)
    .join(Reference.user)
    .filter(Reference.email == "kalanyishihara@gmail.com")
)
result = session.scalars(stmt).unique().all()
print(result)
# for user in session.scalars(stmt).unique().all():
# print(user)
