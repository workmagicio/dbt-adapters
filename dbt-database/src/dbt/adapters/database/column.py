from dbt.adapters.base import Column


class DatabaseColumn(Column):

    @property
    def quoted(self) -> str:
        return "`{}`".format(self.column)

    def __repr__(self) -> str:
        return f"<DatabaseColumn {self.name} ({self.data_type})>"
