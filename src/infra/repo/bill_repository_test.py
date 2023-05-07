from faker import Faker
from .bill_repository import BillRepository
from src.infra.config import DBConnectionHandler

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
