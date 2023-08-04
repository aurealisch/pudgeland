# Tighnari

> Это часть `Pudgeland 💖 Open Source` экосистемы

Неофициальная **[The Cat API](https://thecatapi.com)** оболочка для Python

## 📦 Пакеты

### 🐍 PyPI

```sh
pip install tighnari
```

## 🔎 Примеры

```py
import tighnari

client = tighnari.Client()

for _ in range(5):
    print(client.images.search())
```
