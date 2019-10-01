# example: run this with "python3 grader_filename.py your_code_filename"
# this is an auto-generated file for general student testing

import sys
import subprocess
import os
from difflib import Differ
if __name__ == "__main__":
    fn = sys.argv[1]
    tmp_fn = "tmp.jl"
    feedback_fn = "feedback.txt"
    run_cmd = "julia"
    tests = """

push!(LOAD_PATH, pwd())

using Lexer
using Error

function lexParse(str)
  RudInt.parse(Lexer.lex(str))
end

function parseInter(str)
  RudInt.calc(lexParse(str))
end

function removeNL(str)
  replace(string(str), "\n" => "")
end

function testerr(f, param)
  try
    return removeNL(f(param))
  catch Y
    return "Error"
  end
end

println(testerr(lexParse, "(+ 1 2)"))
println(testerr(lexParse, "(- 1 2)"))
println(testerr(lexParse, "+ 1 2"))
println(testerr(lexParse, "(a)"))

println(testerr(parseInter, "(- 1 2)"))
println(testerr(parseInter, "(* 1 2)"))
println(testerr(parseInter, "(collatz -1)"))
println(testerr(parseInter, "(/ 1 0)"))
println(testerr(parseInter, "(+ (- 10) (mod 10 2))"))
println(testerr(parseInter, "(+ (- (* (/ (mod (collatz (- -2)) 5) 2) (+ 1 1)) 11) 210)"))
println(testerr(parseInter, "(collatz 1230)"))
println(testerr(parseInter, "(/)"))
println(testerr(parseInter, "()"))
println(testerr(parseInter, "(/ 2)"))
println(testerr(parseInter, "(/ 312 394 120)"))
println(testerr(parseInter, "(/ sdf asf)"))
"""
    tests_info = """1. 1 point. parse (+ 1 2)
2. 1 point. parse (- 1 2)
3. 1 point. parse + 1 2
4. 1 point. parse (a)
5. 1 point. calc (- 1)
6. 1 point. calc (* 1 2)
7. 1 point. calc (collatz -1)
8. 1 point. calc (/ 1 0)
9. 1 point. calc (+ (- 10) (mod 10 2))
10. 1 point. calc (+ (- (* (/ (mod (collatz (- -2)) 5) 2) (+ 1 1)) 11) 210)
11. 1 point. calc (collatz 1230)
11. 1 point. calc (/)
11. 1 point. calc ()
11. 1 point. calc (/ 2)
11. 1 point. calc (/ 312 394 120)
11. 1 point. calc (/ sdf asf)
"""
    correctoutput = """Main.RudInt.BinopNode(+, Main.RudInt.NumNode(1), Main.RudInt.NumNode(2))
Main.RudInt.BinopNode(-, Main.RudInt.NumNode(1), Main.RudInt.NumNode(2))
Error
Error
-1
2
Error
Error
-10
200.0
70
Error
Error
Error
Error
Error
"""
    grade = 0
    total_possible = 0
    with open(fn, "r") as f:
        with open(tmp_fn, "w") as w:
            w.write(f.read())
            w.write(tests)
    cmd = [run_cmd, tmp_fn]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    studentoutput, err = process.communicate()
    studentoutput = studentoutput.decode('utf-8')
    comparison = "".join(Differ().compare(correctoutput.splitlines(1), studentoutput.splitlines(1)))
    error_line_nos = []
    extra_line_nos = []
    q_line_nos = []
    for count, i in enumerate(comparison.splitlines()):
        if "-" == i[0]:
            error_line_nos.append(count)
        elif "+" == i[0]:
            extra_line_nos.append(count)
        elif "?" == i[0]:
            q_line_nos.append(count)
    failed_tests_line_nos = []
    for x in error_line_nos:
        numextralines = len([y for y in extra_line_nos if y < x])
        numqlines = len([z for z in q_line_nos if z < x])
        failed_tests_line_nos.append(x - numextralines - numqlines)
    with open(feedback_fn, "w") as feedback_file:
        feedback_file.write("        Correct output:\n")
        feedback_file.write(str(correctoutput))
        feedback_file.write("\n        Your output:\n")
        feedback_file.write(str(studentoutput))
        feedback_file.write("\n        Failed tests:\n")
        for count, l in enumerate(tests_info.splitlines(1)):
            points = int(l.split()[1])
            if count in failed_tests_line_nos:
                total_possible += points
                feedback_file.write(l)
            else:
                total_possible += points
                grade += points
        feedback_file.write("\n        Grade:\n" + str(grade) + " out of " + str(total_possible))
    os.remove(tmp_fn)
    print("See feedback file: " + feedback_fn)
