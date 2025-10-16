from dbt.adapters.record import RecordReplayHandle

from dbt.adapters.database.record.cursor.cursor import DatabaseRecordReplayCursor


class DatabaseRecordReplayHandle(RecordReplayHandle):
    """A custom extension of RecordReplayHandle that returns
    a psycopg-specific DatabaseRecordReplayCursor object."""

    def cursor(self):
        cursor = None if self.native_handle is None else self.native_handle.cursor()
        return DatabaseRecordReplayCursor(cursor, self.connection)
