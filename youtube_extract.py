import os.path
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re
import numpy as np
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


class ChannelCountryScraper(object):

	def __init__(self):
		self.channel_about_urls = []
		self.channel_cuntry = []


	def run(self):
		self.read_youtube_urls()
		self.get_page_source()
		self.channel_country_write()
		self.driver.close()
		# self.parse_channel_country()
		# self.channel_country_data_save_as_csv_file()


	def read_youtube_urls(self):
		channel_url_data = pd.read_csv('sample.csv',index_col='channel_url')
		channel_urls_ndarray = channel_url_data.index.values
		channel_urls = channel_urls_ndarray.tolist()
		for i in channel_urls:
			youtube_url = 'https://www.youtube.com'
			self.channel_url = ('%s' % i)
			about_url = 'about'
			channel_about_url = urlparse.urljoin(youtube_url, self.channel_url+'/about')
			self.channel_about_urls.append(channel_about_url)


	def get_page_source(self):
		self.driver = webdriver.Chrome()
		for i in self.channel_about_urls:
			self.driver.get(i)
			self.current_html = self.driver.page_source
			element = self.driver.find_element_by_xpath('//*[@class="style-scope ytd-page-manager"]')
			actions = ActionChains(self.driver)
			actions.move_to_element(element)
			actions.perform()
			actions.reset_actions()
			while True:
				for j in range(100):
					actions.send_keys(Keys.PAGE_DOWN)
				actions.perform()
				# sleep(1)
				html = self.driver.page_source
				if self.current_html != html:
					self.current_html=html
				else:
					self.parse_channel_country()
					break


	def parse_channel_country(self):
		soup = BeautifulSoup(self.current_html, 'html.parser')
		'''
			CuntryOfIntExtractionFunction
		'''
		for i in soup.find_all("td", class_="style-scope ytd-channel-about-metadata-renderer"):
			cuntry_i_findall = re.findall('<yt-formatted-string class="style-scope ytd-channel-about-metadata-renderer">.*</yt-formatted-string>', str(i))
			cuntry_i_replace = str(cuntry_i_findall).replace('<yt-formatted-string class="style-scope ytd-channel-about-metadata-renderer">', '').replace('</yt-formatted-string>', '')
			cuntry = str(cuntry_i_replace).replace("['", '').replace("']", '')
			'''
			NoneExclusion
			'''
			if "<" in cuntry:
				cuntry = None
			if "[]" in str(cuntry):
				cuntry = None
			if cuntry is None:
				continue
			if str(cuntry):
				self.channel_cuntry.append(cuntry)
				# print(cuntry)
				# self.channel_country_write()


# import StringIO
# import io 
# import urllib.request
# from PIL import Image
	def channel_country_write(self):
		# # channel_url_data = pd.read_csv('sample.csv',index_col='channel_url')
		# # print(df)
		# # print(self.channel_url)
		# # print(self.channel_cuntry)
		# # data['new_column'] = ''
		# # s = pd.Series(self.channel_cuntry, self.channel_url)
		# print(self.channel_cuntry)
		# # print(self.channel_url)
		# df = pd.read_csv('sample.csv', index_col='channel_url')
		# s = pd.Series({self.channel_cuntry: self.channel_url}, name='channel_country')
		# # s3 = s3.append(s4)
		# # df['channel_cuntry'] = s
		# # print(assign(s.values))
		# # print(s)
		# df.insert(len(df.columns), 'channel_country', self.channel_cuntry)
		# # pd.DataFrame(df_x).to_csv('sample.csv',index=True)
		# # print(channel_country_save)
		# print(df)
		data = {
		# "title": self.titles,
		# "video_url": self.video_urls,
		# "view": self.views,
		# "channel_url": self.channel_urls,
		# "channel_name": self.channel_names,
		# "video_time": self.video_times,
		"channel_country": self.channel_cuntry
		}
		print(self.channel_cuntry)
        # print(self.channel_cuntry)
		pd.DataFrame(data).to_csv('sample.csv',index=True)
		# for index, row in data.iterrows():
		# 	data['new_column'][index] = self.channel_cuntry
		# 	data.to_csv('sample.csv', index=False)
		# 	print(open('sample.csv').read())
# s = io.BytesIO(text)
# with open('sample.csv', 'w') as f:
# 	for line in s:
# 		f.write(line)



if __name__ == "__main__":
    channel_country = ChannelCountryScraper()
    channel_country.run()
