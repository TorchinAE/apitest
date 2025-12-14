from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import EmailStr, BaseModel


class CreateUser(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
