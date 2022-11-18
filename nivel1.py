#!/usr/bin/python3

import pygame
import random

pygame.init()
# F UNCIONES ENCARGADAS DE CREAR LOS MUROS Y LA COMIDA

class Pacman(pygame.sprite.Sprite):
    """ Clase de pacman, encargada de crear el personaje de pacman
        Lee el teclado para poder mover el personaje a lo largo del mapa.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('pac.png').convert()
        self.image.set_colorkey(NEGRO)
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.bottom = 280
        self.speed_x = 10


#FUNCION PARA LEER EL TECLADO, LAS FECHAS
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.centerx  -= 2
            if event.key == pygame.K_RIGHT:
                self.rect.centerx  += 2
            if event.key == pygame.K_UP:
                self.rect.bottom -= 2
            if event.key == pygame.K_DOWN:
                self.rect.bottom += 2



class Fantasma1(pygame.sprite.Sprite):
    """ Clase de fantama1, encargada de crear un personaje de fantamas
        y genera su movimento aleatoriamente.
        fatasma color ROJO
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('fana.png').convert()
        self.image.set_colorkey(NEGRO)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 80
        self.speed_x = 0

    def handle_event(self, mov_fantasma1):
        if mov_fantasma1 == 0:
            self.rect.x += 1
        elif mov_fantasma1 == 1:
            self.rect.x -= 1
        elif mov_fantasma1 == 2:
            self.rect.y += 1
        else:
            self.rect.y -= 1


