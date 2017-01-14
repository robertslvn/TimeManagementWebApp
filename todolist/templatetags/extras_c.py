from django import template
from calendar import HTMLCalendar
import calendar
from django.utils.safestring import mark_safe
from todolist.models import ExtendUser
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date


register = template.Library()
from todolist.models import Habit
from todolist.models import cssnumbers

##generates a calendar full of boxes which include info about whether the habit occurs on that day, and an option to toggle success for that day/habit
@register.simple_tag
def calendarr(year, month, mondaynum, tuesdaynum, wednesdaynum, thursdaynum, fridaynum, saturdaynum, sundaynum, day, endday, endmonth, endyear, startmonth, startyear, habid, friend):
    finalStr = ''
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    ##override the HTMLcalendar methods
    cal = HabitCalendar(cal) 
    myStr = cal.formatmonth(year,month, mondaynum, tuesdaynum, wednesdaynum, thursdaynum, fridaynum, saturdaynum, sundaynum, day, endday, endmonth, endyear, startmonth, startyear, habid, friend)
    finalStr = finalStr + "<p></p>" + myStr
    ##create other calendars in the same way, for every month/year between start date and end date
    while month != endmonth or year != endyear:
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        cal = calendar.HTMLCalendar(calendar.SUNDAY)
        cal = HabitCalendar(cal)
        myStr = cal.formatmonth(year,month, mondaynum, tuesdaynum, wednesdaynum, thursdaynum, fridaynum, saturdaynum, sundaynum, day, endday, endmonth, endyear, startmonth, startyear, habid, friend)
        finalStr = finalStr + "<p></p>" + myStr
    finalStr = mark_safe(finalStr)
    tem = Habit.objects.get(id = HabitCalendar.id)
    tem.passthrough = True ##signify that we've generated the calendar and thus established a link between the habit and its cssnumbers needed to properly fill the calendars with info/colors
    tem.save()
    return finalStr

##override HTMLcalendar
class HabitCalendar(HTMLCalendar):
    
    
    def __init__(self, workouts):
        super(HabitCalendar, self).__init__()

    ##format the day cells of the calendar to include a link to change the css of the cell as well as other information
    def formatday(self, day, weekday):
        inita = Habit.objects.get(id = HabitCalendar.id)
        pas = inita.passthrough
        ##get the current day as a string of integers
        cssclass = str(day) + str(HabitCalendar.mont) + str(HabitCalendar.yea)
        cssclass = str(cssclass)
        ##if we havent yet generated the calendar we need to create links between the habit and its cssnumbers
        if pas == False:
            h1 = Habit.objects.get(id = HabitCalendar.id)
            h1.save()
            c1 = cssnumbers(number=cssclass)
            c1.save()
        ##creates a link reference to a certain day so that we can change the css for that day only
        tempstring = '/' +str(HabitCalendar.id) + "!" + str(HabitCalendar.id) + "?" + cssclass
        if day != 0:
            
            ##check that the current day is before the end date
            if HabitCalendar.endd < day and HabitCalendar.endm == HabitCalendar.mont and HabitCalendar.endy == HabitCalendar.yea:
                HabitCalendar.keepgoing = 0
            ##monday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.mon) > 0 and int(weekday) == 0 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.mon + '</b>')
                ##if this calendar is being generated for a friend's view, dont give the toggle success option
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                ##if we are generating the calendar for the first time, create links between the habit and its cssnumbers
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))
            ##tuesday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.tue) > 0 and int(weekday) == 1 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.tue + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))

            ##wednesday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.wed) > 0 and int(weekday) == 2 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.wed + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))
            
            ##thursday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.thur) > 0 and int(weekday) == 3 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.thur + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))
            
            ##friday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.fri) > 0 and int(weekday) == 4 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.fri + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))
            
            ##saturday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.sat) > 0 and int(weekday) == 5 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.sat + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))

            ##sunday cells of calendar, check if habit occurs on that day and its after the startdate
            if int(HabitCalendar.sun) > 0 and int(weekday) == 6 and (HabitCalendar.startd <= day or HabitCalendar.startm != HabitCalendar.mont) and HabitCalendar.keepgoing == 1:
                body = ['<p>']
                body.append('<b>goal: ' + HabitCalendar.sun + '</b>')
                if HabitCalendar.friend == False:
                    body.append('<p> </p><a href="' + tempstring + '">toggle success</a>')
                if pas == False:
                    c1.habits.add(h1)
                return self.day_cell('c' + cssclass, '%d %s' % (day, ''.join(body)))
            ##if there are no habits set for a day of the week
            else:
                cssclass = self.cssclasses[weekday]
                body = ['<p>']
                body.append('goal: none')
                if HabitCalendar.friend == False:
                    body.append('<p> </p>n/a')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
        
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month, mondaynum, tuesdaynum, wednesdaynum, thursdaynum, fridaynum, saturdaynum, sundaynum, day, endday, endmonth, endyear, startmonth, startyear, habid, friend):
        HabitCalendar.mon = mondaynum
        HabitCalendar.tue = tuesdaynum
        HabitCalendar.wed = wednesdaynum
        HabitCalendar.thur = thursdaynum
        HabitCalendar.fri = fridaynum
        HabitCalendar.sat = saturdaynum
        HabitCalendar.sun = sundaynum
        HabitCalendar.startd = day
        HabitCalendar.endd = endday
        HabitCalendar.endm = endmonth
        HabitCalendar.endy = endyear
        HabitCalendar.mont = month
        HabitCalendar.yea = year
        HabitCalendar.startm = startmonth
        HabitCalendar.starty = startyear
        HabitCalendar.id = habid
        HabitCalendar.friend = friend
        HabitCalendar.keepgoing = 1
        self.year, self.month = year, month
        return super(HabitCalendar, self).formatmonth(year, month)


    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

