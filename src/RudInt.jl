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

# <AE> ::= (with ((<id> <AE>)*) <AE>)
struct WithNode <: AE
    vars::Dict{Symbol, AE}
    body::AE
end

# <AE> ::= <id>
struct VarRefNode <: AE
    sym::Symbol
end

# <AE> ::= (lambda (<id>*) <AE>)
struct FuncDefNode <: AE
    formals::Array{Symbol}
    body::AE
end

# <AE> ::= (<AE> <AE>*)
struct FuncAppNode <: AE
    fun_expr::AE
    arg_exprs::Array{AE}
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
    formals::Array{Symbol}
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
unops = Dict(:- => -, :collatz => collatz)

# Binary operations mapping from symbol to function
binops = Dict(:+ => +, :- => -, :* => *, :/ => divide, :mod => mod)


#               Parse Helper Functions
# ==================================================
#

function parseUnop(expr::Array{Any})
    return UnopNode(unops[expr[1]], parse(expr[2]))
end

function parseBinop(expr::Array{Any})
    return BinopNode(binops[expr[1]], parse(expr[2]), parse(expr[3]))
end

function parseIf0(expr::Array{Any})
    return If0Node(parse(expr[2]), parse(expr[3]), parse(expr[4]))
end

function parseWith(expr::Array{Any})
    vars = Dict()
    #TODO verify types
    for statement in expr[2]
        #TODO verify symbol not reserved
        vars[statement[1]] = parse(statement[2])
    end
    return WithNode(vars, parse(expr[3]))
end

function parseLambda(expr::Array{Any})
    vars = []
    for id in expr[2]
        push!(vars, id)
    end
    return FuncDefNode(vars, parse(expr[3]))
end

function parseFuncApp(expr::Array{Any})
    arg_exprs = []
    for i in 2:length(expr)
        push!(arg_exprs, parse(expr[i]))
    end
    return FuncAppNode(parse(expr[1]), arg_exprs)
end

#                      Parse
# ==================================================
#

function parse(expr::Number)
    return NumNode(expr)
end

function parse(expr::Symbol)
    return VarRefNode(expr)
end

function parse(expr::Array{Any})
    if length(expr) == 0
        throw(LispError("Empty expression!"))
    end
    op = expr[1]
    if haskey(unops, op)
        return parseUnop(expr)
    elseif haskey(binops, op)
        return parseBinop(expr)
    elseif op == :if0
        return parseIf0(expr)
    elseif op == :with
        return parseWith(expr)
    elseif op == :lambda
        return parseLambda(expr)
    end
    return parseFuncApp(expr)
end

function parse(expr::Any)
    type = typeof(expr)
    throw(LispError("Invalid type: $type"))
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
    ext_env = env
    for (k,v) in ast.vars
        binding_val = calc(v, ext_env)
        ext_env = ExtendedEnv(k, binding_val, ext_env)
    end
    return calc( ast.body, ext_env )
end

function calc( ast::VarRefNode, env::EmptyEnv )
    throw( LispError("Undefined variable " * string( ast.sym )) )
end

function calc( ast::VarRefNode, env::ExtendedEnv )
    if ast.sym == env.sym
        return env.val
    else
        return calc( ast, env.parent )
    end
end

function calc(ast::FuncDefNode, env::Environment)
    return ClosureVal(ast.formals, ast.body, env)
end

function calc(ast::FuncAppNode, env::Environment)
    #TODO expects first AE to be lambda and following not
    actual_parameters = []
    for expr in ast.arg_exprs
        push!(actual_parameters, calc(expr, env))
    end
    closure_val = calc(ast.fun_expr, env)
    ext_env = closure_val.env
    for (i, formal) in enumerate(closure_val.formals)
        ext_env = ExtendedEnv(formal, actual_parameters[i], ext_env)
    end
    return calc(closure_val.body, ext_env)
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
