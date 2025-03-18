import pygame  
import sys  
import random  
import os  
import math  
  
# Initialize Pygame  
pygame.init()  
  
# Screen Settings  
WIDTH, HEIGHT = 1200, 900  
window = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Agario Clone")  
  
# Colors  
colors = [  
    (255, 0, 0),    # Red  
    (255, 165, 0),  # Orange  
    (204, 255, 0),  # Neon Yellow  
    (57, 255, 20),    # Neon Green  
    (31, 81, 255),    # Blue  
    (156, 0, 183),   # Indigo  
    (238, 130, 238) # Violet  
]  
BLOB_COLOR = (0, 0, 255)  
FOOD_SIZE = 8  
PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT = 2400, 1800  
spawn_rate = 20 

# Blob and Camera Settings  
blobs = [{'x': WIDTH // 2, 'y': HEIGHT // 2, 'size': 20, 'food': 20}]  
camera_x, camera_y = 0, 0  
speed = 3  
  
# Load Blob Image  
blob_image_path = "C:\\Users\\feldtsky000\\Desktop\\TERM 4 PROGRAMS\\Blob.png"  
blob_image = pygame.image.load(blob_image_path) if os.path.exists(blob_image_path) else None  
  
# Font Settings  
font = pygame.font.SysFont("Arial", 24, bold=True)  
  
# Game Clock  
clock = pygame.time.Clock()  
  
# Function to spawn food  
def spawn_food():  
    x = random.randint(10, WIDTH - 10)  
    y = random.randint(10, HEIGHT - 10)  
    color = random.choice(colors)  
    return (x, y, color)  
  
# Function to calculate food loss rate based on size  
def calculate_food_loss_rate(blob_size):  
    base_rate = 0.01  
    return base_rate * (blob_size / 60) ** 2  
  
# Function to check collision and grow blob  
def check_collision(blob_x, blob_y, food_items):  
    global blobs  
    for blob in blobs:  
        for food in food_items[:]:  
            fx, fy, color = food  
            if math.hypot(blob['x'] - fx, blob['y'] - fy) < (blob['size'] + FOOD_SIZE):  
                food_items.remove(food)  
                blob['food'] += 1  
                blob['size'] = int(blob['food'])  
  
# Function to display food count  
def display_food_count(surface, count, x, y):  
    text = font.render(str(int(count)), True, (255, 255, 255))  
    text_rect = text.get_rect(center=(x, y - 15))  
    surface.blit(text, text_rect)  
  
# Function to draw moving grid  
def draw_moving_grid(surface, width, height, spacing, camera_x, camera_y):  
    grid_color = (200, 200, 200, 77)  
    grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)  
    offset_x = camera_x % spacing  
    offset_y = camera_y % spacing  
  
    for x in range(-offset_x, width, spacing):  
        pygame.draw.line(grid_surface, grid_color, (x, 0), (x, height))  
    for y in range(-offset_y, height, spacing):  
        pygame.draw.line(grid_surface, grid_color, (0, y), (width, y))  
  
    surface.blit(grid_surface, (0, 0))  
  
# Function to handle splitting with smooth animation  
def split_blob(blob):  
    if blob['food'] >= 50:  
        blob['food'] //= 2  
        blob['size'] = int(blob['food'])  
        new_blob = {  
            'x': blob['x'],  
            'y': blob['y'],  
            'size': blob['size'],  
            'food': blob['food'],  
            'vx': random.choice([-1, 1]) * 3,  
            'vy': random.choice([-1, 1]) * 3  
        }  
        blobs.append(new_blob)  
  
# Main Game Loop  
running = True  
food_timer = 0  
food_items = []  
  
while running:  
    # Event Handling  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
            for blob in blobs:  
                split_blob(blob)  
  
    # Get the current state of the keyboard  
    keys = pygame.key.get_pressed()  
  
    # Update blobs' positions  
    for blob in blobs:  
        # Calculate the center of the camera view  
        center_x, center_y = camera_x + WIDTH // 2, camera_y + HEIGHT // 2  
  
        if blob is blobs[0]:  
            if keys[pygame.K_a]: blob['x'] -= speed  
            if keys[pygame.K_d]: blob['x'] += speed  
            if keys[pygame.K_w]: blob['y'] -= speed  
            if keys[pygame.K_s]: blob['y'] += speed  
        else:  
            # Calculate direction towards the center of the camera view  
            direction_x = center_x - blob['x']  
            direction_y = center_y - blob['y']  
            distance = math.hypot(direction_x, direction_y)  
  
            # Normalize direction  
            if distance > 0:  
                direction_x /= distance  
                direction_y /= distance  
  
            # Apply a smooth centering velocity  
            blob['vx'] = direction_x * 2  
            blob['vy'] = direction_y * 2  
  
            # Update blob position  
            blob['x'] += blob['vx']  
            blob['y'] += blob['vy']  
  
            # Gradual slowdown when near the center  
            if distance < 10:  
                blob['vx'] *= 0.9  
                blob['vy'] *= 0.9  
  
        # Keep blobs inside the playfield  
        blob['x'] = max(blob['size'], min(PLAYFIELD_WIDTH - blob['size'], blob['x']))  
        blob['y'] = max(blob['size'], min(PLAYFIELD_HEIGHT - blob['size'], blob['y']))  
  
    # Update camera based on the first blob  
    camera_x = min(max(blobs[0]['x'] - WIDTH // 2, 0), PLAYFIELD_WIDTH - WIDTH)  
    camera_y = min(max(blobs[0]['y'] - HEIGHT // 2, 0), PLAYFIELD_HEIGHT - HEIGHT)  
  
    # Food Spawning  
    food_timer += clock.get_time()  
    if food_timer > 1000 // spawn_rate:  
        food_items.append(spawn_food())  
        food_timer = 0  
  
    # Exponential Food Loss  
    for blob in blobs:  
        food_loss_rate = calculate_food_loss_rate(blob['size'])  
        blob['food'] = max(0, blob['food'] - food_loss_rate)  
        blob['size'] = int(blob['food'])  
  
    # Drawing  
    window.fill((0, 0, 0))  # Black background  
    draw_moving_grid(window, WIDTH, HEIGHT, 30, camera_x, camera_y)  
  
    for blob in blobs:  
        check_collision(blob['x'], blob['y'], food_items)  
        if blob_image:  
            scaled_image = pygame.transform.scale(blob_image, (blob['size'] * 2, blob['size'] * 2))  
            window.blit(scaled_image, (blob['x'] - blob['size'] - camera_x, blob['y'] - blob['size'] - camera_y))  
        else:  
            pygame.draw.circle(window, BLOB_COLOR, (blob['x'] - camera_x, blob['y'] - camera_y), blob['size'])  
        display_food_count(window, blob['food'], blob['x'] - camera_x, blob['y'] - blob['size'] - camera_y)  
  
    for fx, fy, color in food_items:  
        pygame.draw.circle(window, color, (fx - camera_x, fy - camera_y), FOOD_SIZE)  
  
    pygame.display.flip()  
    clock.tick(60)  
  
pygame.quit()  
sys.exit()  
