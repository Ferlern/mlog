# mlog — Neat and optimized logic for Mindustry

- If you want to take some logic go to [/compiled](https://github.com/Ferlern/mlog/tree/main/compiled) and take what u need
- If you want to make/change logic go to [/raw](https://github.com/Ferlern/mlog/tree/main/raw) and learn how my compiler works

# Purpose of the repository
Collect convenient templates and ready-made solutions for most situations in the game.
All logic here must be clear, neat and optimized. Made in one easy to read style

# About compiler
I want to keep logic as logic, so it only implements additional features without turning the code into an unreadable clutter

- All files from `/raw` with ext .mlog will be compiled in `/compiled`
- logic stored in [/for_compiler](https://github.com/Ferlern/mlog/tree/main/raw/for_compiler) is only needed for the compiler

All you have to do is make changes to `/raw` and run `compiler.py`

# Imports
Compiler will replace all lines of the form  
```
import <file> (<var1> = <value1>, 
               <var2> = <value2>, 
               ...)
```
with the contents of <file>, replacing all <var> with its value