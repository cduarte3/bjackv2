import pygame
from pygame.locals import *
from deck import *
import sys

# Initialize Pygame
pygame.init()

pygame.mixer.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# Other initializations...
chip1 = pygame.transform.scale(pygame.image.load('assets/images/chip1.png'), (70, 70))
chip5 = pygame.transform.scale(pygame.image.load('assets/images/chip5.png'), (70, 70))
chip10 = pygame.transform.scale(pygame.image.load('assets/images/chip10.png'), (70, 70))
chip25 = pygame.transform.scale(pygame.image.load('assets/images/chip25.png'), (70, 70))
chip50 = pygame.transform.scale(pygame.image.load('assets/images/chip50.png'), (70, 70))
chip100 = pygame.transform.scale(pygame.image.load('assets/images/chip100.png'), (70, 70))

original_width, original_height = pygame.image.load(f'assets/gifs/frame (1).gif').get_size()  # Get size of the first frame
scaled_width = original_width * 0.8
scaled_height = original_height * 0.8

# Pre-load frames
frames = [pygame.transform.scale(pygame.image.load(f'assets/gifs/frame ({i+1}).gif'), (scaled_width, scaled_height)) for i in range(39)]
frame_count = len(frames)
current_frame = 0
frame_rate = 10  # Frames per second

table = pygame.transform.scale(pygame.image.load('assets/images/table.png'), (1000, 600))

# colours, font, and coordinates for text
X = 400
Y = 400
button_colour = (70, 115, 100)

