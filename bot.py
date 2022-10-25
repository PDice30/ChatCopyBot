from twitchio.ext import commands
from twitchio import Message, Channel
import json

# List of channels to possibly join
dtv = "dice_the_vice"
fftbg = "fftbattleground"
pdice30 = "pdice30"
phildo3 = "phildo3"

# Config vars
me="pdice30"
parentChannel = fftbg
childChannel = me
delimitingChar = '~'

# Will store the Channel connection web socket
capturedMessage = ''

class Bot(commands.Bot):

  def __init__(self):
    # Initialise our Bot with our access token, prefix and a list of channels to join on boot
    f = open('secret.json')
    data = json.load(f)
    super().__init__(token=data['oauth'], prefix='', initial_channels=[pdice30, fftbg])

  async def event_ready(self):
    # Notify us when everything is ready!
    # We are logged in and ready to chat and use commands
    print(f'Logged in as | {self.nick}')

  async def event_message(self, message):
    global capturedMessage

    # Messages with echo set to True are messages sent by the bot
    # For now we just want to ignore them
    if message.echo:
        return

    # Only ever read messages from the bot's owner
    if message.author.name == me:

    # We need to capture a message from FFTBG and store the channel websocket
    # Note: there's probably a better way to do this, but it is what it is
      if capturedMessage == '' and message.channel.name == parentChannel and message.content[:7] == 'HeyGuys':
        capturedMessage = message
        print('captured {phildo3} message, starting')
        print (message.content[:7])

      # A message sent in the child channel starting with the delimitingChar will be sent to the parent channel sans that char
      if message.channel.name == childChannel and message.content[:1] == delimitingChar and capturedMessage != '':
        capturedMessage.content = message.content[1:]
        print (message.content[1:])
        await capturedMessage.channel.send(capturedMessage.content)
  
    # Since we have commands and are overriding the default `event_message`
    # We must let the bot know we want to handle and invoke our commands...
    await self.handle_commands(message)

  @commands.command()
  async def hello(self, ctx: commands.Context):
    # Here we have a command hello, we can invoke our command with our prefix and command name
    # e.g ?hello
    # We can also give our commands aliases (different names) to invoke with.

    # Send a hello back!
    # Sending a reply back to the channel is easy... Below is an example.
    await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.