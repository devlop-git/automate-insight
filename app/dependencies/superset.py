from functools import lru_cache

from app.clients.superset_client import SupersetClient


@lru_cache()
def get_superset_client():
    return SupersetClient()

# @lru_cache()
# def get_db():
#     return SingletonDatabase().get_db()

