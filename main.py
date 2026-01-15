import pygame
import random
import asyncio

# Cấu hình
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hoán vị chai nước - Thử thách Logic")

# Màu sắc
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
HIGHLIGHT = (255, 0, 255)
GRAY = (200, 200, 200)
BUTTON_COLOR = (50, 200, 50)

BOTTLE_COLORS = [
    (255, 50, 50),   (50, 255, 50),   
    (50, 50, 255),   (255, 215, 0)
]

def get_vietnamese_font(size, bold=False):
    return pygame.font.SysFont("sans-serif", size, bold=bold)

font_text = get_vietnamese_font(24, bold=True)
font_big = get_vietnamese_font(32, bold=True)

class WaterSortSwap:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.secret_order = list(BOTTLE_COLORS)
        random.shuffle(self.secret_order)
        self.player_order = list(self.secret_order)
        while self.player_order == self.secret_order:
            random.shuffle(self.player_order)
        self.selected_idx = None
        self.moves_left = 6
        self.correct_count = 0
        self.game_over = False
        self.won = False
        self.update_correct_count()

    def update_correct_count(self):
        count = 0
        for i in range(4):
            if self.player_order[i] == self.secret_order[i]:
                count += 1
        self.correct_count = count

    def draw_bottle(self, x, y, color, is_selected=False):
        rect = pygame.Rect(x, y, 60, 130)
        pygame.draw.rect(screen, color, rect, border_radius=12)
        border_color = HIGHLIGHT if is_selected else (50, 50, 50)
        thickness = 5 if is_selected else 2
        pygame.draw.rect(screen, border_color, rect, thickness, border_radius=12)
        pygame.draw.rect(screen, border_color, (x + 15, y - 15, 30, 15), thickness)

    def handle_click(self, pos):
        if self.game_over:
            if 225 <= pos[0] <= 375 and 520 <= pos[1] <= 570:
                self.reset_game()
                return
        if self.game_over: return
        for i in range(4):
            x_pos = 100 + i * 110
            if x_pos <= pos[0] <= x_pos + 60 and 220 <= pos[1] <= 350:
                if self.selected_idx is None:
                    self.selected_idx = i
                else:
                    if self.selected_idx != i:
                        self.player_order[self.selected_idx], self.player_order[i] = \
                            self.player_order[i], self.player_order[self.selected_idx]
                        self.moves_left -= 1
                        self.update_correct_count()
                        if self.player_order == self.secret_order:
                            self.won = True
                            self.game_over = True
                        elif self.moves_left <= 0:
                            self.game_over = True
                    self.selected_idx = None
                break

    def draw(self):
        screen.fill(WHITE)
        move_txt = font_text.render(f"Lượt còn lại: {self.moves_left}", True, (200, 0, 0))
        hint_txt = font_text.render(f"Số chai đúng vị trí: {self.correct_count}", True, (0, 100, 200))
        screen.blit(move_txt, (30, 20))
        screen.blit(hint_txt, (30, 60))
        pygame.draw.rect(screen, GRAY, (80, 100, 440, 80), border_radius=15)
        label_hidden = font_text.render("THỨ TỰ ẨN", True, (80, 80, 80))
        screen.blit(label_hidden, (WIDTH//2 - label_hidden.get_width()//2, 125))
        for i in range(4):
            offset_y = -20 if i == self.selected_idx else 0
            self.draw_bottle(100 + i * 110, 220 + offset_y, self.player_order[i], i == self.selected_idx)
        if self.game_over:
            res_txt = "CHIẾN THẮNG!" if self.won else "BẠN ĐÃ HẾT LƯỢT!"
            res_color = (0, 150, 0) if self.won else (200, 0, 0)
            img = font_big.render(res_txt, True, res_color)
            screen.blit(img, (WIDTH//2 - img.get_width()//2, 400))
            btn_rect = pygame.Rect(225, 520, 150, 50)
            pygame.draw.rect(screen, BUTTON_COLOR, btn_rect, border_radius=10)
            play_again_txt = font_text.render("Chơi lại", True, WHITE)
            screen.blit(play_again_txt, (btn_rect.centerx - play_again_txt.get_width()//2, 
                                          btn_rect.centery - play_again_txt.get_height()//2))
            if not self.won:
                ans_txt = font_text.render("ĐÁP ÁN:", True, BLACK)
                screen.blit(ans_txt, (120, 470))
                for i in range(4):
                    pygame.draw.rect(screen, self.secret_order[i], (220 + i * 60, 475, 40, 20), border_radius=5)


async def main():
    game = WaterSortSwap()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        game.draw()
        pygame.display.flip()
        

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())