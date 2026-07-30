import pygame
import random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image_path=None):  # تم إصلاح المسمى إلى __init__
        super().__init__()  # تم إصلاح المسمى إلى __init__
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (40, 40))
            except Exception:
                self._create_default_crosshair()
        else:
            self._create_default_crosshair()
            
        self.rect = self.image.get_rect()

    def _create_default_crosshair(self):
        """إنشاء نيشان افتراضي في حال عدم وجود صورة"""
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 5)
        pygame.draw.line(self.image, (255, 0, 0), (20, 0), (20, 40), 2)
        pygame.draw.line(self.image, (255, 0, 0), (0, 20), (40, 20), 2)

    def update(self):
        # تحديث موقع النيشان مع الماوس
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None):  # تم إصلاح المسمى إلى __init__
        super().__init__()  # تم إصلاح المسمى هنا وتجاوز خطأ التمرير

        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (40, 40))
            except Exception:
                self._create_default_target()
        else:
            self._create_default_target()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # --- إضافة خاصيات لتتوافق مع ملف الفيزياء (effects.py) ---
        self.pos = pygame.math.Vector2(self.rect.center)
        self.radius = 20  # نصف قطر الهدف للتصويب الدائري
        self.alive = True

        # تحديد سرعة الحركة
        self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])
        self.speed_y = random.choice([-4, -3, -2, 2, 3, 4])

    def _create_default_target(self):
        """إنشاء هدف افتراضي في حال عدم وجود صورة"""
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # تحسين شكل الهدف الافتراضي ليكون حلقة هدف حمراء وبيضاء
        pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 20)
        pygame.draw.circle(self.image, (255, 255, 255), (20, 20), 12)
        pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 5)

    def update(self, screen_width=800, screen_height=600):
        if not self.alive:
            return

        # تحريك الهدف
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # الارتداد عند ملامسة حواف الشاشة الديناميكية
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1
            
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        # تحديث المتجه pos ليكون دائماً متطابقاً مع مركز rect
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery

    def kill(self):
        """تحديث حالة الهدف عند تدميره"""
        self.alive = False
        super().kill()