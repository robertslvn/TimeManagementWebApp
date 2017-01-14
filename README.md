Project Implementation
==============

Run the server ("production"):
------------------------------  
vagrant up --provision
URL: http://localhost:8000/



Project Features:

Dashboard

The Dashboard takes information from all upcoming tasks and habits displays them on one page. Clicking on them will link to their more detailed page.

Tasks

Users can add tasks and subtasks. Tasks can then be modified on the ‘task manager’ page..  Tasks and subtasks can be modified dynamically by clicking various areas on the task display bars and their icons. Everything about a task is dynamically editable except the task description. Tasks's order and heirarchy can be rearranged by dragging them above or below other tasks.

Matrix Tasks

This page sorts all tasks by urgency/importance

Habit Tracker

Users can add habits (daily or weekly) and set their daily frequency. Habits can be viewed on the main habit tracker page (list of habits). The user can toggle success for the current day from here. A more detailed view of each habit with various options/a calendar of the habit is seen by clicking any habit on the list page. 

Task/Habit Sharing

The friends page shows a list of all the current user’s friends. Clicking a friend will take you to a page showing a read only view of that person’s public tasks/habits. 

Groups

Users can create their own groups and invite their current friends to be in their groups. The Owner can manage privileges and Admins in a group can edit the tasks in the same ways as for the individual tasks. They can also assign tasks to other members of the group. Future: Allow tasks to be reassigned

Known specific issue:
In the task manager, if you have a private main task and manually add a public subtask under it using the detailed add form:
-if any other public main tasks are under this, a friend who tries to view your task page under friends will get a server error.
