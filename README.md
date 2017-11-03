instalar: pygame, Pillow, numpy

Windows
py -m pip install --upgrade pip
py -m pip install pygame --user
py -m pip install Pillow --user
py -m pip install numpy --user

----------------------------------
aprobado -> queda esta good
revisado, sujeto a cambios -> se reviso pero falta unos cambios pequeños
no aprobado -> para rehacer
abandonado -> ya no es necesario hacerlo

----------------------------------
Entregable 3->4

Angel Wong (Jugabilidad y tester)
->30/09/17: Encargate de hacer el diseño del jefe final, solo vamos a tener un jefe; también enfocate en su escenario
<-03/10/17: Esquema de acciones y sprites posibles del Jefe Final (70% sujeto a modificacion).
<-15/10/17: Esquema de enemigos subordinados, sprites, mecanicas (100% sin revision)
<-28/10/17: Escenarios con decoraciones, imagenes y sonidos (45%)

Franco Casanova
->25/09/17: Haz el caso de uso Sacar lengua; la expansión, contracción de esta y reaccion con enemigos
->04/10/17: Termina de una vez la funcionalidad de sacar la lengua (mira el caso de uso). Además haz el caso de uso mostrar pantalla de inicio
<-30/10/17: Caso de uso sacar la lengua y merge con caso de uso escupir (100%, aprobado)

Aarón Agüero
->30/09/17: Programa la animación del movimiento de la rana (incluye saltos), es decir al moverse simula que camina/salta
->04/10/17: Termina la animación y haz el caso de uso escupir.
->23/10/17: Deja de hacer lo que estés haciendo completa el caso de uso Mostrar pantalla de inicio
<-30/10/17: Caso de uso Mostrar pantalla de inicio (100% sujeto a cambios, una imagen de fondo)

<-30/10/17: 
Joan Pinto
->30/09/17: busca sprites para ambientar el juego: bloques de pasto, bosques de plataforma, bloques de salida, entre otros. Estos deben tener la ambientación de jungla o tipo mario bross.
<-03/10/17: comenta de avance, pero no presentó
->04/10/17: Haz el caso de uso coger ítems (solo de puntuación y vida; además de una barra del tablero de puntuaciones del caso de uso mostrar escenario)
<-16/10/17: Spites (excelentisimos) de items de puntuación, items de hailidades, bloques de ambiente/escenario (100% aprobado)
->23/10/17: Haz el diagrama de robustez para el caso de uso Gestionar configuración, haz el diagrama de despliegue, haz el Modelo de dominio acutalizado, revisa el BurndDown Chart
<-30/10/17: Diagrama de despliegue (100%, aprobado -vistarapida, quintana), robustez (gestionar configuración) (100% sin revision), modelo de dominio actualizado (100% sin revision)

Leo Wong (Líder)
->30/09/17: termina la modificacion de la documentación: modelo de dominio, diagrama de casos de uso (con especificaciones), diagrama de robustez, gestión de casos de uso/burndownchart
<-03/10/17: Modelo de dominio (100% revisado, sujeto a cambios), diagrama de casos de uso (100% revisado, sujeto a cambios) y sus especificaciones (100% revisado, sujeto a cambios). Reestructuración del alcance del proyecto.
->04/10/17: Terminar la documentación. Hacer el caso de uso ser observado por los enemigos (solo subordinados).
<-08/10/17: Cambios pequeños en Modelo de dominio, diagrama de casos de uso y sus especificaciones
<-15/10/17: Diagrama de robustez (100% sin revision), avances en gestión de casos de uso/burndownchart (20%)
<-21/10/17: Caso de uso Ser observado (100%, aprobado), avances en gestión de casos de uso/burndownchart (75%)
<-30/10/17: Caso de uso escupir (100%, aprobado)

