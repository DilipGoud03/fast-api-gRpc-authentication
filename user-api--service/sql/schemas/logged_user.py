from __future__ import annotations
from typing import List
from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True  # replaces orm_mode in v2
    }
