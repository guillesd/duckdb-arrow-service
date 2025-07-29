import duckdb

if __name__ == "__main__":
    # Connect to the DuckDB database
    con = duckdb.connect("../db/database.duckdb")

    # Create TPCH tables
    con.execute("INSTALL tpch")
    con.execute("LOAD tpch")
    con.execute("CALL dbgen(sf=10)")

    # Close the connection
    con.close()
