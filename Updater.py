# /usr/bin/python
import requests
import sqlite3
import BeautifulSoup as bs

#Setting the global valriables
headers= {'User-Agent':   'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
Category=[]
conn = sqlite3.connect('GHDB.db')
c=conn.cursor()

#Finding all GHDB Search commands
def findall_ghdblinks_within(urllink):
	global Category
	response=requests.get(urllink , headers=headers)
	soup=bs.BeautifulSoup(response.text)
	ghdburls_inpage=[]
	for links in soup.findAll('a', href=True):
		if ("".join(links['href'].split()).__contains__("ghdb")) and not("".join(links['href'].split()).__contains__("?action=")):
			ghdburls_inpage.append("".join(links['href'].split()))
			Category = soup.findAll('td', {'class': 'gd-description'})
	return(ghdburls_inpage)


#Parse the Content
def parse_content(urllink , num):
	#ghdbid, link, date, description , dork , other_details
	global Category
	response=requests.get(urllink, headers=headers)
	soup=bs.BeautifulSoup(response.text)
	description=soup.tbody.getText().__getslice__(soup.tbody.getText().index("Google Dork Description:"),soup.tbody.getText().index("Google Search:")).replace("Google Dork Description:","").lstrip().rstrip()
	dork=soup.tbody.getText().__getslice__(soup.tbody.getText().index("Google Search:"),soup.tbody.getText().index("Submitted:")).replace("Google Search:","").lstrip().rstrip()
	date=soup.tbody.getText().__getslice__(soup.tbody.getText().index("Submitted:"),soup.tbody.getText().index("Submitted:")+21).replace("Submitted:","").lstrip().rstrip()
	other_details=soup.tbody.getText().__getslice__(soup.tbody.getText().index("Submitted:")+21,soup.tbody.getText().__len__()).lstrip().rstrip()
	ghdbid=int(urllink.replace("https://www.exploit-db.com/ghdb/","").replace("/",""))
	use= soup.tbody.findAll('a',href=True)[0]['href']
	category=Category[num].a.getText()
	print "\n\nGHDB ID: " + str(ghdbid)
	print "Category: " + category
	print "Date Submitted: " + date
	print "Dork: " + dork
	print "Dork Use Link: " + use
	print "Description: "  + description
	print "Other Details:" + other_details
	#conn = sqlite3.connect('GHDB.db')
	#c.execute('CREATE TABLE GHDB (ID integer, CATEGORY  text, DATE date, DORK text, USE text,DESCRIPTION text, OTHER_DETAILS other_details, SOURCE text)')
	params=(ghdbid,category,date,dork,use,description,other_details,"GHDB")
	c.execute('INSERT INTO GHDB VALUES(?,?,?,?,?,?,?,?)',params)
	conn.commit()
	

#Identifying the last page

def find_last_page(urllink):
	lastpage=0
	response=requests.get(urllink, headers=headers)
	soup=bs.BeautifulSoup(response.text)
	pagelinks_inpage=[]
	for links in soup.findAll('a', href=True):
		url="".join(links['href'].split())
		if (url.__contains__("?action=")):
			pagelinks_inpage.append(url.replace("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=","").replace(url.__getslice__(url.index("&ghdb_search_text=&ghdb_search_cat_id="),url.__len__()),""))
	return(int(max(pagelinks_inpage)))
	


def update():
	try:
		c.execute('CREATE TABLE GHDB (ID integer PRIMARY KEY, CATEGORY  text, DATE date, DORK text, USE text,DESCRIPTION text, OTHER_DETAILS other_details, SOURCE text)')
		lastpage=find_last_page("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=1")
		for page in range(1,lastpage+1):
			links=findall_ghdblinks_within("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page="+str(page))
			print "#"*166
			for alls,num in zip(links,range(links.__len__())):
				parse_content(alls, num)
				print "#"*166
		print "Successfully Updated !!"
	except Exception as e:
		if e.message.__contains__("table GHDB already exists"):
			maxval=c.execute("select max(id) from GHDB where id!='' and id not like 'FSDB%'")
			maxval=maxval.fetchone()[0]
			latestids=findall_ghdblinks_within("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=0")
			latestid=int(max(latestids).replace("https://www.exploit-db.com/ghdb/","").replace("/",""))
			if maxval == latestid:
				print "Dork database is already up to date !! :)"
			elif maxval < latestid:
				while maxval != latestid:
					lastpage=find_last_page("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=1")
					for page in range(1,lastpage+1):
                        			links=findall_ghdblinks_within("https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page="+str(page))
                        			print "#"*166
						#if the identified links contain the GHDB ID , cut it till before GHDB ID and define the values links
                        			l="https://www.exploit-db.com/ghdb/"+str(maxval)+"/"
						if any(l in s for s in links):
							links=links.__getslice__(0,links.index(l))
							for alls,num in zip(links,range(links.__len__())):
								parse_content(alls, num)
								print "#"*166
							maxval=latestid
							break
						else:
							for alls,num in zip(links,range(links.__len__())):
								parse_content(alls, num)
								print "#"*166
				print "Successfully Updated !!"
try :
#use parseargs api here
	update() #-- custom-update download database from github and insert all entires into database which are not present from the ondownloaded from the github
	#search() --id --dork --description --date --others --category ( if id is given source is important else default GHDB will be taken as id is not unique) ":" character is strict without it is resembling; and or in between; default and
	#scan() --custom-dork --id --dork --description --date --others --category --delay --domain ( if id is given source is important else default GHDB will be taken as id is not unique) ":" character is strict without it is resembling; and or in between; default and
	#add() for custom dork

#use generic exception  , depending on the user arguments like if it is update or recon etc.  make necessary warning comments for each exception such as db corrupt while exiting during update
except KeyboardInterrupt:
	print "Exiting ..."

