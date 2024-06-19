import pygame
import random

cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
twos = ['C2.png', 'D2.png', 'H2.png', 'S2.png']
threes = ['C3.png', 'D3.png', 'H3.png', 'S3.png']
fours = ['C4.png', 'D4.png', 'H4.png', 'S4.png']
fives = ['C5.png', 'D5.png', 'H5.png', 'S5.png']
sixes = ['C6.png', 'D6.png', 'H6.png', 'S6.png']
sevens = ['C7.png', 'D7.png', 'H7.png', 'S7.png']
eights = ['C8.png', 'D8.png', 'H8.png', 'S8.png']
nines = ['C9.png', 'D9.png', 'H9.png', 'S9.png']
tens = ['C10.png', 'D10.png', 'H10.png', 'S10.png']
jacks = ['CJ.png', 'DJ.png', 'HJ.png', 'SJ.png']
queens = ['CQ.png', 'DQ.png', 'HQ.png', 'SQ.png']
kings = ['CK.png', 'DK.png', 'HK.png', 'SK.png']
aces = ['CA.png', 'DA.png', 'HA.png', 'SA.png']
card_name = ''

class Dealer:
    def __init__ (self):
        self.hand = []
        self.hand_value = 0
        self.hand_images = []

    def reset_hand(self):
        self.hand = []
        self.hand_value = 0
        self.hand_images = []

    def hit_card(self, card_deck):
        card = random.choice(card_deck)
        card_deck.remove(card)
        self.hand.append(card)
        self.update_hand_images(card)
    
    def update_hand_images(self, card):
        # This method updates self.hand_images based on the latest card added
        card_map = {
            '2': twos, '3': threes, '4': fours, '5': fives,
            '6': sixes, '7': sevens, '8': eights, '9': nines,
            '10': tens, 'J': jacks, 'Q': queens, 'K': kings, 'A': aces
        }
        if card in card_map:
            self.hand_images.append(random.choice(card_map[card]))
            if card == 'A':
                if self.hand_value + 11 > 21:
                    self.hand_value += 1
                else:
                    self.hand_value += 11
            elif card in ['J', 'Q', 'K']:
                self.hand_value += 10
            else:
                self.hand_value += int(card)

    def setup_hand(self, card_deck):
        self.reset_hand()
        self.hit_card(card_deck)
        self.hit_card(card_deck)

    def draw_hand(self, screen, player, start_x, start_y, card_offset, player_type):

        for i, card in enumerate(player.hand_images):
            # Calculate the position for this card
            if player_type == 1:
                card_pos_y = start_y - (i * card_offset)
            elif player_type == 2:
                card_pos_y = start_y + (i * card_offset)
            # Draw the card
            card_image = pygame.image.load('assets/images/cards/'+str(card))
            card_image = pygame.transform.scale(card_image, (90, 130))
            screen.blit(card_image, (start_x, card_pos_y))

    def dealer_play(self, card_deck, player):
        while self.hand_value <= 16 and player.hand_value <= 21:
            self.hit_card(card_deck)

        
class Player(Dealer):
    def __init__ (self):
        super().__init__()
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.balance = 100


def check_winner(player, dealer):
    if player.hand_value > 21:
        player.losses += 1
        return 0
    else:
        if dealer.hand_value > 21 or player.hand_value > dealer.hand_value:
            player.wins += 1
            return 2
        elif player.hand_value == dealer.hand_value:
            player.draws += 1
            return 1
        elif dealer.hand_value > player.hand_value:
            player.losses += 1
            return 0
        else: 
            return 3