# TODO finish modularizing Test case runner. Currently expected values are still hard coded in this file. Should be able to load test cases from txt file.

import sys
import subprocess
import os
from difflib import Differ
if __name__ == "__main__":
    fn = sys.argv[1]
    tmp_fn = "tmp.jl"
    feedback_fn = "feedback.txt"
    run_cmd = "julia"
    tests = "RudInt2Tests.jl"
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
11. 1 point. Main.RudInt.NumVal(5)
12. 1 point. Main.RudInt.NumVal(-9223372036854775808)
13. 1 point. Main.RudInt.NumVal(0)
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
25. 1 point. Main.RudInt.NumVal(2)
26. 1 point. Main.RudInt.NumVal(-9223372036854775808)
27. 1 point. Main.RudInt.NumVal(0)
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
38. 1 point. Main.RudInt.NumVal(-1)
39. 1 point. Main.RudInt.NumVal(2)
40. 1 point. Main.RudInt.NumVal(0)
41. 1 point. Main.RudInt.NumVal(-9223372036854775807)
42. 1 point. Main.RudInt.NumVal(-9223372036854775808)
43. 1 point. Error
44. 1 point. Error
45. 1 point. Main.RudInt.NumVal(6)
46. 1 point. Main.RudInt.NumVal(-87)
47. 1 point. Main.RudInt.NumVal(0)
48. 1 point. Main.RudInt.NumVal(-12.0)
49. 1 point. Main.RudInt.NumVal(4.5)
50. 1 point. Main.RudInt.NumVal(-0.1)
51. 1 point. Error
52. 1 point. Error
53. 1 point. Error
54. 1 point. Error
55. 1 point. Error
56. 1 point. Main.RudInt.NumVal(1)
57. 1 point. Error
58. 1 point. Error
59. 1 point. Error
60. 1 point. Error
61. 1 point. Main.RudInt.NumVal(0)
62. 1 point. Main.RudInt.NumVal(25)
63. 1 point. Error
64. 1 point. Error
65. 1 point. Main.RudInt.FuncAppNode(Main.RudInt.VarRefNode(:q), Main.RudInt.AE[])
66. 1 point. Main.RudInt.FuncAppNode(Main.RudInt.VarRefNode(:qwerty23546uuioiop), Main.RudInt.AE[])
67. 1 point. Error
68. 1 point. Error
69. 1 point. Error
70. 1 point. Error
71. 1 point. Error
72. 1 point. Error
73. 1 point. Error
74. 1 point. Error
75. 1 point. Main.RudInt.NumVal(1)
76. 1 point. Main.RudInt.NumVal(100)
77. 1 point. Error
78. 1 point. Main.RudInt.NumVal(1)
79. 1 point. Main.RudInt.ClosureVal(Symbol[:x, :y], Main.RudInt.NumNode(1), Main.RudInt.EmptyEnv())
80. 1 point. Main.RudInt.NumVal(6)
81. 1 point. Main.RudInt.NumVal(1)
82. 1 point. Error
83. 1 point. Error
84. 1 point. Error
85. 1 point. Error
86. 1 point. Error
87. 1 point. Main.RudInt.ClosureVal(Symbol[], Main.RudInt.NumNode(4), Main.RudInt.EmptyEnv())
88. 1 point. Main.RudInt.ClosureVal(Symbol[:x], Main.RudInt.VarRefNode(:x), Main.RudInt.EmptyEnv())
89. 1 point. Main.RudInt.ClosureVal(Symbol[:x], Main.RudInt.NumNode(34), Main.RudInt.EmptyEnv())
90. 1 point. Main.RudInt.ClosureVal(Symbol[:x, :y], Main.RudInt.BinopNode(+, Main.RudInt.VarRefNode(:x), Main.RudInt.VarRefNode(:y)), Main.RudInt.EmptyEnv())
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
107. 1 point. Main.RudInt.NumVal(12)
108. 1 point. Main.RudInt.NumVal(12)
109. 1 point. Main.RudInt.NumVal(14)
110. 1 point. Main.RudInt.NumVal(4.0)
111. 1 point. Error
112. 1 point. Error
113. 1 point. Error
114. 1 point. Error
115. 1 point. Error
116. 1 point. Error
117. 1 point. Error
118. 1 point. Error
119. 1 point. Error
120. 1 point. Main.RudInt.ClosureVal(Symbol[], Main.RudInt.NumNode(53), Main.RudInt.EmptyEnv())
121. 1 point. Main.RudInt.NumVal(12)
"""
    correctoutput = """1. Pass
