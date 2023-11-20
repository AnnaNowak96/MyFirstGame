import pygame
import os
pygame.init()
pygame.font.init()


SZEROKOSC = 1000
WYSOKOSC = 600
WINDOW = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Fello goni kuriera")
FONT_ZYCIA = pygame.font.SysFont("comicrelief", 40)
FONT_TEKST = pygame.font.SysFont("comicrelief", 100)

PIESEK_SZEROKOSC = 90
PIESEK_WYSOKOSC = 110
KURIER_SZEROKOSC = 80
KURIER_WYSOKOSC = 180
PACZKA_SZEROKOSC = 70
PACZKA_WYSOKOSC = 50

PIESEK_IMAGE = pygame.image.load(os.path.join("Assets", "piesek.png"))
PIESEK = pygame.transform.scale(PIESEK_IMAGE, (PIESEK_SZEROKOSC, PIESEK_WYSOKOSC))
KURIER_IMAGE = pygame.image.load(os.path.join("Assets", "kurier.png"))
KURIER = pygame.transform.scale(KURIER_IMAGE, (KURIER_SZEROKOSC, KURIER_WYSOKOSC))
PIESEK_HIT = pygame.USEREVENT + 1
KURIER_HIT = pygame.USEREVENT + 2
PACZKA_IMAGE = pygame.image.load(os.path.join("Assets", "paczka.png"))
PACZKA = pygame.transform.scale(PACZKA_IMAGE,(PACZKA_SZEROKOSC, PACZKA_WYSOKOSC))

TLO_IMAGE = pygame.image.load((os.path.join("Assets", "background.png")))
TLO = pygame.transform.scale(TLO_IMAGE, (SZEROKOSC, WYSOKOSC))

GREEN = (0, 255, 0)
CZARNE = (0, 0, 0)
FPS = 50
VEL = 5
VEL_KURIER = 2
SHOOT_DELAY = 1200

moving_up = True


def draw_window(piesek, kurier, piesek_zycia, paczka, strzaly):
    WINDOW.blit(TLO, (0, 0))
    piesek_zycie_tekst = FONT_ZYCIA.render("Życia: " + str(piesek_zycia), 1, CZARNE)
    WINDOW.blit(piesek_zycie_tekst, (SZEROKOSC - piesek_zycie_tekst.get_width() - 20, 10))
    WINDOW.blit(PIESEK, (piesek.x, piesek.y))
    WINDOW.blit(KURIER, (kurier.x, kurier.y))
    for paczka in strzaly:
        WINDOW.blit(PACZKA, (paczka.x, paczka.y))

    pygame.display.update()


def dog_movement(key_pressed, piesek):
    if key_pressed[pygame.K_a] and piesek.x - VEL > 0:
        piesek.x -= VEL
    if key_pressed[pygame.K_d] and piesek.x + VEL + piesek.width < SZEROKOSC:
        piesek.x += VEL
    if key_pressed[pygame.K_s] and piesek.y + VEL + piesek.height < WYSOKOSC:
        piesek.y += VEL
    if key_pressed[pygame.K_w] and piesek.y -VEL > 0:
        piesek.y -= VEL


def kurier_movement(kurier):
    global moving_up
    if moving_up:
        kurier.y -= VEL_KURIER
    else:
        kurier.y += VEL_KURIER
    if kurier.top <= 0:
        moving_up = False
    elif kurier.bottom >= WYSOKOSC:
        moving_up = True


def rzucanie_paczkami(kurier, strzaly, piesek):
    for paczka in strzaly:
        WINDOW.blit(PACZKA, (paczka.x, paczka.y))
        paczka.x += VEL_KURIER
        if piesek.colliderect(paczka):
            pygame.event.post(pygame.event.Event(PIESEK_HIT))
            strzaly.remove(paczka)
        elif paczka.x >= SZEROKOSC:
            strzaly.remove(paczka)
        pygame.display.update()

def gryzienie(kurier, piesek):
    if piesek.colliderect(kurier):
        pygame.event.post(pygame.event.Event(KURIER_HIT))


def stworz_paczke(kurier):
    return pygame.Rect(kurier.x, kurier.y + kurier.height // 2, PACZKA_SZEROKOSC, PACZKA_WYSOKOSC)

def wygrany_komunikat(tekst):
    draw_tekst = FONT_ZYCIA.render(tekst, 1, CZARNE)
    WINDOW.blit(draw_tekst, (SZEROKOSC//2 - draw_tekst.get_width()//2, WYSOKOSC//2 - draw_tekst.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    piesek = pygame.Rect(900, 300, PIESEK_SZEROKOSC, PIESEK_WYSOKOSC)
    kurier = pygame.Rect(10, 100, KURIER_SZEROKOSC, KURIER_WYSOKOSC)
    paczka = pygame.Rect(500, 300, PACZKA_SZEROKOSC, PACZKA_WYSOKOSC)

    strzaly = []

    piesek_zycia = 3
    kurier_zycia = 1
    shoot_timer = pygame.time.get_ticks()
    zegar = pygame.time.Clock()

    run = True
    while run:
        zegar.tick(FPS)
        current_time = pygame.time.get_ticks()
        if current_time - shoot_timer > SHOOT_DELAY:
            nowa_paczka = stworz_paczke(kurier)
            strzaly.append(nowa_paczka)
            shoot_timer = current_time

        for event in pygame.event.get():
            if event.type == PIESEK_HIT:
                piesek_zycia -= 1

            if event.type == KURIER_HIT:
                kurier_zycia -= 1

        wygrany_tekst = ""
        if piesek_zycia <= 0:
            wygrany_tekst = "Kurier Cię pokonał"
        if kurier_zycia <= 0:
            wygrany_tekst = "Kurier pokonany. ZWYCIĘSTWO!"
        if wygrany_tekst != "":
            wygrany_komunikat(wygrany_tekst)
            break


        key_pressed = pygame.key.get_pressed()

        dog_movement(key_pressed, piesek)
        kurier_movement(kurier)
        rzucanie_paczkami(kurier, strzaly, piesek)
        gryzienie(kurier, piesek)
        draw_window(piesek, kurier, piesek_zycia, paczka, strzaly)

        if event.type == pygame.QUIT:
            run = False
            break

    main()

if __name__ == '__main__':
    main()






