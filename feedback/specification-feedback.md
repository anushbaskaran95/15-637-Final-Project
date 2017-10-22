Project Specification Feedback
==================

### The product backlog (9/10)
Your list of functionality is generally good, however, I think several improvements can be made to improve the specification. Each module within the specification should be split further into specific user-facing actions. This will help you organize the different functionality you need to implement and will also expose holes in your specification--for example, you said you will display the percentage of completion of the task. Will the user input this information? The Tasks module, for example, could include different functionality like Add Task, Add Subtask, Edit Task, etc. To make this more clear, you could use a spreadsheet-like format that is easier to read for backlogs, rather than prose. You could also explore online tools for generating and tracking work on a project. You should also have clear assignment of responsibility for each feature, to the student or students on the team who will complete each feature. Each team member should have sole responsibility for some features on the overall project. You should also have a cost estimate for each feature, in hours.  If the cost estimate is more than 5 or 8 hours, you should consider breaking the feature into smaller work units to improve your ability to track progress on it. Finally, you might want to include how you will integrate the APIs (which part of the functionality uses what). This will make it more clear as to who needs to figure out how to interact with your APIs.

In terms of functionality, your project seems slightly too similar to Grumblr. Please be sure to read the feedback we gave to the original project, as your project will not succeed if it is merely an extension of Grumblr. Incorporating interesting data visualizations and with real-time user interactions will elevate the project.

One more note of caution--implementing a way to interact with other users (e.g. a chat feature) is a common way that students try to extend their projects. I would suggest reconsidering if these features will actually enhance your project and exploring other options.

### Data models (9/10)
Your data models are generally good. However, you might want to better organize your the task models. Instead of having a separate model for each category of task, you can combine these by using class inheritance, adding a "Category" field to the model, or other ways. Since they all have similar fields (User, Name, TaskInfo), it would be better to combine these models so that if you can add/modify the fields more easily. Additionally, it is unclear from the models what the difference between a Task and a Subtask is.

### Wireframes or mock-ups (10/10)
Your wireframes are good.

### Additional Information
Please put your models and wireframes in the specification folder in your repository. I almost gave you 0's on these parts because I didn't see them at first.

---
#### Total score (28/30)
---
Graded by: <Sandy Jiang> (sandraj@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team310/blob/master/feedback/specification-feedback.md