2. Error
3. Error
4. Main.RudInt.NumVal(3)
5. Main.RudInt.NumVal(1)
6. Pass
7. Pass
8. Error
9. Error
10. Main.RudInt.NumVal(4)
11. Main.RudInt.NumVal(5)
12. Main.RudInt.NumVal(-9223372036854775808)
13. Main.RudInt.NumVal(0)
14. Error
15. Error
16. Error
17. Error
18. Main.RudInt.NumVal(6)
19. Main.RudInt.NumVal(66)
20. Error
21. Error
22. Error
23. Error
24. Error
25. Main.RudInt.NumVal(1)
26. Main.RudInt.NumVal(-9223372036854775808)
27. Main.RudInt.NumVal(0)
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
38. Main.RudInt.NumVal(-2)
39. Main.RudInt.NumVal(2)
40. Main.RudInt.NumVal(-9223372036854775807)
41. Main.RudInt.NumVal(-9223372036854775808)
42. Main.RudInt.NumVal(0)
43. Error
44. Error
45. Main.RudInt.NumVal(6)
46. Main.RudInt.NumVal(-87)
47. Main.RudInt.NumVal(0)
48. Main.RudInt.NumVal(-12.0)
49. Main.RudInt.NumVal(4.5)
50. Main.RudInt.NumVal(-0.1)
51. Error
52. Error
53. Error
54. Error
55. Error
56. Main.RudInt.NumVal(1)
57. Error
58. Error
59. Error
60. Error
61. Main.RudInt.NumVal(0)
62. Main.RudInt.NumVal(25)
63. Error
64. Error
65. Main.RudInt.FuncAppNode(Main.RudInt.VarRefNode(:q), Main.RudInt.AE[])
66. Main.RudInt.FuncAppNode(Main.RudInt.VarRefNode(:qwerty23546uuioiop), Main.RudInt.AE[])
67. Error
68. Error
69. Error
70. Error
71. Error
72. Error
73. Error
74. Error
75. Main.RudInt.NumVal(1)
76. Main.RudInt.NumVal(100)
77. Error
78. Main.RudInt.NumVal(1)
79. Main.RudInt.ClosureVal(Symbol[:x, :y], Main.RudInt.NumNode(1), Main.RudInt.EmptyEnv())
80. Main.RudInt.NumVal(6)
81. Main.RudInt.NumVal(1)
82. Error
83. Error
84. Error
85. Error
86. Error
87. Main.RudInt.ClosureVal(Symbol[], Main.RudInt.NumNode(4), Main.RudInt.EmptyEnv())
88. Main.RudInt.ClosureVal(Symbol[:x], Main.RudInt.VarRefNode(:x), Main.RudInt.EmptyEnv())
89. Main.RudInt.ClosureVal(Symbol[:x], Main.RudInt.NumNode(34), Main.RudInt.EmptyEnv())
90. Main.RudInt.ClosureVal(Symbol[:x, :y], Main.RudInt.BinopNode(+, Main.RudInt.VarRefNode(:x), Main.RudInt.VarRefNode(:y)), Main.RudInt.EmptyEnv())
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
107. Main.RudInt.NumVal(12)
108. Main.RudInt.NumVal(12)
109. Main.RudInt.NumVal(14)
110. Main.RudInt.NumVal(4.0)
111. Error
112. Error
113. Error
114. Error
115. Error
116. Error
117. Error
118. Error
119. Error
120. Main.RudInt.ClosureVal(Symbol[], Main.RudInt.NumNode(53), Main.RudInt.EmptyEnv())
121. Main.RudInt.NumVal(12)
"""
    grade = 0
    total_possible = 0
    rudint_dir = "/".join(fn.split("/")[:-1])
    with open(fn, "r") as f:
        with open(tmp_fn, "w") as w:
            w.write("push!(LOAD_PATH, \"" + rudint_dir + "\")")
            w.write(f.read())
            with open(tests, "r") as t:
              w.write(t.read())
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
