# example: run this with "python grader_filename.py your_code_filename"
# this is an auto-generated file for general student testing

import sys
import subprocess
import os
from difflib import Differ
if __name__ == "__main__":
    fn = sys.argv[1]
    tmp_fn = "tmp.rkt"
    feedback_fn = "feedback.txt"
    run_cmd = "julia"
    tests = """

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
  ExtInt.parse(Lexer.lex(str))
end

function interpretT(str)
  ExtInt.calc(parseT(str))
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
testErr(interpretT, "(+ 1 2 3)", tnum())
testErr(interpretT, "(+ 1 2 3 4 5 6 7 8 9 10 11)", tnum())
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
"""
    tests_info = """1. 1 point. parse (+ 1 (- 3 4)), nested expressions
2. 1 point. parse (-) Be sure to check arguments
3. 1 point. parse if0, Don't use Key words as id's
4. 1 point. calc (if0 1 2 3), Make sure your If statements work
5. 1 point. calc (with ((x 1)) x), Make sure your withs work
6. 1 point. calc (lambda (x) x), Make sure your lambdas parse and calc
7. 1 point. parse (1 2 3), Not a parse error,
8. 1 point. calc (+ (lambda (x) x) 2), make sure to check your types
9. 1 point. calc (collatz -1), Don't allow invalid arithmatic
10. 1 point. calc ((lambda () 4)), Function application
11. 1 point. Main.ExtInt.NumVal(5)
12. 1 point. Main.ExtInt.NumVal(-9223372036854775808)
13. 1 point. Main.ExtInt.NumVal(0)
14. 1 point. Error
15. 1 point. Error
16. 1 point. Error
17. 1 point. Error
18. 1 point. Error
19. 1 point. Error
20. 1 point. Error
21. 1 point. Error
22. 1 point. Error
23. 1 point. Error
24. 1 point. Error
25. 1 point. Main.ExtInt.NumVal(2)
26. 1 point. Main.ExtInt.NumVal(-9223372036854775808)
27. 1 point. Main.ExtInt.NumVal(0)
28. 1 point. Error
29. 1 point. Error
30. 1 point. Error
31. 1 point. Error
32. 1 point. Error
33. 1 point. Error
34. 1 point. Error
35. 1 point. Error
36. 1 point. Error
37. 1 point. Error
38. 1 point. Main.ExtInt.NumVal(-1)
39. 1 point. Main.ExtInt.NumVal(2)
40. 1 point. Main.ExtInt.NumVal(0)
41. 1 point. Main.ExtInt.NumVal(-9223372036854775807)
42. 1 point. Main.ExtInt.NumVal(-9223372036854775808)
43. 1 point. Error
44. 1 point. Error
45. 1 point. Main.ExtInt.NumVal(6)
46. 1 point. Main.ExtInt.NumVal(-87)
47. 1 point. Main.ExtInt.NumVal(0)
48. 1 point. Main.ExtInt.NumVal(-12.0)
49. 1 point. Main.ExtInt.NumVal(4.5)
50. 1 point. Main.ExtInt.NumVal(-0.1)
51. 1 point. Error
52. 1 point. Error
53. 1 point. Error
54. 1 point. Error
55. 1 point. Error
56. 1 point. Main.ExtInt.NumVal(1)
57. 1 point. Error
58. 1 point. Error
59. 1 point. Error
60. 1 point. Error
61. 1 point. Main.ExtInt.NumVal(0)
62. 1 point. Main.ExtInt.NumVal(25)
63. 1 point. Error
64. 1 point. Error
65. 1 point. Main.ExtInt.FuncAppNode(Main.ExtInt.VarRefNode(:q), Main.ExtInt.AE[])
66. 1 point. Main.ExtInt.FuncAppNode(Main.ExtInt.VarRefNode(:qwerty23546uuioiop), Main.ExtInt.AE[])
67. 1 point. Error
68. 1 point. Error
69. 1 point. Error
70. 1 point. Error
71. 1 point. Error
72. 1 point. Error
73. 1 point. Error
74. 1 point. Error
75. 1 point. Main.ExtInt.NumVal(1)
76. 1 point. Main.ExtInt.NumVal(100)
77. 1 point. Error
78. 1 point. Main.ExtInt.NumVal(1)
79. 1 point. Main.ExtInt.ClosureVal(Symbol[:x, :y], Main.ExtInt.NumNode(1), Main.ExtInt.EmptyEnv())
80. 1 point. Main.ExtInt.NumVal(6)
81. 1 point. Main.ExtInt.NumVal(1)
82. 1 point. Error
83. 1 point. Error
84. 1 point. Error
85. 1 point. Error
86. 1 point. Error
87. 1 point. Main.ExtInt.ClosureVal(Symbol[], Main.ExtInt.NumNode(4), Main.ExtInt.EmptyEnv())
88. 1 point. Main.ExtInt.ClosureVal(Symbol[:x], Main.ExtInt.VarRefNode(:x), Main.ExtInt.EmptyEnv())
89. 1 point. Main.ExtInt.ClosureVal(Symbol[:x], Main.ExtInt.NumNode(34), Main.ExtInt.EmptyEnv())
90. 1 point. Main.ExtInt.ClosureVal(Symbol[:x, :y], Main.ExtInt.BinopNode(+, Main.ExtInt.VarRefNode(:x), Main.ExtInt.VarRefNode(:y)), Main.ExtInt.EmptyEnv())
91. 1 point. Pass
92. 1 point. Error
93. 1 point. Error
94. 1 point. Error
95. 1 point. Error
96. 1 point. Error
97. 1 point. Error
98. 1 point. Error
99. 1 point. Error
100. 1 point. Error
101. 1 point. Error
102. 1 point. Error
103. 1 point. Pass
104. 1 point. Pass
105. 1 point. Pass
106. 1 point. Pass
107. 1 point. Main.ExtInt.NumVal(12)
108. 1 point. Main.ExtInt.NumVal(12)
109. 1 point. Main.ExtInt.NumVal(14)
110. 1 point. Main.ExtInt.NumVal(4.0)
111. 1 point. Error
112. 1 point. Error
113. 1 point. Error
114. 1 point. Error
115. 1 point. Error
116. 1 point. Error
117. 1 point. Error
118. 1 point. Error
119. 1 point. Error
120. 1 point. Main.ExtInt.ClosureVal(Symbol[], Main.ExtInt.NumNode(53), Main.ExtInt.EmptyEnv())
121. 1 point. Main.ExtInt.NumVal(12)
"""
    correctoutput = """1. Pass
2. Error
3. Error
4. Main.ExtInt.NumVal(3)
5. Main.ExtInt.NumVal(1)
6. Pass
7. Pass
8. Error
9. Error
10. Main.ExtInt.NumVal(4)
11. Main.ExtInt.NumVal(5)
12. Main.ExtInt.NumVal(-9223372036854775808)
13. Main.ExtInt.NumVal(0)
14. Error
15. Error
16. Error
17. Error
18. Error
19. Error
20. Error
21. Error
22. Error
23. Error
24. Error
25. Main.ExtInt.NumVal(1)
26. Main.ExtInt.NumVal(-9223372036854775808)
27. Main.ExtInt.NumVal(0)
28. Error
29. Error
30. Error
31. Error
32. Error
33. Error
34. Error
35. Error
36. Error
37. Error
38. Main.ExtInt.NumVal(-2)
39. Main.ExtInt.NumVal(2)
40. Main.ExtInt.NumVal(-9223372036854775807)
41. Main.ExtInt.NumVal(-9223372036854775808)
42. Main.ExtInt.NumVal(0)
43. Error
44. Error
45. Main.ExtInt.NumVal(6)
46. Main.ExtInt.NumVal(-87)
47. Main.ExtInt.NumVal(0)
48. Main.ExtInt.NumVal(-12.0)
49. Main.ExtInt.NumVal(4.5)
50. Main.ExtInt.NumVal(-0.1)
51. Error
52. Error
53. Error
54. Error
55. Error
56. Main.ExtInt.NumVal(1)
57. Error
58. Error
59. Error
60. Error
61. Main.ExtInt.NumVal(0)
62. Main.ExtInt.NumVal(25)
63. Error
64. Error
65. Main.ExtInt.FuncAppNode(Main.ExtInt.VarRefNode(:q), Main.ExtInt.AE[])
66. Main.ExtInt.FuncAppNode(Main.ExtInt.VarRefNode(:qwerty23546uuioiop), Main.ExtInt.AE[])
67. Error
68. Error
69. Error
70. Error
71. Error
72. Error
73. Error
74. Error
75. Main.ExtInt.NumVal(1)
76. Main.ExtInt.NumVal(100)
77. Error
78. Main.ExtInt.NumVal(1)
79. Main.ExtInt.ClosureVal(Symbol[:x, :y], Main.ExtInt.NumNode(1), Main.ExtInt.EmptyEnv())
80. Main.ExtInt.NumVal(6)
81. Main.ExtInt.NumVal(1)
82. Error
83. Error
84. Error
85. Error
86. Error
87. Main.ExtInt.ClosureVal(Symbol[], Main.ExtInt.NumNode(4), Main.ExtInt.EmptyEnv())
88. Main.ExtInt.ClosureVal(Symbol[:x], Main.ExtInt.VarRefNode(:x), Main.ExtInt.EmptyEnv())
89. Main.ExtInt.ClosureVal(Symbol[:x], Main.ExtInt.NumNode(34), Main.ExtInt.EmptyEnv())
90. Main.ExtInt.ClosureVal(Symbol[:x, :y], Main.ExtInt.BinopNode(+, Main.ExtInt.VarRefNode(:x), Main.ExtInt.VarRefNode(:y)), Main.ExtInt.EmptyEnv())
91. Pass
92. Error
93. Error
94. Error
95. Error
96. Pass
97. Error
98. Error
99. Error
100. Error
101. Error
102. Error
103. Pass
104. Pass
105. Pass
106. Pass
107. Main.ExtInt.NumVal(12)
108. Main.ExtInt.NumVal(12)
109. Main.ExtInt.NumVal(14)
110. Main.ExtInt.NumVal(4.0)
111. Error
112. Error
113. Error
114. Error
115. Error
116. Error
117. Error
118. Error
119. Error
120. Main.ExtInt.ClosureVal(Symbol[], Main.ExtInt.NumNode(53), Main.ExtInt.EmptyEnv())
121. Main.ExtInt.NumVal(12)
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
