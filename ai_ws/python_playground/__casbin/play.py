from typing import cast
from casbin_async_sqlalchemy_adapter import Adapter  # type: ignore
import casbin
from sqlalchemy.ext.asyncio import create_async_engine


class TenantEnforcer:

    _adapter: Adapter
    _enforcer: casbin.async_enforcer.AsyncEnforcer

    def __init__(self) -> None:
        engine = create_async_engine("sqlite+aiosqlite:///__casbin/db.db")
        self._adapter = Adapter(engine)  # type: ignore
        self._enforcer = casbin.async_enforcer.AsyncEnforcer("__casbin/conf.conf", self._adapter)  # type: ignore

        def match_action(action: str, pattern: str) -> bool:
            """
            Match action against pattern with wildcard support

            Examples:
                _match_action("r", "r") -> True
                _match_action("r", "*") -> True
                _match_action("w", "r") -> False
            """
            print("Executing Custom Function")
            if pattern == "*":
                return True

            return action == pattern

        self._enforcer.add_function("matchAction", match_action)  # type: ignore

    async def initialize(self):
        # To load roles-policies from tenant db and register in policy storate
        await self._adapter.create_table()  # type: ignore
        await self._enforcer.load_policy()  # type: ignore
        print("Successfully initialized")

    async def assign_role_to_user(
        self, *, member_id: str, role: str, org_id: str
    ) -> None:
        # self._session.add(CasbinRule(ptype="g", v0=member_id, v1=role, v2=org_id))  # type: ignore
        # await self._session.commit()
        await self._enforcer.add_grouping_policy(member_id, role, org_id)  # type: ignore

    # Attach perimssion to user
    async def attach_permission_to_user(
        self,
        *,
        member_id: str,
        resource: str,
        action: str,
        org_id: str,
    ) -> None:
        # p = [ sub , domain , obj, action ]
        # self._session.add(CasbinRule(ptype="p", v0=role, v1=org_id, v2=resource, v3=action , v4=effect))  # type: ignore
        # await self._session.commit()
        await self._enforcer.add_policy(member_id, org_id, resource, action)  # type: ignore

    def have_permission(
        self, *, member_id: str, org_id: str, resource: str, action: str
    ) -> bool:
        # r = [ sub, domain, obj, action]
        self._enforcer.enforce(member_id, org_id, resource, action)  # type: ignore
        result: bool = self._enforcer.enforce(member_id, org_id, resource, action)  # type: ignore
        return cast(bool, result)

    async def create_role(
        self,
        *,
        role: str,
        org_id: str,
        resource: str,
        action: str,
    ) -> None:
        await self._enforcer.add_policy(role, org_id, resource, action)  # type: ignore

    async def attach_permission_to_role(
        self,
        *,
        role: str,
        org_id: str,
        resource: str,
        action: str,
    ) -> None:
        await self._enforcer.add_policy(role, org_id, resource, action)  # type: ignore
        # self._session.add(CasbinRule(ptype="p", v0=role, v1=org_id, v2=resource, v3=action , v4=effect))  # type: ignore
        # await self._session.commit()

    async def remove_permission_from_role(
        self,
        *,
        role: str,
        org_id: str,
        resource: str,
        action: str,
    ) -> None:
        await self.delete_permission_for_user(role, org_id, resource, action)  # type: ignore


async def main():
    e = TenantEnforcer()
    await e.initialize()
    # await e.create_role(role="admin", org_id="1", resource="data1", action="*")
    # # await e.attach_permission_to_role(
    # #     role="admin", org_id="domain1", resource="data1", action="write"
    # # )
    # await e.create_role(
    #     role="admin2", org_id="2", resource="data2", action="write"
    # )
    # await e.attach_permission_to_role(
    #     role="admin2", org_id="2", resource="data2", action="read"
    # )
    # await e.assign_role_to_user(member_id="1", role="admin", org_id="1")
    # await e.attach_permission_to_user(
    #     member_id="1", org_id="2", resource="data2", action="read"
    # )

    print(e.have_permission(member_id="1", org_id="1", resource="data1", action="read"))
    print(e.have_permission(member_id="1", org_id="2", resource="data2", action="read"))
    print(
        e.have_permission(member_id="1", org_id="2", resource="data2", action="write")
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
