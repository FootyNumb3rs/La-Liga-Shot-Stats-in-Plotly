from matplotlib import pyplot as plt
import pandas as pd
import requests as req 
from bs4 import BeautifulSoup
import pprint as pp 
import numpy as np


def get_fox_table(season = '', competition = '', category = '',pos='', table_type='', sort = ''):
	frames = []
	competiton_keys = {
	'Liga':'2',
	'CL': '7',
	'PL': '1',
	'Bundesliga':'4',
	'Ligue':'43',
	'Serie':'3'
	}
	comp_key = competiton_keys[competition]
	#done = False
	page = 1
	while True:
		#if table -- In the middle of an idea
		fox_url='http://www.foxsports.com/soccer/{}?competition={}&season={}0&category={}&pos={}&page={}'.format(table_type,comp_key,season,category,pos,page)           
		site_soup = BeautifulSoup(req.get(fox_url).text,'html.parser')
		table = site_soup.find('table',class_='wisbb_standardTable')
		print(fox_url)
		if (table == None) | ((table_type=='standings') & (page == 2)):
			print('{} is done at page {}'.format(competition,page))
			break
		data_list = []
		for row in table.find_all('tr',class_='wisbb_fvStand'):
			row_data = []
			if row.find_all('th'):
				for item in row.find_all('th'):
					row_data.append(item.get('title'))
				row_data.insert(1,'TEAM CODE')
			else:
				for item in row.find_all('td'):
					if item.get('class'):
						if 'wisbb_text' in item.get('class'): # if it is a name
							name = ' '.join(reversed(item.find('a').find('span').get_text().split(', ')))
							team_code = item.find_all('span')[-1].get_text()[1:4]
							row_data.extend([name,team_code])
							continue # So once the name is added, you don't do another item.get_text()

					row_data.append(item.get_text())
			data_list.append(row_data)

		frame = pd.DataFrame(data_list,columns=data_list[0])
		frame = frame.loc[1:,:]
		frame.columns.values[0]='Name'
		frame['Season'] = season
		frame['Competition'] = competition
		frames.append(frame)
		page+=1
	return(pd.concat(frames))

df = get_fox_table(season='2017',competition='PL',category='STANDARD',table_type='stats',pos='None')
df.to_csv('pl_cont.csv',index=False)
