from dbt.adapters.database.relation_configs.constants import (
    MAX_CHARACTERS_IN_IDENTIFIER,
)
from dbt.adapters.database.relation_configs.index import (
    DatabaseIndexConfig,
    DatabaseIndexConfigChange,
)
from dbt.adapters.database.relation_configs.materialized_view import (
    DatabaseMaterializedViewConfig,
    DatabaseMaterializedViewConfigChangeCollection,
)
