# Rudimentary Interpreter

The grammer for the language is as follows:
```
<AE>	::=	 	number
 	 	|	 	(+ <AE> <AE>)
 	 	|	 	(- <AE> <AE>)
 	 	|	 	(* <AE> <AE>)
 	 	|	 	(/ <AE> <AE>)
        |       (mod <AE> <AE>)
        |       (collatz <AE>)
        |       (- <AE>)
```