using DuckDB

con = DBInterface.connect(DuckDB.DB, "../db/database.duckdb")

# create tchp tables
DBInterface.execute(con, "INSTALL tpch")
DBInterface.execute(con, "LOAD tpch" )
DBInterface.execute(con, "CALL dbgen(sf = 10)")
DBInterface.close(con)