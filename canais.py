import json
from canal import Canal

class Canais:
    canais = []
    def getCanais(self):
        canais = []
        data = json.loads(open('canais.json').read())
        for c in data['canais']:
            canal = Canal()
            canal.numero = c['numero']
            canal.canal = c['canal']
            canais.append(canal)

        return canais
