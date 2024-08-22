## Step-1

```bash
alembic init alembic
```

## Step-2

Modify `sqlalchemy.url` in alembic.ini

```bash
sqlalchemy.url = sqlite:///src/mydb.db
```

## Step-3

Modify env.py

```bash
from src.models import Base
...
target_metadata = Base.metadata
```

## Step-4

```bash
alembic revision --autogenerate
```
