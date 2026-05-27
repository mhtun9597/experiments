import asyncio
import copy
from pathlib import Path
from types import NoneType
from typing import (
    Annotated,
    Any,
    AsyncGenerator,
    AsyncIterator,
    Generator,
    Generic,
    Iterator,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
import logging
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    TypeAdapter,
    ValidationError,
    ValidationInfo,
    create_model,
    field_validator,
)


class HandoffEevnt(BaseModel):
    h_id: str


class ConvEvent(BaseModel):
    id: str
    msg: str


class Event(BaseModel):
    type: str
    payload: Any


var = "124"


class IWS(BaseModel):
    sid: str


class WS(BaseModel):
    id: int
    sids: list[IWS]


from abc import ABC, abstractmethod


class Speakable(ABC):
    @abstractmethod
    def speak(self) -> int: ...


class Flyable(ABC):
    @abstractmethod
    def fly(self) -> str: ...


S = TypeVar("S", bound=Speakable)
F = TypeVar("F", bound=Flyable)


class Animal(Generic[S, F]):
    def __int__(self):
        super().__init__()


class Speakable1(Speakable):

    def speak(self) -> int:
        return 1


class Flyable1(Flyable):
    def fly(self) -> str:
        return "Testing"


class Animal1(Animal[Speakable1, Flyable1]):
    def __init__(self) -> None:
        super().__init__()


class Duck(Animal):

    async def speak(self) -> AsyncIterator[int]:
        print("waiting ")
        await asyncio.sleep(2)
        yield 1


_str = "Hello {World}"


async def _itr(r: int) -> AsyncIterator[int]:
    print("called _itr")
    for i in range(r):
        await asyncio.sleep(2)
        yield i


async def itr(r: int) -> AsyncIterator[int]:
    print("called itr")
    async for i in _itr(r):
        yield i


class C:

    def __init__(self, a: str, b: str) -> None:
        print(a, b)


def t(**kwargs: Any) -> None:
    C(**kwargs)


async def f() -> int:
    await asyncio.sleep(2)
    raise Exception("testing")


def cb(result: asyncio.Task[int]) -> None:
    async def __acb() -> None:
        print("result ", result.result())
        await asyncio.sleep(2)

    asyncio.create_task(__acb())


class C1:
    def __init__(self, name: str = "default") -> None:
        self.name = name


def t(**kwargs: Any) -> None:
    print(C1(**kwargs).name)


from datetime import datetime, timedelta


class Address(BaseModel):
    name: str


class Person(BaseModel):
    name: str
    address: list[Address]


# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

import re

import ast

logger = logging.getLogger(__name__)


async def request():
    import httpx

    try:
        async with httpx.AsyncClient() as client:

            res = await client.request(
                url="http://localhost:3333/register",
                method="POST",
                json={"name": "Facebook"},
            )
            return res.json()
    except Exception as e:
        logger.warning(f"http tool call failed {e}")
    return "Tool call failed"


async def kf(**kwargs: Any):
    url = "{test}"
    url = url.format(**kwargs)
    print(url)
    try:
        url = ast.literal_eval(url)
    except Exception as e:
        pass

    print(isinstance(url, str))


from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
# T = TypeVar("T")


class RequestContext:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


