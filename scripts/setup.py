import os

from src.database.model import Base, Product, User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

host = os.getenv("DB_HOST", "localhost")
url = f"mysql+pymysql://testUser:password@{host}/testDB"
print("db url:", url)
engine = create_engine(url)

if not database_exists(engine.url):
    create_database(engine.url)
else:
    drop_database(engine.url)
    create_database(engine.url)

session = sessionmaker(engine)
db = session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


db.add_all([
    User(id=1, name="Alice", email="alice@example.com",
         address="9653 Halifax St. Hoboken, NJ 07030 "),
    User(id=2, name="Bob", email="bob@example.com",
         address="7972 North Branch Lane Powder Springs, GA 30127"),
    Product(id=111, name="Apple", price=1.99, inventory=10),
    Product(id=222, name="Banana", price=2.99, inventory=8),
    Product(id=333, name="Grape", price=2, inventory=1),
    Product(id=444, name="Kiwi", price=5.79, inventory=10),
    Product(id=555, name="Strawberry", price=10, inventory=0),
])
db.commit()

users = db.query(User).all()
for user in users:
    print(vars(user))
products = db.query(Product).all()
for product in products:
    print(vars(product))
print("database created & initialized!!!")
