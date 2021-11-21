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

	async def on_message(self, message):
		if message.author.id == self.user.id:
			return

		if message.content.startswith('connexion'):
			try:
				response = self.tgtg_client.login()
			except Exception as e:
				print("connexion: "+str(e))
				await self.channel.send("connexion: "+str(e))
				self.exception = True
			
			if self.exception == False :
				await self.channel.send("Connected.")

		if message.content.startswith('on'):
			self.sleeping = False
			self.exception = False
			await self.channel.send("Bot on.")

		if message.content.startswith('off'):
			self.sleeping = True
			await self.clear()
			await self.channel.send("Bot off.")

		if message.content.startswith('focus'):
			await self.clear()

			focused_store_id = message.content.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.append(store)
						await self.channel.send(store.name+" focused.")
			else :
				await self.channel.send("You need to call favorite first.")

			self.sleeping = False

		if message.content.startswith('unfocus'):
			await self.clear()

			focused_store_id = message.content.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.remove(store)
						await self.channel.send(store.name+" unfocused.")
			else :
				await self.channel.send("You need to call favorite first.")

			self.sleeping = False


		if message.content.startswith('favorite'):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			if self.favorite :
				for store in self.favorite :
					await self.channel.send(store.index+"# "+store.name)
			else :
				try:
					response = self.tgtg_client.get_items()
				except Exception as e:
					print("favorite: "+str(e))
					await self.channel.send("favorite: "+str(e))
					self.exception = True

				if self.exception == False :
					i = 0
					for store in response :
						self.favorite.append(storeTgtg(str(i),store["store"]["store_name"],str(store["items_available"])))
						await self.channel.send(self.favorite[i].index+"# "+self.favorite[i].name)
						i += 1

		if message.content.startswith("add"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			self.favorite = list()

			latitude = message.content.split(" ")[1].split(',')[0]
			longitude = message.content.split(" ")[1].split(',')[1]

			response = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)

			try:
				self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=True)
			except Exception as e:
				print("add: "+str(e))
				await self.channel.send("add: "+str(e))
				self.exception = True

			if self.exception == False :
				self.favorite = list()
				await self.channel.send(str(response[0]["store"]["store_name"])+" added")

		if message.content.startswith("remove"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			self.favorite = list()

			latitude = message.content.split(" ")[1].split(',')[0]
			longitude = message.content.split(" ")[1].split(',')[1]

			response = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)

			try:
				self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=False)
			except Exception as e:
				print("remove: "+str(e))
				await self.channel.send("remove: "+str(e))
				self.exception = True

			if self.exception == False:
				self.favorite = list()
				await self.channel.send(str(response[0]["store"]["store_name"])+" removed")

