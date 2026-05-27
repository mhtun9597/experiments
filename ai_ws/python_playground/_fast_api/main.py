from collections.abc import Callable
from contextlib import asynccontextmanager, contextmanager
from typing import Annotated, Any, AsyncGenerator, Awaitable, Final, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
import socketio
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
import asyncio
from starlette.responses import Response
from starlette.types import ASGIApp
from fastapi.middleware.cors import CORSMiddleware


class MyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, setting: str) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        print("before middleware called")
        response = await call_next(request)
        print("after middleware called")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Life span before hook")

        yield
        print("Life span after hook")

    except Exception as e:
        print("exception ", e)
    finally:
        print("Done")


async def get_resource() -> float:
    import asyncio
    from datetime import datetime

    await asyncio.sleep(2)
    return datetime.timestamp(datetime.now())


async def resource_provider[T](request: Request):
    print("Extracting Path now")
    return request.url.path


redis_url = "redis://localhost:6379/0"
from socketio import AsyncRedisManager

redis_manager = AsyncRedisManager(redis_url)


app: Final[FastAPI] = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    MyMiddleware,
    setting="Test",
)
sio = socketio.AsyncServer(
    client_manager=redis_manager, async_mode="asgi", cors_allowed_origins=["*"]
)
sio_app = socketio.ASGIApp(
    socketio_server=sio,
)
# sub_app = FastAPI()
# sub_app.mount("/", sio_app

app.mount("/socket.io", sio_app)


class Data(BaseModel):
    id: Optional[str] = None
    msg: str


class NS1(socketio.AsyncNamespace):

    def __init__(self, namespace: str, id: str) -> None:
        super().__init__(namespace)
        print("ID ", id)

    async def on_connect(self, sid: str, environ: Any, auth: Any):
        print(f"sid {sid} connected to ns1 {environ} and auth {auth}")
        await sio.save_session(sid, {"test": "test"}, namespace="/ns1")  # type: ignore
        query_str: str | None = environ.get("QUERY_STRING")
        if query_str:
            query_arr = query_str.split("&")
            session_query_str: str | None = next(
                (q for q in query_arr if q.startswith("sessionId")), None
            )
            if session_query_str:
                session: str | None = session_query_str.split("=")[1]
                print(session)

    async def on_disconnect(self, sid: str, reason: str):
        print(f"sid {sid} disconnected to ns1 {reason}")

    async def on_my_event(self, sid: str, data: str):

        print("data ", data)

        def cb(*args: Any) -> None:
            print(f"client {sid} acked ", args)

        await self.emit(event="my_event", data="Testing", to=sid, callback=cb)  # type: ignore

    async def on_enter_room(self, sid: str, data: str):
        await self.enter_room(room=data, sid=sid)  # type: ignore
        print("client entered room")

    async def on_room_event(self, sid: str, data: Any):

        # await self.emit(
        #     event="my_event",
        #     data="Testing",
        #     room=data,
        # )  # type: ignore
        print("broadcasted room event")


class NS2(socketio.AsyncNamespace):
    async def on_connect(self, sid: str, environ: Any):
        print(f"sid {sid} connected to ns2 {environ}")
        await sio.save_session(sid, {"test": "test"}, namespace="/ns2")  # type: ignore

    async def on_disconnect(self, sid: str, reason: str):
        print(f"sid {sid} disconnected to ns2 {reason}")

    async def on_my_event(self, sid: str, data: Any):
        session: dict = sio.get_session(sid)  # type: ignore
        print(f"session {session} received ns2 event {data}")


sio.register_namespace(NS1("/ns1", "sdfdsfds"))  # type: ignore

sio.register_namespace(NS2("/ns2"))  # type: ignore


PathInfo = Annotated[str, Depends(resource_provider)]


@sio.event  # type: ignore
async def connect(sid: str, environ: Any, auth: Any) -> None:
    print("Client connected: ", sid, auth)


@sio.event  # type: ignore
async def disconnect(sid: str, reason: str) -> None:
    print("Client disconnected: ", sid, reason)


@sio.on("message")  # type: ignore
async def handle_message(sid: str, data: Any) -> None:
    print("Message from ", sid, ": ", data)


