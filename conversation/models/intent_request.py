from pydantic import BaseModel


class IntentRequest(BaseModel):
    user_input: str
