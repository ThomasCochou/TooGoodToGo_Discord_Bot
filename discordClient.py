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

			print(self.focus)

			i = 0
			for store in response:
				update_favorite.append(storeTgtg(str(i),store["store"]["store_name"],str(store["items_available"])))
				i += 1

			if self.favorite :
				i = 0
				for store in self.favorite :
					if update_favorite[i].index != store.index :
						print("here")
						self.favorite = update_favorite

						return True
					i += 1

			self.favorite = update_favorite

			print(update_favorite[0].availability)
			print(self.favorite[0].availability)
			return False

			
			
	async def send_new_basket(self):
		for store in self.favorite :
			if self.focus :
				for focused_store in self.focus :
					if focused_store == store :
						if int(store.availability) == 1 :
							await self.channel.send(store.name+" have "+store.availability+" basket available.")
						elif int(store.availability) >= 1 :
							await self.channel.send(store.name+" have "+store.availability+" baskets available.")
			else :
				if int(store.availability) == 1 :
					await self.channel.send(store.name+" have "+store.availability+" basket available.")
				elif int(store.availability) >= 1 :
					await self.channel.send(store.name+" have "+store.availability+" baskets available.")

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
				await message.channel.send("Connected.".format(message))

		if message.content.startswith('on'):
			self.sleeping = False
			self.exception = False
			await message.channel.send("Bot on.".format(message))

		if message.content.startswith('off'):
			self.sleeping = True
			await self.clear()
			await message.channel.send("Bot off.".format(message))

		if message.content.startswith('focus'):
			await self.clear()

			focused_store_id = message.content.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.append(store)
						await message.channel.send(store.name+" focused.".format(message))
			else :
				await message.channel.send("You need to call favorite first.".format(message))

			self.sleeping = False

		if message.content.startswith('unfocus'):
			await self.clear()

			focused_store_id = message.content.split(" ")[1]

			if self.favorite :
				for store in self.favorite :
					if store.index == focused_store_id :
						self.focus.remove(store)
						await message.channel.send(store.name+" unfocused.".format(message))
			else :
				await message.channel.send("You need to call favorite first.".format(message))

			self.sleeping = False


		if message.content.startswith('favorite'):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			if self.favorite :
				for store in self.favorite :
					await message.channel.send(store.index+"# "+store.name.format(message))
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
						await message.channel.send(self.favorite[i].format(message))
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
				await message.channel.send(str(response[0]["store"]["store_name"])+" added".format(message))

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
			print("store_name: "+str(response[0]["store"]["store_name"]))
			print("store_id: "+str(response[0]['item']['item_id']))

			try:
				self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=False)
			except Exception as e:
				print("remove: "+str(e))
				await self.channel.send("remove: "+str(e))
				self.exception = True

			if self.exception == False:
				await message.channel.send(str(response[0]["store"]["store_name"])+" removed".format(message))

