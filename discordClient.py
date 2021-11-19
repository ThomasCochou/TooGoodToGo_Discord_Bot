import discord

general_channel_id = 910191399733952566

class discordClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		self.channel = self.get_channel(id=general_channel_id)
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
			print(e)
			await self.channel.send("Exception.")
			self.exception = True

		new_msg = list()

		for store in response:
			if store["items_available"] == 1 :
				new_msg.append(str(store["store"]["store_name"])+" have "+str(store["items_available"])+" basket available.")
			elif store["items_available"] >= 1 :
				new_msg.append(str(store["store"]["store_name"])+" have "+str(store["items_available"])+" baskets available.")

		return(new_msg)
			
	async def send_new_basket(self,new_msg):
		for msg in new_msg :
			if self.focus :
				for focused_store in self.focus :
					if focused_store.split("# ")[1] == msg.split(" have")[0]:
						await self.channel.send(msg)
			else :
				await self.channel.send(msg)

	async def get_last_msg(self):
		last_msg = list()
		async for msg in self.channel.history():
			last_msg.append(msg.content)

		last_msg.reverse()
		return(last_msg)

	async def clear(self):
		async for msg in self.channel.history():
			await msg.delete()

	async def API_connexion(self) :
		try:
			response = self.tgtg_client.login()
		except Exception as e:
			print(e)
			await self.channel.send("Exception.")
			self.exception = True
		
		if response == None :
			await message.channel.send("Connected.".format(message))

	async def on_message(self, message):
		if message.author.id == self.user.id:
			return

		if message.content.startswith('connexion'):
			self.API_connexion()

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
				for favorite in self.favorite :
					if favorite.split("#")[0] == focused_store_id :
						self.focus.append(favorite)
						await message.channel.send(str(favorite)+" focused.".format(message))
			else :
				await message.channel.send("You need to call favorite first.".format(message))

			self.sleeping = False

		if message.content.startswith('unfocus'):
			await self.clear()

			focused_store_id = message.content.split(" ")[1]

			for favorite in self.favorite :
				if favorite.split("#")[0] == focused_store_id :
					self.focus.remove(favorite)
					await message.channel.send(str(favorite)+" unfocused.".format(message))

			self.sleeping = False


		if message.content.startswith('favorite'):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			if self.favorite :
				for favorite in self.favorite :
					await message.channel.send(favorite.format(message))
			else :
				try:
					response = self.tgtg_client.get_items()
				except Exception as e:
					print(e)
					await self.channel.send("Exception.")
					self.exception = True

				i = 0
				for store in response :
					self.favorite.append(str(i)+"# "+str(store["store"]["store_name"]))
					await message.channel.send(str(i)+"# "+str(store["store"]["store_name"]).format(message))
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
			print("store_name: "+str(response[0]["store"]["store_name"]))
			print("store_id: "+str(response[0]['item']['item_id']))

			try:
				self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=True)
			except Exception as e:
				print(e)
				await self.channel.send("Exception.")
				self.exception = True

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
				print(e)
				await self.channel.send("Exception.")
				self.exception = True
		
			await message.channel.send(str(response[0]["store"]["store_name"])+" removed".format(message))

