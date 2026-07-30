"""
main.py
========
الملف الرئيسي للعبة - بعد حماية استدعاءات UI وتفادي خطأ big_font
"""

import sys
import os
import pygame

# إضافة مجلد المشروع الحالي إلى مسار النظام لتفادي مشاكل استيراد الموديولات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. استيراد الموديولات الخاصة بالفريق
try:
    from entities import Crosshair, Target
    from effects import ParticleSystem, ScreenShake, check_collision
    from ui import UI
except ImportError as e:
    print(f"خطأ في استيراد أحد موديولات الفريق: {e}")
    print("تأكد من وجود ملفات entities.py و effects.py و ui.py في نفس المجلد.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# إعدادات عامة
# ---------------------------------------------------------------------------
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h
FPS = 60
ROUND_TIME_LIMIT = 60  # حد الجولة بالثواني

# حالات اللعبة
STATE_START_MENU = "start_menu"
STATE_GAMEPLAY = "gameplay"
STATE_GAME_OVER = "game_over"
STATE_PAUSE = "pause"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Shooter Game")

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_START_MENU

        # --- ربط مكونات الفريق ---
        self.ui = UI()
        self.music_volume = 0.2
        self.ui.set_volume(self.music_volume)
        
        # التأكد من وجود المتغيرات الأساسية للخط في UI لتجنب الانهيار
        if not hasattr(self.ui, 'big_font'):
            self.ui.big_font = pygame.font.SysFont(None, 64)
        if not hasattr(self.ui, 'font'):
            self.ui.font = pygame.font.SysFont(None, 36)

        self.crosshair = Crosshair()
        self.targets = pygame.sprite.Group()
        self.particles = ParticleSystem()
        self.shake = ScreenShake()

        self.time_left = ROUND_TIME_LIMIT
        self.score = 0

    def spawn_targets(self, count=5):
        """دالة مساعدة لإعادة إنشاء أهداف جديدة"""
        self.targets.empty()
        import random
        for _ in range(count):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT - 50)
            self.targets.add(Target(x, y))

    def run(self):
        try:
            self.ui.play_music()
        except Exception:
            pass  # في حالة عدم وجود ملف الصوت
        
        pygame.mouse.set_visible(False)

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # الوقت بالثواني

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == STATE_START_MENU:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or \
                   event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_gameplay()

            elif self.state == STATE_GAMEPLAY:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = STATE_PAUSE

                # عند النقر بالماوس (إطلاق النار)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    try:
                        self.ui.play_shoot()
                    except Exception:
                        pass

                    mouse_pos = pygame.mouse.get_pos()

                    # فحص الاصطدام مع الأهداف
                    for target in list(self.targets):
                        if check_collision(mouse_pos, target):
                            self.score += 10
                            try:
                                self.particles.explode(target.rect.centerx, target.rect.centery, (255, 50, 50))
                            except Exception:
                                pass
                            
                            try:
                                self.shake.start(duration=10, magnitude=5)
                            except Exception:
                                pass

                            try:
                                self.ui.play_hit()
                            except Exception:
                                pass
                            
                            target.kill()  # إزالة الهدف المصاب

                    # إعادة توليد أهداف جديدة إذا انتهت
                    if len(self.targets) == 0:
                        self.spawn_targets(5)


            elif self.state == STATE_PAUSE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_GAMEPLAY
                    elif event.key == pygame.K_m:
                        if self.music_volume > 0:
                            self.music_volume = 0
                        else:
                            self.music_volume = 0.2
                        self.ui.set_volume(self.music_volume)
                    

            elif self.state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_gameplay()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def update(self, dt):
        if self.state != STATE_GAMEPLAY:
            return
        if self.state == STATE_GAMEPLAY:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.go_to_game_over()
                return

            for obj in (self.crosshair, self.targets, self.particles, self.shake):
                try:
                    if obj == self.targets:
                        obj.update(WINDOW_WIDTH, WINDOW_HEIGHT)
                    else:
                        obj.update()
                except Exception:
                    pass

    def draw(self):
        try:
            offset_x, offset_y = self.shake.get_offset()
        except Exception:
            offset_x, offset_y = 0, 0

        render_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        if self.state == STATE_START_MENU:
            try:
                self.ui.show_start_screen(render_surface)
            except Exception:
                # رسم شاشة بداية افتراضية لو حدث خطأ داخل UI
                render_surface.fill((20, 20, 40))
                font = pygame.font.SysFont(None, 48)
                txt = font.render("Press Enter to Start", True, (255, 255, 255))
                render_surface.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, WINDOW_HEIGHT//2))

        elif self.state == STATE_GAMEPLAY:
            try:
                self.ui.draw_background(render_surface)
            except Exception:
                render_surface.fill((30, 30, 30))

            self.targets.draw(render_surface)
            
            try:
                self.particles.draw(render_surface)
            except Exception:
                pass

            try:
                render_surface.blit(self.crosshair.image, self.crosshair.rect)
            except Exception:
                pass

            try:
                self.ui.draw_score(render_surface, self.score)
                self.ui.draw_timer(render_surface, self.time_left)
            except Exception:
                pass

        elif self.state == STATE_PAUSE:
            try:
                self.ui.draw_background(render_surface)
            except Exception:
                render_surface.fill((30, 30, 30))

                self.targets.draw(render_surface)

            try:
                self.particles.draw(render_surface)
            except Exception:
                pass

            try:
                render_surface.blit(self.crosshair.image, self.crosshair.rect)
            except Exception:
                pass

            try:
                self.ui.draw_score(render_surface, self.score)
                self.ui.draw_timer(render_surface, self.time_left)
                self.ui.show_pause(render_surface, self.music_volume > 0)
            except Exception:
                pass

        elif self.state == STATE_GAME_OVER:
            try:
                self.ui.show_game_over(render_surface, self.score)
            except Exception:
                render_surface.fill((40, 20, 20))
                font = pygame.font.SysFont(None, 48)
                txt = font.render(f"GAME OVER - Score: {self.score}", True, (255, 255, 255))
                render_surface.blit(txt, (WINDOW_WIDTH//2 - txt.get_width()//2, WINDOW_HEIGHT//2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(render_surface, (offset_x, offset_y))

    def start_gameplay(self):
        self.state = STATE_GAMEPLAY
        self.time_left = ROUND_TIME_LIMIT
        self.score = 0
        self.spawn_targets(5)

    def go_to_game_over(self):
        self.state = STATE_GAME_OVER


if __name__ == "__main__":
    game = Game()
    game.run()