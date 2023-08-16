import collei

client = collei.Client()

for _ in range(5):
  print(client.images.search())
