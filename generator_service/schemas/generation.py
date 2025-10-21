from pydantic import BaseModel


class GenerateRequest(BaseModel):
    length: int


class GenerateResponse(BaseModel):
    id: str
    initial_fill: str
    sequence: str


class GenerateFileRequest(BaseModel):
    length: int


class GenerateFileResponse(BaseModel):
    generation_id: str
    initial_fill: str
    file_url: str

class GenerateWinnersRequest(BaseModel):
    max_number: int
    count_of_winning_numbers: int

# Новая схема для ответа
class GenerateWinnersResponse(BaseModel):
    winning_tickets: str
    sequence: str
    initial_fill: str