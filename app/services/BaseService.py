
from fastapi import HTTPException


class BaseService:
    def find_by_id(self, items, id_field: str, value: str, detail: str):
        result = next((i for i in items if getattr(i, id_field) == value), None)
        if result is None:
            raise HTTPException(status_code=404, detail=detail)
        return result
