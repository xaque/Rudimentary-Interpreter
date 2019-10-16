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

# Linked list of KV pairs
struct ExtendedEnv <: Environment
    sym::Symbol
    val::RetVal
    parent::Environment
end


#            Language Operation Definitions
# ==================================================
#

function divide(n1::Real, n2::Real)
    if n2 == 0
        throw(LispError("Divide by zero error!"))
    end
    return n1 / n2
end

function safeMod(n1::Real, n2::Real)
    if n2 == 0
        throw(LispError("Divide by zero error!"))
    end
    return mod(n1, n2)
end

function collatz(n::Real)
    if n <= 0
        throw(LispError("Collatz zero or less error!"))
    end
    return collatz_helper(n, 0)
end

function collatz_helper(n::Real, num_iters::Int)
    if n == 1
        return num_iters
    end
    if mod(n, 2) == 0
        return collatz_helper(n / 2, num_iters + 1)
    else
        return collatz_helper(3 * n + 1, num_iters + 1)
    end
end

# Unary operations mapping from symbol to function
unops = Dict(:- => -, :collatz => collatz)

# Binary operations mapping from symbol to function
binops = Dict(:+ => +, :- => -, :* => *, :/ => divide, :mod => safeMod)

# A set of symbols which should not be used as <id>
reservedSymbols = Set([:if0, :with, :lambda])
reservedSymbols = union(reservedSymbols, keys(unops))
reservedSymbols = union(reservedSymbols, keys(binops))


#               Error Helper Functions
# ==================================================
#

function typeError(actualType::Type, expectedType::Type)
    throw(LispError("Type Error: expected type $expectedType, but got $actualType"))
end

function syntaxError(message::String)
    throw(LispError("Syntax Error: $message"))
end

function arityError(op::Symbol, actual::Integer, expected::Integer)
    throw(LispError("Arity Error: Operation $op expected $expected arguments, but got $actual."))
end

function arityError(op::Symbol, actual::Integer, minExpected::Real, maxExpected::Real)
    throw(LispError("Arity Error: Operation $op expected $minExpected-$maxExpected arguments, but got $actual."))
end

function typeCheck(obj::Any, type::Type)
    if !(obj isa type)
        typeError(typeof(obj), type)
    end
end

function arityCheck(expr::Array{Any}, expectedLength::Integer)
    if length(expr) != expectedLength
        arityError(expr[1], length(expr) - 1, expectedLength - 1)
    end
end

function arityCheck(expr::Array{Any}, minExpLength::Real, maxExpLength::Real)
    if length(expr) < minExpLength || length(expr) > maxExpLength
        arityError(expr[1], length(expr) - 1, minExpLength - 1, maxExpLength - 1)
    end
end

function symbolCheck(sym::Symbol)
    if sym in reservedSymbols
        syntaxError("$sym is a reserved symbol")
    end
end

function symbolCheck(sym::Any)
    typeError(typeof(sym), Symbol)
end


#               Parse Helper Functions
# ==================================================
#

function parseUnop(expr::Array{Any})
    arityCheck(expr, 2)
    return UnopNode(unops[expr[1]], parse(expr[2]))
end

function parseBinop(expr::Array{Any})
    arityCheck(expr, 3)
    return BinopNode(binops[expr[1]], parse(expr[2]), parse(expr[3]))
end

function parseIf0(expr::Array{Any})
    arityCheck(expr, 4)
    return If0Node(parse(expr[2]), parse(expr[3]), parse(expr[4]))
end

function parseWith(expr::Array{Any})
    arityCheck(expr, 3)
    typeCheck(expr[2], Array)
    # Store (<id>, <AE>) pairs of variables and definitions
    vars = Dict()
    for statement in expr[2]
        # Check that statement looks like (<id> <AE>)
        typeCheck(statement, Array)
        if length(statement) != 2
            syntaxError("")
        end
        # Make sure symbol is not reserved
        symbolCheck(statement[1])
        vars[statement[1]] = parse(statement[2])
    end
    # Verify there are no duplicate definitions, i.e. (with ((x 1)(y 1)(x 2)) <AE>)
    if length(vars) != length(expr[2])
        syntaxError("Duplicate variable definition in with expression")
    end
    return WithNode(vars, parse(expr[3]))
end

