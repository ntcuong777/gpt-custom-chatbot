from pydantic import BaseModel, Field


class ModelRequestBody(BaseModel):
    user_query: str = Field(..., description="User query", alias="user_query")
    model: str = Field(..., description="Model name", alias="model")
    llm_params: dict = Field({}, description="Model specific parameters", alias="llm_params")


class NewSessionBody(BaseModel):
    model: str = Field(..., description="Model name", alias="model")
    user_id: str = Field("anonymous", description="User ID", alias="user_id")


class UpdateSysMsgBody(BaseModel):
    session_id: str = Field(..., description="Session ID", alias="session_id")
    system_message: str = Field(..., description="System message", alias="system_message")
