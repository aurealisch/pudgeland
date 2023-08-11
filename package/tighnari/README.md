# Tighnari

#### _Read this in [other translations](translation/translations.md)._

<kbd>[<img title="Русский язык" alt="Русский язык" src="https://cdn.staticaly.com/gh/hjnilsson/country-flags/master/svg/ru.svg" width="22">](translation/README.ru.md)</kbd>
<kbd>[<img title="Українська" alt="Українська" src="https://cdn.staticaly.com/gh/hjnilsson/country-flags/master/svg/ua.svg" width="22">](translation/README.uk.md)</kbd>

> This is part of `Pudgeland 💖 Open Source` ecosystems

An unofficial **[The Cat API](https://thecatapi.com)** wrapper for Python

## 📦 Packages

### 🐍 PyPI

```sh
pip install tighnari
```

## 🔎 Examples

```py
import tighnari

client = tighnari.Client()

for _ in range(5):
    print(client.images.search())
```
