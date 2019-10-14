#
# Rudimentary Interpreter 2
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

# <AE> ::= (if0 <AE> <AE> <AE>)
struct If0Node <: AE
    cond::AE
    zerobranch::AE
    nzerobranch::AE
end

# <AE> ::= (with <id> <AE> <AE>)
struct WithNode <: AE
    sym::Symbol
    binding_expr::AE
    body::AE
end

# <AE> ::= <id>
struct VarRefNode <: AE
    sym::Symbol
end

# <AE> ::= (lambda <id> <AE>)
struct FuncDefNode <: AE
    formal::Symbol
    body::AE
end

# <AE> ::= (<AE> <AE>)
struct FuncAppNode <: AE
    fun_expr::AE
    arg_expr::AE
end


#             Environment/Return Types
# ==================================================
#

abstract type RetVal
end

abstract type Environment
end

struct NumVal <: RetVal
    n::Real
end

struct ClosureVal <: RetVal
    formal::Symbol
    body::AE
    env::Environment
end

struct EmptyEnv <: Environment
end

struct ExtendedEnv <: Environment
    sym::Symbol
    val::RetVal
    parent::Environment
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

function parse2( expr::Array{Any} )
    if expr[1] isa Symbol && haskey( unOps, expr[1] )
        return UnopNode( getOpFunction( expr[1], unOps ), parse( expr[2] ) )
    end
    return FuncAppNode( parse(expr[1]), parse(expr[2]) )
end

function parse3( expr::Array{Any} )
    if expr[1] == :lambda
        return FuncDefNode( expr[2], parse(expr[3]) )
    end
    return BinopNode( getOpFunction( expr[1], binOps ), parse( expr[2] ), parse( expr[3] ) )
end

function parse4( expr::Array{Any} )
    if expr[1] == :if0
        return If0Node( parse(expr[2]), parse(expr[3]), parse(expr[4]) )
    elseif expr[1] == :with
        return WithNode( expr[2], parse(expr[3]), parse(expr[4]) )
    end
end


#                      Parse
# ==================================================
#

function parse( expr::Number )
    return NumNode( expr )
end

function parse( expr::Symbol )
    return VarRefNode( expr )
end

function parse( expr::Array{Any} )
    len = length(expr)
    if len == 0
        throw( LispError("Empty expression!") )
    elseif len == 2
        return parse2(expr)     
    elseif len == 3
        return parse3(expr)
    elseif len == 4
        return parse4(expr)
    end
    op = expr[1]
    throw( LispError("Invalid expression at: $op") )
end

function parse( expr::Any )
    type = typeof(expr)
    throw( LispError("Invalid type: $type") )
end


#                 Calculate/Evaluate
# ==================================================
#

function calc( ast::NumNode, env::Environment )
    return NumVal(ast.n)
end

function calc( ast::BinopNode, env::Environment )
    return NumVal( ast.op( calc( ast.lhs, env ).n, calc( ast.rhs, env ).n ) )
end

function calc( ast::UnopNode, env::Environment )
    return NumVal( ast.op( calc( ast.child, env ).n ) )
end

function calc( ast::If0Node, env::Environment )
    cond = calc( ast.cond, env )
    if cond.n == 0
        return calc( ast.zerobranch, env )
    else
        return calc( ast.nzerobranch, env )
    end
end

function calc( ast::WithNode, env::Environment )
    binding_val = calc( ast.binding_expr, env )
    ext_env = ExtendedEnv( ast.sym, binding_val, env )
    return calc( ast.body, ext_env )
end

function calc( ast::VarRefNode, env::EmptyEnv )
    throw( Error.LispError("Undefined variable " * string( ast.sym )) )
end

function calc( ast::VarRefNode, env::ExtendedEnv )
    if ast.sym == env.sym
        return env.val
    else
        return calc( ast, env.parent )
    end
end

function calc( ast::FuncDefNode, env::Environment )
    return ClosureVal( ast.formal, ast.body , env )
end

function calc( ast::FuncAppNode, env::Environment )
    closure_val = calc( ast.fun_expr, env )
    actual_parameter = calc( ast.arg_expr, env )
    ext_env = ExtendedEnv( closure_val.formal,
                           actual_parameter,
                           closure_val.env )
    return calc( closure_val.body, ext_env )
end

function calc( ast::AE )
    return calc( ast, EmptyEnv() )
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
