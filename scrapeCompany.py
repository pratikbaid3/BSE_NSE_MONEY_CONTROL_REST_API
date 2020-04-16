import bs4 
import urllib.request as ur
import requests

def getNewEvents(soup,formData):
	try:

		VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
		VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")['value']
		EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']

		formData["__VIEWSTATE"]=VIEWSTATE
		formData["__VIEWSTATEGENERATOR"]=VIEWSTATEGENERATOR
		formData["__EVENTVALIDATION"]=EVENTVALIDATION

	except Exception:
		pass


def getCompanyCorporateActions(secName,secCode,fromDate=None):
	site_url = "https://www.bseindia.com/corporates/corporate_act.aspx"

	head = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	   'Accept-Encoding': 'none',
	   'Accept-Language': 'en-US,en;q=0.8',
	   'Connection': 'keep-alive'}

	data = {
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'__VIEWSTATE': '',
		'__VIEWSTATEGENERATOR': '',
		'__VIEWSTATEENCRYPTED': '',
		'__EVENTVALIDATION': '',
		'ctl00$ContentPlaceHolder1$hndvalue': 'S',
		'ctl00$ContentPlaceHolder1$hdnCheck': '',
		'ctl00$ContentPlaceHolder1$ddlcategory': 'E',
		'ctl00$ContentPlaceHolder1$txtDate': '',
		'ctl00$ContentPlaceHolder1$txtTodate': '',
		'ctl00$ContentPlaceHolder1$SmartSearch$hdnCode': '',
		'ctl00$ContentPlaceHolder1$SmartSearch$smartSearch': '',
		'ctl00$ContentPlaceHolder1$hf_scripcode': '',
		'ctl00$ContentPlaceHolder1$ddlindustry': 'Select',
		'ctl00$ContentPlaceHolder1$ddlPurpose': 'Select',
		'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit',
	}

	if(fromDate):
		data['ctl00$ContentPlaceHolder1$txtDate']=fromDate
	data['ctl00$ContentPlaceHolder1$SmartSearch$smartSearch']=secName
	data['ctl00$ContentPlaceHolder1$SmartSearch$hdnCode']=secCode
	data['ctl00$ContentPlaceHolder1$hf_scripcode']=secCode

	with requests.Session() as s:

		r = s.get(site_url)
		soup = bs4.BeautifulSoup(r.content, 'lxml')
		getNewEvents(soup,data)

		r = s.post(site_url, data=data)
		soup = bs4.BeautifulSoup(r.content, 'lxml')
		getNewEvents(soup,data)
		del data['ctl00$ContentPlaceHolder1$btnSubmit']

		page = 2
		total = 0

		while(True):

			r = s.post(site_url, data=data)
			soup = bs4.BeautifulSoup(r.content, 'lxml')
			getNewEvents(soup,data)
			rows = soup.find_all('tr', attrs={"class":"TTRow"})

			if(len(rows) == 0):
				break

			total += len(rows)

			# just do whatever you want with the soup
			for row in rows:
				columns = row.find_all('td')
				for col in columns:
					print(col.string)

			data["__EVENTTARGET"]="ctl00$ContentPlaceHolder1$gvData"
			data["__EVENTARGUMENT"]=f"Page${page}"
			page += 1
	print(total)

getCompanyCorporateActions("NESTLEIND","500790") # example