def wrapper_1(
    func: Callable[Concatenate[int, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Wrapper 1 see", args)
        print(kwargs)
        return await func(1, *args, **kwargs)

    return wrapper


def wrapper_2(
    func: Callable[Concatenate[int, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Wrapper 2 see", args)
        print(kwargs)
        return await func(2, *args, **kwargs)

    return wrapper


@wrapper_1
@wrapper_2
async def _t(one: int, two: int, test: str):
    print(
        "Test",
        one,
    )


def tt(t: list[Any]):
    pass


class MyModel(BaseModel):
    url: HttpUrl


__primitive_type: dict[
    Literal["string", "boolean", "integer", "number", "null"],
    type[str] | type[bool] | type[int] | type[float] | type[NoneType],
] = {"string": str, "boolean": bool, "number": float, "integer": int, "null": NoneType}


def __convert_outputSchema(schema: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for k, v in schema.items():
        if not isinstance(v, dict):
            continue
        props = cast(dict[str, Any], v)
        _type = props.get("type")
        if _type == "object":
            if props.get("properties"):
                model = __convert_outputSchema(props.get("properties"))  # type: ignore
                if model:
                    result[k] = create_model(k, **model)
        elif _type == "array":
            items = props.get("items")
            item_type = items.get("type")  # type: ignore

            if item_type in __primitive_type:
                result[k] = (list[__primitive_type[item_type]], ...)
            elif item_type == "object":
                if items.get("properties"):  # type: ignore
                    model = __convert_outputSchema(items.get("properties"))  # type: ignore
                    print(model)
                    print(create_model(k, **model))
                    if model:
                        result[k] = (list[create_model(k, **model)], ...)
            elif item_type == "array":
                model = __convert_outputSchema(items)  # type: ignore
                print("Array Model ", model)
                if model:
                    result[k] = (list[list[model.get("items")]], ...)
            elif item_type == "any":
                types = []
                annotates = []
                for vv in items.get("anyOf"):  # type: ignore
                    __type = vv.get("type")
                    if __type in __primitive_type:
                        types.append(__primitive_type.get(__type))  # type: ignore
                    elif __type == "object":
                        model = __convert_outputSchema(vv.get("properties"))
                        if model:
                            annotates.append(create_model(k, **model))  # type: ignore
                    elif __type == "array":
                        model = __convert_outputSchema(vv.get("items"))
                        if model:
                            types.append(model)  # type: ignore

                __types = []
                if types:
                    __types = [*types]
                if annotates:
                    if len(annotates) > 1:
                        __types = [
                            *__types,
                            Annotated[Union[*annotates], Field(discriminator="type")],
                        ]
                    else:
                        __types = [*__types, *annotates]
                if __types:
                    result[k] = (
                        list[Union[*__types] if len(__types) > 1 else __types[0]],
                        ...,
                    )
        elif _type in __primitive_type:
            result[k] = (__primitive_type[_type], ...)
        elif _type == "any":
            types = []
            annotates = []
            for vv in props.get("anyOf"):  # type: ignore
                __type = vv.get("type")
                if __type in __primitive_type:
                    types.append(__primitive_type.get(__type))  # type: ignore
                elif __type == "object":
                    model = __convert_outputSchema(vv.get("properties"))
                    if model:
                        annotates.append(create_model(k, **model))  # type: ignore
                elif __type == "array":
                    __items = vv.get("items")
                    item_type = __items.get("type")  # type: ignore
                    print("Arrraay Type ", item_type)
                    if item_type in __primitive_type:
                        types.append(list[__primitive_type[item_type]])
                    else:
                        array_model = __convert_outputSchema(vv)
                        print("array modelk ", array_model)
                        types.append(list[array_model.get("items")])

            __types = []
            if types:
                __types = [*types]
            if annotates:
                if len(annotates) > 1:

                    __types = [
                        *__types,
                        Annotated[Union[*annotates], Field(discriminator="type")],
                    ]
                else:
                    __types = [*__types, *annotates]
            if __types:
                result[k] = (
                    Union[*__types] if len(__types) > 1 else __types[0],
                    ...,
                )
        else:
            continue

    return result


# Descriptionable Field

D = TypeVar("D")


class AnnotatedToolInput(BaseModel, Generic[D]):
    description: Optional[str] = None
    default: Optional[D] = None
    model_config = ConfigDict(extra="forbid")


# For the model tool calling simplicity, not supported nested object
class ToolPrimitiveTypeField(AnnotatedToolInput[int | str | float | bool | NoneType]):
    type: Literal["boolean", "string", "integer", "number", "null"]


#
class ToolObjectTypeField(AnnotatedToolInput[dict[str, Any]]):
    properties: dict[
        str,
        Annotated[
            "ToolPrimitiveTypeField | ToolObjectTypeField |ToolListTypeField | AnyTypeField",
            Field(discriminator="type"),
        ],
    ]
    required: list[str]
    type: Literal["object"]


#  |  | AnyTypeField
class AnyTypeField(AnnotatedToolInput[Any]):
    anyOf: list[
        Annotated[
            "ToolPrimitiveTypeField | ToolObjectTypeField |ToolListTypeField | AnyTypeField",
            Field(discriminator="type"),
        ]
    ]
    type: Literal["any"]


class ToolListTypeField(AnnotatedToolInput[list[Any]]):
    items: Union[
        "ToolPrimitiveTypeField",
        "ToolObjectTypeField",
        "ToolListTypeField",
        "AnyTypeField",
    ] = Field(discriminator="type")
    type: Literal["array"]


class ToolValidationMsg(BaseModel):
    msg: str
    field: str


warnings: list[ToolValidationMsg] = []
errors: list[ToolValidationMsg] = []

field_depths: dict[str, int] = {}


def detect_input_schema_errors(
    prop: (
        ToolPrimitiveTypeField | ToolObjectTypeField | ToolListTypeField | AnyTypeField
    ),
    field: str,
) -> None:

    if isinstance(prop, ToolPrimitiveTypeField):
        # if not prop.description:
        #     warnings.append(
        #         ToolValidationMsg(
        #             field=f"{field}.descriptions",
        #             msg="add description for tool call awarness",
        #         )
        #     )

        __dict = prop.model_dump(exclude_unset=True)

        if "default" in __dict:
            __type = __primitive_type.get(prop.type)
            if type(prop.default) is not __type:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg="value must be {prop.type}",
                    )
                )
        return

    elif isinstance(prop, ToolObjectTypeField):
        # if not prop.description:
        #     warnings.append(
        #         ToolValidationMsg(
        #             field=f"{field}.descriptions",
        #             msg="add description for tool call awarness",
        #         )
        #     )
        if len(prop.properties.keys()) > 7:
            warnings.append(
                ToolValidationMsg(
                    field=f"{field}.properties",
                    msg="field length too long",
                )
            )
            return
        __fields = field.split(".")
        prev = field_depths.get(__fields[1]) or 0
        field_depths[__fields[1]] = prev + 1
        print(field_depths)
        for k in prop.required:
            if not k in prop.properties:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.required",
                        msg=f"{k} not include in ${field}.properties",
                    )
                )
        __dict = prop.model_dump(exclude_unset=True)
        if "default" in __dict:
            schema = __convert_outputSchema(prop.model_dump())
            print("Schemaa ", schema)
            try:
                model = create_model("model", **schema)
                model.model_validate(prop.default)
            except ValidationError:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg=f"invalid values",
                    )
                )
            except Exception:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg=f"invalid values",
                    )
                )

        for _field, _prop in prop.properties.items():
            detect_input_schema_errors(_prop, f"{field}.properties.{_field}")

        return

    elif isinstance(prop, ToolListTypeField):
        # if not prop.description:
        #     warnings.append(
        #         ToolValidationMsg(
        #             field=f"{field}.descriptions",
        #             msg="add description for tool call awarness",
        #         )
        #     )
        __dict = prop.model_dump(exclude_unset=True)
        if "default" in __dict:
            if not isinstance(__dict["default"], list):
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg=f"invalid values must be list",
                    )
                )
            else:
                schema = __convert_outputSchema(prop.model_dump())
                model = create_model("model", **schema)
                print("Array Default Schema ", schema)
                try:
                    for v in __dict["default"]:
                        model.model_validate({"items": v})
                except ValidationError as e:
                    print(e.errors())
                    errors.append(
                        ToolValidationMsg(
                            field=f"{field}.default",
                            msg=f"invalid values",
                        )
                    )

        return detect_input_schema_errors(prop.items, f"{field}.items")

    else:
        # if not prop.description:
        #     warnings.append(
        #         ToolValidationMsg(
        #             field=f"{field}.descriptions",
        #             msg="add description for tool call awarness",
        #         )
        #     )
        __dict = prop.model_dump(exclude_unset=True)
        if "default" in __dict:
            schema = __convert_outputSchema({field: __dict})
            print("SCHEMA ", schema)
            try:

                model = create_model("model", **schema)
                model.model_validate({field: prop.default})
            except ValidationError:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg=f"invalid values",
                    )
                )
            except Exception:
                errors.append(
                    ToolValidationMsg(
                        field=f"{field}.default",
                        msg=f"invalid values",
                    )
                )
        for i in range(len(prop.anyOf)):
            detect_input_schema_errors(prop.anyOf[i], f"{field}.anyOf[{i}]")


