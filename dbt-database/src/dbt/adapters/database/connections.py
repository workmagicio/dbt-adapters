from typing import Optional
from contextlib import contextmanager
from dataclasses import dataclass, field
from dbt.adapters.sql import SQLConnectionManager
from dbt_common.exceptions import DbtDatabaseError, DbtRuntimeError
from dbt.adapters.exceptions import FailedToConnectError
from dbt.adapters.events.logging import AdapterLogger
from dbt.adapters.contracts.connection import AdapterResponse, Credentials, Connection

import mysql.connector


logger = AdapterLogger("Database")


@dataclass
class DatabaseCredentials(Credentials):
    database: Optional[str] = None
    schema: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    word: Optional[str] = None

    _ALIASES = {"base": "schema", "pass": "word"}

    @property
    def type(self):
        return "database"

    @property
    def unique_field(self):
        return f"{self.schema}/{self.host}/{self.port}"

    def _connection_keys(self):
        return (
            "schema",
            "host",
            "port",
            "user",
            "word",
        )


class DatabaseConnectionManager(SQLConnectionManager):
    TYPE = "database"

    @classmethod
    def open(cls, connection: Connection) -> Connection:
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection
        credentials = cls.get_credentials(connection.credentials)
        kwargs = {}
        kwargs["host"] = credentials.host
        kwargs["port"] = credentials.port
        kwargs["username"] = credentials.user
        kwargs["password"] = credentials.word
        try:
            connection.handle = mysql.connector.connect(**kwargs)
            connection.state = "open"
        except mysql.connector.Error as e:
            try:
                logger.debug(
                    "Failed connection without supplying the `database`. "
                    "Trying again with `database` included."
                )
                connection.handle = mysql.connector.connect(**kwargs)
                connection.state = "open"
            except mysql.connector.Error as e:
                logger.debug(
                    "Got an error when attempting to open a mysql "
                    "connection: '{}'".format(e)
                )
                connection.handle = None
                connection.state = "fail"
                raise FailedToConnectError(str(e))
        return connection

    @classmethod
    def get_credentials(cls, credentials):
        return credentials

    def cancel(self, connection: Connection):
        connection.handle.close()

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except mysql.connector.DatabaseError as e:
            logger.debug("Database error: {}".format(str(e)))
            raise DbtDatabaseError(str(e).strip()) from e
        except Exception as e:
            logger.debug("Error running SQL: {}", sql)
            if isinstance(e, DbtRuntimeError):
                raise
            raise DbtRuntimeError(e) from e

    @classmethod
    def get_response(cls, cursor) -> AdapterResponse:
        code = "SUCCESS"
        rows = 0
        if cursor is not None and cursor.rowcount is not None:
            rows = cursor.rowcount
        return AdapterResponse(
            _message="{} {}".format(code, rows), rows_affected=rows, code=code
        )

    @classmethod
    def begin(self):
        pass

    @classmethod
    def commit(self):
        pass
