from dataclasses import dataclass
from enum import Enum


@dataclass
class SuapUserDTO:
    class Role(str, Enum):
        STUDENT = "Aluno"
        STAFF = "Servidor"

    registry: str
    name: str
    email: str
    role: "SuapUserDTO.Role"
    course: str
    profile_img_url: str
    password: str = None

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            registry=data["matricula"],
            name=data["vinculo"]["nome"],
            email=data["email"],
            role=data["tipo_vinculo"],
            course=data["vinculo"]["curso"],
            profile_img_url=data["url_foto_75x100"],
        )