async def run():
    schema = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"anyOf": [{"type": "string"}, {"type": "null"}], "type": "any"},
            "parent": {
                "anyOf": [
                    {
                        "properties": {
                            "c": {"type": "string"},
                            "parent": {
                                "properties": {
                                    "b": {"type": "string"},
                                    "parent": {
                                        "properties": {"a": {"type": "string"}},
                                        "required": ["a"],
                                        "type": "object",
                                    },
                                },
                                "required": ["b", "parent"],
                                "type": "object",
                            },
                        },
                        "required": ["c", "parent"],
                        "type": "object",
                    },
                    {"type": "null"},
                ],
                "default": None,
                "type": "any",
            },
        },
        "required": ["id", "name"],
        "type": "object",
    }

    # tschema = {"properties": {"a": { "idd": 123}}}
    data = {
        "id": 1,
        "name": "O",
        "parent": {"c": "123", "parent": {"b": "sdfsd", "parent": {"a": "sdfdsfds"}}},
    }
    try:
        # _tschema = C.model_validate(tschema)
        # type_adapter = TypeAdapter(ToolObjectTypeField)

        _schema = ToolObjectTypeField.model_validate(schema)

        for field, prop in _schema.properties.items():
            detect_input_schema_errors(prop, f"properties.{field}")
        print("Fioeld Deptsh ", field_depths)
        for k, v in field_depths.items():
            if v > 2:
                warnings.append(
                    ToolValidationMsg(
                        field=f"{k}",
                        msg="nested. flatten args is better",
                    )
                )
        m_s = __convert_outputSchema(schema["properties"])
        print(m_s)
        # print(m_s)
        model = create_model("model", **m_s)
        dd = model.model_validate(data)
        print(dd)
        print("Warnings ", warnings)
        print("Errors ", errors)
    except ValidationError as e:
        print("Validation Errors in main")
        print(e.errors())

    # d = {
    #     "properties": {
    #         "id": {"type": "integer"},
    #         "name": {"type": "string"},
    #         "ages": {
    #             "properties": {"id": {"type": "integer"}},
    #             # "required": ["id"],
    #             "type": "object",
    #         },
    #     },
    #     # "required": ["id", "name", "ages"],
    #     "type": "object",
    # }
    # d = __add_required_field(d)  # type: ignore
    # res = {
    #     "properties": {
    #         "id": {"type": "integer"},
    #         "name": {"type": "string"},
    #         "ages": {
    #             "properties": {"id": {"type": "integer"}},
    #             "type": "object",
    #             "required": ["id"],
    #         },
    #     },
    #     "type": "object",
    #     "required": ["id", "name", "ages"],
    # }
    # print(d)
    # d: dict[str, Any] = {
    #     "id": {"type": "integer"},
    #     "name": {"type": "string"},
    #     "ages": {
    #         "items": {
    #             "items": {
    #                 "properties": {"id": {"type": "integer"}},
    #                 "required": ["id"],
    #                 "type": "object",
    #             },
    #             "type": "array",
    #         },
    #         "type": "array",
    #     },
    # }
    # data = {"id": 1, "name": "O", "ages": [[{"id": 123}]]}
    # structure = __convert_outputSchema(d)
    # print(structure)
    # if structure:
    #     model = create_model("model", **structure)
    #     model.model_validate(data)

    # c = {"parent": "dfgdf", "id": "werwere"}
    # field: dict[str, Any] = {"name": (list[int], ...)}
    # mode = create_model("mode", **field)
    # d = {"name": [1]}
    # try:
    #     mode.model_validate(d)
    # except ValidationError as e:
    #     print(e.errors())

    # try:
    #     M.model_validate(d)
    # except ValidationError as e:
    #     print(e.errors())
    #     ctx = e.errors()[0].get("ctx")
    #     if ctx:
    #         err = ctx.get("error")
    #         print(err)

    # data : dict[str, Any]= {"a": 3, "b": 1, "c": 2, "d" : "sdfdsfsd"}
    # filtered_sorted = dict(sorted(
    #     ((k, v) for k, v in data.items() if isinstance(v, int)),
    #     key=lambda item: item[1])

    #  )
    # print(filtered_sorted)

    # a = [1, 2]
    # a.append(3)
    # print(a)
    # await sleeper(2)
    # logger.critical("Testing")
    # import re

    # log: str = (
    #     "2026-04-23 10:39:42,443 - asyncio - DEBUG - Using proactor: IocpProactor"
    # )

    # pattern = (
    #     r"^(?P<timestamp>.*?) - (?P<service>.*?) - (?P<level>.*?) - (?P<message>.*)$"
    # )
    # match = re.match(pattern, log)
    # if match:
    #     data = match.groupdict()
    #     print(data["timestamp"])
    #     logger.info(data)
    # from datetime import datetime

    # s = "212312321"

    # dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S,%f")

    # print(dt)

    # a = [1, 2, 3]
    # print(a[3:])
    # print(a[:float[]-])


