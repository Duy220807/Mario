import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game")

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Màu xanh cho thanh nền

# Tải hình ảnh và thay đổi kích thước
def load_and_scale_image(path, size):    
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# Tải hình ảnh nền
background_image = load_and_scale_image("assets/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tải hình ảnh nền tảng
platform_image = load_and_scale_image("assets/platform.png", (200, 100))  # Kích thước hình ảnh nền tảng

# Kích thước ban đầu và kích thước khi nhận power-up
initial_size = (40, 40)  # Thay đổi kích thước Mario thành hình vuông 
power_up_size = (60, 60)  # Kích thước hình vuông khi nhận power-up

mario_image = load_and_scale_image("assets/mario.png", initial_size)  # Thay đổi hình ảnh thành mario.png
coin_image = load_and_scale_image("assets/coin.png", (20, 20))
enemy_image = load_and_scale_image("assets/enemy.png", (40, 40))
lucky_box_image = load_and_scale_image("assets/lucky_box.png", (40, 40))
power_up_image = load_and_scale_image("assets/power_up.png", (40, 40))  # Hình ảnh power-up
extra_life_image = load_and_scale_image("assets/extra_life.png", (40, 40))  # Hình ảnh extra life

# Tải hình ảnh cổng chiến thắng và thay đổi kích thước
winning_gate_image = load_and_scale_image("assets/winning_gate.png", (100, 100))  # Kích thước của cổng chiến thắng

mario_rect = mario_image.get_rect()
mario_rect.x = 50
mario_rect.y = SCREEN_HEIGHT - mario_rect.height - 50

# Các biến tốc độ di chuyển
speed_x = 0
speed_y = 0
gravity = 0.5
is_jumping = False

# Các nền tảng với hình ảnh nền tảng
platforms = [pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
             pygame.Rect(200, SCREEN_HEIGHT - 150, 200, 20),
             pygame.Rect(500, SCREEN_HEIGHT - 300, 200, 20)]

# Khởi tạo danh sách kẻ thù với tốc độ di chuyển
enemies = []
enemy_speeds = []
for _ in range(10):
    enemy = pygame.Rect(random.randint(100, 700), SCREEN_HEIGHT - 100, 40, 40)
    speed = random.choice([-2, 2])
    enemies.append(enemy)
    enemy_speeds.append(speed)

# Coin
coins = [pygame.Rect(random.randint(100, 700), SCREEN_HEIGHT - 200, 20, 20)]

# Lucky Boxes
lucky_boxes = [pygame.Rect(300, SCREEN_HEIGHT - 200, 40, 40)]

# Vật phẩm ngẫu nhiên
def spawn_random_item(x, y):
    items = ['coin', 'power_up', 'extra_life']
    item = random.choice(items)
    if item == 'coin':
        return pygame.Rect(x, y, 20, 20), coin_image
    elif item == 'power_up':
        return pygame.Rect(x, y, 40, 40), power_up_image
    elif item == 'extra_life':
        return pygame.Rect(x, y, 40, 40), extra_life_image

# Điểm số và mạng sống
score = 0
lives = 3
items = []

# Điểm mục tiêu để chiến thắng
winning_score = 10

# Thêm biến để kiểm soát trạng thái power-up
power_up_active = False
power_up_duration = 0
original_mario_size = initial_size

# Tạo cổng chiến thắng ở vị trí trên thanh màu xanh
winning_gate_rect = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200, 100, 50)  # Vị trí của cổng chiến thắng

# Thay đổi màu sắc cổng chiến thắng theo chu kỳ thời gian
gate_color = RED
gate_timer = 0
gate_flash_duration = 500  # Thời gian nhấp nháy (tính bằng khung hình)

