#!/usr/bin/python

##Here's the first wack at the redcode compiler.  this will be dirty
#samurai@psych0tik.net
#2012-08-06 

import sys

filename =  sys.argv[1]
fh = open(filename, "r")

outfilename = filename.split(".")
outfilename = outfilename[0]+".red"
outfile = open(outfilename, "w")

codes = []


def validateCode(codes):
	error = 0
	bracket_open = bracket_close = 0
	starter = 0
	for code in codes:
		if "{" in code:
			bracket_open += 1
		if "}" in code:
			bracket_close += 1
		if "start()" in code:
			starter = 1
		
	if bracket_open != bracket_close:
		print "[Fatal] Un-matched brackets"
		error = 1
	if starter != 1:
		print "[Fatal] Please provide a start() function"
		error = 1
	return error

def buildFunction(code, funcname):
	funccheck = "func %s()" % (funcname)
	print funccheck
	foundfunc = bracketstatus = 0
	funccode = []
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
	if len(funccode) == 0:
		writeCode("%s: dat #0, #0" %  (funcname))
	else:
		redcode = convertCode(funccode)
		print redcode
		redcode[0] = "%s: %s" % ( funcname, redcode[0] )
		writeCode(redcode[0])
		del(redcode[0])
		for rline in redcode:
			writeCode("\t%s" % ( rline ))	

def convertCode(code):
	return code

def writeCode(redcode):
	global outfile
	outfile.write(redcode + "\n")


for line in fh:
	line = line.replace("\n","").strip()
	tmp = line.split(";")
	line = tmp[0]
	if line != "":
		print line
		codes.append(line)

if validateCode(codes) != 0:
	print "This code won't compile, please fix your errors"
	print codes

else:
	print "Building redcode"
	for line in codes:
		if "func " in line:
			funcname = line.split("func ")
			funcname = funcname[1].split("()")
			funcname = funcname[0]
			print "Found function %s" % ( funcname )
			buildFunction(codes, funcname)

fh.close()