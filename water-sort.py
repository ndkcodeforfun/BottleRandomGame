import pygame
import random

# --- Cài đặt Pygame ---
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Water Sort Puzzle")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Định nghĩa các màu nước (tạm thời)
# Chúng ta sẽ sử dụng các màu này để vẽ hình tròn biểu thị nước
COLOR_MAP = {
    "R": (255, 0, 0),    # Đỏ
    "G": (0, 255, 0),    # Xanh lá
    "B": (0, 0, 255),    # Xanh dương
    "Y": (255, 255, 0),  # Vàng
    "P": (128, 0, 128),  # Tím
    "O": (255, 165, 0),  # Cam
    "C": (0, 255, 255)   # Cyan
}
# Thêm màu trống cho các chai rỗng hoặc phần trống trong chai
EMPTY_COLOR = GRAY

# --- Cài đặt trò chơi ---
NUM_BOTTLES = 4 # Bao gồm cả chai trống
CAPACITY = 4 # Số lượng lớp nước trong mỗi chai

class Bottle:
    def __init__(self, x, y, width, height, capacity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.colors = [] # Chứa các mã màu như 'R', 'G', 'B'

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
    
    def draw(self, screen, index):
        # Vẽ chai
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2) # Viền chai

        # Vẽ nước bên trong
        liquid_height_per_layer = self.height / self.capacity
        for i, color_code in enumerate(self.colors):
            color = COLOR_MAP.get(color_code, BLACK) # Lấy màu từ COLOR_MAP
            # Vẽ từng lớp nước từ dưới lên
            pygame.draw.rect(screen, color, 
                             (self.x + 2, # x + 2 để có viền nhỏ
                              self.y + self.height - (i + 1) * liquid_height_per_layer + 2, # từ đáy lên
                              self.width - 4, # width - 4 để có viền nhỏ
                              liquid_height_per_layer - 4)) # height - 4 để có viền nhỏ
        
        # Vẽ số thứ tự chai
        font = pygame.font.Font(None, 24)
        text = font.render(str(index), True, BLACK)
        screen.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height + 5))


class WaterSortGame:
    def __init__(self, num_bottles, capacity):
        self.num_bottles = num_bottles
        self.capacity = capacity
        self.all_color_codes = list(COLOR_MAP.keys())[:num_bottles-2] # Lấy số lượng màu cần thiết
        self.bottles = []
        self.selected_bottle_index = None # Chai đang được chọn
        self.setup_game()

    def setup_game(self):
        # Tạo danh sách các màu trộn lẫn
        all_liquid_layers = []
        for color_code in self.all_color_codes:
            for _ in range(self.capacity):
                all_liquid_layers.append(color_code)
        random.shuffle(all_liquid_layers)
        
        # Tạo các đối tượng Bottle và phân phối màu
        # Tính toán vị trí các chai
        bottle_width = 70
        bottle_height = 200
        padding = 30
        start_x = (SCREEN_WIDTH - (self.num_bottles * bottle_width + (self.num_bottles - 1) * padding)) // 2
        
        for i in range(self.num_bottles):
            bottle_x = start_x + i * (bottle_width + padding)
            bottle_y = SCREEN_HEIGHT - bottle_height - 50 # Đặt chai ở phía dưới
            bottle = Bottle(bottle_x, bottle_y, bottle_width, bottle_height, self.capacity)
            
            # Gán màu cho các chai ban đầu
            if i < len(self.all_color_codes): # Chỉ đổ màu vào các chai có màu
                for _ in range(self.capacity):
                    if all_liquid_layers:
                        bottle.add_color(all_liquid_layers.pop(0))
            self.bottles.append(bottle)

        # Đảm bảo có ít nhất 2 chai trống
        while len(self.bottles) < self.num_bottles:
            bottle_x = start_x + len(self.bottles) * (bottle_width + padding)
            bottle_y = SCREEN_HEIGHT - bottle_height - 50
            self.bottles.append(Bottle(bottle_x, bottle_y, bottle_width, bottle_height, self.capacity))
            
    def draw(self, screen):
        for i, bottle in enumerate(self.bottles):
            bottle.draw(screen, i)
            # Vẽ một viền sáng nếu chai được chọn
            if i == self.selected_bottle_index:
                pygame.draw.rect(screen, (255, 255, 0), (bottle.x - 5, bottle.y - 5, bottle.width + 10, bottle.height + 10), 3)

    def handle_click(self, mouse_pos):
        for i, bottle in enumerate(self.bottles):
            # Kiểm tra xem chuột có click vào chai hay không
            if bottle.x <= mouse_pos[0] <= bottle.x + bottle.width and \
               bottle.y <= mouse_pos[1] <= bottle.y + bottle.height:
                
                if self.selected_bottle_index is None:
                    # Nếu chưa có chai nào được chọn, chọn chai này
                    if not bottle.is_empty(): # Chỉ chọn chai có nước
                         self.selected_bottle_index = i
                         print(f"Chai {i} được chọn.")
                else:
                    # Nếu đã có chai được chọn, đây là chai đích
                    start_bottle_index = self.selected_bottle_index
                    end_bottle_index = i
                    
                    if start_bottle_index == end_bottle_index:
                        # Bỏ chọn nếu click lại vào chính nó
                        self.selected_bottle_index = None
                        print(f"Bỏ chọn chai {start_bottle_index}.")
                        return
                    
                    if self.try_move(start_bottle_index, end_bottle_index):
                        print(f"Di chuyển từ chai {start_bottle_index} sang chai {end_bottle_index} thành công.")
                    else:
                        print(f"Di chuyển từ chai {start_bottle_index} sang chai {end_bottle_index} thất bại.")
                    
                    self.selected_bottle_index = None # Sau khi di chuyển (thành công hay thất bại) thì bỏ chọn
                return

    def try_move(self, start_idx, end_idx):
        start_bottle = self.bottles[start_idx]
        end_bottle = self.bottles[end_idx]

        if start_bottle.is_empty():
            print("Chai nguồn trống!")
            return False

        color_to_move = start_bottle.get_top_color()

        if end_bottle.is_full():
            print("Chai đích đã đầy!")
            return False

        if not end_bottle.is_empty() and end_bottle.get_top_color() != color_to_move:
            print("Màu không khớp!")
            return False
        
        # Thực hiện di chuyển
        end_bottle.add_color(start_bottle.remove_color())
        return True

    def is_won(self):
        for bottle in self.bottles:
            # Nếu chai không rỗng, nó phải đầy và chỉ chứa một màu duy nhất
            if not bottle.is_empty() and (len(bottle.colors) != self.capacity or len(set(bottle.colors)) > 1):
                return False
        return True

# --- Vòng lặp trò chơi chính ---
def main():
    game = WaterSortGame(NUM_BOTTLES, CAPACITY)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click chuột trái
                    game.handle_click(event.pos)

        # Xóa màn hình
        screen.fill(WHITE)

        # Vẽ trạng thái trò chơi
        game.draw(screen)

        # Kiểm tra điều kiện thắng
        if game.is_won():
            font = pygame.font.Font(None, 74)
            text = font.render("Bạn đã thắng!", True, (0, 128, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        # Cập nhật màn hình
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()