# Vòng lặp chính
running = True
while running:
    # Vẽ nền lên màn hình
    screen.blit(background_image, (0, 0))

    # Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x = -5 if not power_up_active else -7
            if event.key == pygame.K_RIGHT:
                speed_x = 5 if not power_up_active else 7
            if event.key == pygame.K_SPACE and not is_jumping:
                speed_y = -10 if not power_up_active else -12
                is_jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speed_x = 0

    # Áp dụng trọng lực
    speed_y += gravity
    mario_rect.x += speed_x
    mario_rect.y += speed_y

    # Kiểm tra va chạm với nền tảng
    for platform in platforms:
        if mario_rect.colliderect(platform) and speed_y > 0:
            mario_rect.y = platform.top - mario_rect.height
            speed_y = 0
            is_jumping = False

    # Đảm bảo Mario không rơi ra ngoài màn hình
    if mario_rect.y >= SCREEN_HEIGHT - mario_rect.height - 50:
        mario_rect.y = SCREEN_HEIGHT - mario_rect.height - 50
        speed_y = 0
        is_jumping = False

    # Cập nhật và vẽ nền tảng
    for platform in platforms:
        screen.blit(platform_image, platform.topleft)  # Vẽ nền tảng bằng hình ảnh

    # Thay đổi màu sắc của cổng chiến thắng
    gate_timer += 1
    if gate_timer >= gate_flash_duration:
        gate_color = RED if gate_color == (255, 0, 0) else (255, 0, 0)
        gate_timer = 0
    
    # Cập nhật và vẽ cổng chiến thắng
    screen.blit(winning_gate_image, winning_gate_rect.topleft)
    # Kiểm tra va chạm giữa Mario và cổng chiến thắng
    if mario_rect.colliderect(winning_gate_rect) and score >= winning_score:
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("You Win!", True, (0, 255, 0))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Chờ 2 giây để người chơi thấy thông báo chiến thắng
        running = False

    # Cập nhật và vẽ kẻ thù
    for i in range(len(enemies)):
        enemy = enemies[i]
        speed = enemy_speeds[i]
        screen.blit(enemy_image, enemy.topleft)
        
        # Di chuyển kẻ thù ngẫu nhiên
        enemy.x += speed
        # Đổi hướng khi chạm vào các cạnh màn hình hoặc nền tảng
        if enemy.left < 0 or enemy.right > SCREEN_WIDTH:
            enemy_speeds[i] *= -1
        # Kiểm tra va chạm giữa Mario và kẻ thù
        if mario_rect.colliderect(enemy):
            if is_jumping and mario_rect.bottom <= enemy.top + 10:
                # Mario nhảy vào kẻ thù từ trên cao
                enemies.pop(i)
                enemy_speeds.pop(i)
                score += 1  # Thêm điểm khi tiêu diệt kẻ thù
                speed_y = -10  # Tạo hiệu ứng khi nhảy lên
                print("Enemy Defeated!")
                break  # Để tránh lỗi chỉ số sau khi loại bỏ kẻ thù
            else:
                # Kẻ thù chạm vào Mario
                lives -= 1
                if lives <= 0:
                    print("Game Over")
                    pygame.quit()
                    sys.exit()
                else:
                    # Đặt Mario về vị trí bắt đầu hoặc thực hiện hành động khác
                    mario_rect.x = 50
                    mario_rect.y = SCREEN_HEIGHT - mario_rect.height - 50
                    speed_x = 0
                    speed_y = 0
                    is_jumping = False
                break  # Để tránh lỗi chỉ số sau khi loại bỏ kẻ thù

    # Cập nhật và vẽ đồng xu
    for coin in coins:
        screen.blit(coin_image, coin.topleft)
        # Kiểm tra va chạm giữa Mario và đồng xu
        if mario_rect.colliderect(coin):
            coins.remove(coin)
            score += 1

    # Cập nhật và vẽ hộp may mắn
    new_items = []  # Danh sách tạm thời để lưu các vật phẩm mới
    for box in lucky_boxes:
        screen.blit(lucky_box_image, box.topleft)
        # Kiểm tra va chạm giữa Mario và hộp may mắn
        if mario_rect.colliderect(box) and is_jumping and mario_rect.bottom <= box.top + 10:
            lucky_boxes.remove(box)
            item_rect, item_image = spawn_random_item(box.x, box.y - 40)
            new_items.append((item_rect, item_image))
            print("Lucky Box Hit!")

    # Thêm các vật phẩm mới vào danh sách `items`
    items.extend(new_items)

    # Cập nhật và vẽ các vật phẩm
    for item_rect, item_image in items:
        screen.blit(item_image, item_rect.topleft)
        # Kiểm tra va chạm giữa Mario và vật phẩm
        if mario_rect.colliderect(item_rect):
            items.remove((item_rect, item_image))
            if item_image == coin_image:
                score += 1
            elif item_image == power_up_image:
                power_up_active = True
                power_up_duration = 500  # Thời gian hoạt động của power-up (ví dụ: 500 khung hình)
                original_mario_size = mario_image.get_size()  # Lưu kích thước gốc
                mario_image = load_and_scale_image("assets/mario.png", power_up_size)  # Thay đổi kích thước
                mario_rect = mario_image.get_rect(topleft=mario_rect.topleft)  # Cập nhật rect
                print("Power-up Activated!")
            elif item_image == extra_life_image:
                lives += 1
                print("Extra Life!")

    # Xử lý thời gian hoạt động của power-up
    if power_up_active:
        power_up_duration -= 1
        if power_up_duration <= 0:
            power_up_active = False
            mario_image = load_and_scale_image("assets/mario.png", original_mario_size)  # Khôi phục kích thước
            mario_rect = mario_image.get_rect(topleft=mario_rect.topleft)  # Cập nhật rect
            print("Power-up Ended")

    # Vẽ Mario lên màn hình
    screen.blit(mario_image, mario_rect)

    # Hiển thị điểm số và mạng sống
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10)) 
    screen.blit(lives_text, (10, 50))

    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
