from pydantic import BaseModel
from typing import List

class Report(BaseModel):
    summary : str
    impact : str
    root_cause : str
    factors : List[str]
    action_items : List[str]