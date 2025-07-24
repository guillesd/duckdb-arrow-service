import duckdb
import json
import numpy
import pyarrow as pa
import io
import datetime
from decimal import Decimal
from typing import Generator

##########################
### JSON Serialization ###
##########################


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def list_table_json_ser() -> str:
    with duckdb.connect("../db/database.duckdb") as conn:
        result = conn.execute("SHOW TABLES").fetchall()

    result_list = [row[0] for row in result]
    return json.dumps(result_list)


def get_table_stats_row_json_ser(table_name: str) -> str:
    with duckdb.connect("../db/database.duckdb") as conn:
        cursor = conn.execute(f"SUMMARIZE {table_name}")
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

    # Convert the data to a list of dictionaries to make it row oriented, then serialize to JSON
    result_dict = []
    for row in data:
        row_dict = {
            column_names[i]: float(row[i]) if isinstance(row[i], Decimal) else row[i]
            for i in range(len(column_names))
        }
        result_dict.append(row_dict)
    return json.dumps(result_dict)


def get_table_stats_column_json_ser(table_name: str) -> str:
    with duckdb.connect("../db/database.duckdb") as conn:
        result = conn.execute(f"SUMMARIZE {table_name}").fetchnumpy()

    # Use custom numpy serializer
    return json.dumps(result, cls=NumpyArrayEncoder)


def get_nrows_json_ser(table_name: str, nrows: int = 10000) -> str:
    with duckdb.connect("../db/database.duckdb") as conn:
        result = conn.execute(f"SELECT * FROM {table_name} LIMIT {nrows}").fetchnumpy()

    # Use custom numpy serializer
    return json.dumps(result, cls=NumpyArrayEncoder)


###########################
### Arrow Serialization ###
###########################


def get_table_stats_arrow_ser(table_name: str) -> Generator[io.BytesIO, None, None]:
    """
    Returns a generator that yields Arrow serialized statistics for the specified table.
    The generator yields memoryview objects from buffers
    """
    with duckdb.connect("../db/database.duckdb") as conn:
        batch_reader = conn.execute(
            f"SUMMARIZE {table_name}"
        ).fetch_record_batch()  # This is throwing a weird error
        return _arrow_reader_to_ipc_stream(batch_reader)


def get_nrows_arrow_ser(
    table_name: str, nrows: int = 10000
) -> Generator[io.BytesIO, None, None]:
    """
    Returns a generator that yields Arrow serialized rows for the specified table.
    The generator yields memoryview objects from buffers
    """
    with duckdb.connect("../db/database.duckdb") as conn:
        batch_reader = conn.execute(
            f"SELECT * FROM {table_name} LIMIT {nrows}"
        ).fetch_record_batch()
        return _arrow_reader_to_ipc_stream(batch_reader)


def _arrow_reader_to_ipc_stream(
    batch_reader: pa.RecordBatchReader,
) -> Generator[io.BytesIO, None, None]:
    """
    Converts a RecordBatchReader to an IPC stream in a BytesIO buffer.
    """
    arrow_schema = batch_reader.schema
    with (
        batch_reader as source,
        io.BytesIO() as sink,
        pa.ipc.new_stream(sink, arrow_schema) as writer,
    ):
        for batch in source:
            sink.seek(0)
            writer.write_batch(batch)
            sink.truncate()
            with sink.getbuffer() as buffer:
                yield buffer

        sink.seek(0)
        writer.close()
        sink.truncate()
        with sink.getbuffer() as buffer:
            yield buffer
