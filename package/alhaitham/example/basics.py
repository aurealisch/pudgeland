""""""

import alhaitham

client = alhaitham.Client()

for _ in range(5):
    print(client.images.search())
