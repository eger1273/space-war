from pygame import *
from random import randint 

# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# шрифты и надписи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True ,(255, 255, 255))
lose = font1.render('YOU LISE!',  True, (180, 0, 0))
font2 = font.Font(None, 36)

# нам нужны такие картинки
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_bullet = "bullet.png" # пули
img_enemy = "ufo.png" # враг

score = 0 # сбито кораблей
lost = 0 # пропущено кораблей
max_lost = 3 # проигралиб если пропустили столько кораблей
goal = 1001

# класс-родители для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
            # вызываем конструктор класса (Sprite):
            sprite.Sprite.__init__(self)

            # каждый спрайт должен хранить свойство image - изображения
            self.image = transform.scale(image.load(player_image), (size_x, size_y))
            self.speed = player_speed


            # каждый спрайт должен хранить свойство rect - прямоугольник в который он вписан
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y

    # методб отрисовывающих героя на окне
        def  reset(self): 
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
# метод "выстрел" (используем место игрокаб чтобы создть там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# класс спрайта-врага
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# класс спрайта-врага
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает если доется до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# класс спрайт-пули
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает если дойдет до рая экрана
        if self.rect.y < 0:
            self.kill()

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
backround = transform.scale(image.load(img_back), (win_width, win_height))

# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 30)

# создаем группы спрайтов-врага
monsters = sprite.Group()
for i in range(1, 101):
    monster = Enemy(img_enemy, randint(80, win_width  - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False

# Основной цикл игры:
run = True
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
    if mouse.get_pressed()[0]:
        fire_sound.play()
        ship.fire()
    if not finish:
    
        # обновляем фон
        window.blit(backround,(0, 0))

        # пише текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропуск: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # производит движение праятов
        ship.update()
        monsters.update()
        bullets.update()

        # обновляем их в новом местоположение про каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # проверка столкновения пули с монстром
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз сколько монстров подито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # возможный проигрыш
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        # проверка выигрыша
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    time.delay(40)