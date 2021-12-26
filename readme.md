from discord.ext import commands
from discord_buttons_plugin import  *

bot = commands.Bot(command_prefix  =  "!")
buttons = ButtonsClient(bot)
await buttons.send(
	content = "This is an example message!", 
	channel = ctx.channel.id,
	components = [
		ActionRow([
			Button(
				label="Hello", 
				style=ButtonType().Primary, 
				custom_id="button_one"       
			)
		])
	]
)
ActionRow([
	Button(
		...
	),
	Button(
		label = "Button label",
		style = ButtonType().Link,
		url = "https://github.com/SilentJungle399/discord_buttons_plugin"
	)
])