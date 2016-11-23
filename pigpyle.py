#
# Created by Jack Merullo on 11/19/16
#

import sys, getopt

def getSuffix(word, suffix):
	if word.isupper() and len(word)>1:
		return suffix.upper()
	return suffix

def getCapitals(temp):
	frontLen = len(getFront(temp))
	if len(temp)>1 and temp[0].isupper() and not temp[-1].isupper() and frontLen<len(temp):	
		word = temp[:frontLen].lower()+temp[frontLen].upper()
		if frontLen+1 < len(temp):
			word += temp[frontLen+1:]
		return word
	return temp

def getFront(word):
	i = 0
	front = ""
	while i<=(len(word)-1) and not isVowel(word[i]):
		front+=word[i]
		i+=1
	return front

def isVowel(curChar):
	if curChar.lower() in ('a', 'e', 'i', 'o', 'u', 'y'):
		return True
	return False

def convertWord(temp):
	if temp.isdigit():
		return temp
	word = getCapitals(temp)
	if len(word)>1 and not isVowel(word[0]):
			front = getFront(word)
			return word[len(front):]+front+getSuffix(word,"ay")
	elif word.isalnum():
		return word+getSuffix(word,"way")
	return word

def findStart(word):
	start = 0
	for i, c in enumerate(word):
		if c.isalnum():
			return i
		start = i
	return start

def findEnd(start, word):
	for i in range(start, len(word)):
		if not word[i].isalnum():
			return i
		end = i
	return len(word)

def processLine(line):
	words = line.split()
	newLine = ''
	for w in words:
		start = findStart(w)
		end = findEnd(start, w)
		newLine+=w[:start]+convertWord(w[start:end])+w[end:]+" "
	return newLine


def convertFile(file):
	line = file.readline()
	pigFile = open("{name}Pig.txt".format(name = file.name.split('.')[0]), 'w')
	while line:
		pigFile.write(processLine(line)+'\n')
		line = file.readline()
	pigFile.close()
	file.close()


def main(argv):
	fileName = ''
	try:
		opts, args = getopt.getopt(argv, "hf:", ["file="])
	except getopt.GetoptError:
		print("Error:\npigpyle.py -f path/to/file")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("HELP: pigpyle.py -f path/to/file\nthe new file will be saved in this directory\naccepts .txt files")
			sys.exit()
		elif opt in ('-f', '--file'):
			fileName = arg
			break
	if fileName:
		file = open(fileName, 'r')
		convertFile(file)

if __name__ == "__main__":
	main(sys.argv[1:])