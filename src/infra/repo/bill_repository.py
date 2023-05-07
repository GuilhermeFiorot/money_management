# pylint: disable=E1101
from src.domain.models import Bills
from src.infra.config import DBConnectionHandler
from src.infra.entities import Bills as BillsModel


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

        with DBConnectionHandler() as db_conn:
            try:
                new_bill = BillsModel(
                    name=name,
                    description=description,
                    end_date=end_date,
                    user_id=user_id,
                )
                db_conn.session.add(new_bill)
                db_conn.session.commit()
                return Bills(
                    id=new_bill.id,
                    name=new_bill.name,
                    description=new_bill.description.value,
                    end_date=new_bill.end_date,
                    user_id=new_bill.user_id,
                )
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
        return None
