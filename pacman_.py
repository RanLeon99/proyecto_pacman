#!/usr/bin/python3

import pygame
import random

pygame.init()


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # se cargan todas las imagenes del movimeinto
        self.images_pacman = [
            pygame.image.load('imagenes/1.png').convert(),
            pygame.image.load('imagenes/2.png').convert(),
            pygame.image.load('imagenes/3.png').convert(),
            pygame.image.load('imagenes/4.png').convert(),
        ]

        for i in range(len(self.images_pacman)):
            self.images_pacman[i].set_colorkey(NEGRO)
            self.images_pacman[i] = pygame.transform.scale(self.images_pacman[i], (15, 15))

        self.image_index = 0
        self.image = self.images_pacman[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.bottom = 280
        self.speed = 2
        self.animation_counter = 0

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.x -= self.speed
                self.image = pygame.transform.rotate(self.images_pacman[self.animation_counter], 180)
                if self.animation_counter == 3:
                    self.animation_counter = 0
                else:
                    self.animation_counter += 1
            elif event.key == pygame.K_RIGHT:
                self.rect.x += self.speed
                self.image = pygame.transform.rotate(self.images_pacman[self.animation_counter], 0)
                if self.animation_counter == 3:
                    self.animation_counter = 0
                else:
                    self.animation_counter += 1
            elif event.key == pygame.K_UP:
                self.rect.y -= self.speed
                self.image = pygame.transform.rotate(self.images_pacman[self.animation_counter], 90)
                if self.animation_counter == 3:
                    self.animation_counter = 0
                else:
                    self.animation_counter += 1
            elif event.key == pygame.K_DOWN:
                self.rect.y += self.speed
                self.image = pygame.transform.rotate(self.images_pacman[self.animation_counter], -90)
                if self.animation_counter == 3:
                    self.animation_counter = 0
                else:
                    self.animation_counter += 1
            
class Fantasma(pygame.sprite.Sprite):
    """ Clase de fantama1, encargada de crear un personaje de fantamas
        y genera su movimento aleatoriamente.
        fatasma color ROJO
    """
    def __init__(self, image_paths,x,y):
        """ CONTRUCTOR DEL FANTASMA ROJO
            CARGA LA IMAGEN Y LE DA LA POSICION INICIAL
        """
        super().__init__()
        self.images_fantasma_rojo_right = self.load_and_scale_images(image_paths["right"])
        self.images_fantasma_rojo_left = self.load_and_scale_images(image_paths["left"])
        self.images_fantasma_rojo_up = self.load_and_scale_images(image_paths["up"])
        self.images_fantasma_rojo_down = self.load_and_scale_images(image_paths["down"])

        self.image_directions = {
            "right": self.images_fantasma_rojo_right,
            "left": self.images_fantasma_rojo_left,
            "up": self.images_fantasma_rojo_up,
            "down": self.images_fantasma_rojo_down,
        }

        self.image_index = 0
        self.image = self.images_fantasma_rojo_right[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.animation_counter = 0


    def load_and_scale_images(self, image_paths):
        """ Carga y escala las imágenes """
        images = [pygame.image.load(path).convert() for path in image_paths]
        for i in range(len(images)):
            images[i].set_colorkey(NEGRO)
            images[i] = pygame.transform.scale(images[i], (15, 15))
        return images


        

    def handle_event(self,movimiento):
        """ FUNCION ENCARGADA PARA GENERAR EL MOVIMIENTO
            DEL FANTASMA POR TODO EL MAPA

            INT = mov_fantasma
            0 = MOV DERECHA
            1 = MOV IZQUIERDA
            2 = MOV ARRIBA
            3 = MOV ABAJO
        """

        if movimiento == 0:
            self.rect.x += 1
            self.image = pygame.transform.rotate(self.images_fantasma_rojo_right[self.animation_counter], 0)
            if self.animation_counter == 1:
                self.animation_counter = 0
            else:
                self.animation_counter += 1

        elif movimiento == 1:
            self.rect.x -= 1
            self.image = pygame.transform.rotate(self.images_fantasma_rojo_left[self.animation_counter], 0)
            if self.animation_counter == 1:
                self.animation_counter = 0
            else:
                self.animation_counter += 1
        elif movimiento == 2:
            self.rect.y += 1
            self.image = pygame.transform.rotate(self.images_fantasma_rojo_down[self.animation_counter], 0)
            if self.animation_counter == 1:
                self.animation_counter = 0
            else:
                self.animation_counter += 1
        else:
            self.rect.y -= 1
            self.image = pygame.transform.rotate(self.images_fantasma_rojo_up[self.animation_counter],0)
            if self.animation_counter == 1:
                self.animation_counter = 0
            else:
                self.animation_counter += 1


def dibuja_muro(superficie, rectangulo, muro_nuevo):
    """ FUNCION ENCARGADA DE IMPRIMIR CADA IMAGEN DE LOS MUROS
    SUPERFICIE = VENTANA DONDE LO IMPRIME
    RECTACGULO = POSICION EN LA VENTANA (X,Y)
    MURO_NUEVO = LA IMAGEN QUE VAMOS A COLOCAR
    """
    superficie.blit(muro_nuevo, rectangulo)


def dibuja_comida(superficie, rectangulo):
    """ FUNCION ENCARGADA DE IMPRIMIR LA COMIDA (CIRCULOS)
    SUPERFICIE = VENTANA DONDE LO IMPRIME
    RECTACGULO = POSICION EN LA VENTANA (X,Y)
    """
    pygame.draw.rect(superficie, BLANCO, rectangulo, 20, 20)


def dibuja_food_special(superficie, rectangulo):
    """ FUNCION ENCARGADA DE IMPRIMIR LA COMIDA ESPECIAL, IMAGEN QUE CARGAREMOS
    SUPERFICIE = VENTANA DONDE LO IMPRIME
    RECTACGULO = POSICION EN LA VENTANA (X,Y)
    """
    imagen_food = pygame.image.load('imagenes/food.png')
    food = pygame.transform.scale(imagen_food, (20, 20))
    superficie.blit(food, rectangulo)


def construir_mapa(mapa):
    """ FUNCION ENCARGADA DE RECORRER LA LISTA MAPA
        PARA CREAR LISTAS DE CADA CARACTER QUE SE ENCUENTRA EL EL MAPA
        X = MURO
        M = COMIDA NORMAL
        F = COMIDA ESPECIAL

        ENTRADA:
        LIST = MAPA

        SALIDA:
        LISTA = MUROS, COMIDA, FOOD_SPECIAL

        INT = CONTADOR DE COMIDA
    """
    muros = []
    comida = []
    food_special = []
    contador_comida = 0
    x = 0
    y = 0
    # RECORRE LA LISTA MAPA
    for muro in mapa:
        for ladrillo in muro:
            # SI HAY UNA X ES UN MURO Y LO AGREGA A LA LISTA
            # CON SUS COORDENADAS
            if ladrillo == "x":
                # coordernadas y el tamanno donde se ubicaran en el mapa
                muros.append(pygame.Rect(x, y, 20, 20))
                # se mueve a la siguiente columna
                x += 20

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
        y += 20  # Va corriendo a lo largo de todas la comlumnas
    return muros, comida, contador_comida, food_special


def recorre_lista_muros(superficie, muros, muro_nuevo):
    """ FUNCION QUE RECORRE LA LISTA MUROS, QUE CONTIENE LAS COORDENADA DONDE
        SE COLOCARAN LOS MUROS
    """
    for m in muros:
        # LLAMA LA FUNCION PARA CREAR LOS MUROS
        dibuja_muro(superficie, m, muro_nuevo)


def recorre_lista_comida(superficie, comida):
    """ FUNCION QUE RECORRE LA LISTA COMIDA, QUE CONTIENE LAS COORDENADA DONDE
        SE COLOCARA LA COMIDA
    """
    for m in comida:
        # LLAMA LA FUNCION PARA CREAR LA COMIDA
        dibuja_comida(superficie, m)


def recorre_lista_food_special(superficie, food_special):
    """ FUNCION QUE RECORRE LA LISTA COMIDA ESPECIAL
        CONTIENE LAS COORDENADA DONDE SE COLOCARA
    """
    for m in food_special:
        # LLAMA LA FUNCION PARA CREAR eventLA FOOD SPECIAL
        dibuja_food_special(superficie, m)


def eliminar_comida(comida, contador_comida):
    """ FUNCION ENCARAGDA DE VERIFICAR SI PACMAN CHOCA CON UNA COMIDA
        PARA QUE ESTA SEA ELIMINADA
        Y ACTUALIZA EL CONTADOR DE COMIDA

        SALIDA = INT(CONTADOR YA ACTUALIZADO)
    """
    for v_comida in list(comida):
        # ELIMINA DE LA LISTA DE COMIDA SI PACMAN TOCA LA COMIDA
        if pacman.rect.collidepoint(v_comida.centerx, v_comida.centery):
            comida.remove(v_comida)
            # SOLINO FOOD
            pygame.mixer.music.load('sonidos/pacman_chomp.wav')
            pygame.mixer.music.play()
            # VA RESTANDO LA COMIDA
            contador_comida -= 1
    return contador_comida


def eliminar_food_especial(food_special, contador_comida,
                           vidas_pacman, flag_mood_muerte,
                           contador_modo_dead):
    """ FUNCION ENCARAGDA DE VERIFICAR SI PACMAN CHOCA CON UNA COMIDA ESPECIAL
        PARA QUE ESTA SEA ELIMINADA
        Y ACTUALIZA EL CONTADOR DE COMIDA

        CUANDO COME ESTE CARACTE AUMENTA LA VIDA DE PACMAN
        EL MAXIMO DE LA VIDA ES 5


        SALIDA = INT(CONTADOR YA ACTUALIZADO)
                 INT ( VIDA DE PACMAN )
    """
    for v_food_special in list(food_special):
        # ELIMINA DE LA LISTA DE FOOD SPECIAL SI PACMAN TOCA LA COMIDA
        if pacman.rect.collidepoint(v_food_special.centerx,
                                    v_food_special.centery):
            food_special.remove(v_food_special)
            flag_mood_muerte = True
            contador_modo_dead = 0
            # VA RESTANDO LA COMIDA EN EL CONTADOR
            contador_comida -= 1
            # SONIDO ESPECIAL FOOD
            pygame.mixer.music.load('sonidos/pacman_eatfruit.wav')
            pygame.mixer.music.play()
            if vidas_pacman == 5:  # MAXIMO DE VIDAS = 5
                pass
            else:
                vidas_pacman += 1
    return contador_comida, vidas_pacman, flag_mood_muerte, contador_modo_dead


def variable_movimento_fantasma1(mov_fantasma1):
    """ FUNCION QUE GENERAR EL NUMERO PARA QUE PACMAN SE MUEVA

        ENTRADA = VALOR ACTUAL DEL MOVIMIENTO DE PACMAN (INT)
        SE GUARDA ESTA ENTRADA PARA QUE EL VALOR NUEVO NO SEA IGUAL A ESTE
        EN CASO QUE SEA IGUAL GENERA UNA RECURSIVIDAD
        HASTA QUE EL DATO GENERADO
        SEA DIFERENTE A LA ENTRADA

        SALIDA = VALOR NUEVO DE MOVIMIENTO (INT)
    """
    mov_pasado = mov_fantasma1
    mov_fantasma1 = random.randint(0, 3)
    if mov_pasado != mov_fantasma1:
        Fantasma1.handle_event(mov_fantasma1)
        
    else:
        variable_movimento_fantasma1(mov_pasado)
    return mov_fantasma1


def variable_movimento_fantasma2(mov_fantasma2):
    """ FUNCION QUE GENERAR EL NUMERO PARA QUE PACMAN SE MUEVA

        ENTRADA = VALOR ACTUAL DEL MOVIMIENTO DE PACMAN (INT)
        SE GUARDA ESTA ENTRADA PARA QUE EL VALOR NUEVO NO SEA IGUAL A ESTE
        EN CASO QUE SEA IGUAL GENERA UNA
        RECURSIVIDAD HASTA QUE EL DATO GENERADO
        SEA DIFERENTE A LA ENTRADA
        SALIDA = VALOR NUEVO DE MOVIMIENTO (INT)
    """
    mov_pasado = mov_fantasma2
    mov_fantasma2 = random.randint(0, 3)
    if mov_pasado != mov_fantasma2:
        Fantasma2.handle_event(mov_fantasma2)
        
    else:
        variable_movimento_fantasma2(mov_pasado)
    return mov_fantasma2


def variable_movimento_fantasma3(mov_fantasma3):
    """ FUNCION QUE GENERAR EL NUMERO PARA QUE PACMAN SE MUEVA

        ENTRADA = VALOR ACTUAL DEL MOVIMIENTO DE PACMAN (INT)
        SE GUARDA ESTA ENTRADA PARA QUE EL VALOR NUEVO NO SEA IGUAL A ESTE
        EN CASO QUE SEA IGUAL GENERA UNA
        RECURSIVIDAD HASTA QUE EL DATO GENERADO
        SEA DIFERENTE A LA ENTRADA

        SALIDA = VALOR NUEVO DE MOVIMIENTO (INT)
    """
    mov_pasado = mov_fantasma3
    mov_fantasma3 = random.randint(0, 3)
    if mov_pasado != mov_fantasma3:
        Fantasma3.handle_event(mov_fantasma3)
        
    else:
        variable_movimento_fantasma3(mov_pasado)
    return mov_fantasma3



def perdida():
    """ FUNCION ENCARGARDA PARA MOSTRAR LA PANTALLA DE GAME game_over
        HAY QUE PRESIONAR Q PARA SALIR Y RETORNA AL MENU DEL JUEGO"""
    perdio = True
    imagen_gm = pygame.image.load('imagenes/game_over.png')
    game_over = pygame.transform.scale(imagen_gm, (400, 300))
    pygame.mixer.music.load('sonidos/pacman_death.wav')
    pygame.mixer.music.play(2)
    while perdio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Q cierra el juego
                    pygame.quit()
                    quit()

        ventana_juego.fill(pygame.Color('black'))
        texto2 = fuente1.render("PRESIONE Q PARA SALIR",
                                True, BLANCO)
        ventana_juego.blit(texto2, (200, 450))
        ventana_juego.blit(game_over, (120, 50))

        pygame.display.flip()
        pygame.display.update()


def pausa():
    """ FUNCION ENCARGADA DE MOSTAR LA PANTALLA DE PAUSA
        SI PRESIONA P, SE CARGA LA PANTALLA
        PARA SALIR DEL JUEGO HAY QUE PRESIONAR Q
        Y PARA CONTINUAR JUGANDO HAY QUE PRESIONAR C"""
    pausado = True
    imagen_pausa = pygame.image.load('imagenes/pausa.png')
    pausa = pygame.transform.scale(imagen_pausa, (400, 400))
    pygame.display.set_caption("PAUSA")

    pygame.mixer.music.load('sonidos/pacman_intermission.wav')
    pygame.mixer.music.play(88888)
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # C para continuar
                    pausado = False
                elif event.key == pygame.K_q:  # Q cierra el juego
                    pygame.quit()
                    quit()

        ventana_juego.fill(pygame.Color('black'))

        texto = fuente1.render("PRESIONE C PARA JUGAR", True, BLANCO)
        ventana_juego.blit(texto, (190, 490))

        texto2 = fuente1.render("PRESIONE  Q PARA SALIR",
                                True, BLANCO)
        ventana_juego.blit(texto2, (190, 460))

        texto3 = fuente1.render("JUEGO PAUSADO", True, BLANCO)
        ventana_juego.blit(texto3, (218, 400))
        ventana_juego.blit(pausa, (120, 0))

        pygame.display.flip()
        pygame.display.update()


def menu_inicial():
    """FUNCION QUE MUESTRA EL MENU INICIAL DEL JUEGO
    """
    pausado = True
    imagen_pausa = pygame.image.load('imagenes/inicio.png')
    pausa = pygame.transform.scale(imagen_pausa, (400, 400))
    pygame.display.set_caption("INCIO")

    pygame.mixer.music.load('sonidos/pacman_beginning.wav')
    pygame.mixer.music.play(88888)
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # C para continuar
                    pausado = False
                elif event.key == pygame.K_q:  # Q cierra el juego
                    pygame.quit()
                    quit()

        ventana_juego.fill(pygame.Color('black'))
        texto = fuente1.render("PRESIONE C PARA JUGAR", True, BLANCO)
        ventana_juego.blit(texto, (180, 350))
        texto2 = fuente1.render("PRESIONE Q PARA SALIR",
                                True, BLANCO)
        ventana_juego.blit(texto2, (180, 370))
        ventana_juego.blit(pausa, (120, 0))

        pygame.display.flip()
        pygame.display.update()


def NIVEL2():
    """ FUNCION QUE SE EJECUTA AL GANAR UN NIVEL
    """
    pausado = True
    imagen_pausa = pygame.image.load('imagenes/ganador.png')
    pausa = pygame.transform.scale(imagen_pausa, (400, 400))
    pygame.display.set_caption("WIN")

    pygame.mixer.music.load('sonidos/pacman_beginning.wav')
    pygame.mixer.music.play(88888)
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # C para continuar
                    pausado = False
                    return True
                elif event.key == pygame.K_q:  # Q cierra el juego
                    pygame.quit()
                    quit()
        ventana_juego.fill(pygame.Color('black'))
        ventana_juego.blit(pausa, (120, 20))
        texto = fuente1.render("PRESIONE C PARA JUGAR", True, BLANCO)
        ventana_juego.blit(texto, (180, 470))
        texto2 = fuente1.render("PRESIONE  Q PARA SALIR",
                                True, BLANCO)
        ventana_juego.blit(texto2, (180, 440))

        pygame.display.flip()
        pygame.display.update()


def main(
            contador_comida, vidas_pacman, mov_fantasma1,
            mov_fantasma2, mov_fantasma3,
            muros, food_special, comida, flag_manu,
            flag_mood_muerte, contador_modo_dead, direccion_pacman
        ):
    """
        FUNCION PRINCIAL
        DONDE ESTA TODO EL LLAMADO DEL FUNCIOAMIENTO DEL JUEGO

        ENTRADAS = INT ( COTADOR DE COMIDA Y ESPECIAL, VIDAS DE PACMAN
                        MOVIMENTO INICALES DE LOS FANTASMAS
                        BANDERA PARA EL MENU INICIAL)
                   LSITAS ( MUROS, COMIDA Y COMIDA ESPECIAL )

        SALIDA = TRUE O FALSE, PARA QUE PUEDA INICAL O NO EL SIGUIENTE NIVEL2

        TODOS LOS NIVEL EJECUTAN ESTA FUNCION
    """
    game_over = False
    reloj = pygame.time.Clock()  # variable de tiempo, ejecucion del programa

    event = None

    while game_over is False:

        reloj.tick(FPS)  # ajustando los FPS
        # EVENTO PARA QUE EL EXIT DE LA VENTANA FUNCIONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # si se preiosna p, abre pausa
                    pausa()

        # CONFICION PARA IMPRIMIR EL MENU PRINCIAL
        if flag_manu == 1:
            menu_inicial()
            flag_manu += 1

        # ACTUALIZACION EL MOVIMIENTO DE PACMAN
        if event is not None:
            pacman.handle_event(event)

        # IMPRIME LA PANTALLA CON EL FONDO NEGRO
        ventana_juego.fill(pygame.Color('black'))

        # imprimo las listas de sprite
        enemigo1.draw(ventana_juego)
        enemigo2.draw(ventana_juego)
        enemigo3.draw(ventana_juego)
        jugador.draw(ventana_juego)

        # ACTUALIZA LAS LISTAS DE SPRITE
        jugador.update()
        enemigo1.update()
        enemigo2.update()

        # funciones para crear el mapa
        recorre_lista_muros(ventana_juego, muros, muro_nuevo)
        recorre_lista_comida(ventana_juego, comida)
        recorre_lista_food_special(ventana_juego, food_special)

        # imprime el texto de la comida
        ventana_juego.blit(texto, (90, 530))

        # imprime el contador de comida
        puntos = fuente1.render(str(contador_comida), True, BLANCO)
        ventana_juego.blit(puntos, (280, 530))

        # IMPRIME LA VIDA EN IMAGENES
        x = 0
        for imagen in range(0, vidas_pacman):
            ventana_juego.blit(vida, (500+x, 560))
            x += 17
        # ELIMINA LA COMIDA CUANDO SE TOCAN
        contador_comida = eliminar_comida(comida, contador_comida)
        (contador_comida, vidas_pacman,
         flag_mood_muerte, contador_modo_dead) = eliminar_food_especial(
            food_special, contador_comida,
             vidas_pacman, flag_mood_muerte, contador_modo_dead)

        # SI TIENE PODER, CAMBIA DE COLOR A LOS FANTASMAS
        if flag_mood_muerte is True:

            Fantasma1.image = imagen_fantasmas_dead
            Fantasma1.image.set_colorkey(NEGRO)
            Fantasma1.image = pygame.transform.scale(Fantasma1.image, (15, 15))

            Fantasma2.image = imagen_fantasmas_dead
            Fantasma2.image.set_colorkey(NEGRO)
            Fantasma2.image = pygame.transform.scale(Fantasma2.image, (15, 15))

            Fantasma3.image = imagen_fantasmas_dead
            Fantasma3.image.set_colorkey(NEGRO)
            Fantasma3.image = pygame.transform.scale(Fantasma3.image, (15, 15))

        """
            BANDERA PARA GENERAR EL PRIMER MOVIMENTO DE LOS FANTASMAS
            LUEGO LO HACE AUTOMATICO CON LAS COLICIONES CONTRA LOS MUROS
        """
        flag = 0
        if flag == 0:
            Fantasma1.handle_event(mov_fantasma1)
            Fantasma2.handle_event(mov_fantasma2)
            Fantasma3.handle_event(mov_fantasma3)
            flag += 1

        # creo la colisiones entre grupos de sprite y quita vida
        # VERIFICA SI EL MOOD FANTAS DEAD ESTE APAGADO
        # SI ESTA ACTIVADO NO GENERA LAS COLISIONES
        if flag_mood_muerte is False:
            colision = pygame.sprite.spritecollide(pacman, enemigo1, False)
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
                if (event is not None):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            pacman.rect.centerx += 3
                        if event.key == pygame.K_RIGHT:
                            pacman.rect.centerx -= 3
                        if event.key == pygame.K_UP:
                            pacman.rect.bottom += 3
                        if event.key == pygame.K_DOWN:
                            pacman.rect.bottom -= 3
                pygame.mixer.music.load('sonidos/pacman_death.wav')
                pygame.mixer.music.play(1)

                vidas_pacman -= 1

        if flag_mood_muerte is False:
            colision = pygame.sprite.spritecollide(pacman, enemigo2, False)
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
                if (event is not None):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            pacman.rect.centerx += 3
                        if event.key == pygame.K_RIGHT:
                            pacman.rect.centerx -= 3
                        if event.key == pygame.K_UP:
                            pacman.rect.bottom += 3
                        if event.key == pygame.K_DOWN:
                            pacman.rect.bottom -= 3
                pygame.mixer.music.load('sonidos/pacman_death.wav')
                pygame.mixer.music.play(1)

                vidas_pacman -= 1

        if flag_mood_muerte is False:
            colision = pygame.sprite.spritecollide(pacman, enemigo3, False)
            if colision:
                if mov_fantasma3 == 0:
                    Fantasma3.rect.x -= 2
                    mov_fantasma3 = 1
                    Fantasma3.handle_event(mov_fantasma3)
                elif mov_fantasma3 == 1:
                    Fantasma3.rect.x += 2
                    mov_fantasma3 = 0
                    Fantasma3.handle_event(mov_fantasma3)
                elif mov_fantasma3 == 2:
                    Fantasma3.rect.y -= 2
                    mov_fantasma3 = 3
                    Fantasma3.handle_event(mov_fantasma3)
                else:
                    Fantasma3.rect.y += 2
                    mov_fantasma3 = 2
                    Fantasma3.handle_event(mov_fantasma3)
                if (event is not None):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            pacman.rect.centerx += 3
                        if event.key == pygame.K_RIGHT:
                            pacman.rect.centerx -= 3
                        if event.key == pygame.K_UP:
                            pacman.rect.bottom += 3
                        if event.key == pygame.K_DOWN:
                            pacman.rect.bottom -= 3
                pygame.mixer.music.load('sonidos/pacman_death.wav')
                pygame.mixer.music.play(1)
                vidas_pacman -= 1

        # colision de pacman con el mapa
        for muro in muros:
            if pacman.rect.colliderect(muro):
                if (event is not None):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            pacman.rect.centerx += 2
                        if event.key == pygame.K_RIGHT:
                            pacman.rect.centerx -= 2
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

            elif Fantasma3.rect.colliderect(muro):
                if mov_fantasma3 == 0:
                    Fantasma3.rect.x -= 2
                elif mov_fantasma3 == 1:
                    Fantasma3.rect.x += 2
                elif mov_fantasma3 == 2:
                    Fantasma3.rect.y -= 2
                else:
                    Fantasma3.rect.y += 2
                mov_fantasma3 = variable_movimento_fantasma3(mov_fantasma3)

        # CONDICION PARA DESACTIR EL PODER
        if flag_mood_muerte is True:
            contador_modo_dead += 1
            
            if contador_modo_dead >= 200:
                flag_mood_muerte = False
                contador_modo_dead = 200

        tiempo_poder = fuente1.render("TIEMPO PODER ", True, BLANCO)
        ventana_juego.blit(tiempo_poder, (10, 580))
        # DIBUJA EL INDICADOR DEL PODER
        pygame.draw.rect(ventana_juego, BLANCO, (150, 580, 200, 20))
        pygame.draw.rect(
                            ventana_juego, BLUE,
                            (150, 580, contador_modo_dead, 20)
                        )

        # VUELVE A LA NORMALIDAD LOS FANTASMAS
        if contador_modo_dead == 200:
            flag_mood_muerte = False
            Fantasma1.image = pygame.image.load('imagenes/fana.png').convert()
            Fantasma1.image.set_colorkey(NEGRO)
            Fantasma1.image = pygame.transform.scale(Fantasma1.image, (15, 15))

            Fantasma2.image = pygame.image.load('imagenes/fantaa.png').convert()
            Fantasma2.image.set_colorkey(NEGRO)
            Fantasma2.image = pygame.transform.scale(Fantasma2.image, (15, 15))

            Fantasma3.image = pygame.image.load('imagenes/azul.png').convert()
            Fantasma3.image.set_colorkey(NEGRO)
            Fantasma3.image = pygame.transform.scale(Fantasma3.image, (15, 15))
            contador_modo_dead = 0

        # NORMALIZANDO LAS BANDERAS DEL PODER
        if contador_modo_dead >= 200:
            flag_mood_muerte = False
            contador_modo_dead = 0

        # termina cuando la comida es 0 Y LLAMA LA NIVEL2
        if contador_comida == 0:
            game_over = True
            return NIVEL2()

        # TERMINA EL NIVEL SI LAS VIDA ES 0
        if vidas_pacman == 0:
            perdida()

        jugador.update()
        enemigo1.update()
        enemigo2.update()
        pygame.display.flip()
        pygame.display.update()

    return


# COLORES
BLANCO = (255, 255, 255)
BLUE = (0, 0, 255)
NEGRO = (0, 0, 0)

# VARIABLES
ancho_ventana = 600
alto_ventana = 600
ventana_juego = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("PACMAN")
clock = pygame.time.Clock()


vidas_pacman = 3
imagen_vida = pygame.image.load('imagenes/pac.png')
vida = pygame.transform.scale(imagen_vida, (15, 15))

jugador = pygame.sprite.Group()
enemigo1 = pygame.sprite.Group()
enemigo2 = pygame.sprite.Group()
enemigo3 = pygame.sprite.Group()

# genero el primer movimeinto
mov_fantasma1 = 0
mov_fantasma2 = 1
mov_fantasma3 = 0

#  llamo los objetos de los personajes
pacman = Pacman()

paths_rojo = {
    "right": ['imagenes/rojo_1_rigth.png', 'imagenes/rojo_2_rigth.png'],
    "left": ['imagenes/rojo_1_left.png', 'imagenes/rojo_2_left.png'],
    "up": ['imagenes/rojo_1_up.png', 'imagenes/rojo_2_up.png'],
    "down": ['imagenes/rojo_1_down.png', 'imagenes/rojo_2_down.png'],
}

paths_blue = {
    "right": ['imagenes/blue_1_rigth.png', 'imagenes/blue_2_rigth.png'],
    "left": ['imagenes/blue_1_left.png', 'imagenes/blue_2_left.png'],
    "up": ['imagenes/blue_1_up.png', 'imagenes/blue_2_up.png'],
    "down": ['imagenes/blue_1_down.png', 'imagenes/blue_2_down.png'],
}

paths_pink = {
    "right": ['imagenes/pink_1_rigth.png', 'imagenes/pink_2_rigth.png'],
    "left": ['imagenes/pink_1_left.png', 'imagenes/blue_2_left.png'],
    "up": ['imagenes/pink_2_left.png', 'imagenes/pink_2_up.png'],
    "down": ['imagenes/pink_1_down.png', 'imagenes/pink_2_down.png'],
}


x_rojo = 100
y_rojo = 80

x_blue = 500
y_blue = 80

x_pink = 30
y_pink = 400


Fantasma1 = Fantasma(paths_rojo,x_rojo,y_rojo)
Fantasma2 = Fantasma(paths_blue,x_blue,y_blue)
Fantasma3 = Fantasma(paths_pink,x_pink,y_pink)

#  los agrego a un grupo de sprite
enemigo1.add(Fantasma1)
enemigo2.add(Fantasma2)
enemigo3.add(Fantasma3)
jugador.add(pacman)

FPS = 60
fuente1 = pygame.font.SysFont("segoe print", 25)
texto = fuente1.render("COMIDA DISPONIBLE: ", True, BLANCO)
imagen_muro = pygame.image.load('imagenes/muro_1.png')
imagen_fantasmas_dead = pygame.image.load('imagenes/powerup.png').convert()
muro_nuevo = pygame.transform.scale(imagen_muro, (20, 20))

# MAPAS

mapa = [
                 "                              ",
                 "                              ",
                 "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                 "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxfxxxxxxxxxxmxxxxxmx",
                 "xfxxxxxxxxxmxxxxxxxxxxmxxxxxfx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxfxxxxxxxxxxmxxxxxmx",
                 "xfxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmxxxxxxxxxmxxxxxxxxxxmxxxxxmx",
                 "xmmmmmmmmmmmmmmmmmmmmmmmmmmmmx",
                 "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                 
 ]

MAPA2 = [
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
                "xmxxxxxxxxxmxxxxxxxmxxxmxxxxmx",
                "xmxxxxxxxxxmxxxxxxxmxxxmxxxxmx",
                "xmxxxxxxxxxmxxxxxxxmxxxmxxxxmx",
                "xmmmmxmmmmmmmmmmmmmmmmmmxmmmmx",
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

flag_manu = 1
flag_mood_muerte = False
contador_modo_dead = 0
direccion_pacman = 0

# llamar la funcion de contruir mapa 1 para que forme la listas
muros, comida, contador_comida, food_special = construir_mapa(MAPA2)

main(contador_comida, vidas_pacman, mov_fantasma1, mov_fantasma2,
    mov_fantasma3, muros, food_special, comida, flag_manu,
    flag_mood_muerte, contador_modo_dead, direccion_pacman)