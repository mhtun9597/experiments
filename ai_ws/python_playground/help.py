D = TypeVar("D")


class AnnotatedToolInput(BaseModel, Generic[D]):
    description: Optional[str] = None
    default: Optional[D] = None


# For the model tool calling simplicity, not supported nested object
class ToolPrimitiveTypeField(BaseModel):
    type: Literal["boolean", "string", "integer", "number"]


class ToolObjectTypeField(BaseModel):
    properties: dict[
        str,
        "AnnotatedToolPrimitiveTypeField | AnnotatedToolListTypeField | AnnotatedToolObjectTypeField | AnyTypeField",
    ]
    required: list[str]
    type: Literal["object"]


class AnyTypeField(BaseModel):
    anyOf: "ToolPrimitiveTypeField | ToolObjectTypeField | ToolListTypeField"


class ToolListTypeField(BaseModel):
    items: "ToolPrimitiveTypeField | ToolObjectTypeField | ToolListTypeField | AnyTypeField"
    type: Literal["array"]


class AnnotatedToolPrimitiveTypeField(
    ToolPrimitiveTypeField, AnnotatedToolInput[int | str | float | bool]
):
    pass


class AnnotatedToolObjectTypeField(
    ToolObjectTypeField, AnnotatedToolInput[dict[str, Any]]
):
    pass


class AnnotatedToolListTypeField(ToolListTypeField, AnnotatedToolInput[list[Any]]):
    pass