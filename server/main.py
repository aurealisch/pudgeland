import bottle
import env as environment

DISCORD = environment.get('DISCORD')
VK = environment.get('VK')

bottle.route('/discord')(lambda: bottle.redirect(DISCORD))
bottle.route('/vk')(lambda: bottle.redirect(VK))

HOST = environment.get('HOST')
PORT = environment.get('PORT')

bottle.run(host=HOST, port=PORT)
