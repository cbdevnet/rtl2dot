# rtl2dot
Convert gcc RTL dumps to call graphs via GraphViz.

Based on [egypt](http://www.gson.org/egypt/egypt.html), rewritten in python with added support for configurable root nodes and omission by regex.
May or may not work with C++ code.

## Usage
Compile your code with `-fdump-rtl-expand` (eg. by running `make CFLAGS=-fdump-rtl-expand`).
This will generate some new files, most commonly with the extension `.expand`.

Run `rtl2dot myproject.beepbop.expand | dot -Tsvg > myproject.svg` to get a graph of the `main` function of your project.

Valid options are:
* `--ignore <regex>`	Regular expression describing function names to be ignored
* `--root <function>`	Select the function to use as root node of the graph
* `--local`		Ignore functions that are not defined within the rtl dump (most likely library functions) 

Any other arguments are treated as input files. If no input files are given, input is expected on stdin.

## License
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar and 
reproduced below.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
Version 2, December 2004 

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

	Everyone is permitted to copy and distribute verbatim or modified 
	copies of this license document, and changing it is allowed as long 
	as the name is changed. 

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

	0. You just DO WHAT THE FUCK YOU WANT TO.
