import pygame

pygame.init()
pygame.mixer.init()


class UI:
    def __init__(self):
        # Fonts
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 50)

        # Images
        self.background = pygame.image.load("assets/images/background.png")
        self.crosshair = pygame.image.load("assets/images/crosshair.png")
        self.icon = pygame.image.load("assets/images/icon.png")

        # Sounds
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.mp3")
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.mp3")

        # Background Music
        pygame.mixer.music.load("assets/sounds/bg.mp3")

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_score(self, screen, score):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    def draw_high_score(self, screen, high_score):
        high_score_text = self.font.render(
            f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (20, 60))

    def draw_timer(self, screen, time_left):
         timer = self.font.render(f"Time: {int(time_left)}", True, (255, 255, 0))
         screen.blit(timer, (850, 20))

    def draw_fps(self, screen, clock):
        fps = self.font.render(f"FPS: {int(clock.get_fps())}", True, (0, 255, 0))
        screen.blit(fps, (850, 60))

    def play_music(self):
        pygame.mixer.music.play(-1)

    def pause_music(self):
          pygame.mixer.music.pause()

    def resume_music(self):
         pygame.mixer.music.unpause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_shoot(self):
        self.shoot_sound.play()

    def play_hit(self):
        self.hit_sound.play()

    def show_game_over(self, screen):
        text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(500, 350))
        screen.blit(text, text_rect)

    def draw_crosshair(self, screen):
        x, y = pygame.mouse.get_pos()
        rect = self.crosshair.get_rect(center=(x, y))
        screen.blit(self.crosshair, rect)

    def show_pause(self, screen):
        text = self.big_font.render("PAUSED", True, (255, 255, 0))
        hint = self.font.render("Press ESC To Continue", True, (255, 255, 255))

        screen.blit(text, text.get_rect(center=(500, 300)))
        screen.blit(hint, hint.get_rect(center=(500, 360)))

    def show_start_screen(self, screen):
        title = self.big_font.render("TARGET SHOOTER", True, (255, 255, 255))
        hint = self.font.render("Press ENTER To Start", True, (255, 255, 0))

        screen.blit(title, title.get_rect(center=(500, 250)))
        screen.blit(hint, hint.get_rect(center=(500, 320)))

    def set_icon(self):
        pygame.display.set_icon(self.icon)

    def hide_cursor(self):
        pygame.mouse.set_visible(False)

    def show_cursor(self):
        pygame.mouse.set_visible(True)