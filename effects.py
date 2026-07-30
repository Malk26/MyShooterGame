"""
effects.py
Responsible member: Member 3 (Physics, Collisions & Effects Developer)

Contains:
- check_collision: precise hit detection between crosshair and a target
- Particle / ParticleSystem: small "explosion" pieces when a target is hit
- ScreenShake: simple camera-shake effect used when shooting / hitting
"""

import random
import unittest
import pygame


def check_collision(point, target):
    """Precise collision check between a point (crosshair/mouse position) and a target.

    Supports both Vector2 and (x, y) tuples for point.
    """
    if not hasattr(target, 'alive') or not target.alive:
        return False
        
    point_vec = pygame.math.Vector2(point)
    target_pos = pygame.math.Vector2(target.pos) if hasattr(target, 'pos') else pygame.math.Vector2(target.rect.center)
    radius = getattr(target, 'radius', target.rect.width / 2 if hasattr(target, 'rect') else 20)

    return point_vec.distance_to(target_pos) <= radius


class Particle:
    """A single small piece flying outward from an explosion point."""

    def __init__(self, x, y, color):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)
        self.vel = pygame.math.Vector2(speed, 0).rotate(angle)
        self.color = color
        self.radius = random.randint(2, 4)
        self.lifetime = random.randint(20, 40)  # frames
        self.age = 0
        self.alive = True

        # إنشاء سطح الجسيم مرة واحدة للأداء المباشر
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.surface, (*self.color, 255), (self.radius, self.radius), self.radius
        )

    def update(self):
        """Update particle position and age."""
        self.pos += self.vel
        self.vel *= 0.95  # friction / slow down
        self.age += 1

        if self.age >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return
        fade = max(0, 255 - int(255 * (self.age / self.lifetime)))
        self.surface.set_alpha(fade)
        surface.blit(self.surface, (self.pos.x - self.radius, self.pos.y - self.radius))


class ParticleSystem:
    """Manages all active particles (explosions) at once."""

    def __init__(self):
        self.particles = []

    def explode(self, x, y, color, count=18):
        """Spawn a burst of particles at (x, y) -- called when a target is hit."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        """Update and filter particles quickly using List Comprehension."""
        for p in self.particles:
            p.update()
        
        # تصفية الجسيمات الميتة بسطر واحد سريعة للأداء
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class ScreenShake:
    """Camera shake effect generator."""

    def __init__(self):
        self.duration = 0
        self.timer = 0
        self.magnitude = 0

    def start(self, duration=20, magnitude=10):
        self.duration = duration
        self.timer = duration
        self.magnitude = magnitude

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def get_offset(self):
        if self.timer <= 0 or self.duration == 0:
            return (0, 0)

        strength = self.magnitude * (self.timer / self.duration)

        return (
            random.randint(-int(strength), int(strength)),
            random.randint(-int(strength), int(strength)),
        )


# =============================================================
# UNIT TESTS
# =============================================================

class DummyTarget:
    def init(self, pos, radius, alive=True):
        self.pos = pygame.math.Vector2(pos)
        self.radius = radius
        self.alive = alive


class TestEffects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
# 1. Test check_collision Function
    def test_check_collision_hit(self):
        target = DummyTarget((100, 100), radius=20, alive=True)
        point = (105, 100)  # اختبار إرسال tuple بدلاً من Vector2
        self.assertTrue(check_collision(point, target))

    def test_check_collision_miss(self):
        target = DummyTarget((100, 100), radius=20, alive=True)
        point = (130, 100)
        self.assertFalse(check_collision(point, target))

    def test_check_collision_dead_target(self):
        target = DummyTarget((100, 100), radius=20, alive=False)
        point = (100, 100)
        self.assertFalse(check_collision(point, target))

    # 2. Test Particle System
    def test_particle_lifecycle(self):
        particle = Particle(0, 0, (255, 0, 0))
        initial_lifetime = particle.lifetime

        for _ in range(initial_lifetime):
            particle.update()

        self.assertFalse(particle.alive)

    def test_particle_system_explode_and_update(self):
        ps = ParticleSystem()
        ps.explode(50, 50, (0, 255, 0), count=10)

        self.assertEqual(len(ps.particles), 10)

        for p in ps.particles:
            p.age = p.lifetime
            p.alive = False      

        ps.update()
        self.assertEqual(
            len(ps.particles),
            0,
            "Dead particles should be removed after update",
        )

    # 3. Test ScreenShake
    def test_screen_shake(self):
        shake = ScreenShake()
        self.assertEqual(shake.get_offset(), (0, 0))

        shake.start(duration=5, magnitude=10)
        self.assertNotEqual(shake.duration, 0)

        offset_x, offset_y = shake.get_offset()
        self.assertTrue(-10 <= offset_x <= 10)
        self.assertTrue(-10 <= offset_y <= 10)

        for _ in range(5):
            shake.update()

        self.assertEqual(shake.get_offset(), (0, 0))


if __name__ == "main":
    unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)