import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.account import Account
from src.models.db.role import Role
from src.models.schemas.role import RoleInCreate, RoleInUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.securities.verifications.rolechecks import role_verifier
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist, ForbiddenAttrChange


class RoleCRUDRepository(BaseCRUDRepository):
    async def create_role(self, role_create: RoleInCreate) -> Role:
        new_role = Role(name=role_create.name, description=role_create.description, is_logged_in=True)

        self.async_session.add(instance=new_role)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_role)

        return new_role

    async def read_roles(self) -> typing.Sequence[Role]:
        stmt = sqlalchemy.select(Role)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_role_by_id(self, id: int) -> Role:
        stmt = sqlalchemy.select(Role).where(Role.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_role_by_name(self, name: str) -> Role:
        stmt = sqlalchemy.select(Role).where(Role.name == name)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with username `{username}` does not exist!")

        return query.scalar()  # type: ignore

    async def update_role_by_id(self, id: int, role_update: RoleInUpdate) -> Role:
        new_role_data = role_update.dict()

        select_stmt = sqlalchemy.select(Role).where(Role.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_role = query.scalar()

        if not update_role:
            raise EntityDoesNotExist(f"Role with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Role).where(Role.id == update_role.id).values(updated_at=sqlalchemy_functions.now())  # type: ignore

        if new_role_data["name"]:
            raise ForbiddenAttrChange(f"Changing role name {update_role.name} is not allowed!")

        if new_role_data["description"]:
            update_stmt = update_stmt.values(username=new_role_data["description"])

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_role)

        return update_role  # type: ignore

    async def delete_role_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(Role).where(Role.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_role = query.scalar()

        if not delete_role:
            raise EntityDoesNotExist(f"Role with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=Role).where(Role.id == delete_role.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Account with id '{id}' is successfully deleted!"

    async def read_role_by_acc_id(self, id: int) -> Role:
        user_stmt = sqlalchemy.select(Account).where(Account.id == id)
        query = await self.async_session.execute(statement=user_stmt)
        user = query.scalar()

        if not user:
            raise EntityDoesNotExist(f"User contained in JWT does not exist!")

        user_role = await self.read_role_by_id(user.role_id)

        return user_role

    async def is_role_taken(self, name: str) -> bool:
        name_stmt = sqlalchemy.select(Role.name).select_from(Role).where(Role.name == name)
        name_query = await self.async_session.execute(name_stmt)
        db_name = name_query.scalar()

        if not role_verifier.is_name_available(name=db_name):
            raise EntityAlreadyExists(f"Role with name `{name}` is already taken!")  # type: ignore

        return True
