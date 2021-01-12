from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseNotification


class TodoTransactionNotification(BaseModel, BaseNotification):
    id: int = Field(0, gt=0, title="todo id")
