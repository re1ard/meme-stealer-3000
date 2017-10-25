# -*- coding: utf-8 -*-

#######################################
##contact: https://vk.com/id27919760 ##
#######################################

from vk_api import VkApi as VK
import vk_api
from json import load, dump
from time import time
from time import strftime
from time import sleep
from time import localtime
from random import choice
import random

import traceback
import threading
import sys

class root:
	def __init__(self,gids):
		self.api = VK('login','password')#login,password
		self.api.auth()
                
		print u'[\033[92mINFO\033[0m] %s' % u'Start stealer!'

		self.owners = owner_ids = [-1 * gid['id'] for gid in self.api.method('groups.getById',{'group_ids':gids})]

		self.vault = self.loadcfg()

		self.attach_types = [u'photo']

		self.GID = -XXXXXXXX#id group

	def loadcfg(self):
		try:
			with open('mmstlr.config.json') as data_file:
				return load(data_file)
		except:
			with open('mmstlr.config.json', 'w') as data_file:
				dump({'time':int(time()),'posts':{},'offsets':{}},data_file)
				return {'time':int(time()),'posts':{},'offsets':{}}

	def savecfg(self):
		with open('mmstlr.config.json', 'w') as data_file:
			dump(self.vault,data_file)
			return True

	def post(self,text,attachments):
		print u'[\033[93mPOST\033[0m] Save config file, dude.'
		self.savecfg()
		try:
			print u'[\033[93mPOST\033[0m] Attachments: %s' % attachments
			self.api.method('wall.post',{'owner_id':self.GID,'attachments':attachments,'message':text})
		except:
			print u'[\033[91mFAIL\033[0m]\n %s' % traceback.format_exc()
			return False

	def get_pool(self,offset = 0):
		if True:
			with vk_api.VkRequestsPool(self.api) as pool:
				response = pool.method_one_param(
					'wall.get',
					key = 'owner_id',
					values = self.owners,
					default_values = {'count':100,'offset':offset}
					)
			return response.result

	def eject_attach(self,post):
		if True:
			if True:
				if True:
					attachs = []
					post_id = '%s_%s' % (post['owner_id'],post['id'])
					if 'attachments' in post:
						for attach in post['attachments']:
							if attach['type'] in self.attach_types:
								if 'access_key' in attach[attach['type']]:
									attachs.append('%s%s_%s_%s' % (attach['type'],attach[attach['type']]['owner_id'],attach[attach['type']]['id'],attach[attach['type']]['access_key']))
								else:
									attachs.append('%s%s_%s' % (attach['type'],attach[attach['type']]['owner_id'],attach[attach['type']]['id']))
						if len(attachs):
							return {post_id:attachs}
						else:
							self.vault['posts'].update({post_id:attachs})
							return {}
					else:
						self.vault['posts'].update({post_id:attachs})
						return {}

	def getter(self):
		try:
			posts = {'new':{},'old':{},'len_new':0,'len_old':0,'offset':0}
			while posts['len_new'] < 11 and posts['len_old'] < 11:
				print 'Get pool... Offset: %s' % posts['offset']
				response = self.get_pool(posts['offset'])
				posts['offset'] += 100
				for pub in response.values():
					get_pub = False
					if not get_pub:
						for post in pub['items']:
							if ('is_pinned' in post and post['is_pinned']) or ('marked_as_ads' in post and post['marked_as_ads']):
								this_shit = True
							else:
								this_shit = False
							post_id = '%s_%s' % (post['owner_id'],post['id'])
							if not this_shit and not post_id in self.vault['posts']:
								if post['date'] > self.vault['time']:
									reject = self.eject_attach(post)
									if reject:
										posts['new'].update(reject)
										for popst in reject.values():
											posts['len_new'] += len(popst)
								else:
									reject = self.eject_attach(post)
									if reject:
										posts['old'].update(reject)
										for popst in reject.values():
											posts['len_old'] += len(popst)
							
			if posts['len_new'] > posts['len_old']:	
				return posts['new']
			else:
				return posts['old']
		except:
			print u'[\033[91mFAIL\033[0m]\n %s' % traceback.format_exc()
			return False
		

	def process(self):
		try:
			posts = self.getter()
			print u'[\033[92mINFO\033[0m] %s' % posts
		except:
			print u'[\033[91mFAIL\033[0m]\n %s' % traceback.format_exc()
			return False
							
		self.vault['time'] = int(time())

		attachments = u''
		text = u''
		attach_counter = 0

		for attach in posts.keys():
			if not attach in self.vault['posts']:
				self.vault['posts'].update({attach:posts[attach]})
			for atta4 in posts[attach]:
				attachments += atta4 + ','
				attach_counter += 1
			text += 'vk.com/wall%s\n' % attach
			if attach_counter > 9:
				return self.post(text,attachments)
		return self.post(text,attachments)

	def updater(self,test = False):
		if test:
			thread = threading.Thread(target=self.process,args = [])
			thread.daemon = True
			thread.start()
		for zavali_ebalo in self.timer():
			if int(zavali_ebalo[0]) in range(10,22):
				if int(zavali_ebalo[1]) in [0,15,30,45]:
					if int(zavali_ebalo[2]) == 0:
						thread = threading.Thread(target=self.process,args = [])
						thread.daemon = True
						thread.start()

	def timer(self):
		while True:
			yield tuple(strftime("%H:%M:%S", localtime(time())).split(':'))
			sleep(1)

def main(q = False):
	try:
		with open('public.list') as pl:
			lines = pl.readlines()
			links = [list(reversed(link.split('/')))[0] for link in lines if not '#' in link]
		if not len(links):
			print u'[\033[92mINFO\033[0m] %s' % u'append links in public.list'
			return
	except:
		with open('public.list','w') as pl:
			pl.write('#ADD TO THIS FILE LINKS ON PUBLICS OR GID')
		print u'[\033[92mINFO\033[0m] %s' % u'check public.list file'
		return


	gids = ''
	for link in links:
		gids += '%s,' % link

	ROOT = root(gids)
	ROOT.updater(q)
	


if __name__ == '__main__':
	if 'tstart' in sys.argv:
		main(True)
	else:
		main()
