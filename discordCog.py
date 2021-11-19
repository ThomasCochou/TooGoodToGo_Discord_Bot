from discord.ext import tasks, commands

from discordClient import discordClient

fetch_API_seconds = 300.0

class discordCog(commands.Cog):
	def __init__(self, discord_client):
		self.index = 0
		self.discord_client = discord_client
		self.printer.start()

	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=fetch_API_seconds)
	async def printer(self):
		if self.discord_client.sleeping == False and self.discord_client.exception == False:
			self.index += 1
			last_msg = await self.discord_client.get_last_msg()
			new_msg = await self.discord_client.check_new_basket()

			if last_msg != new_msg :
				await self.discord_client.clear()
				await self.discord_client.send_new_basket(new_msg)

	@printer.before_loop
	async def before_printer(self):
		print('waiting...')
		await self.discord_client.API_connexion()
		await self.discord_client.wait_until_ready()
