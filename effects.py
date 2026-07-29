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
    """Precise collision check between a point (crosshair position) and a target.

    Returns True only if the point is within the target's circular radius.
    """
    return target.alive and point.distance_to(target.pos) <= target.radius


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

    def update(self):
        """Update particle position and age (Standard method style)."""
        self.pos += self.vel
        self.vel *= 0.95  # friction / slow down
        self.age += 1

        
        if self.age >= self.lifetime:
            self.alive = False

    def draw(self, surface):
        fade = max(0, 255 - int(255 * (self.age / self.lifetime)))
        color = (self.color[0], self.color[1], self.color[2])
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            s, (*color, fade), (self.radius, self.radius), self.radius
        )
        surface.blit(s, (self.pos.x - self.radius, self.pos.y - self.radius))


class ParticleSystem:
    """Manages all active particles (explosions) at once."""

    def __init__(self):
        self.particles = []

    def explode(self, x, y, color, count=18):
        """Spawn a burst of particles at (x, y) -- called when a target is hit."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        """Update and filter particles using list methods (for loop & remove)."""
        
        for p in self.particles:
            p.update()

        active_particles = []
        for p in self.particles:
            if p.alive:
                active_particles.append(p)
        self.particles = active_particles

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class ScreenShake:


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
        
        if self.timer <= 0:
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

    def __init__(self, pos, radius, alive=True):
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
        point = pygame.math.Vector2(105, 100)
        self.assertTrue(check_collision(point, target))

    def test_check_collision_miss(self):
        target = DummyTarget((100, 100), radius=20, alive=True)
        point = pygame.math.Vector2(130, 100)
        self.assertFalse(check_collision(point, target))

    def test_check_collision_dead_target(self):
        target = DummyTarget((100, 100), radius=20, alive=False)
        point = pygame.math.Vector2(100, 100)
        self.assertFalse(check_collision(point, target))

    # 2. Test Particle System
    def test_particle_lifecycle(self):
        particle = Particle(0, 0, (255, 0, 0))
        initial_lifetime = particle.lifetime

        for _ in range(initial_lifetime):
            particle.update()

        self.assertFalse(
            particle.alive, 
        )

    def test_particle_system_explode_and_update(self):
        ps = ParticleSystem()
        ps.explode(50, 50, (0, 255, 0), count=10)

        self.assertEqual(
            len(ps.particles), 10, 
        )

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
        self.assertEqual(
            shake.get_offset(), (0, 0), "Offset should be (0, 0) initially"
        )

        shake.start(duration=5, magnitude=10)
        self.assertNotEqual(shake.duration, 0, "Shake duration should be set")

        offset_x, offset_y = shake.get_offset()
        self.assertTrue(-10 <= offset_x <= 10)
        self.assertTrue(-10 <= offset_y <= 10)

        for _ in range(5):
            shake.update()

        self.assertEqual(
            shake.get_offset(),
            (0, 0),
            "Offset should return to (0, 0) after duration ends",
        )


# Run tests
if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)