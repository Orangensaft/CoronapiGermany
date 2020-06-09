import bs4
import requests
import time


class CoronaScraper:
    def __init__(self):
        self._init()

    def _init(self):
        self.soup = bs4.BeautifulSoup(requests.get("https://www.coronazaehler.de").content)
        self.kreise = [k.attrs["id"] for k in self.soup.select("td.text-left")]
        self.anzahl = len(self.kreise)
        self.lastUpdate = time.time()

    def updateMaybe(self):
        if time.time() - self.lastUpdate >= 60 * 60: #60 mins
            print("Cooking new soup")
            self._init()
            print("New soup there")

    def getKreise(self) -> [str]:
        return self.kreise

    def getAnzahl(self) -> int:
        return self.anzahl

    def getStats(self, kreis: str):
        if not (kreis in self.kreise):
            raise Exception("Unbekannter Kreis")
        fields = ["I100K", "dead", "infected", "recovered"]
        out = {}
        for field in fields:
            selected = self.soup.select("td#"+field+kreis)
            if len(selected)==0:
                raise Exception("Kreis nicht gelistet!")
            text = selected[0].text.replace(".","").replace(",",".")
            value = float(text) if field == "I100K" else int(text)
            out[field] = value
        out["active"] = max(out["infected"] - out["recovered"] - out["dead"],0)
        return out
