import nahida

client = nahida.Client()

print(client.nsfw.search('neko'))

print(client.sfw.search('awoo'))
print(client.sfw.search('bite'))
