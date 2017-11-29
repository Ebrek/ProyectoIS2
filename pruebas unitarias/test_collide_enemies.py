import unittest
from collide_enemies import collide_enemies



class TestCalculadora(unittest.TestCase):

    
    def setUp(self): 
        print("Se inicia el test")
        

        
    def tearDown(self): 
        print("Se termina el test")

    def test_collide_enemies(self):
        
        enemy_get = None
        vidas_restantes = 0
        resultado = collide_enemies(vidas_restantes)
        
        self.assertEqual(resultado, False, 'Operacion incorrecta')

