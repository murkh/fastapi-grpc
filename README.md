# FastAPI gRPC Integration Example

This project is a demonstration of how to integrate a [FastAPI](https://fastapi.tiangolo.com/) application with a [gRPC](https://grpc.io/) service.

The FastAPI server can act as a gateway, receiving HTTP requests and forwarding them to a backend gRPC service for processing. This architecture allows you to leverage the web-friendliness of REST APIs and the performance of gRPC.

## Project Structure

A typical structure for this project would be:

```
.
├── proto/
│   └── user.proto          # Protobuf definition for the UserService
├── src/
│   ├── generated/          # Auto-generated gRPC code
│   │   ├── __init__.py
│   │   ├── user_pb2.py
│   │   └── user_pb2_grpc.py
│   ├── client.py           # Example gRPC client for testing
│   ├── main.py             # FastAPI application
│   └── server.py           # gRPC server implementation
├── .venv/                  # Python virtual environment
├── requirements.txt        # Project dependencies
└── README.md
```

## Prerequisites

- Python 3.8+
- `pip` and `venv`

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd fastapi-grpc
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    On Windows, use:

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install the dependencies:**
    Create a `requirements.txt` file if one doesn't exist:

    ```txt
    fastapi
    uvicorn[standard]
    grpcio
    grpcio-tools
    protobuf
    ```

    Then install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate gRPC Code:**
    The `src/generated` directory contains the Python code generated from the `.proto` file. If you modify `proto/user.proto`, you need to regenerate these files. First, ensure a `proto` directory exists and contains your `user.proto` file.
    ```bash
    python -m grpc_tools.protoc -I./proto --python_out=./src/generated --pyi_out=./src/generated --grpc_python_out=./src/generated ./proto/user.proto
    ```
    _Note: You might need to create an empty `src/generated/__init__.py` file to make it a package._

## Running the Application

You will likely need to run the gRPC server and the FastAPI server in separate terminals.

1.  **Start the gRPC Server:**

    ```bash
    python -m src.user_service
    ```

2.  **Start the FastAPI Server:**
    ```bash
    uvicorn src.main:app --reload
    ```

## Usage

Once both servers are running, you can interact with the FastAPI endpoint. For example, if you have a `/users/{user_id}` endpoint in FastAPI that calls the gRPC service:

```bash
curl http://127.0.0.1:8000/users/1
```

This might return a JSON response like:

```json
{
  "id": "1",
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```
