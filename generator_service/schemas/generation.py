from pydantic import BaseModel


class GenerateRequest(BaseModel):
    length: int


class GenerateResponse(BaseModel):
    initial_fill: str
    sequence: str


class GenerateFileRequest(BaseModel):
    length: int


class GenerateFileResponse(BaseModel):
    generation_id: str
    initial_fill: str
    file_url: str
