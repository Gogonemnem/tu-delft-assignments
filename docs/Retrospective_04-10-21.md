# Retrospective 04-10-21

Created: October 4, 2021 9:55 AM
Last Edited Time: October 5, 2021 5:43 PM
Minutes Secretary: Anonymous
Next Meeting: October 6, 2021 5:05 PM
Participants: Anonymous, Anonymous, Anonymous, Anonymous, Anonymous
Scrum Master: Anonymous
Type: Retrospective

# Points of Improvement from Last Week

- To improve, we make planning on Mondays for the entire week.
- The part of code that is worked on has to be done by Monday so every Monday all new parts can be merged into the main branch
- From today on we will be using milestones

# **What went well?**

- We used the milestones a bit and our progression can be seen on it
- We had a plan for the whole week and more things were accomplished than before
- A lot of code was produced
    - The add a task widget is almost finished
    - The delete button works in the task list
    - An external database is added
    - There is a template for the agenda
    - There is a beginning of the daily task list

# What could improve?

- Code-wise:
    - There is a beginning of the randomizer. We want the randomizer to look for a suitable time during the day and distribute the tasks over those times. But that proved to be more difficult than expected. It might help to break the code up into smaller parts, instead of a very large task, it's now.
    - A roundabout way is used for deleting and adding new tasks to the database. Panda seems to have a function to do it semi-automatically. So look into that. (read CSV)
    - The task list updates only after closing the application after adding a new task.
    - There still need to be an option to add a new appointment to the visualization of the agenda
- While the milestones feature was used, most of it was only done after the group has done everything (on Monday). Therefore, the TA could not see our progress in real-time with that feature.
- At the moment nothing has been pushed to main, and thus a sub-branch became very large, so it's difficult to review everything with merge requests.
- Code has not been tested and we do not know whether our code is correct.

# How do we proceed?

- Everyone needs to update the status of their issues. Keeping up with milestones and branches in real-time
- We will create more merge requests and more branches. We need to split the issues up into smaller issues and giving them their own issues & branches
- We will merge our finished products into main. However, it is not clear when we should push things to main? Does it need to be completely done, free from foreseeable bugs, and free of comments (such as TODO, etc.)?
- We will finish writing tests (before the next TA meeting)

# Question for TA?

- What are the requirements for pushing to main?
- How much of the testing needs to be automated? (e.g. PyQT5 testing will be hard)
- Should we also upload our notes/sprint planning to docs? Or can we keep them internally?