##check if the url is the page itself or the page and an argument to change css
@register.assignment_tag
def redirecturl(path):
    nteste = False
    fromwhere = 0
    
    for iter in range(len(path)):
        if path[iter] == '?':
            fromwhere = 1

    
    return int(fromwhere)

##update the css for a habit (initiated by a toggle success link or the change friend viewability link)           
@register.simple_tag
def updatecss(path):
    
    ##get the id of the habit being updated
    for iter in range(len(path)):
        if path[iter] == '!':
            iddstart = iter+1
        if path[iter] == '?':
            iddend = iter-1

    idd = path[iddstart:iddend+1]
    
    ##get the habit object thats being updated
    t = Habit.objects.get(id = int(idd))
    
    ##get the cssnumbers/the calendar cell who's css is being changed (or 'fr' if its a friend viewability change)
    nteste = False
    iter = 0
    while nteste == False:
        if path[iter] == '?':
            numb = path[iter+1:]
            nteste = True
        else:
            iter = iter+1
    
    ##run this if we are simply changing the viewability of a habit to the user's friends
    if numb == "fr":
        if t.viewable_by_friends == True:
            t.viewable_by_friends = False
            t.save()
        else:
            t.viewable_by_friends = True
            t.save()
    
    ##run this if we are changing the css value for a success/fail
    else:
        numb = int(numb)
        entry_list2 = list(t.cssnumbers_set.all().values_list('number', flat=True))
        entry_list = list(t.cssnumbers_set.all().filter(number = numb).values_list('number', flat=True))
        ts = list(t.cssnumbers_set.all().filter(number = numb).values_list('id', flat=True))
        idfield = ts[0] 
        entry = cssnumbers.objects.get(id = idfield)
        if entry.isgreen == False:
            entry.isgreen = True
            if entry.isred == True:
                entry.isred = False
                t.fails = int(t.fails) - 1
            entry.save()
            t.successes = int(t.successes)+1
            t.save()
        else:
            entry.isgreen = False
            entry.isred = True
            entry.save()
            t.fails = int(t.fails)+1
            t.successes = int(t.successes)-1
            t.save()
      
    return ''

##create the css for the list habit/view habit pages based on the values stored for a habit's cssnumbers (info about which days are successes/fails)
##places css into the html template which will be within <style></style>
@register.simple_tag
def createcss(idd, listpage):
    x = 0
    cssstring = ''
    t = Habit.objects.get(id = idd)
    entry = list(t.cssnumbers_set.all().filter(isgreen = True).values_list('number', flat=True))
    ##successes (green)
    while x < len(entry):
        if listpage == 1:
            cssstring = cssstring + '.c' + str(idd) + str(entry[x]) + ' {background-color: #608362;}\n'
        else:
            cssstring = cssstring + '.c' + str(entry[x]) + ' {background-color: #608362;}\n'
        x = x+1
    x=0
    entry2 = list(t.cssnumbers_set.all().filter(isred = True).values_list('number', flat=True))
    ##fails (red)
    while x < len(entry2):
        if listpage == 1:
            cssstring = cssstring + '.c' + str(idd) + str(entry2[x]) + ' {background-color: #c62f2f;}\n'
        else:
            cssstring = cssstring + '.c' + str(entry2[x]) + ' {background-color: #c62f2f;}\n'
        x = x+1

    return cssstring

