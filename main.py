import pygame
import random
import sys  # 导入sys模块以便使用exit函数

# 游戏窗口大小
WIDTH = 800
HEIGHT = 600 + 300 - 80 - 30
# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWNISH_YELLOW = (205, 133, 63)
BROWNISH_YELLOW_PLUS = (153, 76, 0)
DarkSlateBlue = (72, 61, 139)

# 卡槽容量
SLOT_CAPACITY = 7

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("类似羊了个羊的游戏")
clock = pygame.time.Clock()


# 加载开始页面背景图片
start_background = pygame.image.load('start_background.jpg')
start_background = pygame.transform.scale(start_background, (WIDTH, HEIGHT))


# 加载游戏页面背景图片
game_background = pygame.image.load('game_background.jpg')
game_background = pygame.transform.scale(game_background, (WIDTH, HEIGHT))

# 加载成功页面背景图片
success_background = pygame.image.load('success_background.jpg')
success_background = pygame.transform.scale(success_background, (WIDTH, HEIGHT))

# 加载失败页面背景图片
fail_background = pygame.image.load('fail_background.jpg')
fail_background = pygame.transform.scale(fail_background, (WIDTH, HEIGHT))

# 加载道具图片
prop_image = pygame.image.load('clock.jpg')
prop_image = pygame.transform.scale(prop_image, (50, 50))


# 游戏元素类
class Card:
    def __init__(self, x, y, img_path, layer=0):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.is_selected = False
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.layer = layer  # 表示图块的层，0为最底层

    def is_above(self, other):
        # 判断当前图块是否在另一个图块之上
        return self.rect.colliderect(other.rect) and self.layer < other.layer


# 生成游戏卡片布局
def generate_cards():
    cards = []
    img_paths = [f'pattern_{i}.png' for i in range(1, 11)] * 3
    random.shuffle(img_paths)
    x = (WIDTH - (135 * 4)) // 2
    y = (HEIGHT - (135 * 3)) // 2
    num_blocks = 0
    index = 0
    while num_blocks < 10:
        for layer in range(3):
            card = Card(x, y, img_paths[index], layer)
            cards.append(card)
            if layer == 2:
                x += 135
            else:
                x += 10
            index += 1
            if index >= len(img_paths):
                index = 0
        if num_blocks % 4 == 3:
            x = (WIDTH - (135 * 4)) // 2
            y += 135
        num_blocks += 1
    return cards


