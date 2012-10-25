#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import Image
import re

#Get filename as argument, instruction if no argument
if len(sys.argv)<2:
	print "This script needs arguments..."
	print ":>python fiximgsize.py <htmlfile.html>"
	print "It will read PNG filenames from the HTML"
	print "Replace by correct size and save everything"
	print "in a new HMTL file."
	sys.exit()
filename = sys.argv[1] 

# RegEx expressions to get what we need in HTML
# reg1 = <img [...] >
reg1 = re.compile('<img[^>]*>')
# reg2 = path+filename in src
reg2 = re.compile('src="([^"]*)"')
# reg3 = height
reg3 = re.compile('height="([^"]*)"')
# reg4 = width
reg4 = re.compile('width="([^"]*)"')

# open HTML and split in lines
input = open(filename, 'r').read().split('\n')
lastline = len(input) - 1

# search on each lines for the regex
for lines in range(len(input)):
	matchObj1 = re.search(reg1, input[lines])
	if matchObj1!=None:
		matchObj2 = re.search(reg2, matchObj1.group())
		matchObj3 = re.search(reg3, matchObj1.group())
		matchObj4 = re.search(reg4, matchObj1.group())

		#test if height is there... 
		if matchObj3!=None: 
			filenamePNG = matchObj2.group(1)
			#get height in HMTL
			heightHTML = int(matchObj3.group(1))
			#get width in HTML
			widthHTML = int(matchObj4.group(1))

			#read image to get size in pixels
			im = Image.open(matchObj2.group(1))
			heightPNG = int(im.size[1])
			widthPNG = int(im.size[0])
			
			#get the PNG ratio for later... 
			ratioImage = float(widthPNG)/float(heightPNG)

			#if width of PNG is smaller or equal than in HTML 	
			if widthPNG <= widthHTML:
				#insert width and height in HTML
				input[lines] = re.sub(matchObj3.group(1),str(heightPNG),input[lines])
				input[lines] = re.sub(matchObj4.group(1),str(widthPNG),input[lines])			
			else:
				#if width of PNG is larger than in HTML
				#keep HTML width as it is
				newWidth = widthHTML
				#compute new height based on HTML width and ratio
				newHeight = int(float(newWidth)/ratioImage)
				#insert in HTML code
				input[lines] = re.sub(matchObj3.group(1),str(newHeight),input[lines])			

#All done, write everything in new file
tempFilename = filename.replace('.html','_DONE.html')
output = open(tempFilename, 'w')
output.write('\n'.join(input))
output.close()
print "Done!"
print "Good bye..."

