from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionBase(BaseModel):
    id: str
    question: str
    options: List[str] = Field(default_factory=list)
    

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    pass

class FormBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    questions: List[QuestionBase]
    model_name: str
    model_version: str

class FormCreate(FormBase):
    pass

class FormOut(FormBase):
    id: str
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    questions: List[QuestionOut]

    class Config:
        orm_mode = True