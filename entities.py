import pygame
import random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image_path=None):
        super().__init__()
        
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        else:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 5)
            pygame.draw.line(self.image, (255, 0, 0), (20, 0), (20, 40), 2)
            pygame.draw.line(self.image, (255, 0, 0), (0, 20), (40, 20), 2)
            
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None):
        super().__init__()
        
        # تحميل الصورة إذا كانت متوفرة، وإلا يتم رسم شكل افتراضي
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        else:
            # شكل افتراضي: مربع أحمر بحجم 40x40
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # تجنب السرعة صفر لتستمر الحركة دائماً
        self.speed_x = random.choice([-5, -4, -3, 3, 4, 5])
        self.speed_y = random.choice([-5, -4, -3, 3, 4, 5])

    def update(self):
        # تحريك الهدف
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # الارتداد عند ملامسة حواف الشاشة (أبعاد 800x600)
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.speed_x *= -1
            
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.speed_y *= -1