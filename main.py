import discord
import os
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


class FoobarDB(object):
    def __init__(self , location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self , location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}
        return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        try:
            json.dump(self.db , open(self.location, "w+"))
            return True
        except:
            return False


fdb = FoobarDB("channels.db")
current_linking = None

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return
        global current_linking, fdb
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith("!link") and message.author.id in [826451713484783677, 160888334195884032]:
            if current_linking is None:
                current_linking = message.channel.id
            else:
                # current_linking = from channel (private)
                # message.channel.id = to channel (with people to talk to)
                fdb.db[str(current_linking)] = message.channel.id
                fdb.dumpdb()
                current_linking = None
        else:
            if str(message.channel.id) in fdb.db.keys():
                # me -> world
                channel = client.get_channel(int(fdb.db[str(message.channel.id)]))
                print(channel)
                try:
                    await channel.send(message.content)  # prints out the message
                except Exception:
                    print("Fucky wucky")

                try:  # tries to send the url of the file
                    await channel.send(message.attachments[0].url)
                except IndexError:  # if index error is received, that means the user entered a regular message
                    pass
            elif message.channel.id in fdb.db.values():
                # world -> me
                channel = client.get_channel(int(list(fdb.db.keys())[list(fdb.db.values()).index(message.channel.id)]))
                print(channel)
                try:
                    await channel.send('***{0.author}***\n'.format(message) + message.content)  # prints out the message
                except Exception:
                    print("Fucky wucky")

                try:  # tries to send the url of the file
                    await channel.send(message.attachments[0].url)
                except IndexError:  # if index error is received, that means the user entered a regular message
                    pass


client = MyClient()
client.run(config["discord"].get('token'))
