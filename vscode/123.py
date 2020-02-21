import math
import pygame
from pygame.locals import *
import sys
import time
import traceback
import chess
import random


# 初始化
pygame.init()
try:
    pygame.mixer.init()
except:
    print("您没有音频设备！")
    raise Exception

bg_size = width, height = 474, 663
screen = pygame.display.set_mode(bg_size)
bg_rect = screen.get_rect()
pygame.display.set_caption("象棋小游戏")

# 初始化音乐
pygame.mixer.Sound('.\.vscode\music\Mario.wav')

#初始化图片
chess_pan_img = pygame.image.load('./pic/chess_bg.png').convert()
chess_select1_img = pygame.image.load('./pic/selected.png').convert()
chess_select2_img = pygame.image.load('./pic/selected2.png').convert()

# 初始化移动，翻棋子，吃棋子
choosed = False

# 初始化字体
my_font = pygame.font.Font('./font/simhei.ttf', 25)

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 象棋 1*将 + 2*（士+象+马+车+炮）+ 5 * 兵 = 一共16子*2 = 32 子
chess_class = []  # [shi_chess,xiang_chess,ma_chess,che_chess,pao_chess]*2
for j in range(2):
    for i in range(2):
        chess_class.append(ChessPieces.ShiChess(bg_rect))
        chess_class.append(ChessPieces.XiangChess(bg_rect))
        chess_class.append(ChessPieces.MaChess(bg_rect))
        chess_class.append(ChessPieces.CheChess(bg_rect))
        chess_class.append(ChessPieces.PaoChess(bg_rect))

    chess_class.append(ChessPieces.JiangChess(bg_rect))
    for i in range(5):
        chess_class.append(ChessPieces.ZuChess(bg_rect))

