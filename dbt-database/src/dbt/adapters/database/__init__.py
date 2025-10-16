from dbt.adapters.base import AdapterPlugin

from dbt.adapters.database.column import PostgresColumn
from dbt.adapters.database.connections import PostgresConnectionManager, PostgresCredentials
from dbt.adapters.database.impl import PostgresAdapter
from dbt.adapters.database.relation import PostgresRelation
from dbt.include import database


Plugin = AdapterPlugin(
    adapter=PostgresAdapter,  # type: ignore
    credentials=PostgresCredentials,
    include_path=database.PACKAGE_PATH,
)
