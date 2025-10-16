from dataclasses import dataclass, field
from dbt.adapters.base.relation import BaseRelation, Policy


@dataclass
class DatabaseQuotePolicy(Policy):
    schema: bool = True
    database: bool = False
    identifier: bool = True


@dataclass
class DatabaseIncludePolicy(Policy):
    schema: bool = True
    database: bool = False
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class DatabaseRelation(BaseRelation):
    quote_policy = field(default_factory=lambda: DatabaseQuotePolicy())
    include_policy = field(default_factory=lambda: DatabaseIncludePolicy())
    quote_character: str = "`"
