from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from .models import Sprint, Goal, Habit, Week, Day, Day_habit, Task

# 
# 
# View for sprint
# and defs for sprint beyond
# 

def new_sprint(request):
    isCreate = request.POST.get("isCreate", "")

    if (isCreate == ""):
        sprints = Sprint.objects.order_by('date_begin')
        if len(sprints) != 0:
            return sprint_list(request)

    return render(request, 'kosmos/new_sprint.html')

def create_sprint(request):
    sprDateBeg = request.POST.get("sprDateBeg", "")
    sprRew = request.POST.get("sprRew", "")

    if sprDateBeg == "":
        return render(request, 'kosmos/new_sprint.html', {'err_message': '(Вы не ввели дату для спринта)'})
    
    # Yes, yes... I know. Bad solution) But Ok :D
    # It's a study project)

    goals = []
    codes = [100,110,111,112,113,120,121,122,123,130,131,132,133,200,210,211,212,213,220,221,222,223,230,231,232,233,300,310,311,312,313,320,321,322,323,330,331,332,333]

    # Oh my God... :D
    goal100 = request.POST.get("goal100", "")
    goals.append(goal100)
    goals.append(request.POST.get("goal110", ""))
    goals.append(request.POST.get("goal111", ""))
    goals.append(request.POST.get("goal112", ""))
    goals.append(request.POST.get("goal113", ""))
    goals.append(request.POST.get("goal120", ""))
    goals.append(request.POST.get("goal121", ""))
    goals.append(request.POST.get("goal122", ""))
    goals.append(request.POST.get("goal123", ""))
    goals.append(request.POST.get("goal130", ""))
    goals.append(request.POST.get("goal131", ""))
    goals.append(request.POST.get("goal132", ""))
    goals.append(request.POST.get("goal133", ""))
    
    goal200 = request.POST.get("goal200", "")
    goals.append(goal200)
    goals.append(request.POST.get("goal210", ""))
    goals.append(request.POST.get("goal211", ""))
    goals.append(request.POST.get("goal212", ""))
    goals.append(request.POST.get("goal213", ""))
    goals.append(request.POST.get("goal220", ""))
    goals.append(request.POST.get("goal221", ""))
    goals.append(request.POST.get("goal222", ""))
    goals.append(request.POST.get("goal223", ""))
    goals.append(request.POST.get("goal230", ""))
    goals.append(request.POST.get("goal231", ""))
    goals.append(request.POST.get("goal232", ""))
    goals.append(request.POST.get("goal233", ""))

    goal300 = request.POST.get("goal300", "")
    goals.append(goal300)
    goals.append(request.POST.get("goal310", ""))
    goals.append(request.POST.get("goal311", ""))
    goals.append(request.POST.get("goal312", ""))
    goals.append(request.POST.get("goal313", ""))
    goals.append(request.POST.get("goal320", ""))
    goals.append(request.POST.get("goal321", ""))
    goals.append(request.POST.get("goal322", ""))
    goals.append(request.POST.get("goal323", ""))
    goals.append(request.POST.get("goal330", ""))
    goals.append(request.POST.get("goal331", ""))
    goals.append(request.POST.get("goal332", ""))
    goals.append(request.POST.get("goal333", ""))
    
    if goal100 == "" or goal200 == "" or goal300 == "":
        return render(request, 'kosmos/new_sprint.html', {'err_message': '(Введите главные цели)'})

    habits = []
    habits.append(request.POST.get("hab1", ""))
    habits.append(request.POST.get("hab2", ""))
    habits.append(request.POST.get("hab3", ""))
    habits.append(request.POST.get("hab4", ""))
    habits.append(request.POST.get("hab5", ""))

    hab1 = request.POST.get("hab1", "")

    if hab1 == "":
        return render(request, 'kosmos/new_sprint.html', {'err_message': '(Введите хотя бы одну привычку)'})

    try:
        # date_end be sprDateBeg, but after we will update it!
        Sprint.objects.create(date_begin=sprDateBeg, date_end=sprDateBeg, reward=sprRew)
    except:
        return render(request, 'kosmos/new_sprint.html', {'err_message': '(Не удалось создать спринт)'})

    sprint = Sprint.objects.filter(date_begin=sprDateBeg)

    # Goals
    for i in range(39):
        if goals[i] != "":
            Goal.objects.create(text=goals[i], is_complete=0, code_heirarchy=codes[i], sprint_id=sprint[0])
    
    for i in range(5):
        if habits[i] != "":
            Habit.objects.create(text=habits[i], count_complete=0, sprint_id=sprint[0])

    # Create Sprint Data (Yes, it was in another method, but now it here!)
    # 
    # sprint_data
    sprintId = sprint[0].pk
    weeks = Week.objects.filter(sprint_id=sprintId).order_by('date_begin')
    
    sprints = Sprint.objects.order_by('date_begin')

    selected = sprint[0]

    lastDate = selected.date_begin

    # 9 weeks (like in "kosmos" methodology :D)
    for i in range(1, 10):
        nextDate = lastDate + timedelta(days=6)
        Week.objects.create(week_number=i, date_begin=lastDate, date_end=nextDate, sprint_id=selected, goal1="", goal2="", goal3="", reflexy1="", reflexy2="", reflexy3="")
        lastDate = nextDate + timedelta(days=1)

        # Update date_end in Sprint
        if i == 9:
            Sprint.objects.filter(pk=selected.pk).update(date_end=nextDate)

    weeks = Week.objects.filter(sprint_id=sprintId).order_by('date_begin')

    lastDate = selected.date_begin
    habits = Habit.objects.filter(sprint_id=selected.pk)

    for w in weeks:
        for i in range(1, 8):
            Day.objects.create(day_number=i, day_date=lastDate, week_id=w, reflexy1="", reflexy2="")
            lastDate = lastDate + timedelta(days=1)
        
        days = Day.objects.filter(week_id=w)

        for d in days:
            for h in habits:
                Day_habit.objects.create(is_complete=0, day_id=d, habit_id=h)
    
    goals = sprint_get_goals(selected.pk)

    if len(habits) == 0:
        habits = []

    # Renew object
    selected = Sprint.objects.filter(pk=selected.pk).get()

    return render(request, 'kosmos/sprint_list.html', {'sprints': sprints, 'selected': selected, 'sprintId': sprintId, 'goals': goals, 'habits': habits})