# import json
# chunk: bytes
# async with aiofiles.open(f"help.py", "rb") as out_file:
#     chunk = await out_file.read(1024 * 1024)
# print(b)
# s = b.decode()
# print(s)
# await kf(test="teterte")
# print(a)
# import ast

# res = await request()
# print(res)
# a = a.format(test="12312312")
# a = ast.literal_eval(a)
# print(a)
# print(isinstance(a, list))
# kf(test="1231232")

# json_string = '{"name": "John Doe", "id": "123456789", "verified": true}'
# my_dict = json.loads(json_string)

# print(my_dict)
# a = "12312"
# if a:
#     print("Triggered")
# current = datetime.now()
# future = current + timedelta(hours=1)
# print(current)

# print(future)

# sorted_items = sorted(d.items(), key=lambda x: x[1])

# print(sorted_items)


async def sleeper(sec: int):
    print("called")
    await asyncio.sleep(sec)
    print("waited")


async def start(id: int, sec: int) -> None:
    # t: asyncio.Task[None] = asyncio.create_task(sleeper(2))
    # t1: asyncio.Task[None] = asyncio.create_task(sleeper(4))

    # def cb(result: asyncio.Task[None]) -> None:
    #     print(f"Done ")

    # t.add_done_callback(cb)
    # t1.add_done_callback(cb)
    # print("Done all")
    # while True:
    #     await asyncio.sleep(3)
    print(f"started {id}")
    await sleeper(sec)
    print(f"finished {id}")