# @contextmanager
# def timer():
#     ctx = ContextManager("Testingsdfsdfds")  # Setup
#     try:
#         yield ctx  # Execution occurs here
#     finally:
#         end_time = time.perf_counter()
#         elapsed = end_time - start_time
#         print(f"{label} completed in {elapsed:.4f} seconds")


class ContextManager:

    def __init__(self, session: str):
        self.session = session

    async def __aenter__(self) -> "ContextManager":
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        self.session = None
        print("Existed")


async def get_context() -> AsyncGenerator[ContextManager, Any]:

    try:
        async with ContextManager("Testing") as ctx:
            yield ctx
    except Exception as e:
        print(e)
    finally:
        pass


ContextManagerDep = Annotated[ContextManager, Depends(get_context)]

import aiofiles


async def async_file_streamer(file_path: str) -> AsyncGenerator[bytes, Any]:
    async with aiofiles.open(file_path, "rb") as f:
        while chunk := await f.read(1024 * 1024):
            yield chunk


async def async_file_reader(file_path: str):

    async with aiofiles.open(file_path, "rb") as f:
        return await f.read1()


from fastapi.responses import StreamingResponse, FileResponse
from langchain_unstructured import UnstructuredLoader
from fastapi import UploadFile, File


@app.post("/upload")
async def upload_file(file: UploadFile) -> str:
    print("received")
    # Async write in chunks
    file.headers
    print(file.size)
    file_path: str = file.filename or datetime.now().isoformat()
    chunk_size = 1024
    async with aiofiles.open(f"uploads/{file_path}", "wb") as out_file:
        content = await file.read()  # 1MB chunks
        for i in range(0, len(content), chunk_size):
            await out_file.write(content[i : i + chunk_size])

    # return FileResponse(
    #     path=file_path, media_type="application/octet-stream", filename="test.js"
    # )
    return "Success"


@app.get("/download1")
def download_file() -> StreamingResponse:
    print("called")
    file_path = "test.js"
    # return FileResponse(
    #     path=file_path, media_type="application/octet-stream", filename="test.js"
    # )
    return StreamingResponse(async_file_streamer(file_path), media_type="text/plain")


import io


@app.get("/ingest")
async def ingest() -> Any:
    file = await async_file_reader("test.js")
    print(file)
    loader = UnstructuredLoader(
        file=io.BytesIO(file), chunking_strategy="basic", metadata_filename="test.js"
    )
    docs = await loader.aload()
    print(docs)
    return "Success"


class _Request(BaseModel):
    name: str


class _Response(_Request):
    id: str


@app.post("/register/{region}")
async def register(req: _Request, region: str) -> _Response:
    return _Response(name=req.name, id=datetime.now().isoformat())


from datetime import datetime


class SampleResponse(BaseModel):
    msg: str
    status: bool
    dt: datetime
    data: Any


async def loop() -> None:
    for i in range(5):
        await asyncio.sleep(1)
        print("Working")


@app.get("/api")
async def root(path: PathInfo) -> SampleResponse:
    print("path ", path)

    # # raise HTTPException(status_code=404, detail={"a": "a"})
    # def cb(task: asyncio.Task[None]) -> None:
    #     print("Doneeee")

    # task = asyncio.create_task(loop())
    # task.add_done_callback(cb)

    await asyncio.sleep(3)
    return SampleResponse(msg="Test", status=True, dt=datetime.now(), data={"a": "a"})


class Account(BaseModel):
    id: int
    name: str
    country: str
    email: str


accs = [
    Account(id=1, name="MrFoo", country="china", email="foo@gmail.com"),
    Account(id=2, name="MsBoo", country="china", email="boo@gmail.com"),
]


@app.get("/accounts")
async def get_accounts() -> list[Account]:
    return accs


class AccCreationRequest(BaseModel):
    name: str
    email: str
    country: str


@app.post("/accounts")
async def register_accounts(acc: AccCreationRequest) -> str:
    id = id = len(accs) + 1
    accs.append(Account(id=id, name=acc.name, email=acc.email, country=acc.country))
    return f"Account Successfully Created with ID {id}"


if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run(
            "_fast_api.main:app",
            host="0.0.0.0",
            port=8083,
            reload=True,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
