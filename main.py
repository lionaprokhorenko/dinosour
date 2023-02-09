import pygame
import sys
import os
from random import randint
import sqlite3

#загружаем картинки
bg_image = pygame.image.load(os.path.join('files', 'bg.png'))
start_image = pygame.image.load(os.path.join('files', 'start_image.png'))
player_images = [pygame.image.load(os.path.join('files', 'DinoRun1.png')),
    pygame.image.load(os.path.join('files', 'DinoRun2.png')),
    pygame.image.load(os.path.join('files', 'DinoJump.png'))]
cactus_images = [pygame.image.load(os.path.join('files', 'cactus1.png')),
    pygame.image.load(os.path.join('files', 'cactus2.png')),
    pygame.image.load(os.path.join('files', 'cactus3.png'))]
cactus_images_2_level = [pygame.image.load(os.path.join('files', 'cactus1_2.png')),
    pygame.image.load(os.path.join('files', 'cactus2_2.png')),
    pygame.image.load(os.path.join('files', 'cactus3_2.png'))]
player_images_2_level = [pygame.image.load(os.path.join('files', 'DinoRun1_2.png')),
    pygame.image.load(os.path.join('files', 'DinoRun2_2.png')),
    pygame.image.load(os.path.join('files', 'DinoJump_2.png'))]
pygame.init()

sound_jump = pygame.mixer.Sound(os.path.join('files', 'finish.wav'))
sound_finish = pygame.mixer.Sound(os.path.join('files', 'jumpp.wav'))
db = sqlite3.connect('players.db')

cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    text TEXT,
   score integer);
