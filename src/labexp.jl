using  DataFrames
using PGFPlotsX
using CSV


function list_files(path::AbstractString="."; pattern::Regex=r"", all_files::Bool=true, full_names::Bool=false)::Vector{String}
    files = [file for file in readdir(path) if isfile(abspath(joinpath(path, file)))]
    if pattern != r""
        files = [m.match for m in match.(pattern, files) if m != nothing]
    end
    if !all_files && Sys.isunix()
        files = [file for file in files if !startswith(file, '.')]
    end
    if full_names
        files = realpath.(files)
    end
    return files
end
