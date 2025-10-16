from dbt.adapters.sql import SQLAdapter
from dbt.adapters.events.logging import AdapterLogger
from dbt.adapters.database.column import DatabaseColumn
from dbt.adapters.database.relation import DatabaseRelation
from dbt.adapters.database.connections import DatabaseConnectionManager


logger = AdapterLogger("database")


class DatabaseAdapter(SQLAdapter):
    ConnectionManager = DatabaseConnectionManager
    Relation = DatabaseRelation
    Column = DatabaseColumn

    @classmethod
    def date_function(cls) -> str:
        return "current_date()"

    @classmethod
    def convert_datetime_type(cls, agate_table: "agate.Table", col_idx: int) -> str:
        return "datetime"

    @classmethod
    def convert_text_type(cls, agate_table: "agate.Table", col_idx: int) -> str:
        return "string"

    @classmethod
    def quote(cls, identifier: str) -> str:
        return "`{}`".format(identifier)
