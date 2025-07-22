from locales import locales

def _(lang: str, key: str) -> str:
    return locales.get(lang, locales["en"]).get(key, key)