def ttt() -> str:
    a = ""
    return a or "Testinjg"


def trim_api_version(path: str) -> str:
    import re

    return re.sub(r"/v\d+(?=/)", "", path)


# tests
paths = [
    "api/v2/admin",
    "api/v10/admin",
    "api/admin",
    "api/v3/users/123",
]


def b(*args: Any) -> None:
    print(args)


def sync_fn(x: int) -> int:
    import time

    time.sleep(x)
    return x * 2


async def async_fn(x: int) -> int:
    return await asyncio.to_thread(sync_fn, x)


class A(BaseModel):
    type: Literal["A"]
    ida: int


class B(BaseModel):
    type: Literal["B"]
    idb: int


class C(BaseModel):
    c: Optional[int] = None


async def run1():
    c = C(c=None)
    print(c)
    print(c.model_dump(exclude_unset=True))


if __name__ == "__main__":
    asyncio.run(run())
# def process_desciption_required_warnings(
#     prop: (
#         MCPCompatibleToolInputPrimitiveTypeField
#         | MCPCompatibleToolInputListTypeField
#         | MCPCompatibleToolInput
#     ),
#     field: str,
# ) -> None:
#     if isinstance(prop, MCPCompatibleToolInputPrimitiveTypeField):
#         if not prop.description:
#             warnings.append(
#                 ToolValidationMsg(
#                     field=field,
#                     msg=f"should include description for tool call awarness by model.",
#                 )
#             )
#     if isinstance(prop, MCPCompatibleToolInputListTypeField):
#         if not prop.description:
#             warnings.append(
#                 ToolValidationMsg(
#                     field=field,
#                     msg=f"should include description for tool call awarness by model.",
#                 )
#             )
#         if isinstance(prop.items, MCPCompatibleToolInput):
#             process_desciption_required_warnings(
#                     prop.items, f"{field}.items"
#                 )
#         else:
#             if prop.items.description:
#                 warnings.append(
#                     ToolValidationMsg(
#                         field=field,
#                         msg=f"description field is not required",
#                     )
#                 )

#     if isinstance(prop, MCPCompatibleToolInput):
#         if not prop.description:
#             warnings.append(
#                 ToolValidationMsg(
#                     field=field,
#                     msg=f"should include description for tool call awarness by model.",
#                 )
#             )
#         # TODO : recursive
#         for k, _prop in prop.properties.items():
#             process_desciption_required_warnings(_prop, f"{field}.{k}")

# for k, prop in validated_tool.inputSchema.properties.items():
#     process_desciption_required_warnings(
#         prop, f"inputSchema.properties.{k}"
#     )
