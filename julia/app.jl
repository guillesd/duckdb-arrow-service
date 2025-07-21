include("backend.jl")

using Genie, Genie.Renderer.Html, Genie.Renderer.Json
using .Backend

route("/list") do
    return Backend.list_tables()
end

route("/stats/:table_name::String") do
    return Backend.get_table_stats(params(:table_name))
end