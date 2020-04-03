from django.conf import settings
from django.db import models
from django.utils import timezone


class Sprint(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_begin = models.DateField()
    date_end = models.DateField()
    reward = models.CharField(max_length=200, blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.date_begin)

class Goal(models.Model):
    text = models.TextField()
    is_complete = models.IntegerField()
    code_heirarchy = models.IntegerField()
    sprint_id = models.ForeignKey('Sprint', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return (self.text + ' ; ' + str(self.sprint_id.date_begin))

class Habit(models.Model):
    text = models.TextField()
    count_complete = models.IntegerField()
    sprint_id = models.ForeignKey('Sprint', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return self.text

class Week(models.Model):
    week_number = models.IntegerField()
    date_begin = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    goal1 = models.TextField(blank=True, null=True)
    goal2 = models.TextField(blank=True, null=True)
    goal3 = models.TextField(blank=True, null=True)
    reflexy1 = models.TextField(blank=True, null=True)
    reflexy2 = models.TextField(blank=True, null=True)
    reflexy3 = models.TextField(blank=True, null=True)
    sprint_id = models.ForeignKey('Sprint', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.date_begin)

class Day(models.Model):
    day_number = models.IntegerField()
    day_date = models.DateField()
    reflexy1 = models.TextField(blank=True, null=True)
    reflexy2 = models.TextField(blank=True, null=True)
    week_id = models.ForeignKey('Week', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.day_date)

class Day_habit(models.Model):
    is_complete = models.IntegerField()
    day_id = models.ForeignKey('Day', on_delete=models.CASCADE)
    habit_id = models.ForeignKey('Habit', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.habit_id) + " ; " + str(self.day_id)

class Task(models.Model):
    text = models.TextField()
    is_complete = models.IntegerField()
    is_main = models.IntegerField()
    day_id = models.ForeignKey('Day', on_delete=models.CASCADE)

    def publish(self):
        self.save()

    def __str__(self):
        return self.text + " ; " + str(self.day_id)