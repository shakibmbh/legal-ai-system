
from pydantic import BaseModel
from typing import List

class LegalDocument(BaseModel):

    parties: List[str]

    dates: List[str]

    obligations: List[str]

    notices: List[str]

    addresses: List[str]
