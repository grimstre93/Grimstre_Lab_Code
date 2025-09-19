# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 11:06:07 2025

@author: samng
"""

import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Memorization Test")

# Colors
BACKGROUND = (25, 25, 40)
ACCENT = (70, 130, 180)
HIGHLIGHT = (100, 180, 255)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (50, 150, 100)
BUTTON_HOVER = (70, 170, 120)
TIMER_WARNING = (220, 120, 100)

# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
main_font = pygame.font.SysFont("Arial", 32)
button_font = pygame.font.SysFont("Arial", 28)
word_font = pygame.font.SysFont("Arial", 36, bold=True)
timer_font = pygame.font.SysFont("Arial", 46, bold=True)

# Word list - you can customize this list
WORD_BANK = [
    "PYTHON", "PYGAME", "PROGRAMMING", "ALGORITHM", "VARIABLE",
    "FUNCTION", "LOOP", "CONDITIONAL", "LIST", "DICTIONARY",
    "STRING", "INTEGER", "BOOLEAN", "CLASS", "OBJECT",
    "METHOD", "MODULE", "LIBRARY", "INTERFACE", "ARGUMENT",
    "PARAMETER", "RETURN", "EXCEPTION", "DEBUGGING", "ITERATION",
    "RECURSION", "COMPILER", "INTERPRETER", "SYNTAX", "SEMANTICS"
]

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, HIGHLIGHT, self.rect, 3, border_radius=12)
        
        text_surf = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos) and self.action is not None

class Game:
    def __init__(self):
        self.state = "start"  # start, memorizing, testing, results
        self.words_to_memorize = []
        self.user_input = ""
        self.correct_words = []
        self.incorrect_words = []
        self.missed_words = []
        self.start_time = 0
        self.memorize_time = 120  # 2 minutes in seconds
        self.test_start_time = 0
        
        # Create buttons
        center_x = WIDTH // 2
        self.start_button = Button(center_x - 100, 400, 200, 60, "Start Game", self.start_game)
        self.submit_button = Button(center_x - 100, 500, 200, 60, "Submit", self.submit_test)
        self.retry_button = Button(center_x - 100, 500, 200, 60, "Try Again", self.reset_game)
        
    def start_game(self):
        self.state = "memorizing"
        self.words_to_memorize = random.sample(WORD_BANK, 10)
        self.start_time = time.time()
        
    def submit_test(self):
        self.state = "results"
        user_words = [word.strip().upper() for word in self.user_input.split(",") if word.strip()]
        
        self.correct_words = []
        self.incorrect_words = []
        self.missed_words = []
        
        for word in user_words:
            if word in self.words_to_memorize and word not in self.correct_words:
                self.correct_words.append(word)
            else:
                self.incorrect_words.append(word)
                
        for word in self.words_to_memorize:
            if word not in self.correct_words:
                self.missed_words.append(word)
                
    def reset_game(self):
        self.__init__()
        
    def update(self):
        if self.state == "memorizing":
            elapsed = time.time() - self.start_time
            if elapsed >= self.memorize_time:
                self.state = "testing"
                self.test_start_time = time.time()
                
    def draw(self, surface):
        if self.state == "start":
            self.draw_start_screen(surface)
        elif self.state == "memorizing":
            self.draw_memorize_screen(surface)
        elif self.state == "testing":
            self.draw_testing_screen(surface)
        elif self.state == "results":
            self.draw_results_screen(surface)
            
    def draw_start_screen(self, surface):
        # Draw title
        title = title_font.render("Word Memorization Test", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw instructions
        instructions = [
            "You will have 2 minutes to memorize 10 words.",
            "After time is up, you will be tested on how many",
            "words you can remember.",
            "Enter your answers separated by commas."
        ]
        
        for i, line in enumerate(instructions):
            text = main_font.render(line, True, TEXT_COLOR)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*50))
            
        # Draw start button
        self.start_button.draw(surface)
        
    def draw_memorize_screen(self, surface):
        # Draw title
        title = title_font.render("Memorize These Words", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw timer
        elapsed = time.time() - self.start_time
        remaining = max(0, self.memorize_time - elapsed)
        mins, secs = divmod(int(remaining), 60)
        timer_text = timer_font.render(f"Time: {mins:02d}:{secs:02d}", True, 
                                     TIMER_WARNING if remaining < 30 else HIGHLIGHT)
        surface.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 120))
        
        # Draw words in two columns
        for i, word in enumerate(self.words_to_memorize):
            column = i % 2
            row = i // 2
            word_text = word_font.render(word, True, TEXT_COLOR)
            x_pos = WIDTH//4 * (1 + 2*column) - word_text.get_width()//2
            y_pos = 200 + row * 60
            surface.blit(word_text, (x_pos, y_pos))
            
    def draw_testing_screen(self, surface):
        # Draw title
        title = title_font.render("Enter Words You Remember", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw instructions
        instruction = main_font.render("Separate words with commas", True, TEXT_COLOR)
        surface.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 120))
        
        # Draw input box
        input_rect = pygame.Rect(WIDTH//2 - 300, 200, 600, 60)
        pygame.draw.rect(surface, (40, 40, 60), input_rect, border_radius=10)
        pygame.draw.rect(surface, HIGHLIGHT, input_rect, 3, border_radius=10)
        
        # Draw user input text
        input_text = main_font.render(self.user_input, True, TEXT_COLOR)
        surface.blit(input_text, (input_rect.x + 15, input_rect.y + 15))
        
        # Draw submit button
        self.submit_button.draw(surface)
        
    def draw_results_screen(self, surface):
        # Draw title based on performance
        correct_count = len(self.correct_words)
        title_text = ""
        if correct_count == 10:
            title_text = "Perfect Score! Amazing Memory!"
        elif correct_count >= 7:
            title_text = "Great Job!"
        elif correct_count >= 5:
            title_text = "Good Effort!"
        else:
            title_text = "Keep Practicing!"
            
        title = title_font.render(title_text, True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw score
        score_text = main_font.render(f"You remembered {correct_count} out of 10 words", True, TEXT_COLOR)
        surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 120))
        
        # Draw correct words
        if self.correct_words:
            correct_title = main_font.render("Correct words:", True, BUTTON_COLOR)
            surface.blit(correct_title, (WIDTH//2 - 350, 180))
            
            for i, word in enumerate(self.correct_words):
                word_text = main_font.render(word, True, TEXT_COLOR)
                surface.blit(word_text, (WIDTH//2 - 350, 220 + i*40))
        
        # Draw missed words
        if self.missed_words:
            missed_title = main_font.render("Missed words:", True, TIMER_WARNING)
            surface.blit(missed_title, (WIDTH//2 + 50, 180))
            
            for i, word in enumerate(self.missed_words):
                word_text = main_font.render(word, True, TEXT_COLOR)
                surface.blit(word_text, (WIDTH//2 + 50, 220 + i*40))
        
        # Draw retry button
        self.retry_button.draw(surface)

def main():
    game = Game()
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == "start" and game.start_button.check_click(mouse_pos):
                    game.start_button.action()
                elif game.state == "testing" and game.submit_button.check_click(mouse_pos):
                    game.submit_button.action()
                elif game.state == "results" and game.retry_button.check_click(mouse_pos):
                    game.retry_button.action()
                    
            if event.type == pygame.KEYDOWN:
                if game.state == "testing":
                    if event.key == pygame.K_RETURN:
                        game.submit_test()
                    elif event.key == pygame.K_BACKSPACE:
                        game.user_input = game.user_input[:-1]
                    elif event.key == pygame.K_COMMA:
                        game.user_input += ","
                    elif event.unicode.isalpha() or event.unicode.isspace():
                        game.user_input += event.unicode.upper()
        
        # Update button hover states
        if game.state == "start":
            game.start_button.check_hover(mouse_pos)
        elif game.state == "testing":
            game.submit_button.check_hover(mouse_pos)
        elif game.state == "results":
            game.retry_button.check_hover(mouse_pos)
            
        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(BACKGROUND)
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()