from twitchio.ext import commands
from twitchio import Message, Channel
import json

# Config vars
me='pdice30'
parentChannel = 'fftbattleground'
childChannel = 'dice_the_vice'
startPhrase = 'HeyGuys'
delimitingPhrase = '~'

# Will store the Channel connection web socket
capturedMessage = ''

class Bot(commands.Bot):

  def __init__(self):
    # Initialise our Bot with our access token, prefix and a list of channels to join on boot
    f = open('secret.json')
    data = json.load(f)
    super().__init__(token=data['oauth'], prefix='', initial_channels=[parentChannel, childChannel])

  async def event_ready(self):
    # Notify us when everything is ready!
    print(f'Logged in as | {self.nick}')
    print(f'Enter your startPhrase in the parentChannel chat to begin!')

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
      if capturedMessage == '' and message.channel.name == parentChannel and message.content[:len(startPhrase)] == startPhrase:
        capturedMessage = message
        print('Captured {parentChannel} message, listening for messages beginning with {delimitingPhrase} in {childChannel} chat...')
        print (message.content[:len(startPhrase)])

      # A message sent in the child channel starting with the delimitingChar will be sent to the parent channel sans that char
      if message.channel.name == childChannel and message.content[:1] == delimitingPhrase and capturedMessage != '':
        capturedMessage.content = message.content[1:]
        print (message.content[len(delimitingPhrase):])
        await capturedMessage.channel.send(capturedMessage.content)

    await self.handle_commands(message)

  @commands.command()
  async def hello(self, ctx: commands.Context):
    await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.