def sprint_list(request):
    sprintId = request.POST.get("sprintId", "")
    weekId = request.POST.get("weekId", "")

    if (sprintId != ""):
        return sprint_get_selected(request, sprintId, weekId)

    sprints = Sprint.objects.order_by('date_begin')

    if len(sprints) == 0:
        return render(request, 'kosmos/new_sprint.html')

    # Here selected is like Sprint object
    selected = sprints[0]
    goals = sprint_get_goals(selected.pk)
    habits = Habit.objects.filter(sprint_id=selected.pk)

    if len(habits) == 0:
        habits = []

    return render(request, 'kosmos/sprint_list.html', {'sprints': sprints, 'selected': selected, 'sprintId': sprintId, 'goals': goals, 'habits': habits})

def sprint_get_selected(request, sprintId, weekId):
    sprints = Sprint.objects.order_by('date_begin')
    
    # Should write .get() or selected will be not an object, but QuerySet
    selected = Sprint.objects.filter(pk=sprintId).get()
    goals = sprint_get_goals(sprintId)
    habits = Habit.objects.filter(sprint_id=sprintId)

    if len(habits) == 0:
        habits = []

    return render(request, 'kosmos/sprint_list.html', {'sprints': sprints, 'selected': selected, 'sprintId': sprintId, 'goals': goals, 'habits': habits})

def sprint_get_goals(pk):
    temp = Goal.objects.filter(sprint_id=pk).order_by('code_heirarchy')

    goals = []

    # Levels
    a = {
        'data': [],
        'childs': []
    }
    b = {
        'data': [],
        'childs': []
    }

    if len(temp) != 0:
        for t in temp:
            # a level
            if t.code_heirarchy % 100 == 0:
                if len(b['data']) != 0:
                    a['childs'].append(b)
                
                if len(a['data']) != 0:
                    goals.append(a)

                a = {
                    'data': [],
                    'childs': []
                }
                b = {
                    'data': [],
                    'childs': []
                }

                a['data'].append(t)
            
            # b level
            if t.code_heirarchy % 100 != 0 and t.code_heirarchy % 10 == 0:
                if len(b['data']) != 0:
                    a['childs'].append(b)
                
                b = {
                    'data': [],
                    'childs': []
                }

                b['data'].append(t)

            # c level
            if t.code_heirarchy % 10 != 0:
                b['childs'].append(t)

        # last iterations
        if len(b['data']) != 0:
            a['childs'].append(b)

        if len(a['data']) != 0:
            goals.append(a)

    return goals

