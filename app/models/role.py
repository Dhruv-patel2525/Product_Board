from sqlmodel import Enum


class Role(str,Enum):
    ADMIN="admin"
    USER="user"
    MODERATOR="moderator"