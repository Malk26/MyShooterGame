"""
main.py
========
الملف الرئيسي للعبة — من مسؤولية "قائد الفريق / المبرمج الرئيسي".

المهام التي يغطيها هذا الملف:
    1) إنشاء النافذة الرئيسية وضبط الـ FPS وحلقة اللعبة الأساسية.
    2) إدارة حالات اللعبة (Game States): شاشة البداية - شاشة اللعب - شاشة النهاية.
    3) ربط أكواد بقية الفريق (اللاعب، الأعداء، العناصر...) عبر نقاط استيراد واضحة.
    4) إدارة الوقت (Timer) بحد 60 ثانية للجولة.

طريقة عمل بقية الفريق:
    - كل عضو يكتب كوده في ملف/موديول خاص به داخل مجلد المشروع
      (مثال: player.py, enemy.py, ui.py ...).
    - كل موديول يوفر (على الأقل) الدوال التالية حتى يسهل ربطه هنا:
          setup()            -> تُستدعى مرة واحدة عند بدء الجولة (Gameplay)
          update(dt)         -> تُستدعى كل فريم لتحديث المنطق
          draw(surface)      -> تُستدعى كل فريم لرسم العناصر
          handle_event(event)-> (اختياري) لمعالجة أحداث خاصة بالموديول
    - إن لم يكن الموديول موجودًا بعد، الكود هنا يعمل بدون أخطاء (Placeholder)
      حتى يتم تسليمه، وذلك عبر try/except عند الاستيراد.
"""

import sys
import pygame

# ---------------------------------------------------------------------------
# إعدادات عامة
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
ROUND_TIME_LIMIT = 60  # حد الجولة بالثواني

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
GREEN = (0, 200, 100)
RED = (200, 50, 50)
YELLOW = (240, 200, 40)

# ---------------------------------------------------------------------------
# حالات اللعبة
# ---------------------------------------------------------------------------
STATE_START_MENU = "start_menu"
STATE_GAMEPLAY = "gameplay"
STATE_GAME_OVER = "game_over"


# ---------------------------------------------------------------------------
# نقطة ربط أكواد بقية الفريق
# ---------------------------------------------------------------------------
# كل عضو بالفريق يضيف اسم الموديول الخاص به هنا بعد الاستيراد.
# مثال حقيقي بعد التسليم:
#     import player
#     import enemy
#     TEAM_MODULES = [player, enemy]
#
# حاليًا نستخدم try/except حتى لا يتوقف المشروع إذا لم تُسلَّم الملفات بعد.

TEAM_MODULES = []

try:
    import player  # noqa: F401  -- ملف زميل الفريق المسؤول عن اللاعب
    TEAM_MODULES.append(player)
except ImportError:
    player = None

try:
    import enemy  # noqa: F401  -- ملف زميل الفريق المسؤول عن الأعداء
    TEAM_MODULES.append(enemy)
except ImportError:
    enemy = None

# أضف أي موديول آخر لبقية الفريق بنفس الطريقة (ui.py, items.py, score.py ...)


def call_if_exists(module, func_name, *args, **kwargs):
    """يستدعي دالة من موديول فقط إن كانت موجودة، لتفادي الأخطاء قبل التسليم."""
    if module is None:
        return
    func = getattr(module, func_name, None)
    if callable(func):
        func(*args, **kwargs)


# ---------------------------------------------------------------------------
# الفئة الرئيسية للعبة
# ---------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("مشروع الفريق - اللعبة")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = STATE_START_MENU

        self.font_big = pygame.font.SysFont(None, 64)
        self.font_med = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 26)

        # الوقت المتبقي للجولة (يُعاد ضبطه عند دخول Gameplay)
        self.time_left = ROUND_TIME_LIMIT

        # مكان لتخزين نتيجة اللاعب (يمكن لأي موديول تحديثها)
        self.score = 0

    # -----------------------------------------------------------------
    # حلقة اللعبة الأساسية
    # -----------------------------------------------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # الوقت بالثواني منذ آخر فريم

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # -----------------------------------------------------------------
    # معالجة الأحداث
    # -----------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == STATE_START_MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start_gameplay()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_gameplay()

            elif self.state == STATE_GAMEPLAY:
                # تمرير الحدث لكل موديولات الفريق التي تحتاج معالجة أحداث خاصة
                for module in TEAM_MODULES:
                    call_if_exists(module, "handle_event", event)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.go_to_game_over()

            elif self.state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = STATE_START_MENU

    # -----------------------------------------------------------------
    # تحديث المنطق حسب الحالة الحالية
    # -----------------------------------------------------------------
    def update(self, dt):
        if self.state == STATE_GAMEPLAY:
            # إدارة المؤقت (60 ثانية للجولة)
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.go_to_game_over()
                return

            # تحديث منطق كل موديولات الفريق
            for module in TEAM_MODULES:
                call_if_exists(module, "update", dt)

    # -----------------------------------------------------------------
    # الرسم حسب الحالة الحالية
    # -----------------------------------------------------------------
    def draw(self):
        if self.state == STATE_START_MENU:
            self.draw_start_menu()
        elif self.state == STATE_GAMEPLAY:
            self.draw_gameplay()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()

    def draw_start_menu(self):
        self.screen.fill(DARK_GRAY)
        title = self.font_big.render("اسم اللعبة", True, WHITE)
        hint = self.font_small.render(
            "اضغط Enter أو انقر لبدء اللعب", True, YELLOW
        )
        self.screen.blit(
            title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        )
        self.screen.blit(
            hint, hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        )

    def draw_gameplay(self):
        self.screen.fill(BLACK)

        # رسم عناصر كل موديولات الفريق
        for module in TEAM_MODULES:
            call_if_exists(module, "draw", self.screen)

        # واجهة المعلومات العلوية: المؤقت والنقاط
        timer_color = RED if self.time_left <= 10 else GREEN
        timer_text = self.font_med.render(
            f"الوقت: {int(self.time_left)}", True, timer_color
        )
        score_text = self.font_med.render(f"النقاط: {self.score}", True, WHITE)

        self.screen.blit(timer_text, (20, 15))
        self.screen.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 15))

    def draw_game_over(self):
        self.screen.fill(DARK_GRAY)
        title = self.font_big.render("انتهت الجولة", True, RED)
        score_text = self.font_med.render(f"نتيجتك: {self.score}", True, WHITE)
        hint = self.font_small.render("اضغط Enter للعودة للقائمة الرئيسية", True, YELLOW)

        self.screen.blit(
            title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        )
        self.screen.blit(
            score_text, score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        )
        self.screen.blit(
            hint, hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        )

    # -----------------------------------------------------------------
    # الانتقال بين الحالات
    # -----------------------------------------------------------------
    def start_gameplay(self):
        self.state = STATE_GAMEPLAY
        self.time_left = ROUND_TIME_LIMIT
        self.score = 0

        # استدعاء دالة setup الخاصة بكل موديول عند بدء جولة جديدة
        for module in TEAM_MODULES:
            call_if_exists(module, "setup")

    def go_to_game_over(self):
        self.state = STATE_GAME_OVER


# ---------------------------------------------------------------------------
# نقطة تشغيل البرنامج
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()
