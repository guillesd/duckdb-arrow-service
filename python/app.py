from backend import list_table_json_ser, get_table_stats_column_json_ser, get_table_stats_row_json_ser, get_table_stats_arrow_ser, get_nrows_json_ser, get_nrows_arrow_ser
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/list")
def list_tables():
    return Response(content=list_table_json_ser(), media_type="application/json")


@app.get("/stats/json/{table_name}")
def get_table_stats_json(table_name: str, format: str = "row"):
    if format == "row":
        return Response(content=get_table_stats_row_json_ser(table_name), media_type="application/json")
    elif format == "column":
        return Response(content=get_table_stats_column_json_ser(table_name), media_type="application/json")
    else:
        return Response(content="Invalid format specified. Use 'row' or 'column'.", media_type="text/plain", status_code=400)
    
@app.get("/stats/arrow/{table_name}")
def get_table_stats_arrow(table_name: str):
    # Placeholder for Arrow format implementation
    return StreamingResponse(
        get_table_stats_arrow_ser(table_name),
        media_type="application/vnd.apache.arrow.stream"
    )

@app.get("/rows/json/{table_name}")
def get_nrows_json(table_name: str, nrows: int = 10000):
    return Response(content=get_nrows_json_ser(table_name, nrows), media_type="application/json")

@app.get("/rows/arrow/{table_name}")
def get_nrows_arrow(table_name: str, nrows: int = 10000):
    return StreamingResponse(
        get_nrows_arrow_ser(table_name, nrows),
        media_type="application/vnd.apache.arrow.stream"
    )