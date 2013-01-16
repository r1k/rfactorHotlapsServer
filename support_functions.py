#!/usr/bin/env python

def pairs(l):

	#return zip(*(iter(l),)*2)
	return [ l[i:i+2] for i in range(0,len(l),2)]