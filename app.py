from flask import Flask
from flask import request
from crawler import CoronaScraper

app = Flask(__name__)

c = CoronaScraper()

@app.route('/')
def home():
    return {"details" : 'GET auf /endpoints um alle verfügbaren Endpunkte aufzulisten'}

@app.route("/endpoints")
def endpoints():
    return {
        "details" : "Hier ist eine Liste der verfügbaren Endpunkte",
        "list" : [
            {
                "url" : "/endpoints",
                "details" : "Listet alle verfügbaren Endpunkte auf",
                "params" : {}
            },
            {
                "url" : "/overview",
                "details" : "Gibt Daten zu Deutschland",
                "params" : {}
            },
            {
                "url" : "/details",
                "details" : "Gibt Daten zu gewählten Landkreis",
                "params" : {"kreis" : "id of landkreis"}
            },
            {
                "url" : "/kreise",
                "details" : "Listet alle verfügbaren Landkreise",
                "params" : {}
            }
        ]
    }

#@app.route("/overview")
def overview():
    death = 0
    regen = 0
    infected = 0
    active = 0
    for kreis in c.getKreise():
        stats = c.getStats(kreis)
        death += stats["dead"]
        regen += stats["recovered"]
        infected += stats["infected"]
        active += stats["active"]
    return {
        "dead" : death,
        "recovered" : regen,
        "infected" : infected,
        "active" : active
    }

@app.route("/details")
def details():
    kreis = request.args.get("kreis")
    try:
        c.updateMaybe()
        return c.getStats(kreis)
    except:
        return "Kreis nicht gefunden", 404


@app.route("/kreise")
def kreise():
    c.updateMaybe()
    return {"kreise" : c.getKreise()}

if __name__ == '__main__':
    app.run()
