# Alhaitham

#### _Read this in [other translations](translation/translations.md)._

<kbd>[<img title="Русский язык" alt="Русский язык" src="https://cdn.staticaly.com/gh/hjnilsson/country-flags/master/svg/ru.svg" width="22">](translation/README.ru.md)</kbd>
<kbd>[<img title="Українська" alt="Українська" src="https://cdn.staticaly.com/gh/hjnilsson/country-flags/master/svg/ua.svg" width="22">](translation/README.uk.md)</kbd>

> This is part of `Pudgeland 💖 Open Source` ecosystems

An unofficial **[The Dog API](https://thedogapi.com)** wrapper for Python

## 📦 Packages

### 🐍 PyPI

```sh
pip install alhaitham
```

## 🔎 Examples

```py
import alhaitham

client = alhaitham.Client()

for _ in range(5):
    print(client.images.search())
```
