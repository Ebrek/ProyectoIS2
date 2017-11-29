import unittest
from player_collide import collide



class TestCalculadora(unittest.TestCase):

    
    def setUp(self): 
        print("Se inicia el test")
        

        
    def tearDown(self): 
        print("Se termina el test")

    def test_collide_choco_falso(self):
        
        xvel = 1
        yvel = 1
        choco = False
        choco_final = True
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "no choco", 'collide_choco_falso incorrecta')

    def test_collide_choco_final(self):
        
        xvel = 1
        yvel = 1
        choco = True
        choco_final = True
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "paso nivel", 'collide_choco_final incorrecta')


    def test_collide_choco_derecha(self):
        
        xvel = 1
        yvel = 0
        choco = True
        choco_final = False
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "choco contra bloque derecho", 'collide_choco_derecha incorrecta')

    def test_collide_choco_izquierda(self):
        
        xvel = -1
        yvel = 0
        choco = True
        choco_final = False
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "choco contra bloque izquierdo", 'collide_choco_izquierda incorrecta')

    def test_collide_choco_abajo(self):
        
        xvel = 0
        yvel = 1
        choco = True
        choco_final = False
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "choco contra bloque de abajo", 'collide_choco_abajo incorrecta')

    def test_collide_choco_arriba(self):
        
        xvel = 0
        yvel = -1
        choco = True
        choco_final = False
        resultado = collide(xvel, yvel, choco, choco_final)
        self.assertEqual(resultado, "choco contra bloque de arriba", 'collide_choco_arriba incorrecta')

