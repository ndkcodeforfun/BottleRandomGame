# 🧪 Xếp Chai Nước - Enhanced Water Sort Game

## Mô Tả Trò Chơi

**Xếp Chai Nước** là một trò chơi giải đố logic hấp dẫn, nơi người chơi cần sắp xếp các chai nước sao cho mỗi chai chỉ chứa một màu duy nhất. Trò chơi được xây dựng trên nền tảng Pygame với nhiều cải tiến về đồ họa, hiệu ứng và tính năng so với phiên bản gốc.

> **Phiên bản cải tiến** của repository gốc: https://github.com/ndkcodeforfun/BottleRandomGame

## 🎮 Tính Năng Mới

### Cải Tiến Đồ Họa

- **Hệ thống hạt (Particle System)**: Hiệu ứng pháo hoa khi chiến thắng, hiệu ứng lựa chọn chai
- **Animation mượt mà**: Chai nước nhảy lên khi được chọn, các nút có hiệu ứng hover
- **Màu sắc đẹp mắt**: Bảng màu hiện đại với gradient cho từng loại chất lỏng
- **Giao diện người dùng tinh tế**: Menu, nút bấm, và các thành phần UI được thiết kế cẩn thận

### Tính Năng Gameplay

- **Hệ thống độ khó**: 4 cấp độ từ Dễ đến Chuyên gia
  - **Dễ (Easy)**: 4 chai, không giới hạn lượt, 5 gợi ý
  - **Trung bình (Medium)**: 5 chai, không giới hạn lượt, 3 gợi ý
  - **Khó (Hard)**: 6 chai, giới hạn 30 lượt, 2 gợi ý
  - **Chuyên gia (Expert)**: 7 chai, giới hạn 50 lượt, 1 gợi ý

- **Hệ thống gợi ý (Hints)**: Gợi ý cho người chơi khi gặp khó khăn
- **Quay lại (Undo)**: Cho phép hoàn tác các nước đi sai
- **Chủ đề màu sắc đa dạng**: Classic, Vibrant, Ocean, Sunset, Garden, Rainbow, Ice, Fire
- **Hệ thống thành tựu (Achievements)**: Theo dõi và khen thưởng thành tựu người chơi

### Hệ Thống Điểm Số

Điểm số được tính dựa trên:
- **Điểm cơ bản**: 100 điểm × số lượng chai
- **Thưởng thời gian**: Tối đa 100 điểm (nhanh hơn = nhiều điểm hơn)
- **Thưởng nước đi**: Tối đa 50 điểm (ít nước đi hơn = nhiều điểm hơn)
- **Phạt gợi ý**: -10 điểm cho mỗi gợi ý được sử dụng

### Thành Tựu (Achievements)

| Thành Tựu | Mô Tả | Điều Kiện |
|-----------|-------|-----------|
| 🎉 Chiến Thắng Đầu Tiên | Thắng trận đầu tiên | Thắng 1 trận |
| 💯 Điểm Hoàn Hảo | Hoàn thành không dùng gợi ý | Thắng không dùng hints |
| ⚡ Nhanh Như Chớp | Thắng trong dưới 30 giây | Thắng dưới 30s |
| 🔥 Bất Khả Chiến Bại | Thắng 5 trận liên tiếp | Chuỗi thắng ≥ 5 |
| 👑 Bậc Thầy | Thắng ở chế độ Expert | Thắng Expert |
| 💪 Kiên Trì | Chơi 20 trận | Tổng trận ≥ 20 |
| 🎯 Nhà Chiến Lược | Sử dụng ít hơn 50% số lượt | Hoàn thành xuất sắc |
| 🏆 Nhà Sưu Tập | Mở khóa tất cả thành tựu | Mở khóa tất cả |

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Pygame 2.5.0 trở lên

### Các Bước Cài Đặt

1. **Clone repository**:
```bash
git clone https://github.com/yourusername/BottleRandomGame.git
cd BottleRandomGame
```

2. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

3. **Chạy trò chơi**:
```bash
python main.py
```

## 🎯 Cách Chơi

### Luật Chơi