""")
db.commit()

#основные константы для позиций
size = width, height = 1000, 600

bg_pos = bg_x, bg_y = 0, 500
speed = 8

jump_delta_y = 1
jump_start_y = 20



class Dinosour(pygame.sprite.Sprite):
    def __init__(self):
        #super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.condition = 0 # 0 и 1 - бег, 2 - прыжок
        self.step = 0
        self.image = player_images[self.condition]
        self.x = 50
        self.y = bg_y - self.image.get_height()
        self.image = player_images[self.condition]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.jump_y = self.y
        self.change_jump = jump_start_y

    def update(self):
        self.step += 1
        if self.condition < 2: # run
            if self.step > 10:
                self.condition = (self.condition + 1) % 2
                self.step = 0
            self.image = player_images[self.condition]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.image = player_images[self.condition] # jump
            self.change_jump -= jump_delta_y
            self.jump_y -= self.change_jump
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.jump_y
            if self.jump_y > self.y:
                self.condition = 0

    def jump(self):
        if self.condition != 2:
            self.condition = 2
            sound_finish.play()
            self.jump_y = self.y
            self.change_jump = jump_start_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))





class DinosourSecond(pygame.sprite.Sprite):
    def __init__(self):
        #super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.condition = 0 # 0 и 1 - бег, 2 - прыжок
        self.step = 0
        self.image = player_images_2_level[self.condition]
        self.x = 50
        self.y = bg_y - self.image.get_height()
        self.image = player_images_2_level[self.condition]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.jump_y = self.y
        self.change_jump = jump_start_y

    def update(self):
        self.step += 1
        if self.condition < 2: # run
            if self.step > 10:
                self.condition = (self.condition + 1) % 2
                self.step = 0
            self.image = player_images_2_level[self.condition]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.image = player_images_2_level[self.condition]  # jump
            self.change_jump -= jump_delta_y
            self.jump_y -= self.change_jump
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.jump_y
            if self.jump_y > self.y:
                self.condition = 0

        def jump(self):
            if self.condition != 2:
                self.condition = 2
                sound_jump.play()
                self.jump_y = self.y
                self.change_jump = jump_start_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cactus_images[randint(0,len(cactus_images)-1)]
        self.x = width
        self.y = self.y = bg_y - self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x -= speed
        if self.x <= - self.image.get_width():
            return True
        return False

    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class CactusSecond(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cactus_images_2_level[randint(0,len(cactus_images_2_level)-1)]
        self.x = width
        self.y = self.y = bg_y - self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x -= speed
        if self.x <= - self.image.get_width():
            return True
        return False
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def bg(screen):
    global bg_x, bg_y
    image_w = bg_image.get_width()
    bg_x -= speed
    if bg_x <= -image_w:
        bg_x = image_w
    screen.blit(bg_image, (bg_x, bg_y))
    if bg_x <= width - image_w:
        screen.blit(bg_image, (bg_x + image_w , bg_y))
    if bg_x >= 0:
        screen.blit(bg_image, (bg_x - image_w , bg_y))


def finish_game(screen, score, name):
    repeat = True
    run = True
    sound_jump.play()
    print(name, score // 10)

    cur.execute("INSERT INTO users(text, score) VALUES(?, ?);",
               (name, score // 10))  # записываем ифнормацию о текущей игре в базу данных
    db.commit()

    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    rows.sort(key=lambda x: -x[1])  # сортируем все игры по счету по убыванию

    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('arial', 30)
    text_repeat = font.render('Если Вы хотите повторить игру, нажмите Enter', True, (0, 0, 0))
    text_repeat_1 = text_repeat.get_rect()
    text_repeat_1.center = (width // 2, height // 2 - 160)
    text_score = font.render("Счёт за игру: " + ' ' + str(score // 10), True, (0, 0, 0))
    score_rect = text_score.get_rect()
    score_rect.center = (width // 2, height // 2 - 100)
    screen.blit(text_repeat, text_repeat_1)
    screen.blit(text_score, score_rect)
    if (score // 10) > 100:
        text_new_level = font.render('Если Вы хотите перейти на новый уровень, нажмите пробел', True, (0, 0, 0))
        text_new_level_1 = text_new_level.get_rect()
        text_new_level_1.center = (width // 2, height // 2 - 200)
        screen.blit(text_new_level, text_new_level_1)


    for i in range(min(len(rows), 5)):
        font = pygame.font.SysFont('arial', 20)
        text_row = font.render(rows[i][0] + str(rows[i][1]), True, (0, 0, 0))
        row_rect = text_row.get_rect()
        row_rect.center = (width // 2, height // 2 + 50 * i)
        screen.blit(text_row, row_rect)

    pygame.display.flip()

    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                repeat = False
                pygame.quit()
                # обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        main()  # Enter
                if event.key == pygame.K_SPACE:  # пробел
                    level_2()



    # while run:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False


def finish_game_2(screen, score, name):
    repeat = True
    sound_finish.play()
    print(name, score // 10)

    cur.execute("INSERT INTO users(text, score) VALUES(?, ?);",
                (name, score // 10))  # записываем ифнормацию о текущей игре в базу данных
    db.commit()

    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    rows.sort(key=lambda x: -x[1])  # сортируем все игры по счету по убыванию
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('arial', 30)
    text_repeat = font.render('Если Вы хотите повторить игру, нажмите Enter', True, (0, 0, 0))
    text_repeat_1 = text_repeat.get_rect()
    text_repeat_1.center = (width // 2, height // 2 - 160)
    text_score = font.render("Счёт за игру: " + ' ' + str(score // 10), True, (0, 0, 0))
    score_rect = text_score.get_rect()
    score_rect.center = (width // 2, height // 2 - 100)
    screen.blit(text_repeat, text_repeat_1)
    screen.blit(text_score, score_rect)



    for i in range(min(len(rows), 5)):
        font = pygame.font.SysFont('arial', 20)
        text_row = font.render(rows[i][0] + str(rows[i][1]), True, (0, 0, 0))
        row_rect = text_row.get_rect()
        row_rect.center = (width // 2, height // 2 + 50 * i)
        screen.blit(text_row, row_rect)

    pygame.display.flip()
    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                repeat = False
                pygame.quit()
            # обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter
                    main()



def level_2():
    pygame.display.set_caption('Динозавр')


    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    run = True
    start = True
    input_box = pygame.Rect(0, 0, 200, 30)
    name = ''
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(name)
                    start = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((255, 255, 255))
        font = pygame.font.SysFont('arial', 30)
        text_name = font.render('Повторите своё имя пожалуйста', True, (0, 0, 0))
        text_name_rect = text_name.get_rect()
        text_name_rect.center = (width // 2, height // 2 - 100)
        screen.blit(text_name, text_name_rect)
        txt = font.render(name, True, (0, 0, 0))
        input_box.center = (width // 2, height // 2 - 250)
        screen.blit(txt, input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
        pygame.display.flip()
        clock.tick(30)

    player = DinosourSecond()
    game_score = 0
    cactus_time = 20
    cactus_list = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                    # обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # пробел
                    player.jump()

        screen.fill((255, 255, 255))

                # обновляем и отрисовываем все объекты
        bg(screen)
        player.draw(screen)
        player.update()

                # отображение счета на экране во время игры
        font = pygame.font.SysFont('arial', 30)
        text = font.render('счёт за игру: ' + str(game_score // 10), True, (0, 0, 0))
        score_rect = text.get_rect()
        score_rect.center = (width - 150, 30)
        screen.blit(text, score_rect)

        if game_score == cactus_time:
            cactus_time += randint(50, 150)
            cactus_list.append(CactusSecond())
        for c in cactus_list:
                c.draw(screen)
                if player.rect.colliderect(c.rect):
                    finish_game_2(screen, game_score, name)
                    run = False
                    break
                kill_cactus = c.update()
                if kill_cactus: cactus_list.remove(c)

        game_score += 1
        clock.tick(30)


def main():
    pygame.display.set_caption('Динозавр')


    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    run = True
    start = True
    input_box = pygame.Rect(0, 0, 200, 30)
    name = ''
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(name)
                    start = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((255, 255, 255))
        screen.blit(start_image, (0, 0))
        font = pygame.font.SysFont('arial', 30)
        txt = font.render(name, True, (0, 0, 0))
        input_box.center = (width // 2, height // 2 - 250)
        screen.blit(txt, input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
        pygame.display.flip()
        clock.tick(30)


    player = Dinosour()
    game_score = 0
    cactus_time = 20
    cactus_list = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # пробел
                    player.jump()

        screen.fill((255, 255, 255))



        # обновляем и отрисовываем все объекты
        bg(screen)
        player.draw(screen)
        player.update()

        # отображение счета на экране во время игры
        font = pygame.font.SysFont('arial', 30)
        text = font.render('счёт за игру: ' + str(game_score // 10), True, (0, 0, 0))
        score_rect = text.get_rect()
        score_rect.center = (width - 150, 30)
        screen.blit(text, score_rect)

        if game_score == cactus_time:
            cactus_time += randint(50,150)
            cactus_list.append(Cactus())
        for c in cactus_list:
            c.draw(screen)
            if player.rect.colliderect(c.rect):
                finish_game(screen, game_score, name)
                run = False
                break
            kill_cactus = c.update()
            if kill_cactus: cactus_list.remove(c)


        pygame.display.flip()
        game_score += 1
        clock.tick(30)


    pygame.quit()







if __name__ == '__main__':
    sys.exit(main())