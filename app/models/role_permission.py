from sqlmodel import Field, SQLModel


class RolePermission(SQLModel,table=True):
    __tablename__="rolepermission"
    id:int | None = Field(default=None,primary_key=True)
    role_id:int=Field(nullable=False,foreign_key="role.id")
    permission_id:int=Field(nullable=False,foreign_key="permission.id")
