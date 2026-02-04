"""
🎮 Bottle Random Game - 2 Chế Độ Chơi
- Chế độ 1: Water Sort Puzzle (Xếp chai nước)
- Chế độ 2: Bottle Swap Challenge (Hoán vị chai)
"""

import pygame
import random
import time
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🧪 Bottle Random Game - Chọn Chế Độ Chơi")

# Colors - Modern palette
COLORS = {
    "background": (240, 245, 255),
    "surface": (255, 255, 255),
    "primary": (99, 102, 241),
    "secondary": (139, 92, 246),
    "accent": (245, 158, 11),
    "success": (16, 185, 129),
    "error": (239, 68, 68),
    "text": (31, 41, 55),
    "text_light": (156, 163, 175),
    "bottle_border": (55, 65, 81),
    "highlight": (251, 191, 36),
}

# Beautiful liquid colors with gradients
LIQUID_COLORS = {
    "R": {"main": (239, 68, 68), "light": (252, 165, 165)},
    "G": {"main": (34, 197, 94), "light": (134, 239, 134)},
    "B": {"main": (59, 130, 246), "light": (147, 197, 253)},
    "Y": {"main": (234, 179, 8), "light": (253, 224, 71)},
    "P": {"main": (168, 85, 247), "light": (216, 180, 254)},
    "O": {"main": (249, 115, 22), "light": (253, 186, 116)},
    "C": {"main": (6, 182, 212), "light": (103, 232, 249)},
    "M": {"main": (236, 72, 153), "light": (251, 182, 206)},
}

# Vietnamese text
TEXT = {
    "title": "Bottle Random Game", # Đổi emoji để tránh lỗi hiển thị trên một số máy
    "subtitle": "Chọn Chế Độ Chơi",
    "mode1": "Water Sort Puzzle",
    "mode2": "Bottle Swap",
    "mode1_desc": "Sắp xếp nước cùng màu vào 1 chai",
    "mode2_desc": "Đoán thứ tự bí mật của 4 chai",
    "back": "Quay Lại",
    "play": "Chơi Ngay",
    "win": "CHIẾN THẮNG!",
    "lose": "HẾT LƯỢT!",
    "moves": "Lượt:",
    "time": "Thời gian:",
    "score": "Điểm:",
    "correct": "Đúng vị trí:",
    "new_game": "Chơi Mới",
    "menu": "Menu",
    "hint": "Gợi ý",
    "undo": "Quay lại",
    "perfect": "HOÀN HẢO!",
    "great": "TUYỆT VỜI!",
    "good": "TỐT LẮM!",
    "easy": "Dễ",
    "medium": "Trung Bình",
    "hard": "Khó",
    "expert": "Chuyên Gia",
}

# --- FIX FONT TIẾNG VIỆT (CẢI TIẾN) ---
def get_vietnamese_font(size, bold=False):
    return pygame.font.Font("Arial.ttf", size)

class Particle:
    def __init__(self, x, y, color, velocity_x, velocity_y, life, size):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 0.2

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.life -= 1
        self.size = max(1, self.size * 0.95)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, spread=3, speed=5):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_var = random.uniform(1, speed)
            vx = math.cos(angle) * speed_var * spread
            vy = math.sin(angle) * speed_var * spread
            life = random.randint(20, 40)
            size = random.randint(3, 8)
            self.particles.append(Particle(x, y, color, vx, vy, life, size))

    def celebrate(self, center_x, center_y):
        colors = [
            (239, 68, 68), (34, 197, 94), (59, 130, 246),
            (234, 179, 8), (168, 85, 247), (249, 115, 22)
        ]
        for color in colors:
            for _ in range(5):
                self.emit(center_x, center_y, color, count=3, spread=2, speed=8)

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or tuple(min(c + 30, 255) for c in color)
        self.hovered = False
        self.scale = 1.0

    def draw(self, surface, font):
        target_scale = 1.05 if self.hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.2

        width = self.rect.width * self.scale
        height = self.rect.height * self.scale
        x = self.rect.centerx - width // 2
        y = self.rect.centery - height // 2
        scaled_rect = pygame.Rect(x, y, width, height)

        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, scaled_rect, border_radius=12)

        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

# ==================== MODE 1: WATER SORT PUZZLE ====================

