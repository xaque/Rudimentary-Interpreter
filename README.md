# Rudimentary Interpreter

The grammer for the language is as follows:
```
<AE>    ::=  number
         |   (+ <AE> <AE>)
         |   (- <AE> <AE>)
         |   (* <AE> <AE>)
         |   (/ <AE> <AE>)
         |   (mod <AE> <AE>)
         |   (collatz <AE>)
         |   (- <AE>)
         |   <id>
         |   (if0 <AE> <AE> <AE>)
         |   with <id> <AE> <AE>)
         |   (lambda <id> <AE>)
         |   (<AE> <AE>)

# Only symbols not already in grammar
<id>    ::=  symbol
```