def sprint_update(request):
    sprintId = request.POST.get("sprintId", "")
    weekId = request.POST.get("weekId", "")

    goals = Goal.objects.filter(sprint_id=sprintId)

    for g in goals:
        val = ''
        pk = g.pk

        s = 'g' + str(pk)

        temp = request.POST.get(s, "")
        if temp == "":
            val = 0
        else:
            val = 1

        Goal.objects.filter(pk=pk).update(is_complete=val)
    
    return sprint_get_selected(request, sprintId, weekId)

# 
# 
# View for week
# and defs for week beyond
# 

def week_list(request):
    # If we comes from Sprint page
    sprintId = request.POST.get("selected", "")
    
    weekId = request.POST.get("weekId", "")

    # If page was reloaded (select week)
    if sprintId == "":
        sprintId = request.POST.get("sprintId", "")

    weeks = Week.objects.filter(sprint_id=sprintId).order_by('date_begin')

    # TODO: Mock :)
    if len(weeks) == 0:
        return render(request, 'kosmos/oops.html', {'text': 'Нет недель'})

    selected = weeks[0]

    # Get selected week
    if weekId != "":
        selected = Week.objects.filter(pk=weekId).get()
    
    goals = Goal.objects.filter(
        Q(code_heirarchy=100) | Q(code_heirarchy=200) | Q(code_heirarchy=300),
        sprint_id=sprintId
    ).order_by('code_heirarchy')

    return render(request, 'kosmos/week_list.html', {'weeks': weeks, 'sprintId': sprintId, 'selected': selected, 'goals': goals})

def week_update(request):
    weekId = request.POST.get("weekId", "")
    sprintId = request.POST.get("sprintId", "")

    g1 = request.POST.get("g1", "")
    g2 = request.POST.get("g2", "")
    g3 = request.POST.get("g3", "")
    ref1 = request.POST.get("ref1", "")
    ref2 = request.POST.get("ref2", "")
    ref3 = request.POST.get("ref3", "")

    Week.objects.filter(pk=weekId).update(goal1=g1,goal2=g2,goal3=g3,reflexy1=ref1,reflexy2=ref2,reflexy3=ref3)
    
    weeks = Week.objects.filter(sprint_id=sprintId).order_by('date_begin')
    selected = weeks[0]

    if weekId != "":
        selected = Week.objects.filter(pk=weekId).get()

    goals = Goal.objects.filter(
        Q(code_heirarchy=100) | Q(code_heirarchy=200) | Q(code_heirarchy=300),
        sprint_id=sprintId
    ).order_by('code_heirarchy')

    return render(request, 'kosmos/week_list.html', {'weeks': weeks, 'sprintId': sprintId, 'selected': selected, 'goals': goals})

# 
# 
# View for day
# and defs for day beyond
# 

def day_list(request):
    weekId = request.POST.get('weekId', "")
    sprintId = request.POST.get('sprintId', "")
    selectedId = request.POST.get('selectedId', "")
    selected = ""

    days = Day.objects.filter(week_id=weekId).order_by('day_date')

    # TODO: Mock :)
    if len(days) == 0:
        return render(request, 'kosmos/oops.html', {'text': 'Нет дней'})

    if selectedId != "":
        if len(days) != 0:
            selected = Day.objects.filter(pk=selectedId).get()
    else:
        if len(days) != 0:
            selected = days[0]

    habits = Habit.objects.filter(sprint_id=sprintId)
    dayHabit = Day_habit.objects.filter(day_id=selected.pk)
    mainTasks = Task.objects.filter(day_id=selected.pk,is_main=1)
    otherTasks = Task.objects.filter(day_id=selected.pk,is_main=0)

    return render(request, 'kosmos/day_list.html', {'sprintId': sprintId, 'weekId': weekId, 'days': days, 'selectedId': selectedId, 'selected': selected, 'habits': habits, 'dayHabit': dayHabit, 'mainTasks': mainTasks, 'otherTasks': otherTasks})

