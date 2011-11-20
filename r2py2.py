#!/usr/bin/env python

"""
R2Py2 - a cross direction CSS LTR <-> RTL converter written in python (for those without Node.js)
Idea by: Dustin Diaz 2011
Python version: kensaggy
https://github.com/kensaggy/r2py2
"""

import sys, os, re, optparse, cssutils

#Supress errors from cssutils
cssutils.log.enabled = False

class r2py2():
    

    propertyMap = {
      'margin-left': 'margin-right',
      'margin-right': 'margin-left',

      'padding-left': 'padding-right',
      'padding-right': 'padding-left',

      'border-left': 'border-right',
      'border-right': 'border-left',

      'border-left-width': 'border-right-width',
      'border-right-width': 'border-left-width',

      'border-radius-bottomleft': 'border-radius-bottomright',
      'border-radius-bottomright': 'border-radius-bottomleft',
      '-moz-border-radius-bottomright': '-moz-border-radius-bottomleft',
      '-moz-border-radius-bottomleft': '-moz-border-radius-bottomright',

      'left': 'right',
      'right': 'left'
    }
    
    def direction(v):
        return 'ltr' if v == 'rtl' else 'rtl';

    def rtltr(v):
        return 'left' if v == 'right' else 'right'
        
    def fix_quad_mapping(v):
        # 1px 2px 3px 4px => 1px 4px 3px 2px
        m = re.split(r'\s+', v.strip()) 
        if (len(m) == 4):
            return ' '.join([m[0], m[3], m[2], m[1]])

        return v
        
    valueMap = {
      'padding': fix_quad_mapping,
      'margin': fix_quad_mapping,
      '-webkit-border-radius': fix_quad_mapping,
      '-moz-border-radius': fix_quad_mapping,
      'border-radius': fix_quad_mapping,
      'text-align': rtltr,
      'float': rtltr,
      'clear': rtltr,
      'direction': direction
    }

        
    def process(self, css):
        
        sheet = cssutils.parseString(css)

        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    if property.name in r2py2.valueMap: #does the property map need to be fixed using a helper method
                        fixed_value = r2py2.valueMap[property.name](property.value)
                        property.value = fixed_value
                    elif property.name in r2py2.propertyMap: #or possible only a different direction
                        property.name = r2py2.propertyMap[property.name]
                
        
        return sheet.cssText;
        
        
 
def main():
    usage_string = r"""
%prog input.css                 - Will output to stdout.
%prog input.css -o output.css   - Will output into the specified file
"""
    
    op = optparse.OptionParser(usage=usage_string, version="%prog")
    op.add_option("-o","--output", action="store", dest="output_file", \
                                    default=False, help="Output to file")
                                    
    (options, args) = op.parse_args()
    
    if len(args) > 1:
        op.error('You must only supply one input file')
        
    """
        if no output file is specified, output will be written to stdout - from there you could also pipe it elsewhere, e.g.:
        ./r2py2.py input.css > output.css should work the same
        ./r2py2.py input.css | less
    """
    if (options.output_file is False): 
        output_stream = sys.stdout
    else:
        try:
            if not os.access(options.output_file, os.R_OK): #make sure output file doesn't exists
                output_stream = open(options.output_file, 'w+')
            else:
                op.error('Output file already exists.\nTo avoid you bumming out, I will not override the output and will stop right here... You\'ll thank me later.')
        except IOError:
            op.error('Could not open output file for writing. Please make sure you have writting privileges')
    
    try:
        input_css = open(args[0], 'r') #open input file
        r2 = r2py2() #create out r2py2 object
        result = r2.process(input_css.read()) #pass the css text into the process method
        output_stream.write( result ) #and how comes the the yummy other-direction css
        input_css.close() #be a good fella
    except IOError:
        op.error('Could not open input file for reading. Please make sure it exists')
            
if __name__ == "__main__":
    main()