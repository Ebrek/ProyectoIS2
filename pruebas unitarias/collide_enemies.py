def collide_enemies( vidas_restantes):
    gravedad = 0
    sigue_vivo = True
    agarrado = True
    contador_sin_perder_vida = updates_sin_perder_vida = 20
    enemy_get = 5
    for e in range(2):
        if agarrado == False and isinstance(e, EnemyMosquito) and  forma[0] != 0 and espera == 15:
            agarrado = agarrarObjeto(e)
            if agarrado == True:
		# Se remueve el mosquito para que paresca que es comido y se agrega a enemy_get
                enemy_get = e
                enemies.remove(e)
                entities.remove(e)
                self.espera = 0
		# este es para que el enemigo tragado no le haga perder vida
        if e == enemy_get:
            pass
            # aca es para todos los demas enemigos
        elif True :
            if contador_sin_perder_vida == updates_sin_perder_vida:
                #perder_vida(datos)
                if vidas_restantes == 0:
                    sigue_vivo = False
                    gravedad ==9.3
                contador_sin_perder_vida = 0
                return sigue_vivo
            else:
                contador_sin_perder_vida = contador_sin_perder_vida + 1
    return sigue_vivo
