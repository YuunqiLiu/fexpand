# fexpand
A Filelist preprocessor for verilog/system verilog filelist.

A pure Python based Filelist preprocessor implementation 
very useful for pre-preprocessing hierarchical fielist into single 
filelist without "-f" index, macros, environment variables and comments.

Note that fexpand expands all environment variables that are present 
(those that are not present are left in place). 
Similarly, all paths are converted to absolute paths 
(non-existing files are left as they are). Fexpand supports most of the c99 macro syntax.


This project is based on the pcpp project modified to expand the verilog/system verilog filelist. The following modifications have been made to pcpp.
1. equate the "-f" keyword with "#include".
2. when include a path, it will replace the environment variable and expand it to absolute path and then include the content.
3. check the duplicity of include, in include the same path for the second time will be ignored.
4. will be in the text of the path are environment variable replacement, and converted to an absolute path.
5. In the text content of the path to repeatability check, in the second encounter the same path will be ignored.
