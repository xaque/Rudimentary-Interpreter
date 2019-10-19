push!(LOAD_PATH, pwd())

using Lexer
using Error

let
	testnum = 0
	global tnum
	tnum() = testnum += 1
end
function testNum(num)
  return string(num) * ". "
end

function parseT(str)
  RudInt.parse(Lexer.lex(str))
end

function interpretT(str)
  RudInt.interp(str)
end

function removeNL(str)
replace(string(str), "\n" => "")
end

function testErr(f, param, num)
  try
    println(testNum(num) *  removeNL(f(param)))
  catch Y
    if (typeof(Y) != Error.LispError)
      println(testNum(num) * removeNL(Y))
    else
      println(testNum(num) * "Error")
    end
  end
end

function testPass(f, param, num)
  try
    f(param)
    println(testNum(num) * "Pass")
  catch Y
    println(testNum(num) * removeNL(Y))
  end
end

function testAns(f, param, num)
  try
    println(testNum(num) *  removeNL(f(param)))
  catch Y
    println(testNum(num) * removeNL(Y))
  end
end


testPass(parseT, "(+ 1 (- 3 4))", tnum()) # Pass RudInt
testErr(parseT, "(-)", tnum()) # Error
testErr(parseT, "if0", tnum()) # Error
testAns(interpretT, "(if0 1 2 3)", tnum()) #Pass
testAns(interpretT, "(with ((x 1)) x)", tnum()) # Pass
testPass(interpretT, "(lambda (x) x)", tnum()) # Pass
testPass(parseT, "(1 2 3)", tnum()) #Pass
testErr(interpretT, "(+ (lambda (x) x) 2)", tnum()) #Error
testErr(interpretT, "(collatz -1)", tnum()) #Error
testAns(interpretT, "((lambda () 4))", tnum()) # numval 4
#10
testAns(interpretT, "(+ 3 2)", tnum())
testAns(interpretT, "(+ 1 9223372036854775807)", tnum())
testAns(interpretT, "(+ 0 0)", tnum())
testErr(interpretT, "(+ 0 9223372036854775808)", tnum())
testErr(interpretT, "(+)", tnum())
testErr(interpretT, "+ 4 3", tnum())
testErr(interpretT, "(+ 99)", tnum())
testAns(interpretT, "(+ 1 2 3)", tnum())
testAns(interpretT, "(+ 1 2 3 4 5 6 7 8 9 10 11)", tnum())
testErr(interpretT, "(+ x q)", tnum())
testErr(interpretT, "(+ 9 q)", tnum())
testErr(interpretT, "(+ 9 with)", tnum())
testErr(interpretT, "(+ 45 234 a)", tnum())
testErr(interpretT, "(+ x 12 12)", tnum())
#24
testAns(interpretT, "(- 3 2)", tnum())
testAns(interpretT, "(- -1 9223372036854775807)", tnum())
testAns(interpretT, "(- 0 0)", tnum())
testErr(interpretT, "(- 0 9223372036854775808)", tnum())
testErr(interpretT, "(-)", tnum())
testErr(interpretT, "- 4 3", tnum())
testErr(interpretT, "(- 1 2 3)", tnum())
testErr(interpretT, "(- 1 2 3 4 5 6 7 8 9 10 11)", tnum())
testErr(interpretT, "(- x q)", tnum())
testErr(interpretT, "(- 9 q)", tnum())
testErr(interpretT, "(- 9 with)", tnum())
testErr(interpretT, "(- 45 234 a)", tnum())
testErr(interpretT, "(- x 12 12)", tnum())
#37
testAns(interpretT, "(- 2)", tnum())
testAns(interpretT, "(- -2)", tnum())
testAns(interpretT, "(- 9223372036854775807)", tnum())
testAns(interpretT, "(- -9223372036854775808)", tnum())
testAns(interpretT, "(- 0)", tnum())
testErr(interpretT, "(- 9223372036854775808)", tnum())
testErr(interpretT, "(- x)", tnum())
#44
testAns(interpretT, "(* 3 2)", tnum())
testAns(interpretT, "(* -1 87)", tnum())
testAns(interpretT, "(* 45654 0)", tnum())
testAns(interpretT, "(* 12.0 -1.0)", tnum())
#48
testAns(interpretT, "(/ 9 2)", tnum())
testAns(interpretT, "(/ -1 10.0)", tnum())
testErr(interpretT, "(/ 353 0)", tnum())
testErr(interpretT, "(/ / 98)", tnum())
testErr(interpretT, "(/)", tnum())
testErr(interpretT, "(/ 98)", tnum())
testErr(interpretT, "(/ 12 12 12)", tnum())
#55
testAns(interpretT, "(mod 3 2)", tnum())
testErr(interpretT, "(mod 0 0)", tnum())
testErr(interpretT, "(mod)", tnum())
testErr(interpretT, "(mod 12)", tnum())
testErr(interpretT, "(mod 12 12 12)", tnum())
#60
testAns(interpretT, "(collatz 1)", tnum())
testAns(interpretT, "(collatz 99)", tnum())
testErr(interpretT, "(collatz)", tnum())
testErr(interpretT, "(collatz 12 12)", tnum())
#64
testAns(parseT, "(q)", tnum())
testAns(parseT, "(qwerty23546uuioiop)", tnum())
testErr(parseT, "(if0)", tnum())
testErr(parseT, "(with)", tnum())
testErr(parseT, "(lambda)", tnum())
testErr(parseT, "(+)", tnum())
testErr(parseT, "(collatz)", tnum())
#71
testErr(parseT, "(* 0)", tnum())
testErr(parseT, "(* 353 6 678)", tnum())
testErr(interpretT, "(* x a)", tnum())
#74
testAns(interpretT, "(if0 0 1 1)", tnum())
testAns(interpretT, "(if0 (* 12 0) (+ 99 1) (* 749274 (+ 58399 (collatz 7385))))", tnum())
testErr(interpretT, "(if0 (lambda (x y) 1 2) 1 1)", tnum())
testAns(interpretT, "(if0 0 1 (lambda (x y) 1))", tnum())
testAns(interpretT, "(if0 0 (lambda (x y) 1) 1)", tnum())
#79
testAns(interpretT, "(with ((x 1)(y 2)(z 3)) (+ x (+ y z)))", tnum())
testAns(interpretT, "(with () 1)", tnum())
testErr(interpretT, "(with ((x 1)) x x)", tnum())
testErr(interpretT, "(with ((x)) x)", tnum())
testErr(interpretT, "(with (x 1) x)", tnum())
testErr(interpretT, "(with ((if0 1)) if0)", tnum())
testErr(interpretT, "(with ((z 1)(z 3)) z)", tnum())
#86
testAns(interpretT, "(lambda () 4)", tnum())
testAns(interpretT, "(lambda (x) x)", tnum())
testAns(interpretT, "(lambda (x) 34)", tnum())
testAns(interpretT, "(lambda (x y) (+ x y))", tnum())
testPass(interpretT, "(lambda (x y z ad qwe fop) (+ x (* ad (/ (fop) (+ ad qwe)))))", tnum())
testErr(interpretT, "(lambda (x if0) 4)", tnum())
testErr(interpretT, "(lambda (x 1) 4)", tnum())
testErr(interpretT, "(lambda (12 c) 4)", tnum())
testErr(interpretT, "(lambda (aslkdj with) 4)", tnum())
testPass(interpretT, "(lambda (x y) (+ x z))", tnum())
testErr(interpretT, "(lambda (x y x) (+ x y))", tnum())
testErr(interpretT, "(lambda (x (q a d)) (+ x y))", tnum())
testErr(parseT, "(lambda x 12)", tnum())
testErr(parseT, "(lambda 12)", tnum())
testErr(parseT, "(lambda () ())", tnum())
testErr(parseT, "(lambda x)", tnum())
#102
testPass(parseT, "(1 2 3)", tnum())
testPass(parseT, "((+ 2 4) (* 353 24) (with ((x 1)) (+ x 2)))", tnum())
testPass(parseT, "((lambda (x y) 12) 3)", tnum())
testPass(parseT, "((lambda (x) x))", tnum())
testAns(interpretT, "((lambda (x) x) 12)", tnum())
testAns(interpretT, "((lambda () 12))", tnum())
testAns(interpretT, "((lambda (x y) (+ x y)) 12 (+ 1 1))", tnum())
testAns(interpretT, "((lambda (x y z) (+ x (* y z))) (* 2 1) (/ 4 2) (+ 0 1))", tnum())
testErr(interpretT, "(1 2 3)", tnum())
testErr(interpretT, "((lambda () 12) 100)", tnum())
testErr(interpretT, "((lambda (x) x))", tnum())
testErr(interpretT, "((lambda (x) x) (12))", tnum())
testErr(interpretT, "((lambda (x y x) x) 12 42 14)", tnum())
testErr(interpretT, "(12 32 (lambda (x y) x))", tnum())
testErr(interpretT, "((+ 1 4) (lambda (x y) x)) 90", tnum())
testErr(interpretT, "((lambda (x y z) (+ x y)) (lambda () 53) 42 14)", tnum())
testErr(interpretT, "((lambda (x y z) (+ x y)) 12 (lambda (x) 422) 14)", tnum())
testAns(interpretT, "((lambda (x y z) x) (lambda () 53) 42 14)", tnum())
testAns(interpretT, "((lambda (x y z) x) 12 (lambda (x) 422) 14)", tnum())
#121