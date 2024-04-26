from pydantic import BaseModel, Json


class UserContextBase(BaseModel):
    context: Json


class UserContextCreateDTO(UserContextBase): ...


class UserContextUpdateDTO(UserContextBase): ...


class UserContextResponseDTO(UserContextBase):
    id: int
