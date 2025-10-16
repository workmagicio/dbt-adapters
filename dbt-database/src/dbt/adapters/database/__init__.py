from dbt.adapters.base import AdapterPlugin

from dbt.adapters.database.column import DatabaseColumn
from dbt.adapters.database.connections import DatabaseConnectionManager, DatabaseCredentials
from dbt.adapters.database.impl import DatabaseAdapter
from dbt.adapters.database.relation import DatabaseRelation
from dbt.include import database


Plugin = AdapterPlugin(
    adapter=DatabaseAdapter,  # type: ignore
    credentials=DatabaseCredentials,
    include_path=database.PACKAGE_PATH,
)
