import discord
from storeTgtg import storeTgtg

brest_channel_id = 910191399733952566

class discordClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		self.channel = self.get_channel(id=brest_channel_id)
		self.sleeping = False
		self.exception = False
		self.focus = list()
		self.favorite= list()

	def create_tgtg_client(self,tgtg_client):
		self.tgtg_client=tgtg_client

	async def check_new_basket(self):
		try:
			response = self.tgtg_client.get_items()
		except Exception as e:
			print("check_new_basket: "+str(e))
			await self.channel.send("check_new_basket: "+str(e))
			self.exception = True

		if self.exception == False:
			update_favorite= list()

			i = 0
			for store in response:
				update_favorite.append(storeTgtg(str(i),store["store"]["store_name"],str(store["items_available"])))
				i += 1

			if self.favorite :
				i = 0
				for store in self.favorite :
					if update_favorite[i].items_available != store.items_available :
						self.favorite = update_favorite

						return True
					i += 1

			self.favorite = update_favorite

			return False

	async def send_focus(self):
		for store in self.focus:
			await self.channel.send(store.name+" focus.")

			
	async def send_new_basket(self):
		for store in self.favorite :
			if self.focus :
				for focused_store in self.focus :
					if focused_store.name == store.name :
						if int(store.items_available) == 1 :
							await self.channel.send(store.name+" have "+store.items_available+" basket available.")
						elif int(store.items_available) >= 1 :
							await self.channel.send(store.name+" have "+store.items_available+" baskets available.")
			else :
				if int(store.items_available) == 1 :
					await self.channel.send(store.name+" have "+store.items_available+" basket available.")
				elif int(store.items_available) >= 1 :
					await self.channel.send(store.name+" have "+store.items_available+" baskets available.")

	async def clear(self):
		async for msg in self.channel.history():
			await msg.delete()

	async def tgtg_connexion(self):
		try:
			response = self.tgtg_client.login()
			return response
		except Exception as e:
			print("connexion: "+str(e))
			await self.channel.send("connexion: "+str(e))
			self.exception = True

	async def tgtg_get_items(self):
		try:
			response = self.tgtg_client.get_items()
		except Exception as e:
			print("favorite: "+str(e))
			await self.channel.send("favorite: "+str(e))
			self.exception = True
		return 

	async def tgtg_set_favorite(self,favorite):
		try:
			self.tgtg_client.set_favorite(item_id=favorite['item']['item_id'], is_favorite=True)
		except Exception as e:
			print("add: "+str(e))
			await self.channel.send("add: "+str(e))
			self.exception = True

	async def tgtg_remove_favorite(self,favorite):
		try:
			self.tgtg_client.set_favorite(item_id=favorite['item']['item_id'], is_favorite=False)
		except Exception as e:
			print("remove: "+str(e))
			await self.channel.send("remove: "+str(e))
			self.exception = True


	async def on_message(self, message):

		msg = message.content
		msg = msg.lower()

		if message.author.id == self.user.id:
			return

		if msg.startswith('connexion'):
			if self.exception == False :
				await self.channel.send("Connected.")

		if msg.startswith('on'):
			self.sleeping = False
			self.exception = False
			await self.clear()
			await self.send_new_basket()
			await self.channel.send("Bot on.")

		if msg.startswith('off'):
			self.sleeping = True
			await self.clear()
			await self.channel.send("Bot off.")

		if msg.startswith('focus'):

			focused_store_id = msg.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.append(store)
						await self.channel.send(store.name+" focused.")
			else :
				await self.channel.send("You need to call favorite first.")

			self.sleeping = False

		if msg.startswith('unfocus'):

			focused_store_id = msg.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.remove(store)
						await self.channel.send(store.name+" unfocused.")
			else :
				await self.channel.send("You need to call favorite first.")

			self.sleeping = False

		if msg.startswith("get focus"):
			if self.focus :
				await self.send_focus()
			else :
				await self.channel.send("No focus.")

		if msg.startswith("clear focus"):
			self.focus= list()
			await self.channel.send("Focus clear.")

		if msg.startswith('favorite'):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			if self.favorite :
				for store in self.favorite :
					await self.channel.send(store.index+"# "+store.name)
			else :
				if self.exception == False :
					i = 0
					await response = self.tgtg_get_items()
					for store in response :
						self.favorite.append(storeTgtg(str(i),store["store"]["store_name"],str(store["items_available"])))
						await self.channel.send(self.favorite[i].index+"# "+self.favorite[i].name)
						i += 1

		if msg.startswith("add"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			self.favorite = list()

			latitude = msg.split(" ")[1].split(',')[0]
			longitude = msg.split(" ")[1].split(',')[1]

			favorite = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)

			await self.tgtg_set_favorite(favorite[0])

			if self.exception == False :
				self.favorite = list()
				await self.channel.send(str(favorite[0]["store"]["store_name"])+" added")

		if msg.startswith("remove"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			self.favorite = list()

			latitude = msg.split(" ")[1].split(',')[0]
			longitude = msg.split(" ")[1].split(',')[1]

			favorite = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)

			await self.tgtg_remove_favorite(favorite[0])

			if self.exception == False:
				self.favorite = list()
				await self.channel.send(str(favorite[0]["store"]["store_name"])+" removed")

