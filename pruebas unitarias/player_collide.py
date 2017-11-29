def collide(xvel, yvel, choco, choco_final):
    onExitBlock = False
    right_jugador = 0
    left_bloque = 1
    left_jugador = 0
    right_bloque = 1
    bottom_jugador = 0
    top_bloque = 1
    top_jugador = 0
    bottom_bloque = 1
    for p in range(2):
        if choco:
            if choco_final:
					#se va al siguiente nivel
                onExitBlock = True
                return "paso nivel"
            if xvel > 0:
                right_jugador = left_bloque
					#print("collide right")
                return "choco contra bloque derecho"
            if xvel < 0:
                left_jugador = right_bloque
					#print("collide left")
                return "choco contra bloque izquierdo"
            if yvel > 0:
                bottom_jugador = top_bloque
                yvel = 0
                return "choco contra bloque de abajo"
            if yvel < 0:
                top_jugador = bottom_bloque
                yvel = 0
                return "choco contra bloque de arriba"
        else:
            return "no choco"