def day_add_task(request):
    selectedId = request.POST.get("selectedId", "")
    inputField = request.POST.get("inputField", "")
    isMain = request.POST.get("isMain", "")
    weekId = request.POST.get("weekId", "")
    sprintId = request.POST.get("sprintId", "")
    selected = ""

    days = Day.objects.filter(week_id=weekId).order_by('day_date')

    if selectedId != "":
        if len(days) != 0:
            selected = Day.objects.filter(pk=selectedId).get()
    else:
        if len(days) != 0:
            selected = days[0]

    Task.objects.create(text=inputField, day_id=selected, is_complete=0, is_main=isMain)

    habits = Habit.objects.filter(sprint_id=sprintId)
    dayHabit = Day_habit.objects.filter(day_id=selected.pk)
    mainTasks = Task.objects.filter(day_id=selected.pk,is_main=1)
    otherTasks = Task.objects.filter(day_id=selected.pk,is_main=0)

    return render(request, 'kosmos/day_list.html', {'sprintId': sprintId, 'weekId': weekId, 'days': days, 'selectedId': selectedId, 'selected': selected, 'habits': habits, 'dayHabit': dayHabit, 'mainTasks': mainTasks, 'otherTasks': otherTasks})

def day_update(request):
    ref1 = request.POST.get("ref1", "")
    ref2 = request.POST.get("ref2", "")

    weekId = request.POST.get("weekId", "")
    sprintId = request.POST.get("sprintId", "")
    selectedId = request.POST.get("selectedId", "")
    selected = ""

    # Initialize block
    days = Day.objects.filter(week_id=weekId).order_by('day_date')

    if selectedId != "":
        if len(days) != 0:
            selected = Day.objects.filter(pk=selectedId).get()
    else:
        if len(days) != 0:
            selected = days[0]

    # Day
    Day.objects.filter(pk=selected.pk).update(reflexy1=ref1, reflexy2=ref2)

    # MainTasks
    mainTasks = Task.objects.filter(day_id=selected.pk,is_main=1)

    for m in mainTasks:
        s = "m" + str(m.pk)
        val = ""

        # It's a checbox bug: when it's unchecked - returns nothing
        temp = request.POST.get(s, "")
        if temp == "on":
            val = 1
        else:
            val = 0

        Task.objects.filter(pk=m.pk).update(is_complete=val)

    # OtherTasks
    otherTasks = Task.objects.filter(day_id=selected.pk,is_main=0)

    for o in otherTasks:
        s = "o" + str(o.pk)
        val = ""

        temp = request.POST.get(s, "")
        if temp == "":
            val = 0
        else:
            val = 1

        Task.objects.filter(pk=o.pk).update(is_complete=val)

    # DayHabit
    dayHabit = Day_habit.objects.filter(day_id=selected.pk)

    for dh in dayHabit:
        s = "dh" + str(dh.pk)
        val = ""

        temp = request.POST.get(s, "")
        if temp == "":
            val = 0
        else:
            val = 1
        
        Day_habit.objects.filter(pk=dh.pk).update(is_complete=val)

    # Update sum habits
    summa = Day_habit.objects.values("habit_id").annotate(summa=Sum("is_complete"))
    
    for s in summa:
        Habit.objects.filter(pk=s['habit_id']).update(count_complete=s['summa'])

    # Return new data
    days = Day.objects.filter(week_id=weekId).order_by('day_date')

    if selectedId != "":
        if len(days) != 0:
            selected = Day.objects.filter(pk=selectedId).get()
    else:
        if len(days) != 0:
            selected = days[0]

    habits = Habit.objects.filter(sprint_id=sprintId)
    dayHabit = Day_habit.objects.filter(day_id=selected.pk)
    mainTasks = Task.objects.filter(day_id=selected.pk,is_main=1)
    otherTasks = Task.objects.filter(day_id=selected.pk,is_main=0)

    return render(request, 'kosmos/day_list.html', {'sprintId': sprintId, 'weekId': weekId, 'days': days, 'selectedId': selectedId, 'selected': selected, 'habits': habits, 'dayHabit': dayHabit, 'mainTasks': mainTasks, 'otherTasks': otherTasks})