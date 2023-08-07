""""""

import tighnari

client = tighnari.Client()

for _ in range(5):
    print(client.images.search())
