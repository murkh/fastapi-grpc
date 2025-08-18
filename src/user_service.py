import grpc
from concurrent import futures
from .generated import user_pb2, user_pb2_grpc


class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user_data = {
            "1": {"id": "1", "name": "Gaurav", "email": "gaurav@mailinator.com"},
            "2": {"id": "2", "name": "Shubham", "email": "shubham@mailinator.com"},
        }

        user_id = request.id
        if user_id not in user_data:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with id {user_id} not found")
            raise Exception("User not found")

        user = user_data[user_id]
        return user_pb2.UserResponse(
            id=user_id,
            name=user['name'],
            email=user["email"]
        )


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051 ...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve_grpc()
