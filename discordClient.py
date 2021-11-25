import discord
from tgtgStore import tgtgStore

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
		response_ok, response = await self.tgtg_client.get_favorites()

		if response_ok == True:
			update_favorite= list()

			for idx, store in enumerate(response):
				update_favorite.append(tgtgStore(str(idx),store["store"]["store_name"],str(store["items_available"])))

			if self.favorite :
				for idx, store in enumerate(self.favorite) :
					if update_favorite[idx].items_available != store.items_available :
						self.favorite = update_favorite
						return True
				return False

			else: 
				self.favorite = update_favorite
				return True
		else :
			self.sleeping = True
			await self.channel.send("Error.")

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

	async def on_message(self, message):

		msg = message.content
		msg = msg.lower()

		if message.author.id == self.user.id:
			return


		if msg.startswith('on'):
			self.sleeping = False
			await self.clear()
			await self.send_new_basket()

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

		if msg.startswith('unfocus'):

			focused_store_id = msg.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.remove(store)
						await self.channel.send(store.name+" unfocused.")
			else :
				await self.channel.send("You need to call favorite first.")

		if msg.startswith("get focus"):
			if self.focus :
				await self.send_focus()
			else :
				await self.channel.send("No focus.")

		if msg.startswith("clear focus"):
			self.focus= list()
			await self.channel.send("Focus clear.")

		if msg.startswith('favorite'):
			self.sleeping = True

			await self.clear()

			if self.favorite :
				for store in self.favorite :
					await self.channel.send(store.index+"# "+store.name)
			else :
				i = 0
				response_ok, response = await self.tgtg_client.get_favorites()
				if response_ok == True :
					for store in response :
						self.favorite.append(tgtgStore(str(i),store["store"]["store_name"],str(store["items_available"])))
						await self.channel.send(self.favorite[i].index+"# "+self.favorite[i].name)
						i += 1
				else :
					self.sleeping = True
					await self.channel.send("Error.")

		if msg.startswith("add"):
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

			response_ok = await self.tgtg_client.set_favorite(favorite[0])

			if response_ok == True :
				self.favorite = list()
				await self.channel.send(str(favorite[0]["store"]["store_name"])+" added")
			else :
				self.sleeping = True
				await self.channel.send("Error.")

		if msg.startswith("remove"):
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

			response_ok = await self.tgtg_client.remove_favorite(favorite[0])

			if response_ok == True:
				self.favorite = list()
				await self.channel.send(str(favorite[0]["store"]["store_name"])+" removed")
			else :
				self.sleeping = True
				await self.channel.send("Error.")

