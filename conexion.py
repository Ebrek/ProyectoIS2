import sqlite3
conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row

class Conexion1(): # usa sqlite

    def listar_niveles(self):
        c = conn.cursor()
        c.execute("""SELECT id, title, bg_music, bg_image FROM Configurador_nivel""")
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
        c.close() 
        return result
        
    def listar_escenarios(self, nivel_id):
        c = conn.cursor()
        c.execute("""SELECT id, title, mapa, orden FROM Configurador_escenario
            WHERE nivel_id = ? 
            ORDER BY orden ASC""", (nivel_id,) )
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
        c.close() 
        return result

    def listar_historia(self, escenario_id, modalidad):
        c = conn.cursor()
        c.execute("""SELECT id, title, imagen, orden, suceso FROM Configurador_historia
            WHERE escenario_id = ? AND suceso = ?
            ORDER BY orden ASC""", (escenario_id, modalidad,) )
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
        c.close()
        return result

    def obtener_ajustesgeneral(self):
        c = conn.cursor()
        c.execute("""SELECT id, title, froggy_health, 
            spider_health, spider_speed_x, spider_speed_y,
            mosquito_health, mosquito_speed_x, mosquito_speed_y FROM Configurador_ajustesgeneral
            LIMIT 1 """)
        row = c.fetchone()
        c.close() 
        return row

    def obtener_puntaje(self, nivel_id):
        c = conn.cursor()
        c.execute("""SELECT id, player, puntaje FROM Configurador_puntaje
            WHERE nivel_id = ? 
            ORDER BY puntaje DESC""", (nivel_id,) )
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
        c.close() 
        return result



######################################################################################
import requests
import json
URL = 'http://localhost:8000/'


class Conexion(): # django con postgres


    def listar_niveles(self):
        REL = 'niveles/'
        response = requests.get(URL + REL)
        return response.json()
    def obtener_nivel(self, nivel_id):
        REL = 'niveles/' + str(nivel_id)
        response = requests.get(URL + REL)
        return response.json()
        
    def listar_escenarios(self, nivel_id):
        REL = 'escenarios/?nivel_id=' + str(nivel_id)
        response = requests.get(URL + REL).json()
        #ASC orden
        #sorted_obj = dict(response.json()) 
        sorted_obj = sorted(response, key=lambda x : int(x['orden']), reverse=False)

        return sorted_obj

    def listar_historia(self, escenario_id, modalidad):
        REL = 'historias/?escenario_id=' + str(escenario_id) + '&suceso=' + modalidad
        response = requests.get(URL + REL).json()
        #ASC orden
        #sorted_obj = dict(response.json()) 
        sorted_obj = sorted(response, key=lambda x : int(x['orden']), reverse=False)

        return sorted_obj

    def obtener_ajustesgeneral(self):
        REL = 'ajustesgenerales/'
        response = requests.get(URL + REL)
        return response.json()[0]

    def obtener_puntaje(self, nivel_id):
        REL = 'puntajes/?nivel_id' + str(nivel_id)
        response = requests.get(URL + REL).json()
        #ASC puntaje

        sorted_obj = sorted(response, key=lambda x : int(x['puntaje']), reverse=True)

        return sorted_obj