class Fantasma2(pygame.sprite.Sprite):
    """ Clase de fantama2, encargada de crear un personaje de fantamas
        y genera su movimento aleatoriamente.
        fatasma color AMARILLO
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('fantaa.png').convert()
        self.image.set_colorkey(NEGRO)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = 80
        self.speed_x = 0

    def handle_event(self,mov_fantasma2):
        if mov_fantasma2 == 0:
            self.rect.x += 1
        elif mov_fantasma2 == 1:
            self.rect.x -= 1
        elif mov_fantasma2 == 2:
            self.rect.y += 1
        else:
            self.rect.y -= 1


# cargarla como una variable
def dibuja_muro(superficie, rectangulo, muro_nuevo):
    pygame.draw.rect(superficie, BLUE, rectangulo)
    # superficie.blit(muro_nuevo,rectangulo)


def dibuja_comida(superficie, rectangulo):
    pygame.draw.rect(superficie, BLANCO, rectangulo, 20, 20)


def dibuja_food_special(superficie, rectangulo):
    imagen_food= pygame.image.load('food.png')
    food = pygame.transform.scale(imagen_food,(20,20))
    superficie.blit(food,rectangulo)

# FUNCION QUE LEE EL MAPA(VARIABLE = LISTA) Y FORMA LISTA DE MUROS Y COMIDA
def construir_mapa(mapa):
    muros=[]
    comida=[]
    food_special=[]
    contador_comida = 0
    x=0
    y=0
    # RECORRE LA LISTA MAPA
    for muro in mapa:
        for ladrillo in muro:
            # SI HAY UNA X ES UN MURO Y LO AGREGA A LA LISTA CON SUS COORDENADAS
            if ladrillo == "x":
                # coordernadas y el tamanno donde se ubicaran en el mapa
                muros.append(pygame.Rect(x, y, 20, 20))
                # se mueve a la siguiente columna
                x+= 20

            # SI ES UNA M ES COMIDA NORMAL
            elif ladrillo == "m":
                # coordernadas y el tamanno donde se ubicaran en el mapa
                comida.append(pygame.Rect(x+7, y+10, 7, 7))
                x += 20
                contador_comida += 1
            # SI ES UNA F ES COMIDA ESPECIAL
            elif ladrillo == "f":
                food_special.append(pygame.Rect(x, y, 10, 10))
                x += 20
                contador_comida += 1
            # SI NO ES NINGUN CARACTER SOLO PASA AL SIGUIENTE PIXEL
            else:
                x += 20
        # SE MUEVE DE FILA
        x = 0
        y += 20 # Va corriendo a lo largo de todas la comlumnas
    return muros,comida, contador_comida, food_special


# FUNCION PARA RECORRER LA LISTA DE MUROS
def recorre_lista_muros(superficie, muros, muro_nuevo):
    for m in muros:
        # LLAMA LA FUNCION PARA CREAR LOS MUROS
        dibuja_muro(superficie, m,muro_nuevo)

# FUNCION PARA RECORRER LA LISTA DE COMIDA
def recorre_lista_comida(superficie, comida):
    for m in comida:
        # LLAMA LA FUNCION PARA CREAR LA COMIDA
        dibuja_comida(superficie, m)

# FUNCION PARA RECORRER LA LISTA DE COMIDA
def recorre_lista_food_special(superficie, food_special):
    for m in food_special:
        # LLAMA LA FUNCION PARA CREAR eventLA FOOD SPECIAL
        dibuja_food_special(superficie, m)


def eliminar_comida(comida, contador_comida):
    for v_comida in list(comida):
        # ELIMINA DE LA LISTA DE COMIDA SI PACMAN TOCA LA COMIDA
        if pacman.rect.collidepoint(v_comida.centerx, v_comida.centery):
            comida.remove(v_comida)

            # SONIDI FOOD
            pygame.mixer.music.load('pacman_chomp.wav')
            pygame.mixer.music.play()
            # VA RESTANDO LA COMIDA
            contador_comida -= 1
    return contador_comida


def eliminar_food_especial(food_special, contador_comida):
    for v_food_special in list(food_special):
        # ELIMINA DE LA LISTA DE FOOD SPECIAL SI PACMAN TOCA LA COMIDA
        if pacman.rect.collidepoint(v_food_special.centerx, v_food_special.centery):
            food_special.remove(v_food_special)
            # VA RESTANDO LA COMIDA EN EL CONTADOR
            contador_comida -= 1
            # SONIDO ESPECIAL FOOD
            pygame.mixer.music.load('pacman_eatfruit.wav')
            pygame.mixer.music.play()
    return contador_comida

def variable_movimento_fantasma1(mov_fantasma1):
    mov_fantasma1 = random.randint(0,3)
    Fantasma1.handle_event(mov_fantasma1)
    print(' mov1 {}'.format(mov_fantasma1))
    return mov_fantasma1




def variable_movimento_fantasma2(mov_fantasma2):
    mov_pasado = mov_fantasma2
    mov_fantasma2 = random.randint(0,3)
    if mov_pasado != mov_fantasma2:
        Fantasma2.handle_event(mov_fantasma2)
        print(' mov2 {}'.format(mov_fantasma2))
    else:
        variable_movimento_fantasma2(mov_pasado)
    return mov_fantasma2


""" FUNCION ENCARGARDA PARA MOSTRAR LA PANTALLA DE GAME game_over
    HAY QUE PRESIONAR Q PARA SALIR Y RETORNA AL MENU DEL JUEGO"""
def perdida():
    perdio = True
    imagen_gm = pygame.image.load('game_over.png')
    game_over = pygame.transform.scale(imagen_gm,(400,300))
    pygame.mixer.music.load('pacman_death.wav')
    pygame.mixer.music.play(2)
    while perdio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q: # Q cierra el juego
                    pygame.quit()
                    quit()



        ventana_juego.fill(pygame.Color('black'))
        texto2 = fuente1.render("PRESIONE Q PARA SALIR",
        True, BLANCO)
        ventana_juego.blit(texto2, (200, 450))
        ventana_juego.blit(game_over, (120, 50))



        pygame.display.flip()
        pygame.display.update()


""" FUNCION ENCARGADA DE MOSTAR LA PANTALLA DE PAUSA
    SI PRESIONA P, SE CARGA LA PNATALLA
    PARA SALIR DEL JUEGO HAY QUE PRESIONAR Q
    Y PARA CONTINUAR JUGANDO HAY QUE PRESIONAR C"""
def pausa():
    pausado = True
    imagen_pausa = pygame.image.load('pausa.png')
    pausa = pygame.transform.scale(imagen_pausa,(400,400))


    pygame.mixer.music.load('pacman_intermission.wav')
    pygame.mixer.music.play(88888)
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # C para continuar
                    pausado = False
                elif event.key == pygame.K_q: # Q cierra el juego
                    pygame.quit()
                    quit()


        ventana_juego.fill(pygame.Color('black'))
        texto = fuente1.render("PRESIONE C PARA CONTINUAR O Q PARA TERMINAR",
        True, BLANCO)
        ventana_juego.blit(texto, (120, 400))
        ventana_juego.blit(pausa, (120, 0))



        pygame.display.flip()
        pygame.display.update()

def NIVEL2():
    pausado = True
    imagen_pausa = pygame.image.load('pausa.png')
    pausa = pygame.transform.scale(imagen_pausa,(400,400))
    pygame.mixer.music.load('pacman_beginning.wav')
    pygame.mixer.music.play(88888)
    flag =1
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pausado = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # C para continuar
                    main(contador_comida2, vidas_pacman, mov_fantasma1,
                     mov_fantasma2, muros2, food_special2, comida2)
                elif event.key == pygame.K_q: # Q cierra el juego
                    pygame.quit()
                    quit()

        ventana_juego.fill(pygame.Color('black'))
        ventana_juego.blit(pausa, (120, 0))
        texto = fuente1.render(
        "PRESIONE C PARA CONTINUAR AL SIGUIENTE NIVEL O Q PARA TERMINAR",
        True, BLANCO)
        ventana_juego.blit(texto, (80, 300))

        pygame.display.flip()
        pygame.display.update()



def main(contador_comida, vidas_pacman, mov_fantasma1,
        mov_fantasma2, muros, food_special, comida):
    game_over = False
    reloj = pygame.time.Clock() # variable de tiempo, ejecucion del programa


    while game_over == False:

        reloj.tick(FPS) # ajustando los FPS
        # EVENTO PARA QUE EL EXIT DE LA VENTANA FUNCIONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p :  #  si se preiosna p, abre pausa
                    pausa()

        pacman.handle_event(event)

        ventana_juego.fill(pygame.Color('black'))


        # imprimo las listas de sprite
        enemigo1.draw(ventana_juego)
        enemigo2.draw(ventana_juego)
        jugador.draw(ventana_juego)


        # funciones para crear el mapa
        recorre_lista_muros(ventana_juego, muros,muro_nuevo)
        recorre_lista_comida(ventana_juego, comida)
        recorre_lista_food_special(ventana_juego, food_special)
        #imprime el texto de la comida
        ventana_juego.blit(texto, (100, 560))

        # ELIMINA LA COMIDA CUNADO SE TOCAN
        contador_comida = eliminar_comida(comida,contador_comida)
        contador_comida = eliminar_food_especial(food_special,contador_comida)


        #IMPRIME EN PANTALLA EL CONTADOR DE COMIDA
        vidas = fuente1.render(str(vidas_pacman), True, BLANCO)
        puntos = fuente1.render(str(contador_comida), True, BLANCO)
        ventana_juego.blit(puntos, (400, 560))
        ventana_juego.blit(vidas, (500, 560))

        flag = 0
        if flag == 0:
            Fantasma1.handle_event(mov_fantasma1)
            Fantasma2.handle_event(mov_fantasma2)



        # creo la colisiones entre grupos de sprite y quita vida
        colision = pygame.sprite.spritecollide(pacman,enemigo1,False)
        if colision:
            if mov_fantasma1 == 0:
                Fantasma1.rect.x -= 2
                mov_fantasma1 = 1
                Fantasma1.handle_event(mov_fantasma1)
            elif mov_fantasma1 == 1:
                Fantasma1.rect.x += 2
                mov_fantasma1 = 0
                Fantasma1.handle_event(mov_fantasma1)
            elif mov_fantasma1 == 2:
                Fantasma1.rect.y -= 2
                mov_fantasma1 = 3
                Fantasma1.handle_event(mov_fantasma1)
            else:
                Fantasma1.rect.y += 2
                mov_fantasma1 = 2
                Fantasma1.handle_event(mov_fantasma1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.rect.centerx  += 2
                if event.key == pygame.K_RIGHT:
                    pacman.rect.centerx  -= 2
                if event.key == pygame.K_UP:
                    pacman.rect.bottom += 2
                if event.key == pygame.K_DOWN:
                    pacman.rect.bottom -= 2

            vidas_pacman -=1

            # Fantasma1.image = pygame.image.load('2.png').convert()
            # Fantasma1.image.set_colorkey(NEGRO)
            # Fantasma1.image = pygame.transform.scale(Fantasma1.image, (20, 20))


        colision = pygame.sprite.spritecollide(pacman,enemigo2,False)
        if colision:
            if mov_fantasma2 == 0:
                Fantasma2.rect.x -= 2
                mov_fantasma2 = 1
                Fantasma2.handle_event(mov_fantasma2)
            elif mov_fantasma2 == 1:
                Fantasma2.rect.x += 2
                mov_fantasma2 = 0
                Fantasma2.handle_event(mov_fantasma2)
            elif mov_fantasma2 == 2:
                Fantasma2.rect.y -= 2
                mov_fantasma2 = 3
                Fantasma2.handle_event(mov_fantasma2)
            else:
                Fantasma2.rect.y += 2
                mov_fantasma2 = 2
                Fantasma2.handle_event(mov_fantasma2)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.rect.centerx  += 2
                if event.key == pygame.K_RIGHT:
                    pacman.rect.centerx  -= 2
                if event.key == pygame.K_UP:
                    pacman.rect.bottom += 2
                if event.key == pygame.K_DOWN:
                    pacman.rect.bottom -= 2
            vidas_pacman -=1

            # Fantasma2.image = pygame.image.load('2.png').convert()
            # Fantasma2.image.set_colorkey(NEGRO)
            # Fantasma2.image = pygame.transform.scale(Fantasma2.image, (20, 20))

        #colision de pacman con el mapa
        for muro in muros:
            if pacman.rect.colliderect(muro):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacman.rect.centerx  += 2
                    if event.key == pygame.K_RIGHT:
                        pacman.rect.centerx  -= 2
                    if event.key == pygame.K_UP:
                        pacman.rect.bottom += 2
                    if event.key == pygame.K_DOWN:
                        pacman.rect.bottom -= 2

            # colosion de los fantasmas con el mapa
            elif Fantasma1.rect.colliderect(muro):
                if mov_fantasma1 == 0:
                    Fantasma1.rect.x -= 2
                elif mov_fantasma1 == 1:
                    Fantasma1.rect.x += 2
                elif mov_fantasma1 == 2:
                    Fantasma1.rect.y -= 2
                else:
                    Fantasma1.rect.y += 2
                mov_fantasma1 = variable_movimento_fantasma1(mov_fantasma1)


            elif Fantasma2.rect.colliderect(muro):
                if mov_fantasma2 == 0:
                    Fantasma2.rect.x -= 2
                elif mov_fantasma2 == 1:
                    Fantasma2.rect.x += 2
                elif mov_fantasma2 == 2:
                    Fantasma2.rect.y -= 2
                else:
                    Fantasma2.rect.y += 2
                mov_fantasma2 = variable_movimento_fantasma2(mov_fantasma2)


        #termina cuando la comida es 0
        if contador_comida == 0:
            NIVEL2()

        if vidas_pacman == 0:
            perdida()

        jugador.update()
        enemigo1.update()
        enemigo2.update()
        pygame.display.flip()
        pygame.display.update()

    pygame.quit ()

# COLORES
VERDE = (0, 255, 0)
BLANCO= (255, 255, 255)
RED=(255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
NEGRO = (0, 0, 0)




pygame.mixer.music.load('pacman_beginning.wav')
pygame.mixer.music.play(8888888)

# VARIABLES
ancho_ventana = 600
alto_ventana = 600
ventana_juego = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("PACMAN")
clock = pygame.time.Clock()
vidas_pacman = 2

jugador = pygame.sprite.Group()
enemigo1 = pygame.sprite.Group()
enemigo2 = pygame.sprite.Group()



# genero el primer movimeinto
mov_fantasma1 = 0
mov_fantasma2 = 1


#  llamo los objetos de los personajes
pacman = Pacman()
Fantasma1 = Fantasma1()
Fantasma2=Fantasma2()


#  los agrego a un grupo de sprite
enemigo1.add(Fantasma1)
enemigo2.add(Fantasma2)
jugador.add(pacman)




FPS = 60
fuente1 = pygame.font.SysFont("segoe print",20)
texto = fuente1.render("COMIDA DISPONIBLE", True, BLANCO)
imagen_muro = pygame.image.load('muro_1.png')
muro_nuevo = pygame.transform.scale(imagen_muro,(20,20))

# MAPAS
mapa = [

                "                              ",
                "                              ",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "x                            x",
                # "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x                            x",
                # "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x                            x",
                # "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x                            x",
                # "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                "x xxxxxxxxxmxxxxxxxxxx xxxxx x",
                # "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "x                            x",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]

MAPA2 =[
                "                              ",
                "                              ",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "xmmmmfmmmmmmxmmmmxmmmmmmmmmfmx",
                "xmxxxxxxxmxmxmxxmxmxmxxxxxxxmx",
                "xmmmmmmmmmxmxmxxmxmxmmmmmmmmmx",
                "xmxxxxxxxmxmxmxxmxmxmxxxxxxxmx",
                "xmxxxxxxxmxmmmmmmmmxmxxxxxxxmx",
                "xmxxxxxxxmxmxmxxmxmxmxxxxxxxmx",
                "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                "xmxxxxxxxxxmxxxxxxxmxxxxxxxxmx",
                "xmxxxxxxxxxmxxxxxxxmxxxxxxxxmx",
                "xmxxxxxxxxxmxxxxxxxmxxxxxxxxmx",
                "xmmmmxmmmmmmmmfmmmmmmmmmxmmmmx",
                "xxxxmxmxxmxxxxxxxxxxmxxmxmxxxx",
                "xxxxmxmxxmxxxxxxxxxxmxxmxmxxxx",
                "xxxxmxmxxmxxxxxxxxxxmxxmxmxxxx",
                "xxxxmxmxxmxxxxxxxxxxmxxmxmxxxx",
                "xmmmmmmxxmxxxxxxxxxxmxxmmmmmmx",
                "xmxxxxxxxmmmmmmmmmmmmxxxxxxxmx",
                "xmmmfmmmmmxxxxxxxxxxmmmfmmmmmx",
                "xmxxxxxxxmxxxxxxxxxxmxxxxxxxmx",
                "xmxxxxxxxmxxxxxxxxxxmxxxxxxxmx",
                "xmxxxxxxxmxxxxxxxxxxmxxxxxxxmx",
                "xmmmmmmmmmxxxxxxxxxxmmmmmmmmmx",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

]
# 600/20= columnas
# 600/20= filas

# COLORES
VERDE = (0, 255, 0)
BLANCO= (255, 255, 255)
RED=(255, 0, 0)
BLUE = (0, 0, 255)
flag_niveles = 0

# main
# llamar la funcion de construit mapa primero para que forme la listas
muros, comida, contador_comida, food_special = construir_mapa(mapa)
muros2, comida2, contador_comida2, food_special2 = construir_mapa(MAPA2)
main(contador_comida, vidas_pacman, mov_fantasma1,
    mov_fantasma2, muros, food_special,comida)

# main(contador_comida2, vidas_pacman, mov_fantasma1,
#  mov_fantasma2, muros2, food_special2, comida2)
