R2Py2
---
R2Py2 helps you convert you css between directions. Converting RTL layouts to LTR and vise versa.
An example input output will look something like this:

** Before **

``` css
#someId {
  float: left;
  margin-right: 2px;
  padding: 1px 2px 3px 4px;
  left: 5px;
}
.someClass {
  text-align: right;
}
```

** After **

``` css
#someId {
  float: right;
  margin-left: 2px;
  padding: 1px 4px 3px 2px;
  right: 5px;
}
.someClass {
  text-align: left;
}
```

Using it
----------
Just download and unpack; then run (make sure the file has executing permissions by chmod-ing it):

	./r2py2.py input.css -o output.css

You can also omit the -o option and output will be sent to stdout (from there you can redirect it as you wish). For example you could do:
	
    $ ./r2py2.py input1.css -o giant-output.css
    $ ./r2py2.py input2.css > giant-output.css
	
or
	
    $ ./r2py2.py input.css | less
	

Dependencies
-------------
R2Py2 uses the [cssutils library](https://bitbucket.org/cthedot/cssutils "cssutils lib") for parsing the input file


Future features
----------------
- Support for multiple input files
- Support minified output by option flag
- Support URL inputs
- Support inline styles embedded in HTML
- Add unit test to verify I don't break stuff

Please feel free to submit other feature requests if you have any... plus it should be very easy for anyone to add new tag swapping into the mechanism


Caution
--------
R2Py2 will only work as good as what you give it, therefore *inline-styles* embedded in your HTML will not converted, and therefore may cause unexpected results. However inline-styles apart from R2Py2 is still a bad idea, and you should avoid it anyway in favor of separating content from presentation.


Original Idea
--------------
The idea behind this project is really by @ded [R2 project](http://karavan/css/bootstrap.css "R2")). I wanted to use his library for something personal but since I don't deal with Node at all I had to come up with my out python version of this tool.
Think of this as a python port of R2 (which is also why I called it R2Py2 ... because it sounds like R2D2.. yeah, nerdy.)
