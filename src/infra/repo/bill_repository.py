# pylint: disable=E1101
from src.domain.models import Bills
from src.infra.config import DBConnectionHandler
from src.infra.entities import Bills as BillsModel
from typing import List


class BillRepository:
    """Class to manage Pet Repository"""

    @classmethod
    def insert_bill(
        cls, name: str, description: str, end_date: str, user_id: int
    ) -> Bills:
        """
        Insert data in Bills entity
        :param - name: name of the bill
               - description: description of the bill
               - end_date: last date to pay the bill
               - user_id: id of the user owner of the bill (FK)
        :return - tuple with new bill inserted
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_bill = BillsModel(
                    name=name,
                    description=description,
                    end_date=end_date,
                    user_id=user_id,
                )
                db_connection.session.add(new_bill)
                db_connection.session.commit()
                return Bills(
                    id=new_bill.id,
                    name=new_bill.name,
                    description=new_bill.description.value,
                    end_date=new_bill.end_date,
                    user_id=new_bill.user_id,
                )
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()
        return None

    @classmethod
    def select_bill(cls, bill_id: int = None, user_id: int = None) -> List[Bills]:
        """
        Select data in PetsEntity entity by id and/or user_id
        :param - bill_id : id of the bill
               - user_id : id of the user owner
        :return - List of Bills selected
        """
        with DBConnectionHandler() as db_connection:
            try:
                query_data = None
                if bill_id and not user_id:
                    data = (
                        db_connection.session.query(BillsModel)
                        .filter_by(id=bill_id)
                        .one()
                    )
                    query_data = [data]
                if not bill_id and user_id:
                    data = (
                        db_connection.session.query(BillsModel)
                        .filter_by(user_id=user_id)
                        .all()
                    )
                    query_data = data
                if bill_id and user_id:
                    data = (
                        db_connection.session.query(BillsModel)
                        .filter_by(id=bill_id, user_id=user_id)
                        .one()
                    )
                    query_data = [data]
                return query_data
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()
        return None
