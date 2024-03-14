using Markdown: Markdown, MD

struct Question
    messages::Dict{Symbol,MD}
    function Question(; kwargs...)
        messages = Dict(name => Markdown.parse(msg) for (name, msg) in kwargs)
        new(messages)
    end
end


function Base.getproperty(q::Question, sym::Symbol)
    if sym in fieldnames(typeof(q))
        return getfield(q, sym)
    else
        return q.messages[sym]
    end
end

function Base.propertynames(q::Question, private::Bool=false)
    return union(fieldnames(typeof(q)), keys(q.messages))
end
