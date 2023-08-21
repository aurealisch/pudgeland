# Nahida

> Это часть `Pudgeland 💖 Open Source` экосистемы

Неофициальная [_Waifu.pics_](https://waifu.pics) API оболочка для Python

## 📦 Пакеты

### 🐍 PyPI

```sh
pip install nahida
```

## 🔎 Примеры

```py
import nahida

client = nahida.Client()

print(client.nsfw.search("neko"))

print(client.sfw.search("awoo"))
print(client.sfw.search("bite"))
```
