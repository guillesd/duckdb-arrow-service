module Backend
using DuckDB, JSONTables, JSON, DataFrames
export random_name, get_table_stats

const DB = DuckDB.DB("../db/database.duckdb")

function list_tables()::String
    # This function returns an array of tables in the duckdb database
    con = DBInterface.connect(DB)
    query = "SHOW TABLES"
    result = DBInterface.execute(con, query)
    DBInterface.close(con)
    table_array = String[]
    collected_result = collect(result)
    for i in eachindex(collected_result)
        push!(table_array, collected_result[i].name)
    end
    return JSON.json(table_array)
end

function get_table_stats(table_name::String)::String
    # This function returns a pretty table with the stats of the table as a HTML formatted String
    con = DBInterface.connect(DB)
    query = "SUMMARIZE $table_name"
    result = DBInterface.execute(con, query)
    DBInterface.close(con)
    result_df = DataFrame(result)
    json_str = arraytable(result_df)
    return json_str
end

end