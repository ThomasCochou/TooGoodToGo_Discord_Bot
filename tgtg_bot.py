from tgtg import TgtgClient
import discord
from decouple import config
from discord.ext import tasks, commands

TGTG_TOKEN = config('TGTG_TOKEN')
TGTG_REFRESH_TOKEN = config('TGTG_REFRESH_TOKEN')
USER_ID = config('USER_ID')

DISCORD_TOKEN = config('DISCORD_TOKEN')

tgtg_client = TgtgClient(access_token=TGTG_TOKEN, refresh_token=TGTG_REFRESH_TOKEN, user_id=USER_ID)

general_channel_id = 910191399733952566

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		self.channel = self.get_channel(id=general_channel_id)
		self.sleeping = False

	def create_tgtg_client(self,tgtg_client):
		self.tgtg_client=tgtg_client

	async def check_new_basket(self):
		response = self.tgtg_client.get_items()
		new_msg = list()

		for store in response:
			if store["items_available"] == 1 :
				new_msg.append(str(store["store"]["store_name"])+" have "+str(store["items_available"])+" basket available.")
			elif store["items_available"] >= 1 :
				new_msg.append(str(store["store"]["store_name"])+" have "+str(store["items_available"])+" baskets available.")

		return(new_msg)
			
	async def send_new_basket(self,new_msg):
		for msg in new_msg :
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

	async def on_message(self, message):
		if message.author.id == self.user.id:
			return

		if message.content.startswith('connexion'):
			
			response = self.tgtg_client.login()

			if response == None :
				await message.channel.send("Connected.".format(message))
			else :
				await message.channel.send(str(response).format(message))

		if message.content.startswith('on'):
			self.sleeping = False
			await message.channel.send("Bot on.".format(message))

		if message.content.startswith('off'):
			self.sleeping = True
			await self.clear()
			await message.channel.send("Bot off.".format(message))

		if message.content.startswith('favorite'):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			response = self.tgtg_client.get_items()

			for store in response : 
				await message.channel.send(str(store["store"]["store_name"]).format(message))

		if message.content.startswith("add"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			latitude = message.content.split(":")[1].split(',')[0]
			longitude = message.content.split(":")[1].split(',')[1]

			response = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)
			print("store_name: "+str(response[0]["store"]["store_name"]))
			print("store_id: "+str(response[0]['item']['item_id']))

			self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=True)

			await message.channel.send(str(response[0]["store"]["store_name"])+" added".format(message))

		if message.content.startswith("remove"):
			if self.sleeping == False :
				self.sleeping = True

			await self.clear()

			latitude = message.content.split(":")[1].split(',')[0]
			longitude = message.content.split(":")[1].split(',')[1]

			response = self.tgtg_client.get_items(
				favorites_only=False,
				latitude=latitude,
				longitude=longitude,
				radius=1,
				)
			print("store_name: "+str(response[0]["store"]["store_name"]))
			print("store_id: "+str(response[0]['item']['item_id']))

			self.tgtg_client.set_favorite(item_id=response[0]['item']['item_id'], is_favorite=False)

			await message.channel.send(str(response[0]["store"]["store_name"])+" removed".format(message))



class MyCog(commands.Cog):
	def __init__(self, discord_client):
		self.index = 0
		self.discord_client = discord_client
		self.printer.start()

	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=3.0)
	async def printer(self):
		if self.discord_client.sleeping == False :
			self.index += 1
			last_msg = await self.discord_client.get_last_msg()
			new_msg = await self.discord_client.check_new_basket()

			if last_msg != new_msg :
				await self.discord_client.clear()
				await self.discord_client.send_new_basket(new_msg)

	@printer.before_loop
	async def before_printer(self):
		print('waiting...')
		await self.discord_client.wait_until_ready()


discord_client = MyClient()

discord_client.create_tgtg_client(tgtg_client)

discord_cog = MyCog(discord_client)

discord_client.run(DISCORD_TOKEN)