import enum
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum
from src.infra.config import Base


class BillTypes(enum.Enum):
    """Defining Bills Types"""

    rent = "Rent"
    utilities = "Utilities"
    food = "Food"
    creditCard = "Credit Card"


class Bills(Base):
    """Users Entity"""

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Enum(BillTypes), nullable=False)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))


def __rep__(self):
    return f"Pet [name={self.name},description={self.description},end_date={self.end_date},user_id={self.user_id}]"
