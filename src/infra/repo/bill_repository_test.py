from faker import Faker
from .bill_repository import BillRepository
from src.infra.config import DBConnectionHandler
from src.infra.entities import Bills as BillsModel
from src.infra.entities.bills import BillTypes

fake = Faker()
bill_repository = BillRepository()
db_connection_handler = DBConnectionHandler()


def test_insert_bill():
    """Should insert bill in Bills table"""
    name = fake.name()
    description = "food"
    end_date = fake.future_date()
    user_id = fake.random_number()

    # SQL Commands
    new_bill = bill_repository.insert_bill(name, description, end_date, user_id)
    engine = db_connection_handler.get_engine()
    query_bill = engine.execute(
        "SELECT * FROM bills WHERE id='{}'".format(new_bill.id)
    ).fetchone()

    assert new_bill.id == query_bill.id
    assert new_bill.name == query_bill.name
    assert new_bill.description == query_bill.description
    assert (new_bill.end_date).strftime("%Y-%m-%d") == query_bill.end_date
    assert new_bill.user_id == query_bill.user_id

    engine.execute("DELETE FROM bills WHERE id='{}'".format(new_bill.id))


def test_select_bill():
    """Should Select Bill"""

    bill_id = fake.random_number(digits=4)
    name = fake.name()
    description = "food"
    end_date = fake.future_date()
    user_id = fake.random_number(digits=1)

    description_mock = BillTypes("food")
    data = BillsModel(
        id=bill_id,
        name=name,
        description=description_mock,
        end_date=end_date,
        user_id=user_id,
    )

    # SQL Commands
    engine = db_connection_handler.get_engine()
    engine.execute(
        "INSERT INTO bills (id, name, description, end_date, user_id) VALUES ('{}','{}','{}','{}','{}');".format(
            bill_id, name, description, end_date, user_id
        )
    )

    query_bill1 = bill_repository.select_bill(bill_id=bill_id)
    query_bill2 = bill_repository.select_bill(user_id=user_id)
    query_bill3 = bill_repository.select_bill(bill_id=bill_id, user_id=user_id)

    assert data in query_bill1
    assert data in query_bill2
    assert data in query_bill3

    engine.execute("DELETE FROM bills WHERE id='{}';".format(bill_id))
