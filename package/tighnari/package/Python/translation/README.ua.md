# Tighnari

> Це частина `Pudgeland 💖 Open Source` екосистеми

Неофіційна **[The Cat API](https://thecatapi.com)** оболонка для Python

## 📦 Пакети

### 🐍 PyPI

```sh
pip install tighnari
```

## 🔎 Приклади

```py
import tighnari

client = tighnari.Client()

for _ in range(5):
    print(client.images.search())
```
