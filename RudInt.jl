#
# Rudimentary Interpreter 0
#

module RudInt

push!(LOAD_PATH, pwd())

using Error
using Lexer
export parse, calc, interp


#                 Grammar Definition
# ==================================================
#

# <AE>
abstract type AE
end

# <AE> ::= <number>
struct NumNode <: AE
    n::Real
end

# <AE> ::= (<op> <AE>)
struct UnopNode <: AE
    op::Function
    child::AE
end

# <AE> ::= (<op> <AE> <AE>)
struct BinopNode <: AE
    op::Function
    lhs::AE
    rhs::AE
end


#            Language Operation Definitions
# ==================================================
#

function divide( n1::Real, n2::Real)
    if n2 == 0
        throw( LispError("Divide by zero error!") )
    end
    return n1 / n2
end

function collatz( n::Real )
    if n <= 0
        throw( LispError("Collatz zero or less error!") )
    end
    return collatz_helper( n, 0 )
end

function collatz_helper( n::Real, num_iters::Int )
    if n == 1
        return num_iters
    end
    if mod(n,2)==0
        return collatz_helper( n/2, num_iters+1 )
    else
        return collatz_helper( 3*n+1, num_iters+1 )  
    end
end

# Unary operations mapping from symbol to function
unOps = Dict(:- => -, :collatz => collatz)

# Binary operations mapping from symbol to function
binOps = Dict(:+ => +, :- => -, :* => *, :/ => divide, :mod => mod)


#                 Helper Functions
# ==================================================
#

function getOpFunction( op::Symbol, dict::Dict )
    if !haskey( dict, op )
        throw( LispError("Invalid expression at: $op") )
    end
    return dict[op]
end


#                      Parse
# ==================================================
#

function parse( expr::Number )
    return NumNode( expr )
end

function parse( expr::Array{Any} )
    len = length(expr)
    if len == 0
        throw( LispError("Empty expression!") )
    elseif len == 2
        return UnopNode( getOpFunction( expr[1], unOps ), parse( expr[2] ) )
    elseif len == 3
        return BinopNode( getOpFunction( expr[1], binOps ), parse( expr[2] ), parse( expr[3] ) )
    end
    op = expr[1]
    throw( LispError("Invalid expression at: $op") )
end

function parse( expr::Any )
  throw( LispError("Invalid type: $expr") )
end


#                 Calculate/Evaluate
# ==================================================
#

function calc( ast::NumNode )
    return ast.n
end

function calc( ast::BinopNode )
    return ast.op( calc( ast.lhs ), calc( ast.rhs ) )
end

function calc( ast::UnopNode )
    return ast.op( calc( ast.child ) )
end


#                      Interpret
# ==================================================
#

function interp( cs::AbstractString )
    lxd = Lexer.lex( cs )
    ast = parse( lxd )
    return calc( ast )
end

end #module
