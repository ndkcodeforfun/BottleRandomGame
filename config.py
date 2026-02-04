# Enhanced Water Sort Game - Configuration
# Tùy chỉnh cấu hình trò chơi

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# Game settings
INITIAL_BOTTLES = 4
CAPACITY = 4
MIN_EMPTY_BOTTLES = 2

# Colors - Beautiful modern color palette
COLORS = {
    "background": (240, 245, 255),
    "surface": (255, 255, 255),
    "primary": (99, 102, 241),
    "secondary": (139, 92, 246),
    "accent": (245, 158, 11),
    "success": (16, 185, 129),
    "error": (239, 68, 68),
    "warning": (245, 158, 11),
    "text": (31, 41, 55),
    "text_light": (156, 163, 175),
    "bottle_border": (55, 65, 81),
    "highlight": (251, 191, 36),
    "shadow": (0, 0, 0, 50),
}

# Liquid colors with beautiful gradients
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

# Color themes
COLOR_THEMES = {
    "Classic": ["R", "G", "B", "Y"],
    "Vibrant": ["R", "G", "B", "Y", "P", "O"],
    "Ocean": ["B", "C", "G", "P"],
    "Sunset": ["O", "R", "Y", "P"],
    "Garden": ["G", "Y", "P", "M"],
    "Rainbow": ["R", "O", "Y", "G", "B", "P"],
    "Ice": ["C", "B", "W", "G"],
    "Fire": ["R", "O", "Y", "P"],
}

# Difficulty settings
DIFFICULTY = {
    "Easy": {"bottles": 4, "moves_unlimited": True, "hints": 5},
    "Medium": {"bottles": 5, "moves_unlimited": True, "hints": 3},
    "Hard": {"bottles": 6, "moves_unlimited": False, "moves_limit": 30, "hints": 2},
    "Expert": {"bottles": 7, "moves_unlimited": False, "moves_limit": 50, "hints": 1},
}

# Animation settings
ANIMATIONS = {
    "pour_speed": 15,
    "select_bounce": 8,
    "transition_duration": 300,
    "particle_count": 20,
}

# Sound settings (placeholders for sound file paths)
SOUNDS = {
    "select": "sounds/select.wav",
    "pour": "sounds/pour.wav",
    "success": "sounds/success.wav",
    "error": "sounds/error.wav",
    "win": "sounds/win.wav",
    "click": "sounds/click.wav",
}

# UI Settings
UI = {
    "button_height": 50,
    "button_width": 180,
    "font_large": 48,
    "font_medium": 32,
    "font_small": 24,
    "font_tiny": 18,
    "corner_radius": 12,
}

# Vietnamese text
TEXT = {
    "title": "🧪 Xếp Chai Nước",
    "subtitle": "Thử thách trí tuệ",
    "new_game": "🎮 Trò Mới",
    "difficulty": "⚡ Độ Khó",
    "hints": "💡 Gợi Ý",
    "undo": "↩️ Quay Lại",
    "settings": "⚙️ Cài Đặt",
    "statistics": "📊 Thống Kê",
    "back": "⬅️ Quay Lại",
    "moves": "🔄 Lượt:",
    "time": "⏱️ Thời Gian:",
    "score": "⭐ Điểm:",
    "hints_remaining": "💡 Gợi ý còn:",
    "win": "🎉 CHIẾN THẮNG!",
    "lose": "😢 HẾT LƯỢT!",
    "continue": "Tiếp Tục",
    "quit": "Thoát",
    "yes": "Có",
    "no": "Không",
    "play_again": "🔄 Chơi Lại",
    "next_level": "➡️ Cấp Tiếp",
    "perfect": "🏆 HOÀN HẢO!",
    "great": "🎯 TUYỆT VỜI!",
    "good": "👍 TỐT LẮM!",
    "try_again": "💪 CỐ GẮNG!",
}

# Achievement definitions
ACHIEVEMENTS = [
    {"id": "first_win", "name": "🎉 Chiến Thắng Đầu Tiên", "description": "Thắng trận đầu tiên"},
    {"id": "perfect_game", "name": "💯 Điểm Hoàn Hảo", "description": "Hoàn thành không dùng gợi ý"},
    {"id": "speed_demon", "name": "⚡ Nhanh Như Chớp", "description": "Thắng trong dưới 30 giây"},
    {"id": "unstoppable", "name": "🔥 Bất Khả Chiến Bại", "description": "Thắng 5 trận liên tiếp"},
    {"id": "master", "name": "👑 Bậc Thầy", "description": "Thắng ở chế độ Expert"},
    {"id": "strategist", "name": "🎯 Nhà Chiến Lược", "description": "Sử dụng ít hơn 50% số lượt cho phép"},
    {"id": "persistent", "name": "💪 Kiên Trì", "description": "Chơi 20 trận"},
    {"id": "collector", "name": "🏆 Nhà Sưu Tập", "description": "Mở khóa tất cả thành tựu"},
]
