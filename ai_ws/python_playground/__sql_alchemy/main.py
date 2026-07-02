from typing import Any, Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy import Column, ForeignKey, Integer, String, Table, select, text
import asyncio
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    joinedload,
    mapped_column,
    relationship,
)


class BaseDB(DeclarativeBase):
    pass


# c = Table(
#     "c",
#     BaseDB.metadata,
#     Column(
#         "a_id",
#         Integer,
#         ForeignKey("as.id", ondelete="CASCADE"),
#         primary_key=True,
#     ),
#     Column(
#         "b_id",
#         Integer,
#         ForeignKey("bs.id", ondelete="CASCADE"),
#         primary_key=True,
#     ),
# )


class A(BaseDB):

    __tablename__ = "as"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bs: Mapped[list["B"]] = relationship(
        "B",
    )  # References org_members.user_id


class B(BaseDB):
    __tablename__ = "bs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    a_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("as.id"), nullable=True, index=True
    )  # References org_members.user_id


async def run():
    connection = "postgresql+asyncpg://mhmarkets:mhmarkets@localhost:5432/test"
    _engine = create_async_engine(connection, echo=True)
    async with _engine.begin() as conn:
        try:
            await conn.run_sync(
                BaseDB.metadata.drop_all,
            )

            await conn.run_sync(
                BaseDB.metadata.create_all,
            )
        except Exception as e:
            print("Exception Table Create ", e)
        finally:
            pass
            # await conn.close()

    print("successfully created")

    Session = async_sessionmaker(
        _engine,
        expire_on_commit=False,
    )

    async with Session() as session:
        try:
            a = A()
            b = B()
            a.bs.append(b)
            session.add(a)
            await session.commit()
            await session.refresh(a)
            await session.refresh(b)
            query = await session.execute(
                select(A).where(A.id == a.id).options(joinedload(A.bs))
            )
            a = query.unique().scalar_one_or_none()
            if a:
                a.bs.remove(b)
                await session.commit()

        except Exception as e:
            print("Exception ", e)


if __name__ == "__main__":
    asyncio.run(run())