class Bottle:
    def __init__(self, x, y, width, height, capacity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.colors = []
        self.target_x = x
        self.target_y = y
        self.selected = False
        self.anim_offset_y = 0
        self.target_anim_offset = 0

    def add_color(self, color):
        if len(self.colors) < self.capacity:
            self.colors.append(color)
            return True
        return False

    def remove_color(self):
        if self.colors:
            return self.colors.pop()
        return None

    def get_top_color(self):
        if self.colors:
            return self.colors[-1]
        return None

    def is_full(self):
        return len(self.colors) == self.capacity

    def is_empty(self):
        return not self.colors

    def is_sorted(self):
        if self.is_empty():
            return True
        if len(self.colors) != self.capacity:
            return False
        return len(set(self.colors)) == 1

    def update_animation(self):
        self.x += (self.target_x - self.x) * 0.3
        self.y += (self.target_y - self.y) * 0.3
        self.anim_offset_y += (self.target_anim_offset - self.anim_offset_y) * 0.3

    def select(self):
        self.selected = True
        self.target_anim_offset = -20

    def deselect(self):
        self.selected = False
        self.target_anim_offset = 0

    def draw(self, surface):
        self.update_animation()
        draw_y = self.y + self.anim_offset_y
        bottle_rect = pygame.Rect(self.x, draw_y, self.width, self.height)

        if self.colors:
            liquid_height = self.height / self.capacity
            for i, color_code in enumerate(self.colors):
                if color_code in LIQUID_COLORS:
                    color_data = LIQUID_COLORS[color_code]
                    liquid_rect = pygame.Rect(
                        self.x + 4,
                        draw_y + self.height - (i + 1) * liquid_height + 2,
                        self.width - 8,
                        liquid_height - 4
                    )
                    pygame.draw.rect(surface, color_data["main"], liquid_rect, border_radius=4)
                    highlight_rect = pygame.Rect(
                        self.x + 6,
                        draw_y + self.height - (i + 1) * liquid_height + 4,
                        (self.width - 12) // 3,
                        liquid_height - 8
                    )
                    pygame.draw.rect(surface, color_data["light"], highlight_rect, border_radius=2)

        outline_color = COLORS["highlight"] if self.selected else COLORS["bottle_border"]
        outline_width = 4 if self.selected else 3
        pygame.draw.rect(surface, outline_color, bottle_rect, outline_width, border_radius=8)

        neck_width = self.width * 0.5
        neck_height = 20
        neck_x = self.x + (self.width - neck_width) // 2
        neck_rect = pygame.Rect(neck_x, draw_y - neck_height, neck_width, neck_height)
        pygame.draw.rect(surface, outline_color, neck_rect, outline_width, border_radius=4)

class WaterSortGame:
    def __init__(self, num_bottles=6, capacity=4):
        self.num_bottles = num_bottles
        self.capacity = capacity
        self.color_codes = list(LIQUID_COLORS.keys())[:num_bottles-2]
        self.bottles = []
        self.selected_bottle = None
        self.undo_stack = []
        self.move_count = 0
        self.hints_remaining = 3
        self.hints_used = 0
        self.game_over = False
        self.won = False
        self.score = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.particle_system = ParticleSystem()
        self.winning_animation_timer = 0

        self._create_buttons()
        self._setup_game()

    def _create_buttons(self):
        button_y = 30
        self.buttons = {
            "new_game": Button(20, button_y, 120, 40, TEXT["new_game"], COLORS["primary"]),
            "hint": Button(150, button_y, 100, 40, TEXT["hint"], COLORS["accent"]),
            "undo": Button(260, button_y, 100, 40, TEXT["undo"], COLORS["secondary"]),
            "menu": Button(370, button_y, 80, 40, TEXT["menu"], COLORS["text"]),
        }

    def _setup_game(self):
        all_liquids = []
        for color_code in self.color_codes:
            for _ in range(self.capacity):
                all_liquids.append(color_code)
        random.shuffle(all_liquids)

        bottle_width = 70
        bottle_height = 220
        padding = 15
        start_x = (SCREEN_WIDTH - (self.num_bottles * bottle_width + (self.num_bottles - 1) * padding)) // 2
        start_y = 150

        self.bottles = []
        for i in range(self.num_bottles):
            x = start_x + i * (bottle_width + padding)
            bottle = Bottle(x, start_y, bottle_width, bottle_height, self.capacity)

            if i < len(self.color_codes):
                for _ in range(self.capacity):
                    if all_liquids:
                        bottle.add_color(all_liquids.pop(0))
            self.bottles.append(bottle)

        self.selected_bottle = None
        self.move_count = 0
        self.hints_remaining = 3
        self.hints_used = 0
        self.game_over = False
        self.won = False
        self.start_time = time.time()
        self.elapsed_time = 0
        self.undo_stack = []
        self.winning_animation_timer = 0

    def save_state(self):
        state = {
            "bottles": [[c for c in bottle.colors] for bottle in self.bottles],
            "selected": self.bottles.index(self.selected_bottle) if self.selected_bottle else None,
            "move_count": self.move_count,
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return False

        state = self.undo_stack.pop()
        for i, bottle in enumerate(self.bottles):
            bottle.colors = state["bottles"][i][:]
        if state["selected"] is not None:
            self.selected_bottle = self.bottles[state["selected"]]
            self.selected_bottle.select()
        else:
            self.selected_bottle = None
        self.move_count = state["move_count"]
        self.hints_remaining = max(0, self.hints_remaining + 1)
        return True

    def get_hint(self):
        if self.hints_remaining <= 0:
            return False
        self.hints_remaining -= 1
        self.hints_used += 1
        for i, source in enumerate(self.bottles):
            if source.is_empty():
                continue
            for j, dest in enumerate(self.bottles):
                if i == j:
                    continue
                if dest.is_empty() or dest.is_full():
                    continue
                if dest.get_top_color() != source.get_top_color():
                    continue
                source.select()
                return True
        return False

    def try_move(self, source, dest):
        if source.is_empty():
            return False
        if dest.is_full():
            return False
        color = source.get_top_color()
        if not dest.is_empty() and dest.get_top_color() != color:
            return False
        dest.add_color(source.remove_color())
        while (not source.is_empty() and not dest.is_full() and source.get_top_color() == color):
            dest.add_color(source.remove_color())
        return True

    def is_won(self):
        for bottle in self.bottles:
            if not bottle.is_empty() and not bottle.is_sorted():
                return False
        return True

    def handle_click(self, pos):
        for name, button in self.buttons.items():
            if button.is_hovered(pos):
                if name == "new_game":
                    self._setup_game()
                elif name == "hint":
                    self.get_hint()
                elif name == "undo":
                    self.undo()
                elif name == "menu":
                    return "menu"
                return True

        if self.game_over:
            return False

        for bottle in self.bottles:
            if (bottle.x <= pos[0] <= bottle.x + bottle.width and
                bottle.y <= pos[1] <= bottle.y + bottle.height):
                if self.selected_bottle is None:
                    if not bottle.is_empty():
                        self.selected_bottle = bottle
                        bottle.select()
                        self.particle_system.emit(
                            bottle.x + bottle.width // 2,
                            bottle.y + bottle.height,
                            COLORS["highlight"], count=5)
                else:
                    if self.selected_bottle == bottle:
                        self.selected_bottle.deselect()
                        self.selected_bottle = None
                    else:
                        self.save_state()
                        if self.try_move(self.selected_bottle, bottle):
                            self.move_count += 1
                            self.particle_system.emit(
                                bottle.x + bottle.width // 2,
                                bottle.y + bottle.height // 2,
                                LIQUID_COLORS.get(bottle.get_top_color(), COLORS["primary"])["main"], count=8)
                            if self.is_won():
                                self.won = True
                                self.game_over = True
                                self._calculate_score()
                                self.particle_system.celebrate(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                self.winning_animation_timer = 120
                        else:
                            if self.undo_stack:
                                self.undo_stack.pop()
                        self.selected_bottle.deselect()
                        self.selected_bottle = None
                return True
        return False

    def _calculate_score(self):
        base_score = 100 * len(self.bottles)
        time_bonus = max(0, 100 - int(self.elapsed_time))
        move_bonus = max(0, 50 - self.move_count)
        hint_penalty = self.hints_used * 10
        self.score = base_score + time_bonus + move_bonus - hint_penalty
        self.score = max(0, self.score)

    def update_hover(self, pos):
        for button in self.buttons.values():
            button.hovered = button.is_hovered(pos)

    def draw(self, surface):
        surface.fill(COLORS["background"])
        
        # --- FIX: Use correct font ---
        font_title = get_vietnamese_font(36)
        title_surf = font_title.render(TEXT["mode1"], True, COLORS["primary"])
        surface.blit(title_surf, (20, 15))

        # --- FIX: Use correct font ---
        font_small = get_vietnamese_font(24)
        stats = [
            f"{TEXT['moves']} {self.move_count}",
            f"{TEXT['time']} {int(self.elapsed_time)}s",
            f"Hints: {self.hints_remaining}",
            f"{TEXT['score']} {self.score}"
        ]
        for i, stat in enumerate(stats):
            stat_surf = font_small.render(stat, True, COLORS["text"])
            surface.blit(stat_surf, (500 + i * 110, 25))

        for button in self.buttons.values():
            button.draw(surface, font_small)

        for bottle in self.bottles:
            bottle.draw(surface)

        self.particle_system.draw(surface)

        if self.game_over and self.won:
            # --- FIX: Use correct font ---
            font_large = get_vietnamese_font(48)
            msg = TEXT["win"]
            msg_surf = font_large.render(msg, True, COLORS["success"])
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(surface, COLORS["surface"], bg_rect, border_radius=20)
            pygame.draw.rect(surface, COLORS["success"], bg_rect, 3, border_radius=20)
            surface.blit(msg_surf, msg_rect)

            if self.elapsed_time < 30 and self.hints_used == 0:
                rating = TEXT["perfect"]
            elif self.move_count < 15:
                rating = TEXT["great"]
            else:
                rating = TEXT["good"]
            rating_surf = font_large.render(rating, True, COLORS["accent"])
            rating_rect = rating_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            surface.blit(rating_surf, rating_rect)

        self.particle_system.update()

# ==================== MODE 2: BOTTLE SWAP CHALLENGE ====================

SWAP_BOTTLE_COLORS = [
    (255, 50, 50),    # Red
    (50, 255, 50),    # Green
    (50, 50, 255),    # Blue
    (255, 215, 0)     # Yellow
]

class SwapBottle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 60
        self.height = 130
        self.offset_y = 0
        self.target_offset = 0

    def draw(self, surface, is_selected=False):
        offset = self.offset_y
        rect = pygame.Rect(self.x, self.y + offset, self.width, self.height)

        if is_selected:
            pygame.draw.rect(surface, COLORS["highlight"], rect, border_radius=12)
            pygame.draw.rect(surface, (255, 255, 0), rect, 5, border_radius=12)
        else:
            pygame.draw.rect(surface, self.color, rect, border_radius=12)
            pygame.draw.rect(surface, (50, 50, 50), rect, 2, border_radius=12)

        pygame.draw.rect(surface, (50, 50, 50), (self.x + 15, self.y + offset - 15, 30, 15), 2)

        self.offset_y += (self.target_offset - self.offset_y) * 0.3

class SwapGame:
    def __init__(self, difficulty="Medium"):
        self.difficulty = difficulty
        self.moves_left = self._get_moves()
        self.reset_game()
        self.particle_system = ParticleSystem()

        self._create_buttons()

    def _get_moves(self):
        moves = {"Easy": 10, "Medium": 8, "Hard": 6, "Expert": 4}
        return moves.get(self.difficulty, 8)

    def _create_buttons(self):
        button_y = 30
        self.buttons = {
            "new_game": Button(20, button_y, 120, 40, TEXT["new_game"], COLORS["primary"]),
            "menu": Button(150, button_y, 80, 40, TEXT["menu"], COLORS["text"]),
        }

    def reset_game(self):
        self.secret_order = list(SWAP_BOTTLE_COLORS)
        random.shuffle(self.secret_order)
        self.player_order = list(self.secret_order)
        while self.player_order == self.secret_order:
            random.shuffle(self.player_order)
        self.selected_idx = None
        self.moves_left = self._get_moves()
        self.correct_count = 0
        self.game_over = False
        self.won = False
        self._update_correct_count()

    def _update_correct_count(self):
        count = 0
        for i in range(4):
            if self.player_order[i] == self.secret_order[i]:
                count += 1
        self.correct_count = count

    def handle_click(self, pos):
        for name, button in self.buttons.items():
            if button.is_hovered(pos):
                if name == "new_game":
                    self.reset_game()
                elif name == "menu":
                    return "menu"
                return True

        if self.game_over:
            return False

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
                        self._update_correct_count()
                        self.particle_system.emit(
                            x_pos + 30, 350,
                            (255, 255, 0), count=10)
                        if self.player_order == self.secret_order:
                            self.won = True
                            self.game_over = True
                        elif self.moves_left <= 0:
                            self.game_over = True
                    self.selected_idx = None
                return True
        return False

    def update_hover(self, pos):
        for button in self.buttons.values():
            button.hovered = button.is_hovered(pos)

    def draw(self, surface):
        surface.fill(COLORS["background"])
        # --- FIX: Use correct font ---
        font_title = get_vietnamese_font(36)
        title_surf = font_title.render(TEXT["mode2"], True, COLORS["secondary"])
        surface.blit(title_surf, (20, 15))

        # --- FIX: Use correct font ---
        font_small = get_vietnamese_font(24)
        stats = [
            f"{TEXT['moves']} {self.moves_left}",
            f"{TEXT['correct']} {self.correct_count}/4",
            f"Độ khó: {self.difficulty}",
        ]
        for i, stat in enumerate(stats):
            stat_surf = font_small.render(stat, True, COLORS["text"])
            surface.blit(stat_surf, (400 + i * 150, 25))

        for button in self.buttons.values():
            button.draw(surface, font_small)

        pygame.draw.rect(surface, (230, 230, 230), (80, 100, 440, 80), border_radius=15)
        
        # --- FIX: Use correct font ---
        font_label = get_vietnamese_font(28)
        label = font_label.render("THỨ TỰ ẨN", True, (80, 80, 80))
        surface.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 125))

        for i in range(4):
            bottle = SwapBottle(100 + i * 110, 220, self.player_order[i])
            if i == self.selected_idx:
                bottle.target_offset = -20
            else:
                bottle.target_offset = 0
            bottle.draw(surface, i == self.selected_idx)

        self.particle_system.draw(surface)
        self.particle_system.update()

        if self.game_over:
            # --- FIX: Use correct font ---
            font_large = get_vietnamese_font(42)
            if self.won:
                msg = TEXT["win"]
                color = COLORS["success"]
            else:
                msg = TEXT["lose"]
                color = COLORS["error"]
            msg_surf = font_large.render(msg, True, color)
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, 420))
            surface.blit(msg_surf, msg_rect)

            if not self.won:
                ans_label = font_small.render("ĐÁP ÁN:", True, COLORS["text"])
                surface.blit(ans_label, (120, 470))
                for i in range(4):
                    pygame.draw.rect(surface, self.secret_order[i], (220 + i * 60, 475, 40, 20), border_radius=5)