# 一半的棋子为黑色
for i in range(len(chess_class)//2):
    chess_class[i].role = ChessPieces.BLACK_ROLE

running = True

# 首先翻牌的为type 为 0
player_role = ChessPieces.BLACK_ROLE


def getChessList():
    # 产生随机数 0-31
    resultList = random.sample(range(0, 32), 32)
    j = 0
    #print('chess_class 的长度 %d  resultList 的长度 %d' % (len(chess_class),len(resultList)))
    for i in resultList:
        # print((i,j,chess_class[j].type))
        chess_class[j].position = (86+(i % 4)*90,
                                   66+((i//4))*71)
        chess_class[j].rect.left = 86+(i % 4)*90
        chess_class[j].rect.top = 66+((i//4))*71
        # print(chess_class[j].position)
        j += 1
    return chess_class


def is_chess_clicked(chess_list, event):
    for each in chess_list:
        if (each.rect.collidepoint(event.pos)):
            return each
    return None


def operation_completed():
    global player_role
    if player_role == ChessPieces.BLACK_ROLE:
        player_role = ChessPieces.RED_ROLE
    else:
        player_role = ChessPieces.BLACK_ROLE


def draw_text(text, font_color, center):
    mytext = my_font.render(text, True, font_color)
    text_rect = mytext.get_rect()
    text_rect.center = center
    screen.blit(mytext, text_rect)


def main():
    global player_role
    overturn_count = 0
    # 初始化音乐
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    # 获得打乱之后，并且有位置信息的对象数组
    chess_list = getChessList()
    selected_img_rect = chess_select1_img.get_rect()
    selected_img_rect.left = -20
    select_chess = None
    #is_start = False

    player1_role = ChessPieces.BLACK_ROLE
    player2_role = ChessPieces.BLACK_ROLE

    player1_color = BLACK
    player2_color = BLACK
    global running

    while running:

        # 首先绘制棋盘
        screen.blit(chess_pan_img, (10, 10))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 按下鼠标左键
                    # print(event.pos)
                    selected = is_chess_clicked(chess_list, event)
                    # print(selected)
                    if selected is not None:
                        # 本次点击点击到了棋子
                        if selected.state == ChessPieces.CHOOSED_STATE:
                            pass
                        elif selected.state == ChessPieces.ACTIVE_STATE:
                            if player_role == selected.role:
                                # 当前用户点击自己的棋子
                                select_chess = selected
                                selected.state = ChessPieces.ACTIVE_STATE
                                selected_img_rect.left = selected.rect.left + 4
                                selected_img_rect.top = selected.rect.top + 4
                            else:
                                # 当前用户点击别人的棋子
                                if select_chess is not None:
                                    # 判断是否可以吃该子
                                    if select_chess.eat(selected, event.pos, chess_list):
                                        operation_completed()
                                        select_chess = None

                        elif selected.state == ChessPieces.HIDDEN_STATE:
                            # 翻转
                            selected.state = ChessPieces.ACTIVE_STATE
                            selected_img_rect.left = selected.rect.left + 4
                            selected_img_rect.top = selected.rect.top + 4
                            # is_start = True  暂时认为该标签无用
                            if overturn_count == 0:
                                player_role = selected.role
                            # 统计翻转的次数
                            overturn_count += 1
                            # 如果当前翻出的是对方的棋子，则 对方自动选中该子
                            if selected.role is not player_role:
                                select_chess = selected
                            else:
                                select_chess = None
                            # 翻转之后相当于一次操作完成
                            operation_completed()
                    else:
                        # 本次点击没有点击棋子，只是点击到了棋盘
                        print('本次点击没有点击棋子，只是点击到了棋盘')
                        print(select_chess)

                        if select_chess is not None:
                            # 判断被选中的棋子是否可以移动到当前位置
                            if select_chess.move(event.pos):
                                operation_completed()
                                select_chess = None

        # 绘制棋子
        for each in chess_list:
            # pass
            if each.state is not ChessPieces.DEAD_STATE:
                screen.blit(each.getImage(each.role), each.rect)
            # print(each.position)
        # 绘制被选中的图标
        # print(player_role)
        if player_role == ChessPieces.BLACK_ROLE:
            screen.blit(chess_select1_img, selected_img_rect)
        else:
            screen.blit(chess_select2_img, selected_img_rect)

        # 绘制当前玩家提示
        marked_words = ''
        font_color = RED
        if overturn_count == 1:
            print('---------------------------------111111')
            player1_role = player_role
            if player1_role == ChessPieces.BLACK_ROLE:
                player1_color = BLACK
            else:
                player1_color = RED

        if overturn_count == 2:
            print('---------------------------------222222')
            player2_role = player_role
            if player2_role == ChessPieces.BLACK_ROLE:
                player2_color = BLACK
            else:
                player2_color = RED

        if player_role == player1_role:
            marked_words = '玩家1'
            font_color = player1_color
        else:
            marked_words = '玩家2'
            font_color = player2_color
        # 确定颜色
        if overturn_count == 0:
            marked_words = '未选定颜色，请玩家1翻牌'
            font_color = GREEN

        draw_text(marked_words, font_color, (width // 2, 25))

        # 判断游戏是否结束
        # 方法，计算棋盘上存活的棋子数量，如果为零就，停止
        black_count = 0
        red_count = 0
        for each in chess_list:
            if each.state == ChessPieces.ACTIVE_STATE or each.state == ChessPieces.HIDDEN_STATE:
                if each.role == ChessPieces.BLACK_ROLE:
                    black_count += 1
                else:
                    red_count += 1

        if black_count == 0:
            # 红方胜利
            draw_text('红方胜利！', RED, (width//2, height//2))
        elif red_count == 0:
            # 黑方胜利
            draw_text('黑方胜利', BLACK, (width//2, height//2))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print("游戏正常退出")
    except:
        print("游戏退出异常")
        traceback.print_exc()
        pygame.quit()
        input()


RED_ROLE = 0
BLACK_ROLE = 1

HIDDEN_STATE = 3
ACTIVE_STATE = 4
DEAD_STATE = 5
CHOOSED_STATE = 6

JIANG_TYPE = 11
SHI_TYPE = 12
XIANG_TYPE = 13
CHE_TYPE = 14
MA_TYPE = 15
PAO_TYPE = 16
ZU_TYPE = 17

to_left = (-90, 0)
to_right = (90, 0)
to_up = (0, -66)
to_down = (0, 66)

bg_image = pygame.image.load('./pic/blankchess.png')


def can_eat(typea, typeb):
    if typea in (JIANG_TYPE, PAO_TYPE):
        return True
    elif typea in (SHI_TYPE, XIANG_TYPE, MA_TYPE, CHE_TYPE):
        if typea <= typeb:
            return True
    elif typea == ZU_TYPE:
        if typeb == JIANG_TYPE or typeb == ZU_TYPE:
            return True
    return False


def can_move_one_step(self, pos):
    # 首先判断移动方向，然后进行移动
    # 判断移动方向
    # 判断是否在棋盘之内
    if pos[0] < 80 or pos[0] > 399 or pos[1] < 63 or pos[1] > 596:
        print("点击超出了范围")
    elif self.rect.left - 90 < pos[0] < self.rect.left - 50 and self.rect.top < pos[1] < self.rect.top + 50:
        # 需要向左移动一位
        self.rect.left -= 90
        print('需要向左移动一位')
        return True
    elif self.rect.left < pos[0] < self.rect.left + 40 and self.rect.top - 70 < pos[1] < self.rect.top - 40:
        # 需要向上移动一位
        self.rect.top -= 71
        print('需要向上移动一位')
        return True
    elif self.rect.left + 90 < pos[0] < self.rect.left + 130 and self.rect.top < pos[1] < self.rect.top + 40:
        # 需要向右移动一位
        self.rect.left += 90
        print('需要向右移动一位')
        return True
    elif self.rect.left < pos[0] < self.rect.left + 40 and self.rect.top + 70 < pos[1] < self.rect.top + 110:
        # 需要向下移动一位
        self.rect.top += 71
        print('需要向下移动一位')
        return True

# -----------------------------------------------------------------------------------------1111 将


class JiangChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rshuai.png')
        self.b_image = pygame.image.load('./pic/bjiang.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = JIANG_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False

# ----------------------------------------------------------------------------------------2222 士


class ShiChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rshi.png')
        self.b_image = pygame.image.load('./pic/bshi.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = SHI_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False

# ----------------------------------------------------------------------------------------3333 象


class XiangChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rxiang.png')
        self.b_image = pygame.image.load('./pic/bxiang.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = XIANG_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False

# ----------------------------------------------------------------------------------------4444 马


class MaChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rma.png')
        self.b_image = pygame.image.load('./pic/bma.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = MA_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                True
            else:
                print('点击位置不在范围内，无法吃子')
        return False

# -----------------------------------------------------------------------------------------5555 车


class CheChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rche.png')
        self.b_image = pygame.image.load('./pic/bche.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = CHE_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False
# ----------------------------------------------------------------------------------------5555 炮


class PaoChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rpao.png')
        self.b_image = pygame.image.load('./pic/bpao.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = PAO_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.can_move_and_eat(enemy_chess, pos, chess_list):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False

    def can_move_and_eat(self, enemy_chess, pos, chess_list):
        # 首先判断，pos 和当前棋子是否在同一行或同一列
        # 然后判断，两个棋子之间有几个棋子
        if self.rect.left - 10 < enemy_chess.rect.left < self.rect.left + 50:
            # 说明在同一列
            count = 0
            for each in chess_list:
                if self.rect.left - 10 < each.rect.left < self.rect.left + 50 \
                        and min(self.rect.center[1], enemy_chess.rect.center[1]) < \
                        each.rect.center[1] < max(self.rect.center[1], enemy_chess.rect.center[1]):
                    count += 1
            if count == 1:
                return True
        elif self.rect.top - 10 < enemy_chess.rect.top < self.rect.top + 50:
            # 说明在同一行
            count = 0
            for each in chess_list:
                if self.rect.top - 10 < each.rect.top < self.rect.top + 50 and \
                    min(self.rect.center[0], enemy_chess.rect.center[0]) < \
                        each.rect.center[0] < max(self.rect.center[0], enemy_chess.rect.center[0]):
                    count += 1
            if count == 1:
                return True
        return False

# ----------------------------------------------------------------------------------------5555 卒


class ZuChess:
    def __init__(self, rect):
        self.r_image = pygame.image.load('./pic/rbing.png')
        self.b_image = pygame.image.load('./pic/bzu.png')
        self.position = x, y = 86, 66
        self.state = HIDDEN_STATE
        self.type = ZU_TYPE
        self.role = RED_ROLE
        self.rect = self.b_image.get_rect()

    def getImage(self, role):
        if self.state == HIDDEN_STATE:
            return bg_image
        elif self.state == DEAD_STATE:
            return -1
        else:
            if role == RED_ROLE:
                return self.r_image
            elif role == BLACK_ROLE:
                return self.b_image
            else:
                print('传入参数有误，无法判断是红方还是黑方！')
                return -1

    def move(self, pos):
        return can_move_one_step(self, pos)

    # 将 可以吃 其它所有
    # 是否可吃需要满足两个条件
    # 1、是否满足该子的行走规律
    # 2、是否满足该子的吃子规律
    def eat(self, enemy_chess, pos, chess_list):
        if can_eat(self.type, enemy_chess.type):
            if self.move(pos):
                self.rect.left = enemy_chess.rect.left
                self.rect.top = enemy_chess.rect.top
                enemy_chess.state = DEAD_STATE
                enemy_chess.rect.left = -100
                enemy_chess.rect.top = -100
                return True
            else:
                print('点击位置不在范围内，无法吃子')
        return False
