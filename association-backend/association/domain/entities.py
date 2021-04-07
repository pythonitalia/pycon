import databases
import sqlalchemy

from association.settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# class StripeCustomer(ormar.Model):
#     class Meta:
#         database = database
#         metadata = metadata

#     id: int = ormar.Integer(primary_key=True)
#     name: str = ormar.String(max_length=100)
#     completed: bool = ormar.Boolean(default=False)