# ==================== MAIN MENU ====================

class MainMenu:
    def __init__(self):
        self.buttons = {}
        self._create_buttons()

    def _create_buttons(self):
        center_x = SCREEN_WIDTH // 2
        self.buttons = {
            "mode1": Button(center_x - 150, 200, 300, 100, TEXT["mode1"], COLORS["primary"]),
            "mode2": Button(center_x - 150, 320, 300, 100, TEXT["mode2"], COLORS["secondary"]),
            "exit": Button(center_x - 60, 500, 120, 50, "Thoát", COLORS["error"]),
        }

    def handle_click(self, pos):
        for name, button in self.buttons.items():
            if button.is_hovered(pos):
                return name
        return None

    def update_hover(self, pos):
        for button in self.buttons.values():
            button.hovered = button.is_hovered(pos)

    def draw(self, surface):
        surface.fill(COLORS["background"])

        # --- FIX: Use correct font ---
        font_large = get_vietnamese_font(48)
        title_surf = font_large.render(TEXT["title"], True, COLORS["primary"])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surf, title_rect)

        # --- FIX: Use correct font ---
        font_medium = get_vietnamese_font(28)
        subtitle_surf = font_medium.render(TEXT["subtitle"], True, COLORS["text_light"])
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 130))
        surface.blit(subtitle_surf, subtitle_rect)

        # --- FIX: Use correct font for buttons ---
        for name, button in self.buttons.items():
            button.draw(surface, get_vietnamese_font(28))

        # Draw descriptions
        # --- FIX: Use correct font ---
        font_small = get_vietnamese_font(20)
        desc1 = font_small.render(TEXT["mode1_desc"], True, COLORS["text_light"])
        surface.blit(desc1, (SCREEN_WIDTH // 2 - desc1.get_width() // 2, 275))

        desc2 = font_small.render(TEXT["mode2_desc"], True, COLORS["text_light"])
        surface.blit(desc2, (SCREEN_WIDTH // 2 - desc2.get_width() // 2, 395))

# ==================== DIFFICULTY SELECTION ====================

class DifficultyMenu:
    def __init__(self, mode):
        self.mode = mode
        self.buttons = {}
        self._create_buttons()

    def _create_buttons(self):
        center_x = SCREEN_WIDTH // 2
        difficulties = ["Easy", "Medium", "Hard", "Expert"]
        colors = [COLORS["success"], COLORS["primary"], COLORS["accent"], COLORS["error"]]

        for i, diff in enumerate(difficulties):
            self.buttons[diff] = Button(center_x - 100, 180 + i * 70, 200, 50,
                                       f"{diff} ({4+i} chai)", colors[i])

        self.back_button = Button(center_x - 60, 580, 120, 45, TEXT["back"], COLORS["text"])

    def handle_click(self, pos):
        if self.back_button.is_hovered(pos):
            return "back"
        for name, button in self.buttons.items():
            if button.is_hovered(pos):
                return name
        return None

    def update_hover(self, pos):
        self.back_button.hovered = self.back_button.is_hovered(pos)
        for button in self.buttons.values():
            button.hovered = button.is_hovered(pos)

    def draw(self, surface):
        surface.fill(COLORS["background"])

        # --- FIX: Use correct font ---
        font_large = get_vietnamese_font(42)
        mode_name = TEXT["mode1"] if self.mode == "mode1" else TEXT["mode2"]
        title_surf = font_large.render(f"{mode_name} - Chọn Độ Khó", True, COLORS["primary"])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surf, title_rect)

        # --- FIX: Use correct font ---
        font_btn = get_vietnamese_font(24)
        for button in self.buttons.values():
            button.draw(surface, font_btn)

        self.back_button.draw(surface, font_btn)

# ==================== GAME MANAGER ====================

class GameManager:
    def __init__(self):
        self.state = "menu"
        self.menu = MainMenu()
        self.difficulty_menu = None
        self.selected_mode = None
        self.difficulty = "Medium"
        self.game = None

    def run_water_sort(self):
        num_bottles = {"Easy": 4, "Medium": 5, "Hard": 6, "Expert": 7}[self.difficulty]
        self.game = WaterSortGame(num_bottles=num_bottles)
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        result = self.game.handle_click(event.pos)
                        if result == "menu":
                            return "menu"
                elif event.type == pygame.MOUSEMOTION:
                    self.game.update_hover(event.pos)

            if not self.game.game_over:
                self.game.elapsed_time = time.time() - self.game.start_time

            self.game.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def run_swap_game(self):
        self.game = SwapGame(difficulty=self.difficulty)
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        result = self.game.handle_click(event.pos)
                        if result == "menu":
                            return "menu"
                elif event.type == pygame.MOUSEMOTION:
                    self.game.update_hover(event.pos)

            self.game.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        return "quit"

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.state == "menu":
                            result = self.menu.handle_click(event.pos)
                            if result:
                                if result == "exit":
                                    return
                                elif result in ["mode1", "mode2"]:
                                    self.selected_mode = result
                                    self.difficulty_menu = DifficultyMenu(result)
                                    self.state = "difficulty"
                        elif self.state == "difficulty":
                            result = self.difficulty_menu.handle_click(event.pos)
                            if result:
                                if result == "back":
                                    self.state = "menu"
                                else:
                                    self.difficulty = result
                                    if self.selected_mode == "mode1":
                                        result = self.run_water_sort()
                                    else:
                                        result = self.run_swap_game()
                                    if result == "quit":
                                        return
                                    self.state = "menu"
                elif event.type == pygame.MOUSEMOTION:
                    if self.state == "menu":
                        self.menu.update_hover(event.pos)
                    elif self.state == "difficulty":
                        self.difficulty_menu.update_hover(event.pos)

            if self.state == "menu":
                self.menu.draw(screen)
            elif self.state == "difficulty":
                self.difficulty_menu.draw(screen)

            pygame.display.flip()
            clock.tick(60)

# ==================== MAIN ====================

if __name__ == "__main__":
    manager = GameManager()
    manager.run()
    pygame.quit()