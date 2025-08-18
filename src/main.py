from fastapi import FastAPI, HTTPException
import grpc
from pydantic import BaseModel

from .generated import user_pb2, user_pb2_grpc

app = FastAPI()


class UserResponse(BaseModel):
    id: str
    name: str
    email: str


@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        async with grpc.aio.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            response = await stub.GetUser(user_pb2.UserRequest(id=user_id))
            return UserResponse(id=response.id, name=response.name, email=response.email)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=404,
                detail={"error": "user not found",
                        "message": f"User with id {user_id} not found"}
            )
        raise HTTPException(status_code=500, detail={
                            "error": "Internal Server Error"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