##takes the number of successes/fails and assigns a grade similar to most schools percentage to grade system
@register.simple_tag
def grading(success, fail):
    if (success + fail) !=0:
        if float(success) / (float(success) + float(fail)) >= 0.9:
            return mark_safe('<span class = agrade>A+<span>')
        if float(success) / (float(success) + float(fail)) < 0.9 and float(success) / (float(success) + float(fail)) >= 0.85:
            return mark_safe('<span class = agrade>A<span>')
        if float(success) / (float(success) + float(fail)) < 0.85 and float(success) / (float(success) + float(fail)) >= 0.80:
            return mark_safe('<span class = agrade>A-<span>')
        if float(success) / (float(success) + float(fail)) < 0.80 and float(success) / (float(success) + float(fail)) >= 0.75:
            return mark_safe('<span class = bgrade>B+<span>')
        if float(success) / (float(success) + float(fail)) < 0.75 and float(success) / (float(success) + float(fail)) >= 0.70:
            return mark_safe('<span class = bgrade>B<span>')
        if float(success) / (float(success) + float(fail)) < 0.70 and float(success) / (float(success) + float(fail)) >= 0.65:
            return mark_safe('<span class = bgrade>B-<span>')
        if float(success) / (float(success) + float(fail)) < 0.65 and float(success) / (float(success) + float(fail)) >= 0.60:
            return mark_safe('<span class = cgrade>C+<span>')
        if float(success) / (float(success) + float(fail)) < 0.60 and float(success) / (float(success) + float(fail)) >= 0.55:
            return mark_safe('<span class = cgrade>C<span>')
        if float(success) / (float(success) + float(fail)) < 0.55 and float(success) / (float(success) + float(fail)) >= 0.50:
            return mark_safe('<span class = cgrade>C-<span>')
        else:
            return mark_safe('<span class = fgrade>F<span>')
    else:
        return mark_safe('<span class = nagrade>N/A<span>')

##checks if 2 users are friends
@register.assignment_tag
def friendTest(habituser, curruser):
    curUser = ExtendUser.objects.get(user=User.objects.get(username=curruser))
                        
    if curUser.isFriend(habituser):
        # already friends
        return 'True'
    else:
        return 'False'

##get the current date
@register.simple_tag
def curdate():
    now = datetime.now()
    finalstr = '<p id = dateline>' + str(calendar.day_name[now.weekday()]) + ', ' + str(calendar.month_name[now.month]) + ' ' + str(now.day) + ' ' + str(now.year) + '</p>'
    finalstr = mark_safe(finalstr)
    
    return finalstr

##generates the 'calendar' cells on the list view of all habits, where you can see the current day's goals and toggle success for the current day
@register.simple_tag
def quickviewonlist(mon, tues, wed, thurs, fri, sat, sun, id, sdate, edate):
    
    Happening = False
    now = datetime.now()
    cssclass = str(now.day) + str(now.month) + str(now.year)
    cssclass = str(cssclass)
    finalstr = '<li id = qlist class = c' + str(id) + cssclass + '><p><table class = quickvtable><td>'
    
    ##the link to change the css based on which habit's current day cell is clicked
    tempstring = '/habit_tracker' + "!" + str(id) + '?' + cssclass
    
    ##check monday to sunday
    
    if now.weekday() == 0 and int(mon) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + mon + '</b></p>'
	finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 1 and int(tue) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + tues + '</b></p>'
	finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 2 and int(wed) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + wed + '</b></p>'
	finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 3 and int(thur) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + thurs + '</b></p>'
	finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 4 and int(fri) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + fri + '</b></p>'
	finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 5 and int(sat) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + sat + '</b></p>'
        finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if now.weekday() == 6 and int(sun) >= 1 and sdate <= now.date() <= edate:
        finalstr = finalstr + "<p><b>Today's Goal: " + sun + '</b></p>'
        finalstr = finalstr + '<p> </p><a href="' + tempstring + '">toggle success</a>'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        Happening = True
    if Happening == False:
        finalstr = finalstr + "<p>Today's Goal: 0 </p>"
        finalstr = finalstr + '<p> </p>N/A'
        finalstr = finalstr + '</td></tr></table></p></li>'
        finalstr = mark_safe(finalstr)
        
        
    return finalstr
