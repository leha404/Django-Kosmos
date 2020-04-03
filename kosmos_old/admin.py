from django.contrib import admin
from .models import Sprint, Goal, Habit, Week, Day, Day_habit, Task

admin.site.register(Sprint)
admin.site.register(Goal)
admin.site.register(Habit)
admin.site.register(Week)
admin.site.register(Day)
admin.site.register(Day_habit)
admin.site.register(Task)