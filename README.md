## API service on top of DuckDB
This project simply aims at building a REST API on top duckDB to explore certain things about building services on top of OLAP systems. Some of the things being explored, for example:
- Performance of using Arrow IPC streams instead of JSON as a serializable/deserializable format for transfer over the network.
- DukcDBs native integration with Arrow
- How easy is to build a service like this in an inmature language like Julia vs a fully estrablished language with a much more robust ecosystem, like Python

And some other things I just wanted to check out of personal curiosity. You can find a blogpost about it [here](https://guillesd.github.io/intro/2025/07/27/arrow-data-transfer.html).

## How to Use

This repository provides implementations in both Julia and Python. Follow the instructions below to set up and run the service in your preferred language.

### Julia Implementation

#### Prerequisites
- Install [Julia](https://julialang.org/downloads/).

#### Setup and running the service
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/duckdb-arrow-service.git
    cd duckdb-arrow-service/julia
    ```
2. Install dependencies with the Julia package manager in the REPL.
    ```
    add DuckDB JSONTables JSON DataFrames Genie
    ```
3. Run the seed script to get the TPCH tables:
    ```bash
    julia seed.jl
    ```
4. In the Julia REPL, run the following command to launch the server:
    ```julia
    using Genie; Genie.loadapp(); up(8000,async=true)
    ```

### Python Implementation

#### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

#### Setup and running the service
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/duckdb-arrow-service.git
    cd duckdb-arrow-service/python
    ```
2. Install dependencies using `uv` in a `venv`:
    ```bash
    uv sync
    ```
3. Run the seed script to get the TPCH tables:
    ```bash
    python seed.py
    ```

4. Start the REST API service using the FastAPI CLI:
    ```bash
    fastapi dev app.py 
    ```

The service will be available at `http://localhost:8000`.

## Notes
- The Julia implementation explores the challenges of using a less mature language for building services.
- The Python implementation leverages a more established ecosystem for comparison.

Feel free to experiment with both implementations and share your feedback!