def draw_button(screen, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    
def draw_text(text, x, y, size):
    font = pygame.font.Font('Lato-Black.ttf', size)
    # text object
    text_surface = font.render(text, True, (255,255,255))
    
    # text box object
    textRect = text_surface.get_rect()
    
    # center of text box
    textRect.center = (x // 2, y // 2)

    # Draw the text onto the surface and return it
    screen.blit(text_surface, textRect)
    return text_surface

button_image = pygame.image.load('assets/images/gray.png')
button_image_2 = button_image = pygame.transform.scale(button_image, (500, 160))
button_image = pygame.transform.scale(button_image, (700, 260))

# Main loop
running = True
waiting_for_player1 = False
waiting_for_player2 = True
menu = True
player_win = 0
player1wins = 0
player2wins = 0
draws = 0
stand = False
result_displayed = False
bet_placed = False
bet_amount = 0
hit = False
placed = False

background_image = pygame.image.load('assets/images/casino.png')
background_image = pygame.transform.scale(background_image, (1200, 600))

while running:
    current_time = pygame.time.get_ticks()
    if menu:
        dealer = Dealer()
        player1 = Player()
        card_deck = 4 * cards
        bet_placed = False
        hit = False
        stand = False
        bet_amount = 0
        screen.blit(background_image, (-130, 0))
        current_frame += 1
        if current_frame >= frame_count * frame_rate:
            current_frame = 0  # Loop the animation
        frame_index = (current_frame // frame_rate) % frame_count
        screen.blit(frames[frame_index], (115, 205))  # Draw the current frame

        screen.blit(button_image, (150, -5))   

        draw_text("Blackjack Demo", 1000, 195, 70)
        draw_text("By Christian Duarte", 1000, 345, 40)

        draw_button(screen, button_colour, 600, 275, 250, 70)
        draw_text("Play Now", 1450, 615, 50)
        draw_button(screen, button_colour, 600, 375, 250, 70)
        draw_text("Quit", 1440, 815, 50)    

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                # Adjusted for "Play Now" button
                if 600 <= x <= 850 and 275 <= y <= 345:
                    menu = False
                    waiting_for_player1 = True
                    waiting_for_player2 = False
                # Adjusted for "Quit" button
                if 600 <= x <= 850 and 370 <= y <= 440:
                    running = False
    else:
        screen.blit(table, (0, 0))
        draw_button(screen, (200,0,0), 31, 29, 40, 40)
        draw_text('X', 100, 95, 40)
        draw_button(screen, button_colour, 30, 75, 115, 44)
        draw_text('Menu', 175, 195, 40)
        draw_text('Bet: ' + str(bet_amount), 190, 700, 40)

        draw_text('$: ' + str(player1.balance), 1560, 100, 40)
        draw_text('W ' + str(player1.wins) + ' D ' + str(player1.draws) + ' L ' + str(player1.losses), 1660, 195, 40)

        draw_button(screen, button_colour, 580, 480, 120, 50)
        draw_text('Stand', 1280, 1005, 40)

        draw_button(screen, button_colour, 320, 480, 120, 50)
        draw_text('Hit', 755, 1005, 40)

        chip1_rect = pygame.Rect(20, 400, chip1.get_width(), chip1.get_height())
        chip5_rect = pygame.Rect(110, 400, chip5.get_width(), chip5.get_height())
        chip10_rect = pygame.Rect(20, 500, chip10.get_width(), chip10.get_height())
        chip25_rect = pygame.Rect(110, 500, chip25.get_width(), chip25.get_height())
        chip50_rect = pygame.Rect(200, 500, chip50.get_width(), chip50.get_height())
        screen.blit(chip1, (20, 400))
        draw_text('1', 110, 870, 25)
        screen.blit(chip5, (110, 400))
        draw_text('5', 290, 870, 25)
        screen.blit(chip10, (20, 500))
        draw_text('10', 110, 1070, 25)
        screen.blit(chip25, (110, 500))
        draw_text('25', 292, 1070, 25)
        screen.blit(chip50, (200, 500))
        draw_text('50', 472, 1070, 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 31 < mouse_pos[0] < 31 + 40 and 29 < mouse_pos[1] < 29 + 40:
                    # X
                    pygame.quit()
                    sys.exit()
                elif 30 < mouse_pos[0] < 30 + 115 and 75 < mouse_pos[1] < 75 + 44:
                    # Menu
                    menu = True
                elif 580 <= mouse_pos[0] <= 700 and 480 <= mouse_pos[1] <= 530 and placed:
                    # Stand
                    stand = True
                elif 320 <= mouse_pos[0] <= 440 and 480 <= mouse_pos[1] <= 530 and placed and player1.hand_value <= 21:
                    # Hit
                    hit = True
                elif 30 <= mouse_pos[0] <= 145 and 270 <= mouse_pos[1] <= 314 and bet_placed and not placed:
                    # Reset
                    player1.balance += bet_amount
                    bet_amount = 0
                    bet_placed = False
                elif 30 <= mouse_pos[0] <= 145 and 210 <= mouse_pos[1] <= 314 and bet_placed and not placed:
                    # Place
                    placed = True
                    dealer.setup_hand(card_deck)
                    player1.setup_hand(card_deck)

                elif chip1_rect.collidepoint(mouse_pos):
                    if player1.balance >= 1:
                        bet_amount += 1
                        player1.balance -= 1
                        bet_placed = True
                elif chip5_rect.collidepoint(mouse_pos):
                    if player1.balance >= 5:
                        bet_amount += 5
                        player1.balance -= 5
                        bet_placed = True
                elif chip10_rect.collidepoint(mouse_pos):
                    if player1.balance >= 10:
                        bet_amount += 10
                        player1.balance -= 10
                        bet_placed = True
                elif chip25_rect.collidepoint(mouse_pos):
                    if player1.balance >= 25:
                        bet_amount += 25
                        player1.balance -= 25
                        bet_placed = True
                elif chip50_rect.collidepoint(mouse_pos):
                    if player1.balance >= 50:
                        bet_amount += 50
                        player1.balance -= 50
                        bet_placed = True

        if stand:
            dealer.dealer_play(card_deck, player1)
            dealer.draw_hand(screen, dealer, 465, 10, 30, 2)
            draw_text(str(player1.hand_value), 750, 870, 40)
            draw_text(str(dealer.hand_value), 750, 100, 40)
            
            result = check_winner(player1, dealer)
            screen.blit(button_image_2, (265, 310))   
            if result == 0:
                draw_text("Dealer Won!", 1035, 770, 70)
            elif result == 1:
                draw_text("Draw!", 1035, 770, 70)
            elif result == 2:
                draw_text("Player Won!", 1035, 770, 70)
                if player1.hand_value == 21:
                    player1.balance += bet_amount * 2.5 # Blackjack pays 3:2
                else:
                    player1.balance += bet_amount * 2 # Regular win pays 1:1
            elif player1.hand_value > 21:
                screen.blit(button_image_2, (265, 310))
                draw_text("Bust!", 1035, 770, 70)
                
            pygame.display.flip()
            pygame.time.wait(1000)
            hit = False
            bet_placed = False
            placed = False
            bet_amount = 0
            player1.reset_hand()
            dealer.reset_hand()
            stand = False
        elif hit:
            player1.hit_card(card_deck)
            pygame.display.flip()
            hit = False

        player1.draw_hand(screen, player1, 465, 420, 30, 1)

        if bet_placed == False and player1.balance > 0:
            screen.blit(button_image_2, (265, 310))  
            draw_text("Place Bet(s)", 1035, 770, 70)
        elif bet_placed == True and not placed:
            draw_button(screen, (200,0,0), 30, 270, 115, 44)
            draw_text('Reset', 175, 580, 40)
            draw_button(screen, button_colour, 30, 210, 115, 44)
            draw_text('Place', 175, 460, 40)
        elif placed:
            draw_text(str(player1.hand_value), 750, 870, 40)
            draw_text(str(dealer.hand_value), 750, 100, 40)
        elif player1.balance == 0:
            screen.blit(button_image_2, (265, 310))  
            draw_text("Game Over", 1035, 770, 70)
        
    

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()