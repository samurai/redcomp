#!/usr/bin/python

##Here's the first wack at the redcode compiler.  this will be dirty
#samurai@psych0tik.net
#2012-08-06 


##this is mostly set ups tuff
import sys

filename =  sys.argv[1]
fh = open(filename, "r")

outfilename = filename.split(".")
outfilename = outfilename[0]+".red"
outfile = open(outfilename, "w")

codes = []

##functions - these will probably be moved to a lib later

##checks to see if the structure of the code looks proper-ish?
def validateCode(codes):
	error = 0
	bracket_open = bracket_close = 0
	starter = 0
	for code in codes:
		##make sure brackets exist all over
		if "{" in code:
			bracket_open += 1
		if "}" in code:
			bracket_close += 1
		##main function, called start() - perhaps should change this to main() to confuse less people?
		if "start()" in code:
			starter = 1
		
	##less than useful errors 
	if bracket_open != bracket_close:
		print "[Fatal] Un-matched brackets"
		error = 1
	if starter != 1:
		print "[Fatal] Please provide a start() function"
		error = 1
	return error

##NOTE: thinking about it, functions and variables will be set-up almost the same way within the redcode
## the only real difference being single vs multi-line.  This may mean that we can use functions/vars interchangably at the higher 
## level?

##this takes the code and a function name and will find/build it in redcode
def buildFunction(code, funcname):
	funccheck = "func %s()" % (funcname) ##need a way to find our start
	print funccheck
	foundfunc = bracketstatus = 0
	funccode = []
	##look through for the func name, when finding brackets use the code in between.
	##the order of the brackets with the other checks is important for getting the right lines
	for line in code:
		if funccheck in line:
			foundfunc = 1
		if "}" in line:
			bracketstatus = 0
		print bracketstatus
		print foundfunc
		if foundfunc and bracketstatus:
			funccode.append(line)
		if "{" in line:
			bracketstatus = 1

	print funccode	
	##empty function 	
	if len(funccode) == 0:
		writeCode("%s: dat #0, #0" %  (funcname))
	## convert code from rcc to redcode (this probably will be hard?)
	##then drop it into the file, built as a "function"
	else:
		redcode = convertCode(funccode)
		print redcode
		redcode[0] = "%s: %s" % ( funcname, redcode[0] )
		writeCode(redcode[0])
		del(redcode[0])
		for rline in redcode:
			writeCode("\t%s" % ( rline ))	

##magic happens here
def convertCode(code):
	return code

##remove global?
def writeCode(redcode):
	global outfile
	outfile.write(redcode + "\n")


##get the code we need to compile, skipping comments
for line in fh:
	line = line.replace("\n","").strip()
	tmp = line.split(";")
	line = tmp[0]
	if line != "":
		print line
		codes.append(line)

##check code for syntax errors
if validateCode(codes) != 0:
	print "This code won't compile, please fix your errors"
	print codes

else:
	##build it
	print "Building redcode"
	for line in codes:
		if "func " in line:
			funcname = line.split("func ")
			funcname = funcname[1].split("()")
			funcname = funcname[0]
			print "Found function %s" % ( funcname )
			buildFunction(codes, funcname)

##done stuff
fh.close()
print "Code written successfully, give it a run to see if this works!"