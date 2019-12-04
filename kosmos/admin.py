from django.contrib import admin
from .models import Sprint, Goal, Habbit, Week, Day, Day_habbit, Task

admin.site.register(Sprint)
admin.site.register(Goal)
admin.site.register(Habbit)
admin.site.register(Week)
admin.site.register(Day)
admin.site.register(Day_habbit)
admin.site.register(Task)