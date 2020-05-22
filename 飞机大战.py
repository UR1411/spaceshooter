from sys import exit
import pygame
from random import randint
from time import sleep
import os,codecs

pygame.init()
pygame.mixer.init()
#size=width,height=436,773

#define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#常量定义

#敌机2
enemy2x = 0
enemy2flag = 0
#按钮
buttonflag1 = 1
#界面
s = 1
#Hp
HPi = 0
HP_begin = 750
#设计游戏得分（游戏中）

score = 0

#################字符定义
#HP字符
hpstr = pygame.font.Font('./font/ResourceHanRoundedCN-Bold.ttf',26)
hpstr_fmt = hpstr.render("生命值：",True,(0,255,0))
hpstr_rect = hpstr_fmt.get_rect()
hpstr_rect.x = HP_begin - 90
hpstr_rect.y = -8
#得分字符
scorestr = pygame.font.Font('./font/ResourceHanRoundedCN-Bold.ttf',26)
scorestr_fmt = scorestr.render("得分：",1,(0,255,0))
scorestr_rect = scorestr_fmt.get_rect()
scorestr_rect.x = 10
scorestr_rect.y = -8
#分数
scoref = pygame.font.Font('./font/ResourceHanRoundedCN-Bold.ttf',23)

#死亡界面
death = pygame.font.SysFont('arial',100)
death_fmt = death.render("GAME OVER",1,(255,0,0))
death_rect = death_fmt.get_rect()
death_rect.centerx = 450
death_rect.centery = 390


#定义函数

#写入文本
def write_txt(context,srtim,path):
    f = codecs.open(path,srtim,'utf8')
    f.write(str(context))
    f.close

#读取文本
def read_txt(path):
    with open(path,'r',encoding='utf8') as f:
        lines = f.readlines()
    return lines
#排行榜
ranking_list = read_txt(r'score.txt')[0].split('f')

score1 = pygame.font.Font("./font/ResourceHanRoundedCN-Bold.ttf",27)
score1_fmt = score1.render(ranking_list[0],1,(230,230,0))
score1_rect = score1_fmt.get_rect()
score1_rect.x = 80
score1_rect.centery = 463

score2 = pygame.font.Font("./font/ResourceHanRoundedCN-Bold.ttf",27)
score2_fmt = score2.render(ranking_list[1],1,(230,230,0))
score2_rect = score2_fmt.get_rect()
score2_rect.x = 80
score2_rect.centery = 505

score3 = pygame.font.Font("./font/ResourceHanRoundedCN-Bold.ttf",27)
score3_fmt = score3.render(ranking_list[2],1,(230,230,0))
score3_rect = score3_fmt.get_rect()
score3_rect.x = 80
score3_rect.centery = 546

