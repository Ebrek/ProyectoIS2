import sys
import sqlite3
conn = sqlite3.connect('db.sqlite3')


class Conexion():

    def listar_niveles(self):
        c = conn.cursor()
        c.execute("""SELECT id, title, bg_music, bg_image FROM Configurador_nivel""")
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
            print(row)
        c.close() 
        return result
        
    def listar_escenarios(self, nivel_id):
        c = conn.cursor()
        c.execute("""SELECT id, title, mapa, order FROM Configurador_escenario 
            WHERE nivel_id = (?) """, (nivel_id,) )
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
            print(row)
        c.close() 
        return result

    def obtener_ajustesgeneral(self):
        c = conn.cursor()
        c.execute("""SELECT id, title, froggy_health, 
            spider_health, spider_speed_x, spider_speed_y,
            mosquito_health, mosquito_speed_x, mosquito_speed_y FROM Configurador_ajustesgeneral
            LIMIT 1 """)
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append(row)
            print(row)
        c.close() 
        return result

preuba = Conexion()
preuba.listar_niveles()
preuba.obtener_ajustesgeneral()