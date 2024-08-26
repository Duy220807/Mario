import pygame
import sys
import os
import random

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mario Game')

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tải hình ảnh nền và điều chỉnh kích thước
background = pygame.image.load('assets/background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Tải hình ảnh nhân vật Mario
mario_image = pygame.image.load('assets/mario.gif').convert_alpha()
mario_image = pygame.transform.scale(mario_image, (50, 50))  # Kích thước ví dụ: 50x50

# Tải hình ảnh kẻ thù và vật phẩm
enemy_image = pygame.image.load('assets/enemy.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Kích thước ví dụ: 50x50

# Tải hình ảnh mặt đất và hộp vật phẩm
ground_image = pygame.image.load('assets/ground.png').convert_alpha()
ground_image = pygame.transform.scale(ground_image, (WIDTH, 50))  # Điều chỉnh kích thước mặt đất nếu cần
box_image = pygame.image.load('assets/box.png').convert_alpha()
box_image = pygame.transform.scale(box_image, (50, 50))  # Điều chỉnh kích thước hộp vật phẩm nếu cần

# Tải hình ảnh vật phẩm ngẫu nhiên
gold_image = pygame.image.load('assets/gold.png').convert_alpha()
gold_image = pygame.transform.scale(gold_image, (30, 30))  # Kích thước ví dụ: 30x30
mushroom_image = pygame.image.load('assets/mushroom.png').convert_alpha()
mushroom_image = pygame.transform.scale(mushroom_image, (30, 30))  # Kích thước ví dụ: 30x30

# Kiểm tra đường dẫn tệp âm thanh
audio_file = 'assets/background_music.mp3'
print(f"Đường dẫn âm thanh: {os.path.abspath(audio_file)}")

# Tải âm thanh
try:
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(-1)  # Phát nhạc nền liên tục
except pygame.error as e:
    print(f"Lỗi khi tải âm thanh: {e}")

jump_sound = pygame.mixer.Sound('assets/jump_sound.wav')

# Tạo đồng hồ để kiểm soát tốc độ khung hình
clock = pygame.time.Clock()

# Tạo lớp Mario với hình ảnh mới
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mario_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = ground.rect.top  # Đặt Mario đứng trên mặt đất
        self.velocity = 5
        self.gravity = 0.5
        self.is_jumping = False
        self.jump_speed = -10
        self.y_velocity = 0
        self.on_ground = True  # Trạng thái để kiểm tra Mario có đứng trên mặt đất không
        self.grown = False  # Trạng thái để kiểm tra Mario đã to lên chưa

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and not self.is_jumping and self.on_ground:
            self.is_jumping = True
            self.y_velocity = self.jump_speed
            jump_sound.play()  # Phát âm thanh khi nhảy

        # Cập nhật vị trí và kiểm soát nhảy
        if self.is_jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity

        # Kiểm tra va chạm với mặt đất
        if self.rect.bottom >= ground.rect.top:
            self.rect.bottom = ground.rect.top
            self.is_jumping = False
            self.y_velocity = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Kiểm tra va chạm với kẻ thù
        if pygame.sprite.collide_rect(self, enemy):
            print("Va chạm với kẻ thù!")

        # Đảm bảo Mario không ra ngoài màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0

    def grow(self):
        if not self.grown:
            new_size = (self.rect.width + 10, self.rect.height + 10)  # Tăng kích thước thêm 10px
            self.image = pygame.transform.scale(mario_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.grown = True  # Đặt trạng thái đã to lên

# Tạo lớp Kẻ thù
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 4
        self.rect.y = HEIGHT - 200  # Đặt kẻ thù lên cao hơn mặt đất
        self.speed = 3  # Tốc độ di chuyển
        self.direction = 1  # 1: Phải, -1: Trái
        self.move_range = 100  # Khoảng cách di chuyển

    def update(self):
        # Di chuyển kẻ thù trong khoảng cách nhất định
        self.rect.x += self.speed * self.direction
        
        # Nếu kẻ thù đạt đến cuối khoảng cách di chuyển, thay đổi hướng
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.direction *= -1

# Tạo lớp Hộp vật phẩm
class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = box_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 25
        self.rect.y = HEIGHT - 200  # Đặt hộp vật phẩm trên mặt đất

    def reveal_item(self):
        # Chọn ngẫu nhiên vàng (70%) hoặc nấm (30%)
        item_type = random.choices(
            ['gold', 'mushroom'], 
            weights=[0.7, 0.3], 
            k=1
        )[0]
        
        if item_type == 'gold':
            return Gold(self.rect.x, self.rect.y)  # Đặt vàng xuất hiện phía trên hộp
        else:
            return Mushroom(self.rect.x, self.rect.y)  # Đặt nấm xuất hiện phía trên hộp

# Tạo lớp Vàng
class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = gold_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fall_speed = 5  # Tốc độ rơi của vàng

    def update(self):
        # Vàng sẽ rơi xuống đất
        if self.rect.bottom < ground.rect.top:
            self.rect.y += self.fall_speed
        else:
            self.rect.bottom = ground.rect.top  # Đặt vàng trên mặt đất

# Tạo lớp Nấm
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = mushroom_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fall_speed = 5  # Tốc độ rơi của nấm

    def update(self):
        # Nấm sẽ rơi xuống đất
        if self.rect.bottom < ground.rect.top:
            self.rect.y += self.fall_speed
        else:
            self.rect.bottom = ground.rect.top  # Đặt nấm trên mặt đất

# Tạo lớp Đất
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 50  # Đặt mặt đất ở dưới cùng của màn hình

# Tạo các đối tượng
ground = Ground()
mario = Mario()
enemy = Enemy()
box = Box()

# Tạo các nhóm sprite
all_sprites = pygame.sprite.Group()
all_sprites.add(mario, enemy, box, ground)

items = pygame.sprite.Group()

# Biến số lượng vàng
gold_count = 0

# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Cập nhật tất cả các đối tượng
    all_sprites.update()
    items.update()

    # Kiểm tra va chạm với hộp vật phẩm
    if pygame.sprite.collide_rect(mario, box):
        item = box.reveal_item()
        items.add(item)
        box.kill()  # Xóa hộp vật phẩm sau khi chạm vào

    # Kiểm tra va chạm với vật phẩm
    collided_items = pygame.sprite.spritecollide(mario, items, True)
    if collided_items:
        item = collided_items[0]
        if isinstance(item, Gold):
            gold_count += 1
        elif isinstance(item, Mushroom):
            mario.grow()

    # Vẽ hình nền và tất cả các đối tượng
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    items.draw(screen)

    # Hiển thị số lượng vàng ở góc phải
    font = pygame.font.SysFont(None, 36)
    gold_text = font.render(f'Gold: {gold_count}', True, BLACK)
    screen.blit(gold_text, (WIDTH - 150, 10))

    # Cập nhật màn hình
    pygame.display.flip()

    # Điều chỉnh tốc độ khung hình
    clock.tick(30)
