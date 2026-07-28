# My Shooter Game - Effects Module

هذا الملف يحتوي على كود الفيزيا والتأثيرات الخاصة باللعبة (Member 3).

## المحتويات:
- `check_collision(point, target)`: لفحص التصادم بين النيشان والأهداف.
- `Particle` & `ParticleSystem`: لعمل تأثير الانفجارات عند إصابة الهدف.
- `ScreenShake`: لعمل تأثير اهتزاز الشاشة عند إطلاق النار أو الإصابة.

## طريقة الاستخدام في ملفك:
```python
from effects import check_collision, ParticleSystem, ScreenShake