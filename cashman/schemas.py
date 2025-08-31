from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from .models import Transaction

class TransactionSchema(SQLAlchemyAutoSchema):
    type = fields.Method("get_type")  # adds income/expense field

    class Meta:
        model = Transaction
        load_instance = True  # allows creating SQLAlchemy objects
        include_fk = True

    def get_type(self, obj):
        return "income" if obj.amount > 0 else "expense"
