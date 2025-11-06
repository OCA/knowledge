This guide explains how to use the Document Page Project Task module to link wiki pages to project tasks.

## Create a Wiki Page from a Task

**Method 1: From the Task**

1. Go to the **Projects** module
2. Open the desired project
3. Select a task
4. In the task view, locate the **Wiki Pages** button (book icon)
5. Click the button to see linked pages or create a new one
6. Click **Create** to add a new wiki page
7. The task and project will be automatically filled

**Method 2: From the Wiki Page**

1. Go to the **Knowledge** or **Documents** module
2. Create a new wiki page or edit an existing one
3. In the page form, you will see the fields:
   * **Project**: Select the project
   * **Task**: Select the task (only tasks from the selected project will be displayed)
4. When you select a task, the project will be automatically filled
5. Save the page

## Automatic Behaviors

**Automatic Project Filling**

When you select a task:
* The **Project** field is automatically filled with the task's project
* This ensures consistency between task and project

**Task Filtering**

When a project is selected:
* Only tasks from that project appear in the selection list
* This prevents selecting tasks from different projects

**Consistency Validation**

The system automatically validates that:
* If a task is linked, the project must also be defined
* The wiki page's project must be the same as the linked task's project
* If you try to link a task to a different project, the system will prevent the operation

**Automatic Cleanup**

When you change the project:
* If the linked task does not belong to the new project, it is automatically removed
* This maintains data consistency

## View Wiki Pages of a Task

1. Access a project task
2. At the top of the form, you will see the **Wiki Pages** button with a counter
3. The displayed number indicates how many wiki pages are linked to the task
4. Click the button to see all linked pages

## Usage Examples

**Example 1: Requirements Documentation**

1. Create a task "Define System Requirements"
2. From the task, create a wiki page "Functional Requirements"
3. Document the requirements in the wiki page
4. The page will be linked to the task and project

**Example 2: Meeting Notes**

1. Create a task "Planning Meeting"
2. Create a wiki page "Meeting Minutes"
3. Document the discussed points
4. The documentation will be organized and easy to find

**Example 3: Technical Specifications**

1. Create a task "Develop Module X"
2. Create a wiki page "Technical Specification"
3. Document the architecture and technical decisions
4. Keep the documentation close to the task work

## Tips

* Use wiki pages to maintain contextual documentation related to specific tasks
* The page counter on the task helps quickly identify tasks with documentation
* When creating a page from the task, fields are automatically filled, saving time
* Organize project documentation hierarchically: Project → Task → Wiki