#自定义敌机出现事件
count = 1
COUNT = pygame.USEREVENT
width = 900
height = 750
screen = pygame.display.set_mode((width,height))         #显示设置
icon = pygame.image.load("./background/player.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("飞机大战")



# add clock
clock = pygame.time.Clock()
pygame.time.set_timer(COUNT,1000)


#精灵组

class Hero(pygame.sprite.Sprite):
    #初始化英雄
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/player.png")
        self.rect = self.image.get_rect()
        self.rect.width *= 0.3
        self.rect.height *= 0.3
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        self.rect.x = 400
        self.rect.y = 600
        self.speed = speed
        self.ready_to_fire = 0
#更新
    def update(self,*args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            if self.ready_to_fire == 0:
                self.fire()
            self.ready_to_fire += 1
            if self.ready_to_fire > 10: #设置子弹冷却
                self.ready_to_fire = 0
        else:
                self.ready_to_fire = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
    def fire(self):
        #发射子弹
        
        bullet = Bullet(10)
        bullet.rect.centery = self.rect.y
        bullet.rect.centerx = self.rect.centerx
        bullet_group.add(bullet)
        sound = pygame.mixer.Sound("./music/shoot.wav")
        sound.play()

class Enemy1(pygame.sprite.Sprite):
    #初始化敌人
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./enemy/enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,width)
        self.rect.y = -40
        self.speed = speed
    #更新
    def update(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > width:
            self.rect.x = width - self.rect.width
        self.rect.y += self.speed
        if self.rect.y > height:
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    #初始化敌人2
    def __init__(self,speed,HP,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./enemy/enemy2.png")
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,width)
        self.rect.y = -100
        self.speed = speed
        self.HP = HP
        self.right = 0
        self.left = 0
        x = randint(0,1)
        self.x = x
        self.ready_to_fire = 0
    #更新
    def update(self):

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > width:
            self.rect.x = width - self.rect.width
        self.rect.y += 1
        if self.x == 1:
            self.rect.x += self.speed
            self.right += 1
        elif self.x == 0:
            self.rect.x -= self.speed
            self.left += 1
        if self.left > randint(60,2000):    #定义敌机2摆动幅度
            self.left = 0
            self.x = 1
        if self.right > randint(60,2000):
            self.right = 0
            self.x = 0
        if self.rect.x < 10:
            self.x = 1
        if self.rect.x + self.rect.width > 890:
            self.x = 0
        global count
        if count % 1 == 0 and self.ready_to_fire == 0:   #设置子弹发射速度（1,60）
            self.fire()
        self.ready_to_fire += 1
        if self.ready_to_fire > 60:
            self.ready_to_fire = 0
        if self.HP == 0:
           self.kill()
        if self.rect.y > height:
            self.kill()
    def fire(self):
        #发射子弹
        e2bullet = Enemy2Bullet(6)
        e2bullet.rect.y = self.rect.bottom - 15
        e2bullet.rect.centerx = self.rect.centerx + 1
        e2bullet_group.add(e2bullet)

class Explode(pygame.sprite.Sprite):
    #初始化爆炸
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sound = pygame.mixer.Sound("./music/explode.wav")
        sound.play()
        self.images = [pygame.image.load("./explode/explode" +  str(i) + ".png") for i in range(1,5)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.ready_to_change = 0
        

    def update(self):
        if self.image_index < 3:
            self.ready_to_change += 1
            if self.ready_to_change %4 == 0:
                self.image_index += 1
                self.image = self.images[self.image_index]
        else :
            self.kill()
class Bullet(pygame.sprite.Sprite):
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./bullet/bullet2.png")
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()
class Enemy2Bullet(pygame.sprite.Sprite):
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./bullet/bullet1.png")
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Background(pygame.sprite.Sprite):
    #初始化背景
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/background1.jpg")
        self.rect = self.image.get_rect()
        self.ready_to_move = 0
    def update(self,*args):
        if self.ready_to_move == 0:
            self.rect.y += 1
            if self.rect.y > height:
                self.rect.y = -self.rect.height
        if self.ready_to_move > 1:
            self.ready_to_move = 0
        else:
            self.ready_to_move += 1
class PlayBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/background3.jpg")
        self.rect = self.image.get_rect()
    def update(self, *args):
        self.rect.x = 0
        self.rect.y = 0

class Button1(pygame.sprite.Sprite):
    def __init__(self,x,y,flag):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/playbutton1.png")
        self.rect = self.image.get_rect()
        self.rect.width *= 0.4
        self.rect.height *= 0.4
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        self.x = x
        self.y = y
        self.flag = flag
    def update(self, *args):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            global buttonflag1
            buttonflag1 -= 1
        if keys[pygame.K_DOWN]:
            buttonflag1 += 1
        if buttonflag1 <= 0:
                buttonflag1 = 1
        elif buttonflag1 > 2:
                buttonflag1 = 2
        if buttonflag1 == 1:
            self.image = pygame.image.load("./background/playbutton2.png")
            self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        else :
            self.image = pygame.image.load("./background/playbutton1.png")
            self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
class Button2(pygame.sprite.Sprite):
    def __init__(self,x,y,flag):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/exitbutton2.png")
        self.rect = self.image.get_rect()
        self.rect.width *= 0.4
        self.rect.height *= 0.4
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        self.x = x
        self.y = y
        self.flag = flag
    def update(self, *args):
        self.rect.centerx = self.x
        self.rect.centery = self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            global buttonflag1
            buttonflag1 -= 1
        if keys[pygame.K_DOWN]:
            buttonflag1 += 1
        if buttonflag1 <= 0:
                buttonflag1 = 1
        elif buttonflag1 > 2:
                buttonflag1 = 2
        if buttonflag1 == 2:
            self.image = pygame.image.load("./background/exitbutton1.png")
            self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        else :
            self.image = pygame.image.load("./background/exitbutton2.png")
            self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))

class Hero_hp(pygame.sprite.Sprite):
    def __init__(self,num,NO):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./background/heart.png")
        self.rect = self.image.get_rect()
        self.rect.y = 3
        self.rect.width *= 0.5
        self.rect.height *= 0.5
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        self.num = num
        self.NO = NO

    def update(self):
        self.rect.x =HP_begin + self.rect.width * self.num +1
        for i in range (0,5) :
            if HPi >= self.NO:
                self.kill()


#初始化玩家角色
hero = Hero(3)
#初始化血量
HP1 = Hero_hp(0,5)
HP2 = Hero_hp(1,4)
HP3 = Hero_hp(2,3)
HP4 = Hero_hp(3,2)
HP5 = Hero_hp(4,1)
MAXHP = 5

#初始化敌机2子弹

#初始化按钮
playbutton = Button1(600,400,buttonflag1)
exitbutton = Button2(600,500,buttonflag1)
#初始化背景
bg = Background()
bg2 = Background()
bg2.rect.y = bg2.rect.height
pbg1 = PlayBackground()
#初始化精灵组
hero_group = pygame.sprite.Group()
enemy_group1 = pygame.sprite.Group()
enemy_group2 = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
e2bullet_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
button_group1 = pygame.sprite.Group()
pbg_group = pygame.sprite.Group()
explode_group = pygame.sprite.Group()
hero_group.add(hero)
bg_group.add(bg,bg2,HP1,HP2,HP3,HP4,HP5)
pbg_group.add(pbg1)
button_group1.add(playbutton,exitbutton)
# main game loop
while True:
    #设置刷新频率
    pygame.mixer.music.load("./music/nizhan.mp3")
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1,0)
    while s == 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if buttonflag1 == 1:
                        s = 2
                    if buttonflag1 == 2:
                        pygame.quit()
                        exit()
            
        for group in [pbg_group,button_group1]:
            group.update()
            group.draw(screen)
        #字符绘制
        screen.blit(score1_fmt,score1_rect)
        screen.blit(score2_fmt,score2_rect)
        screen.blit(score3_fmt,score3_rect)
        pygame.display.update()
    #背景音乐
    pygame.mixer.music.load("./music/Alan Walker - Spectre.flac")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1,0)
    while s == 2:
        clock.tick(60)
        # set event
        for event in pygame.event.get():
            if event.type == COUNT:
                count += 1
                if count % 2 == 0:                     #添加敌机种类数量
                    enemy_group1.add(Enemy1(randint(1,4)))
                if count % 8 == 0:
                    enemy_group2.add(Enemy2(3,3,enemy2x))
                if count == 100:
                    count = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:     #游戏暂停
                    pass
            if event.type == pygame.QUIT:
                
                pygame.quit()
                exit()
       
        #碰撞检测
        enemycollision0 = pygame.sprite.groupcollide(enemy_group1,hero_group,True,False)
        for enemy in enemycollision0.keys():
            explode = Explode()
            explode.rect.x = enemy.rect.x-40
            explode.rect.y = enemy.rect.y-35
            explode_group.add(explode)
            HPi += 1
        enemycollision1 = pygame.sprite.groupcollide(enemy_group2,hero_group,True,False)
        for enemy in enemycollision1.keys():
            explode = Explode()
            explode.rect.x = enemy.rect.x-40
            explode.rect.y = enemy.rect.y-35
            explode_group.add(explode)
            HPi += 2
        if HPi >= MAXHP:
            screen.blit(death_fmt,death_rect)
            j = 0
            k = 0
            ####更新排行榜
            arrayscore = read_txt(r'score.txt')[0].split('f')
            for i in range(0,len(arrayscore)):
                #判断当前获取分数是否大于排行榜上分数
                if score > int(arrayscore[i]):
                    j = arrayscore[i]
                    arrayscore[i] = str(score)
                    score = 0
                if int(j) > int(arrayscore[i]):
                    k = arrayscore[i]
                    arrayscore[i] = str(j)
                    j = k
            for i in range(0,len(arrayscore)):
                if i == 0:
                    write_txt(arrayscore[i]+'f','w',r'score.txt')
                else:
                    if i == 2 :
                        write_txt(arrayscore[i],'a',r'score.txt')
                    else : 
                        write_txt(arrayscore[i]+'f','a',r'score.txt')
            pygame.display.update()
            pygame.mixer.music.load("./music/defeat.mp3")
            pygame.mixer.music.set_volume(2)
            pygame.mixer.music.play(-1,0)
            sleep(5)
            pygame.quit()
            exit()
        bulletcollision2 = pygame.sprite.groupcollide(enemy_group2,bullet_group,False,True)
        for enemy in bulletcollision2.keys():
            enemy.HP -= 1
            if enemy.HP == 0:
                explode = Explode()
                explode.rect.x = enemy.rect.x-40
                explode.rect.y = enemy.rect.y-35
                explode_group.add(explode)
                score += 4
        bulletcollision1 = pygame.sprite.groupcollide(enemy_group1,bullet_group,True,True)
        for enemy in bulletcollision1.keys():
            explode = Explode()
            explode.rect.x = enemy.rect.x-40
            explode.rect.y = enemy.rect.y-35
            explode_group.add(explode)
            score += 2
        bulletcollision3 = pygame.sprite.groupcollide(e2bullet_group,hero_group,True,False)
        for enemy in bulletcollision3.keys():
            explode = Explode()
            explode.rect.x = enemy.rect.x-40
            explode.rect.y = enemy.rect.y-35
            explode_group.add(explode)
            HPi += 1
        #屏幕更新
        for group in [bg_group,hero_group,enemy_group1,enemy_group2,bullet_group,explode_group,e2bullet_group]:
            group.update()
            group.draw(screen)
        #字符显示
        screen.blit(hpstr_fmt,hpstr_rect) #HP：
        screen.blit(scorestr_fmt,scorestr_rect)  #得分字符
        scoref_fmt = scoref.render(str(score),1,(255,255,255))
        scoref_rect = scoref_fmt.get_rect()
        scoref_rect.x = 80
        scoref_rect.y = -4
        screen.blit(scoref_fmt,scoref_rect)
        pygame.display.update()



