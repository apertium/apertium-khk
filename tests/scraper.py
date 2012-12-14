#!/usr/bin/env python3
#GCI 2012 - Apertium - rptynan

import urllib.request
from lxml.html import fromstring
from lxml.html import tostring
import re

matchWord = re.compile(r"([\w\s]*?) [\[\/]")

page = urllib.request.urlopen("http://wiki.firespeaker.org/Khalkha_noun_classes")
#page = urllib.request.urlopen("file:///home/ash/Code/GCI/mongolian_noun_scraper/Khalkha_noun_classes")
pagestr = (page.read()).decode("utf8")
page.close()

def writeNoun(noun, filen):
	#Special case for bolded letters
	if(noun[1].find(".//b")!=None):
		noun[1] = fromstring(re.sub("<.*?>",'',str(tostring(noun[1]),"utf-8"))).text
	else:
		noun[1]=noun[1].text
	#print(noun[1])
	
	if(noun[1].strip()!="[]" and noun[1].strip()!="" and noun[1].strip()!="—"):
		if(noun[0].lower().strip()=="pl"):
			filen.write("    "+name.strip()+"<n><pl><nom> : "+firsttrans(noun[1]).strip()+'\n')
		else:
			filen.write("    "+name.strip()+"<n><"+noun[0].lower().strip()+"> : "+firsttrans(noun[1]).strip()+'\n')
	
def skipCheck(check):
	#Special case for ones to be checked
	try:
		if(check.attrib["class"]=="check"):
			[parsenext("th").text, parsenext("td")]
			return True
	except KeyError:
		return False


def parsenext(tofind):
	global pagestr
	res = fromstring(pagestr).find(".//"+tofind)
	pagestr = re.sub(tofind,'',pagestr,2)
	return res

def firsttrans(inp):
	#gr=re.search(r"(\w+)",inp)
	global matchWord
	gr=matchWord.search(inp)
	return gr.group(1)

def tosorttime():
	global pagestr
	with open("./to sort",'w') as filen:
		filen.write("Config:\n  hfst:\n      App: hfst-optimised-lookup\n      Gen: ../khk.autogen.hfst\n      Morph: ../khk.automorf.hfst")
		filen.write("\n\nTests:\n")
		#Nominitive of noun (name) and the translation
		while(True):
			nxttable=pagestr.find('<table class="wikitable"')
			if(nxttable==-1):
				return
			pagestr=pagestr[nxttable:]
			noun=(parsenext("th").text,parsenext('i').text)
			parsenext("td")
			name = fromstring(pagestr).find(".//td")
			name = firsttrans(fromstring(re.sub("<.*?>",'',str(tostring(name),"utf-8"))).text)
			filen.write('\n "'+name.strip()+' = '+noun[1].strip()+'":\n')
			#Different cases of the noun
			while(True):
				check=fromstring(pagestr).find(".//td")
				#When we hit the next table
				if(check==None or check.find(".//i")!=None):
					break
				if skipCheck(check): continue
				else: pass
				noun = [parsenext("th").text, parsenext("td")]
				writeNoun(noun, filen)




title = fromstring(pagestr).find(".//h1").text
print(title)

para=parsenext("h2") #Get rid of contents header


#Filename
while(True):
	para=parsenext("h2")
	if(para==None):
		break
	para = para.find(".//span").text.strip()
	
	
#Second half of filename
	while(True):
		if(pagestr.find("h2")<pagestr.find("h3")):
			break
		subpara=parsenext("h3")
		if(subpara==None):
			break
		subpara = subpara.find(".//span").text.strip()

		filename = re.sub(r'(?<!\\)/',r'' '',para.lower()+" - "+subpara.lower()+".yaml")
		with open("./"+filename,'w') as filen:

			filen.write("Config:\n  hfst:\n      App: hfst-optimised-lookup\n      Gen: ../khk.autogen.hfst\n      Morph: ../khk.automorf.hfst")
			filen.write("\n\nTests:\n")


			#If Variable
			if(para.lower().find("variable")!=-1):
				#Nominitive of noun (name) and the translation
				while(True):
					nxttable=pagestr.find('<table class="wikitable"')
					nxth=pagestr.find("h3")
					if((nxth<nxttable and nxth!=-1) or nxttable==-1):
						break
					if(pagestr.find("To sort")<nxttable and pagestr.find("To sort")!=-1):
						tosorttime()
						exit()
					pagestr=pagestr[nxttable:]
				
					for i in range(3):
						parsenext("th")
					noun=(parsenext("th").text,parsenext('i').text)
					parsenext("td")
					name = fromstring(pagestr).find(".//td")
					name = firsttrans(fromstring(re.sub("<.*?>",'',str(tostring(name),"utf-8"))).text)
					filen.write('\n "'+name.strip()+' = '+noun[1].strip()+'":\n')
	
	
					#Different cases of the noun
					while(True):
						check=fromstring(pagestr).find(".//td")
						#When we hit he next table
						if(check.find(".//i")!=None):
							break
						if skipCheck(check): continue
						else: pass
	
						noun = [parsenext("th").text,' ']
						
						noun[1] = parsenext("td")
						ch=noun[1]
	
						writeNoun(noun, filen)
	
					
						#If there's second form
						if(str(tostring(ch)).find('colspan="2"')==-1):
							check=fromstring(pagestr).find(".//td")
							if skipCheck(check): continue
							else: pass

							noun[1]=parsenext("td")
							if(noun[1].find(".//b")!=None):
								noun[1] = fromstring(re.sub("<.*?>",'',str(tostring(noun[1]),"utf-8"))).text
							else:
								noun[1]=noun[1].text
	
							if(noun[1].strip()!="[]" and noun[1].strip()!="" and noun[1].strip()!="—"):
								if(noun[0].lower().strip()=="pl"):
									filen.write("    "+name.strip()+"<n><pl><nom> : "+firsttrans(noun[1]).strip()+'\n')
								else:
									filen.write("    "+name.strip()+"<n><"+noun[0].lower().strip()+"> : "+firsttrans(noun[1]).strip()+'\n')
							


			#Else it's normal
			else:
				#Nominitive of noun (name) and the translation
				while(True):
					nxttable=pagestr.find('<table class="wikitable"')
					if(pagestr.find("h3")<nxttable or nxttable==-1):
						break
					pagestr=pagestr[nxttable:]
					noun=(parsenext("th").text,parsenext('i').text)
					parsenext("td")
					name = fromstring(pagestr).find(".//td")
					name = firsttrans(fromstring(re.sub("<.*?>",'',str(tostring(name),"utf-8"))).text)
					filen.write('\n "'+name.strip()+' = '+noun[1].strip()+'":\n')
	

					#Different cases of the noun
					while(True):
						check=fromstring(pagestr).find(".//td")
						#When we hit the next table
						if(check.find(".//i")!=None):
							break
						if skipCheck(check): continue
						else: pass
						
						noun = [parsenext("th").text, parsenext("td")]
						writeNoun(noun,filen)