# 绘制按钮
def draw_button(text, x, y, width, height, mouse_over=False, mouse_down=False):
    button_color = BROWNISH_YELLOW
    if mouse_over:
        button_color = RED
    if mouse_down:
        button_color = (160, 0, 0)
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    font = pygame.font.SysFont("SimSun", 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


# 绘制开始页面
def draw_start_page():
    screen.blit(start_background, (0, 0))
    start_button_x = WIDTH / 2 - 100
    start_button_y = HEIGHT / 2 - 50
    end_button_x = WIDTH / 2 - 100
    end_button_y = HEIGHT / 2 + 50
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    start_button_pressed = False
    end_button_pressed = False
    if start_button_x <= mouse_pos[0] <= start_button_x + 200 and start_button_y <= mouse_pos[1] <= start_button_y + 50:
        if mouse_buttons[0]:
            start_button_pressed = True
        draw_button("开始游戏", start_button_x, start_button_y, 200, 50, mouse_over=True, mouse_down=start_button_pressed)
    else:
        draw_button("开始游戏", start_button_x, start_button_y, 200, 50)
    if end_button_x <= mouse_pos[0] <= end_button_x + 200 and end_button_y <= mouse_pos[1] <= end_button_y + 50:
        if mouse_buttons[0]:
            end_button_pressed = True
        draw_button("结束游戏", end_button_x, end_button_y, 200, 50, mouse_over=True, mouse_down=end_button_pressed)
    else:
        draw_button("结束游戏", end_button_x, end_button_y, 200, 50)


# 绘制游戏页面
def draw_game_page(cards, slot, remaining_time):
    screen.blit(game_background, (0, 0))
    new_cards = []
    for card in cards:
        if not card.is_selected:
            screen.blit(card.img, card.rect)
            new_cards.append(card)
    cards = new_cards
    # 绘制卡槽
    slot_x = (WIDTH - (100 * SLOT_CAPACITY)) // 2
    slot_y = HEIGHT - 150
    pygame.draw.rect(screen, BROWNISH_YELLOW, (slot_x, slot_y, 100 * SLOT_CAPACITY, 100))
    # 给卡槽添加装饰，这里简单地在卡槽周围绘制一个白色边框
    pygame.draw.rect(screen, BROWNISH_YELLOW_PLUS, (slot_x - 5, slot_y - 5, 100 * SLOT_CAPACITY + 10, 100 + 10), 5)
    for i, card in enumerate(slot):
        screen.blit(card.img, (slot_x + i * 100, slot_y))

    # 显示道具图片
    prop_x = (WIDTH - prop_image.get_width()) // 2
    prop_y = (HEIGHT - prop_image.get_height()) // 2 - (135 * 3) // 2 - 30
    screen.blit(prop_image, (prop_x, prop_y))

    # 显示剩余时间
    font = pygame.font.SysFont("SimSun", 36)
    text_color = RED if remaining_time <= 10 else WHITE
    text_surface = font.render(f"{remaining_time}秒", True, text_color)
    text_rect = text_surface.get_rect(x = 10, y = 10)
    screen.blit(text_surface, text_rect)


# 绘制成功页面
def draw_success_page():
    screen.blit(success_background, (0, 0))
    font = pygame.font.SysFont("SimSun", 72)
    text_surface = font.render("你真厉害！", True, BROWNISH_YELLOW)
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(text_surface, text_rect)

    restart_button_x = WIDTH / 2 - 100
    restart_button_y = HEIGHT / 2 - 50
    end_button_x = WIDTH / 2 - 100
    end_button_y = HEIGHT / 2 + 50
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    restart_button_pressed = False
    end_button_pressed = False
    if restart_button_x <= mouse_pos[0] <= restart_button_x + 200 and restart_button_y <= mouse_pos[1] <= restart_button_y + 50:
        if mouse_buttons[0]:
            restart_button_pressed = True
        draw_button("重新开始", restart_button_x, restart_button_y, 200, 50, mouse_over=True, mouse_down=restart_button_pressed)
    else:
        draw_button("重新开始", restart_button_x, restart_button_y, 200, 50)
    if end_button_x <= mouse_pos[0] <= end_button_x + 200 and end_button_y <= mouse_pos[1] <= end_button_y + 50:
        if mouse_buttons[0]:
            end_button_pressed = True
        draw_button("退出游戏", end_button_x, end_button_y, 200, 50, mouse_over=True, mouse_down=end_button_pressed)
    else:
        draw_button("退出游戏", end_button_x, end_button_y, 200, 50)


# 绘制失败页面
def draw_fail_page():
    screen.blit(fail_background, (0, 0))
    font = pygame.font.SysFont("SimSun", 72)
    text_surface = font.render("失败了，再尝试一次吧", True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    screen.blit(text_surface, text_rect)

    restart_button_x = WIDTH / 2 - 100
    restart_button_y = HEIGHT / 2 - 50
    end_button_x = WIDTH / 2 - 100
    end_button_y = HEIGHT / 2 + 50
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    restart_button_pressed = False
    end_button_pressed = False
    if restart_button_x <= mouse_pos[0] <= restart_button_x + 200 and restart_button_y <= mouse_pos[1] <= restart_button_y + 50:
        if mouse_buttons[0]:
            restart_button_pressed = True
        draw_button("重新开始", restart_button_x, restart_button_y, 200, 50, mouse_over=True, mouse_down=restart_button_pressed)
    else:
        draw_button("重新开始", restart_button_x, restart_button_y, 200, 50)
    if end_button_x <= mouse_pos[0] <= end_button_x + 200 and end_button_y <= mouse_pos[1] <= end_button_y + 50:
        if mouse_buttons[0]:
            end_button_pressed = True
        draw_button("退出游戏", end_button_x, end_button_y, 200, 50, mouse_over=True, mouse_down=end_button_pressed)
    else:
        draw_button("退出游戏", end_button_x, end_button_y, 200, 50)


# 处理卡片点击
def handle_click(cards, slot):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected_count = sum(1 for card in slot)
    if selected_count < SLOT_CAPACITY:
        for card in reversed(cards):
            if card.rect.collidepoint(mouse_x, mouse_y) and not card.is_selected:
                if not any(card.is_above(other) for other in cards if other.is_selected):
                    card.is_selected = True
                    break


# 检查是否可消除
def check_clear(slot):
    to_delete = []
    for i in range(len(slot) - 2):
        img1 = pygame.image.tostring(slot[i].img, 'RGBA')
        img2 = pygame.image.tostring(slot[i + 1].img, 'RGBA')
        img3 = pygame.image.tostring(slot[i + 2].img, 'RGBA')
        if img1 == img2 == img3:
            to_delete.append(i)
            to_delete.append(i + 1)
            to_delete.append(i + 2)
    to_delete = sorted(set(to_delete), reverse=True)
    for index in to_delete:
        del slot[index]
    return len(to_delete) > 0


# 游戏主循环
# 游戏主循环
def main():
    running = True
    in_start_page = True
    in_game_page = False
    in_success_page = False
    in_fail_page = False
    cards = []
    slot = []
    start_time = 0

    print("程序开始运行...")  # 添加打印语句

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("游戏退出...")  # 添加打印语句
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if in_start_page:
                    start_button_x = WIDTH / 2 - 100
                    start_button_y = HEIGHT / 2 - 50
                    end_button_x = WIDTH / 2 - 100
                    end_button_y = HEIGHT / 2 + 50
                    if start_button_x <= mouse_x <= start_button_x + 200 and start_button_y <= mouse_y <= start_button_y + 50:
                        in_start_page = False
                        in_game_page = True
                        start_time = pygame.time.get_ticks()
                        cards = generate_cards()
                elif in_game_page:
                    prop_x = (WIDTH - prop_image.get_width()) // 2
                    prop_y = (HEIGHT - prop_image.get_height()) // 2 - (135 * 3) // 2 - 30
                    if prop_x <= mouse_x <= prop_x + prop_image.get_width() and prop_y <= mouse_y <= prop_y + prop_image.get_height():
                        start_time -= 10000
                    handle_click(cards, slot)
                    new_slot = []
                    for card in cards:
                        if card.is_selected:
                            card.is_selected = False
                            new_slot.append(card)
                            cards = [c for c in cards if c!= card]
                    slot.extend(new_slot)
                    if check_clear(slot):
                        pass
                    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                    remaining_time = 60 - elapsed_time
                    if remaining_time <= 0:
                        in_game_page = False
                        in_fail_page = True
                    elif not cards and not slot:
                        in_game_page = False
                        in_success_page = True
                elif in_success_page:
                    restart_button_x = WIDTH / 2 - 100
                    restart_button_y = HEIGHT / 2 - 50
                    end_button_x = WIDTH / 2 - 100
                    end_button_y = HEIGHT / 2 + 50
                    if restart_button_x <= mouse_x <= restart_button_x + 200 and restart_button_y <= mouse_y <= restart_button_y + 50:
                        in_success_page = False
                        in_start_page = True
                        cards = []
                        slot = []
                    elif end_button_x <= mouse_x <= end_button_x + 200 and end_button_y <= mouse_y <= end_button_y + 50:
                        running = False
                elif in_fail_page:
                    restart_button_x = WIDTH / 2 - 100
                    restart_button_y = HEIGHT / 2 - 50
                    end_button_x = WIDTH / 2 - 100
                    end_button_y = HEIGHT / 2 + 50
                    if restart_button_x <= mouse_x <= restart_button_x + 200 and restart_button_y <= mouse_y <= restart_button_y + 50:
                        in_fail_page = False
                        in_start_page = True
                        cards = []
                        slot = []
                    elif end_button_x <= mouse_x <= end_button_x + 200 and end_button_y <= mouse_y <= end_button_y + 50:
                        running = False


        if in_start_page:
            print("绘制开始页面...")  # 添加打印语句
            draw_start_page()
        elif in_game_page:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = 60 - elapsed_time
            print("绘制游戏页面...")  # 添加打印语句
            draw_game_page(cards, slot, remaining_time)
        elif in_success_page:
            print("绘制成功页面...")  # 添加打印语句
            draw_success_page()
        elif in_fail_page:
            print("绘制失败页面...")  # 添加打印语句
            draw_fail_page()


        pygame.display.update()
        clock.tick(60)


    print("程序结束...")  # 添加打印语句

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序运行时发生错误: {e}")  # 捕获并打印异常信息
        sys.exit(1)  # 退出程序并返回错误码