function parseLambda(expr::Array{Any})
    arityCheck(expr, 3)
    typeCheck(expr[2], Array)
    # Store list of expected arguments
    vars = []
    for id in expr[2]
        symbolCheck(id)
        push!(vars, id)
    end
    # Verify there are no duplicate symbols used as argument variable names
    if length(vars) != length(Set(vars))
        syntaxError("Duplicate argument symbol in lambda expression")
    end
    return FuncDefNode(vars, parse(expr[3]))
end

function parseFuncApp(expr::Array{Any})
    # Store list of <AE>s following the first
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
    symbolCheck(expr)
    return VarRefNode(expr)
end

function parse(expr::Array{Any})
    if length(expr) == 0
        syntaxError("empty expression!")
    end
    op = expr[1]
    if op == :if0
        return parseIf0(expr)
    elseif op == :with
        return parseWith(expr)
    elseif op == :lambda
        return parseLambda(expr)
    # :- symbol can be used for negative (unary) or minus (binary) operations
    elseif op == :-
        if length(expr) == 2
            return parseUnop(expr)
        else
            return parseBinop(expr)
        end
    elseif haskey(unops, op)
        return parseUnop(expr)
    elseif haskey(binops, op)
        return parseBinop(expr)
    else
        return parseFuncApp(expr)
    end
end

function parse(expr::Any)
    type = typeof(expr)
    throw(LispError("Invalid type: $type"))
end


#                 Calculate/Evaluate
# ==================================================
#

function calc(ast::NumNode, env::Environment)
    return NumVal(ast.n)
end

function calc(ast::BinopNode, env::Environment)
    lhs = calc(ast.lhs, env)
    rhs = calc(ast.rhs, env)
    # Verify binop is only run on NumVals
    typeCheck(lhs, NumVal)
    typeCheck(rhs, NumVal)
    return NumVal(ast.op(lhs.n, rhs.n))
end

function calc(ast::UnopNode, env::Environment)
    child = calc(ast.child, env)
    # Verify unop is only run on NumVal
    typeCheck(child, NumVal)
    return NumVal(ast.op(child.n))
end

function calc(ast::If0Node, env::Environment)
    cond = calc(ast.cond, env)
    # Verify if condition is NumVal before accessing cond.n
    typeCheck(cond, NumVal)
    if cond.n == 0
        return calc(ast.zerobranch, env)
    else
        return calc(ast.nzerobranch, env)
    end
end

function calc(ast::WithNode, env::Environment)
    ext_env = env
    # Add variables from with expression to environment
    for (k, v) in ast.vars
        binding_val = calc(v, ext_env)
        typeCheck(binding_val, NumVal)
        ext_env = ExtendedEnv(k, binding_val, ext_env)
    end
    return calc(ast.body, ext_env)
end

function calc(ast::VarRefNode, env::EmptyEnv )
    throw(LispError("Undefined variable " * string(ast.sym)))
end

function calc(ast::VarRefNode, env::ExtendedEnv)
    # Recursively search environment for value
    if ast.sym == env.sym
        return env.val
    else
        return calc(ast, env.parent)
    end
end

function calc(ast::FuncDefNode, env::Environment)
    return ClosureVal(ast.formals, ast.body, env)
end

function calc(ast::FuncAppNode, env::Environment)
    # Store list of parameters for closure to absorb
    actual_parameters = []
    for expr in ast.arg_exprs
        push!(actual_parameters, calc(expr, env))
    end
    closure_val = calc(ast.fun_expr, env)
    typeCheck(closure_val, ClosureVal)
    # Check that parameters match expected for given closure
    ext_env = closure_val.env
    if length(actual_parameters) != length(closure_val.formals)
        arityError(:lambda, length(actual_parameters), length(closure_val.formals))
    end
    # Prepare to evaluate closure by adding arguments from actual_parameters into environment
    for (i, formal) in enumerate(closure_val.formals)
        ext_env = ExtendedEnv(formal, actual_parameters[i], ext_env)
    end
    # Evaluate closure with new environment
    return calc(closure_val.body, ext_env)
end

function calc(ast::AE)
    return calc(ast, EmptyEnv())
end


#                      Interpret
# ==================================================
#

function interp(cs::AbstractString)
    if length(cs) == 0
        throw(LispError("Empty program!"))
    end
    lxd = Lexer.lex(cs)
    ast = parse(lxd)
    return calc(ast)
end

end #module
