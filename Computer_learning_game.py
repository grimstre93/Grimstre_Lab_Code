# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 10:01:55 2025

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
pygame.display.set_caption("Computer Shortcuts Memorization Test")

# Colors
BACKGROUND = (25, 25, 40)
ACCENT = (70, 130, 180)
HIGHLIGHT = (100, 180, 255)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (50, 150, 100)
BUTTON_HOVER = (70, 170, 120)
TIMER_WARNING = (220, 120, 100)
CORRECT_COLOR = (100, 200, 100)
INCORRECT_COLOR = (220, 100, 100)

# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
main_font = pygame.font.SysFont("Arial", 32)
button_font = pygame.font.SysFont("Arial", 28)
word_font = pygame.font.SysFont("Arial", 36, bold=True)
timer_font = pygame.font.SysFont("Arial", 46, bold=True)
small_font = pygame.font.SysFont("Arial", 24)

# Shortcut categories
SHORTCUT_CATEGORIES = [
    {
        "name": "General Computer Shortcuts",
        "shortcuts": [
            ("Ctrl + C", "Copy selected text or item"),
            ("Ctrl + V", "Paste copied content"),
            ("Ctrl + X", "Cut selected text or item"),
            ("Ctrl + Z", "Undo last action"),
            ("Ctrl + Y", "Redo last undone action"),
            ("Ctrl + A", "Select all"),
            ("Ctrl + S", "Save current document/file"),
            ("Ctrl + P", "Print"),
            ("Ctrl + F", "Find/search"),
            ("Alt + Tab", "Switch between open apps"),
            ("Alt + F4", "Close current window/app"),
            ("Windows + D", "Show desktop"),
            ("Windows + E", "Open File Explorer"),
            ("Windows + L", "Lock computer"),
            ("Windows + R", "Open Run dialog"),
            ("Windows + Shift + S", "Snip & Sketch (screenshot tool)")
        ]
    },
    {
        "name": "Microsoft Office / Editing Shortcuts",
        "shortcuts": [
            ("Ctrl + B", "Bold"),
            ("Ctrl + I", "Italic"),
            ("Ctrl + U", "Underline"),
            ("Ctrl + K", "Insert hyperlink"),
            ("Ctrl + N", "New document"),
            ("Ctrl + O", "Open document"),
            ("Ctrl + W", "Close document"),
            ("Ctrl + Shift + >", "Increase font size"),
            ("Ctrl + Shift + <", "Decrease font size")
        ]
    },
    {
        "name": "Browser Shortcuts",
        "shortcuts": [
            ("Ctrl + T", "Open new tab"),
            ("Ctrl + W", "Close current tab"),
            ("Ctrl + Shift + T", "Reopen last closed tab"),
            ("Ctrl + Tab", "Switch to next tab"),
            ("Ctrl + Shift + Tab", "Switch to previous tab"),
            ("Ctrl + H", "Open history"),
            ("Ctrl + J", "Open downloads"),
            ("Ctrl + L", "Focus address bar"),
            ("Alt + D", "Focus address bar"),
            ("F5", "Refresh page"),
            ("Ctrl + Shift + R", "Hard refresh (ignore cache)")
        ]
    },
    {
        "name": "Windows CMD Commands",
        "shortcuts": [
            ("dir", "List files and directories"),
            ("cd [path]", "Change directory"),
            ("cls", "Clear screen"),
            ("copy [src] [dest]", "Copy files"),
            ("move [src] [dest]", "Move files"),
            ("del [filename]", "Delete file"),
            ("mkdir [foldername]", "Create new directory"),
            ("rmdir [foldername]", "Remove directory"),
            ("ipconfig", "Show network configuration"),
            ("ping [host]", "Test network connection"),
            ("tasklist", "Show running processes"),
            ("taskkill /IM [process] /F", "Kill a process"),
            ("chkdsk", "Check disk for errors"),
            ("sfc /scannow", "Scan system files for corruption"),
            ("shutdown /s /t 0", "Shutdown immediately"),
            ("shutdown /r /t 0", "Restart immediately")
        ]
    },
    {
        "name": "Power User Shortcuts",
        "shortcuts": [
            ("Windows + X", "Open Quick Link menu"),
            ("Windows + Ctrl + D", "Create new virtual desktop"),
            ("Windows + Ctrl + → / ←", "Switch between virtual desktops"),
            ("Windows + Tab", "Task View (all open windows)"),
            ("Ctrl + Shift + Esc", "Open Task Manager"),
            ("Windows + I", "Open Settings"),
            ("Windows + Pause/Break", "System properties")
        ]
    }
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
        self.current_level = 0
        self.questions = []
        self.user_answers = []
        self.correct_answers = []
        self.score = 0
        self.total_score = 0
        self.start_time = 0
        self.memorize_time = 30  # 30 seconds per level
        self.test_start_time = 0
        
        # Create buttons
        center_x = WIDTH // 2
        self.start_button = Button(center_x - 100, 400, 200, 60, "Start Game", self.start_game)
        self.submit_button = Button(center_x - 100, 500, 200, 60, "Submit", self.submit_test)
        self.retry_button = Button(center_x - 100, 500, 200, 60, "Try Again", self.reset_game)
        self.next_button = Button(center_x - 100, 500, 200, 60, "Next Level", self.next_level)
        
    def start_game(self):
        self.state = "memorizing"
        self.current_level = 0
        self.total_score = 0
        self.prepare_level()
        
    def prepare_level(self):
        category = SHORTCUT_CATEGORIES[self.current_level]
        all_shortcuts = category["shortcuts"]
        self.questions = random.sample(all_shortcuts, min(5, len(all_shortcuts)))
        self.correct_answers = [shortcut[0] for shortcut in self.questions]
        self.user_answers = ["" for _ in self.questions]
        self.start_time = time.time()
        
    def next_level(self):
        self.current_level += 1
        if self.current_level < len(SHORTCUT_CATEGORIES):
            self.state = "memorizing"
            self.prepare_level()
        else:
            self.state = "final_results"
        
    def submit_test(self):
        self.state = "results"
        self.score = 0
        
        for i, answer in enumerate(self.user_answers):
            if answer.strip().upper() == self.correct_answers[i].upper():
                self.score += 1
                
        self.total_score += self.score
        
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
        elif self.state == "final_results":
            self.draw_final_results_screen(surface)
            
    def draw_start_screen(self, surface):
        # Draw title
        title = title_font.render("Shortcut Memorization Test", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw instructions
        instructions = [
            "You will go through 5 levels of computer shortcut tests.",
            "Each level focuses on a different category of shortcuts.",
            "You will have 30 seconds to memorize shortcuts for each level.",
            "Then you'll be tested on what you remember.",
            "You need at least 4/10 correct answers to pass each level."
        ]
        
        for i, line in enumerate(instructions):
            text = main_font.render(line, True, TEXT_COLOR)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, 180 + i*40))
            
        # Draw start button
        self.start_button.draw(surface)
        
    def draw_memorize_screen(self, surface):
        category = SHORTCUT_CATEGORIES[self.current_level]
        
        # Draw title
        title = title_font.render(f"Level {self.current_level + 1}: {category['name']}", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw timer
        elapsed = time.time() - self.start_time
        remaining = max(0, self.memorize_time - elapsed)
        mins, secs = divmod(int(remaining), 60)
        timer_text = timer_font.render(f"Time: {mins:02d}:{secs:02d}", True, 
                                     TIMER_WARNING if remaining < 10 else HIGHLIGHT)
        surface.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 120))
        
        # Draw shortcuts and their functions
        for i, (shortcut, function) in enumerate(self.questions):
            shortcut_text = word_font.render(shortcut, True, TEXT_COLOR)
            function_text = main_font.render(function, True, ACCENT)
            
            y_pos = 180 + i * 70
            surface.blit(shortcut_text, (WIDTH//2 - shortcut_text.get_width()//2, y_pos))
            surface.blit(function_text, (WIDTH//2 - function_text.get_width()//2, y_pos + 40))
            
    def draw_testing_screen(self, surface):
        category = SHORTCUT_CATEGORIES[self.current_level]
        
        # Draw title
        title = title_font.render(f"Level {self.current_level + 1}: {category['name']}", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw instructions
        instruction = main_font.render("Enter the shortcuts for these functions:", True, TEXT_COLOR)
        surface.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 100))
        
        # Draw function descriptions and input boxes
        for i, (_, function) in enumerate(self.questions):
            y_pos = 150 + i * 70
            
            # Draw function description
            function_text = main_font.render(function, True, TEXT_COLOR)
            surface.blit(function_text, (100, y_pos))
            
            # Draw input box
            input_rect = pygame.Rect(500, y_pos - 5, 200, 40)
            pygame.draw.rect(surface, (40, 40, 60), input_rect, border_radius=5)
            pygame.draw.rect(surface, HIGHLIGHT, input_rect, 2, border_radius=5)
            
            # Draw user input text
            input_text = main_font.render(self.user_answers[i], True, TEXT_COLOR)
            surface.blit(input_text, (input_rect.x + 10, input_rect.y + 5))
        
        # Draw submit button
        self.submit_button.draw(surface)
        
    def draw_results_screen(self, surface):
        category = SHORTCUT_CATEGORIES[self.current_level]
        
        # Draw title based on performance
        title_text = "Level Passed!" if self.score >= 4 else "Level Failed"
        title_color = CORRECT_COLOR if self.score >= 4 else INCORRECT_COLOR
        
        title = title_font.render(title_text, True, title_color)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw score
        score_text = main_font.render(f"You got {self.score} out of {len(self.questions)} correct", True, TEXT_COLOR)
        surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 120))
        
        # Draw correct answers and user answers
        for i, ((correct_shortcut, function), user_answer) in enumerate(zip(self.questions, self.user_answers)):
            y_pos = 180 + i * 60
            
            # Draw function
            function_text = small_font.render(function, True, TEXT_COLOR)
            surface.blit(function_text, (100, y_pos))
            
            # Draw correct answer
            correct_text = small_font.render(correct_shortcut, True, CORRECT_COLOR)
            surface.blit(correct_text, (400, y_pos))
            
            # Draw user answer
            user_color = CORRECT_COLOR if user_answer.strip().upper() == correct_shortcut.upper() else INCORRECT_COLOR
            user_text = small_font.render(user_answer, True, user_color)
            surface.blit(user_text, (600, y_pos))
        
        # Draw next button if passed, retry button if failed
        if self.score >= 4:
            self.next_button.draw(surface)
        else:
            self.retry_button.draw(surface)
            
    def draw_final_results_screen(self, surface):
        # Calculate final score and percentage
        total_possible = sum(min(5, len(category["shortcuts"])) for category in SHORTCUT_CATEGORIES)
        percentage = (self.total_score / total_possible) * 100
        
        # Determine grade based on percentage
        if percentage >= 90:
            grade = "Excellent / A"
        elif percentage >= 80:
            grade = "Very Good / B"
        elif percentage >= 70:
            grade = "Good / C"
        elif percentage >= 60:
            grade = "Fair / D"
        else:
            grade = "Poor / Fail"
            
        # Draw title
        title = title_font.render("Final Results", True, HIGHLIGHT)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Draw final score
        score_text = main_font.render(f"Final Score: {self.total_score}/{total_possible} ({percentage:.1f}%)", True, TEXT_COLOR)
        surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 120))
        
        # Draw grade
        grade_text = main_font.render(f"Grade: {grade}", True, TEXT_COLOR)
        surface.blit(grade_text, (WIDTH//2 - grade_text.get_width()//2, 170))
        
        # Draw level scores
        level_y = 220
        for i in range(len(SHORTCUT_CATEGORIES)):
            level_text = main_font.render(f"Level {i+1}: {min(5, len(SHORTCUT_CATEGORIES[i]['shortcuts']))} questions", True, TEXT_COLOR)
            surface.blit(level_text, (WIDTH//2 - 200, level_y + i*40))
        
        # Draw retry button
        self.retry_button.draw(surface)

def main():
    game = Game()
    clock = pygame.time.Clock()
    active_input = None
    
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
                elif game.state == "results" and game.next_button.check_click(mouse_pos):
                    game.next_button.action()
                elif game.state == "final_results" and game.retry_button.check_click(mouse_pos):
                    game.retry_button.action()
                    
                # Check if any input box was clicked
                if game.state == "testing":
                    for i in range(len(game.questions)):
                        input_rect = pygame.Rect(500, 145 + i * 70, 200, 40)
                        if input_rect.collidepoint(mouse_pos):
                            active_input = i
                            break
                    else:
                        active_input = None
                    
            if event.type == pygame.KEYDOWN:
                if game.state == "testing" and active_input is not None:
                    if event.key == pygame.K_RETURN:
                        if active_input < len(game.questions) - 1:
                            active_input += 1
                        else:
                            game.submit_test()
                    elif event.key == pygame.K_TAB:
                        active_input = (active_input + 1) % len(game.questions)
                    elif event.key == pygame.K_BACKSPACE:
                        game.user_answers[active_input] = game.user_answers[active_input][:-1]
                    else:
                        # Only allow certain characters in shortcuts
                        if event.unicode.isprintable() and event.unicode not in '"\'`':
                            game.user_answers[active_input] += event.unicode
        
        # Update button hover states
        if game.state == "start":
            game.start_button.check_hover(mouse_pos)
        elif game.state == "testing":
            game.submit_button.check_hover(mouse_pos)
        elif game.state == "results":
            if game.score >= 4:
                game.next_button.check_hover(mouse_pos)
            else:
                game.retry_button.check_hover(mouse_pos)
        elif game.state == "final_results":
            game.retry_button.check_hover(mouse_pos)
            
        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(BACKGROUND)
        game.draw(screen)
        
        # Draw input cursor in testing mode
        if game.state == "testing" and active_input is not None:
            input_text = main_font.render(game.user_answers[active_input], True, TEXT_COLOR)
            cursor_x = 510 + input_text.get_width()
            cursor_y = 150 + active_input * 70
            pygame.draw.line(screen, HIGHLIGHT, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()