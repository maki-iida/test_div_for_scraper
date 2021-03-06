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
		self.channel_countries = []
		self.channel_subscribers = []


	def run(self):
		self.read_youtube_urls()
		self.get_page_source()
		self.channel_country_additional()
		self.channel_subscriber_additional()
		self.driver.close()


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
				html = self.driver.page_source
				if self.current_html != html:
					self.current_html=html
				else:
					self.parse_channel_country()
					break


	def parse_channel_country(self):
		soup = BeautifulSoup(self.current_html, 'html.parser')
		'''
		channelSubscriberOfIntExtractionFunction
		'''
		
		channel_subscriber_i = soup.find("yt-formatted-string", class_="style-scope ytd-c4-tabbed-header-renderer")
		channel_subscriber_lstrip = str(channel_subscriber_i).lstrip('<yt-formatted-string class="style-scope ytd-c4-tabbed-header-renderer" id="subscriber-count">')
		channel_subscriber_rstrip = channel_subscriber_lstrip.rstrip('</yt-formatted-string>')
		if "万" in channel_subscriber_rstrip:
			channel_subscriber_replace = channel_subscriber_rstrip.replace(' ', '')
			channel_subscriber_sub = re.sub("\\D", "", str(channel_subscriber_replace))
			channel_subscriber_add_million = channel_subscriber_sub + '00'
			channel_subscriber_material = int(channel_subscriber_add_million)
		else:
			channel_subscriber_replace = channel_subscriber_rstrip.replace(' ', '')
			channel_subscriber_sub = re.sub("\\D", "", str(channel_subscriber_replace))
			channel_subscriber_material = int(channel_subscriber_sub)
			'''
			CuntryOfIntExtractionFunction
			'''
		for i in soup.find_all("td", class_="style-scope ytd-channel-about-metadata-renderer"):
			cuntry_i_findall = re.findall('<yt-formatted-string class="style-scope ytd-channel-about-metadata-renderer">.*</yt-formatted-string>', str(i))
			cuntry_i_replace = str(cuntry_i_findall).replace('<yt-formatted-string class="style-scope ytd-channel-about-metadata-renderer">', '').replace('</yt-formatted-string>', '')
			cuntry = str(cuntry_i_replace).replace("['", '').replace("']", '')
			'''
			channelSubscriberOfIntExtractionFunction
			'''
			channel_subscriber = channel_subscriber_material
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
				self.channel_countries.append(cuntry)
				self.channel_subscribers.append(channel_subscriber)


	def channel_country_additional(self):
		df = pd.read_csv('sample.csv')
		df['channel_country'] = self.channel_countries
		pd.DataFrame(df).to_csv('sample.csv',index=False)


	def channel_subscriber_additional(self):
		print(self.channel_subscribers)
		df = pd.read_csv('sample.csv')
		df['channel_subscriber'] = self.channel_subscribers
		pd.DataFrame(df).to_csv('sample.csv',index=False)
		print(df)


if __name__ == "__main__":
    channel_country = ChannelCountryScraper()
    channel_country.run()
