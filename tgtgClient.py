class tgtgClient() :
	def __init__(self, tgtg_client_access):
		self.tgtg_client_access = tgtg_client_access

	async def connexion(self):
		try:
			self.tgtg_client_access.login()
			return True
		except Exception as e:
			print("connexion: "+str(e))
			return False

	async def get_favorites(self):
		try:
			response = self.tgtg_client_access.get_items()
			return True, response
		except Exception as e:
			print("tgtg_get_favorites: "+str(e))
			return False, "Error."

	async def set_favorite(self,favorite):
		try:
			self.tgtg_client_access.set_favorite(item_id=favorite['item']['item_id'], is_favorite=True)
			return True
		except Exception as e:
			print("add: "+str(e))
			return False

	async def remove_favorite(self,favorite):
		try:
			self.tgtg_client_access.set_favorite(item_id=favorite['item']['item_id'], is_favorite=False)
			return True
		except Exception as e:
			print("remove: "+str(e))
			return False