1. **Mục tiêu**: Sắp xếp các chai nước sao cho mỗi chai chỉ chứa một màu duy nhất
2. **Cách chơi**:
   - Click vào một chai để chọn (chai sẽ nhảy lên)
   - Click vào chai khác để đổ nước từ chai đã chọn sang
   - Chỉ có thể đổ khi chai đích trống hoặc có cùng màu trên cùng
   - Chai đích phải còn chỗ trống

### Điều Khiển

| Hành Động | Phím/Thao Tác |
|-----------|---------------|
| Chọn chai | Click chuột trái vào chai |
| Bỏ chọn | Click lại vào chai đang chọn |
| Đổ nước | Click vào chai đích |
| Quay lại | Click nút "↩️ Quay Lại" |
| Gợi ý | Click nút "💡 Gợi ý" |
| Trò mới | Click nút "🎮 Trò Mới" |
| Menu | Click nút "⬅️ Quay Lại" |

### Mẹo Chơi

1. **Bắt đầu từ chai có ít màu**: Những chai chỉ có 1-2 màu dễ xử lý hơn
2. **Tạo không gian trống**: Luôn giữ ít nhất 2 chai trống để di chuyển
3. **Sử dụng gợi ý hợp lý**: Gợi ý có giới hạn, hãy dùng khi thực sự cần
4. **Quay lại khi sai**: Đừng ngại sử dụng tính năng Undo

## 📁 Cấu Trúc Dự Án

```
BottleRandomGame/
├── main.py           # File chính chứa toàn bộ game
├── config.py         # Cấu hình trò chơi (màu sắc, độ khó, v.v.)
├── requirements.txt  # Danh sách thư viện cần thiết
├── README.md         # Tài liệu hướng dẫn
└── build/            # Thư mục build cho web deployment
```

## 🎨 Tùy Chỉnh

### Thêm Chủ Đề Màu Mới

Chỉnh sửa file `config.py`:

```python
COLOR_THEMES = {
    "Tên Theme Mới": ["R", "G", "B", "Y", "P", "O"],
    # Thêm các mã màu khác
}
```

### Điều Chỉnh Độ Khó

```python
DIFFICULTY = {
    "Tên Độ Khó": {
        "bottles": Số_lượng_chai,
        "moves_unlimited": True/False,
        "moves_limit": Số_lượt_giới_hạn,
        "hints": Số_gợi_ý,
    },
}
```

### Thêm Thành Tựu Mới

```python
ACHIEVEMENTS = [
    {"id": "new_achievement", "name": "🏆 Tên", "description": "Mô tả"},
]
```

## 🌐 Web Deployment

Trò chơi có thể được triển khai lên web sử dụng `pygbag`:

```bash
pip install pygbag
pygbag --build build main.py
```

## 🤝 Đóng Góp

Đóng góp luôn được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Dự án này được licensen theo MIT License.

## 📧 Liên Hệ

- Repository: https://github.com/ndkcodeforfun/BottleRandomGame
- Phiên bản cải tiến: https://github.com/yourusername/BottleRandomGame

---

## 🧪 Enhanced Water Sort Game (English Version)

### Description

**Water Sort Puzzle** is an engaging logic puzzle game where players must arrange water bottles so that each bottle contains only one color. Built on Pygame with numerous improvements in graphics, effects, and features compared to the original version.

### Key Features

- **Particle System**: Fireworks on victory, bottle selection effects
- **Smooth Animations**: Bottles bounce when selected, buttons have hover effects
- **Beautiful Colors**: Modern color palette with gradients for each liquid type
- **Polished UI**: Carefully designed menus, buttons, and UI components
- **4 Difficulty Levels**: Easy to Expert
- **Hint System**: Help when stuck
- **Undo Feature**: Recover from mistakes
- **Multiple Color Themes**: Classic, Vibrant, Ocean, Sunset, Garden, Rainbow, Ice, Fire
- **Achievement System**: Track and reward player accomplishments
- **Scoring System**: Time bonus, move bonus, hint penalty

### Installation

```bash
git clone https://github.com/yourusername/BottleRandomGame.git
cd BottleRandomGame
pip install -r requirements.txt
python main.py
```

### Controls

| Action | Control |
|--------|---------|
| Select bottle | Left click |
| Deselect | Click again |
| Pour | Click destination bottle |
| Undo | Click undo button |
| Hint | Click hint button |
| New game | Click new game button |
| Menu | Click back button |

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License.
