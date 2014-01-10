#!\usr\bin\env python
#get RJxxx folder name from DLSITE.com
#input para path for rename
import sys
import os
import re
import urllib.request

MAX_RETRY = 1

def doFilter(str):
	str = str.replace('!?','！？')
	str = str.replace('?','？')
	str = str.replace('&amp;','&')
	str = str.replace('&nbsp;',' ')
	str = str.replace('&lt;','<')
	str = str.replace('&gt;','>')
	return str
 
def toUnicode(s,charset):  
	if( charset == "" ):  
		return s  
	else:  
		try:  
			u = s.decode(charset)  
		except:  
			u = ""  
	return u  
 
def getCharset(self,s):  
	rst = getFromPatten(u'charset=(.*?)"',s,True)  
	if rst != "":  
		if rst == "utf8":  
			rst = "utf-8"  
	return rst  

def getFromPatten(patten,src,single=False):  
	rst = "";  
	#p = re.compile(patten,re.S)  
	p = re.compile(patten)  
	all = p.findall(src)  
	for matcher in all:  
		rst += matcher + " "  
		if( single ):  
			break  
	return rst.strip() 	

def GetRJNumFileName(rjNum):
	url = 'http://www.dlsite.com/maniax/work/=/product_id/' + rjNum + '.html'
	result = rjNum
	charset = "utf-8" 
	page = ""
	retry = 0  

	while True:  
		try:  
			fp = urllib.request.urlopen(url)  
			break  
		except urllib.request.HTTPError as e:  
			print('HTTPError'+str(e.code))
			retry+=1  
			if( retry > MAX_RETRY ):  
				return result
		except urllib.request.URLError as e: 
			retry+=1  
			if( retry > MAX_RETRY ):  
				print('HTTPTimeout')
				return result

	while True:  
		line = fp.readline()  
		if charset == "":  
			charset = getCharset(line)  
		if not line:  
			break  
		page += toUnicode(line,charset)  

	fp.close()

	title = getFromPatten('(?<=<title>)[\w\W]*(?=</title>)',page,True).split('|')[0].strip()

	if title != '':
		rjList = title.split('[')
		rjTitle = doFilter(rjList[0].strip())
		rjGroupName = '' 
		if len(rjList) > 1:
			rjGroupName = doFilter('[' + title.split('[')[1].strip())
		result = rjGroupName + rjTitle + ' ' + rjNum

	return result

def main():
	dirname, pyfilename = os.path.split(os.path.abspath(sys.argv[0]))
	folderStr = dirname
	p = re.compile('RJ\d+',re.IGNORECASE)
	print(folderStr)

	if len(sys.argv) == 2:
		folderStr = sys.argv[1]

	files = os.listdir(folderStr)
	for name in files:
		fullname = os.path.join(folderStr,name)
		if os.path.isdir(fullname):
			templist = p.findall(name)
			if len(templist) > 0:
				m = templist[0]
				rj = m.upper()
				print(rj) 
				newFileName = GetRJNumFileName(rj)
				if  rj != newFileName:
					newFileFullName = os.path.join(folderStr,newFileName)
					if  not os.path.exists(newFileFullName):
						os.rename(fullname, newFileFullName)
						print(fullname + ' => ' + newFileFullName) 


if __name__ == '__main__':
	main()
