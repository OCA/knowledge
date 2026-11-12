This guide explains how to use the Document Page Project Task module to link wiki pages to project tasks.

## Create a Wiki Page from a Task

**Method 1: From the Task**

1. Go to the **Projects** module
2. Open the desired project and select a task
3. In the task view, locate the **Wiki Pages** button (book icon)
4. Click the button to see linked pages or create a new one
5. Click **Create** to add a new wiki page
6. The task and project will be automatically filled

**Method 2: From the Wiki Page**

1. Go to the **Knowledge** or **Documents** module
2. Create a new wiki page or edit an existing one
3. In the page form, you will see the fields:
   * **Project**: Select the project
   * **Tasks**: Select one or more tasks (when a project is selected, only tasks from that project are shown)
4. Save the page

## Automatic Behaviors

**Automatic Project Filling**

When you add tasks and no project is yet selected:
* If all linked tasks belong to the same project, the **Project** field is automatically filled

**Task Filtering**

When a project is selected:
* Only tasks from that project appear in the task selection list
* Tasks from other projects are automatically removed from the list

**Consistency Validation**

The system validates that:
* If a project is defined on the wiki page, all linked tasks must belong to that project
* Attempting to link a task from a different project will be prevented

**No Project Restriction**

If no project is selected on the wiki page, tasks from any project can be linked freely — useful for cross-project reference documents.

## Link a Page to Multiple Tasks

A wiki page can be linked to several tasks at the same time:

1. Open or create a wiki page
2. In the **Tasks** field (shown as tags), add all relevant tasks
3. The page will appear in the **Wiki Pages** counter on each of those tasks

## View Wiki Pages of a Task

1. Access a project task
2. At the top of the form, you will see the **Wiki Pages** button with a counter
3. The number indicates how many wiki pages are linked to the task
4. Click the button to see all linked pages

## Usage Examples

**Example 1: Shared Requirements Document**

1. Create a wiki page "Functional Requirements"
2. Link it to tasks "Backend Implementation", "Frontend Implementation", and "QA Testing"
3. All three tasks will reference the same documentation

**Example 2: Technical Specification**

1. Create a task "Develop Module X"
2. From the task, create multiple wiki pages: "Technical Spec", "API Design", "Database Schema"
3. Each page is linked to the task and accessible via the Wiki Pages button

**Example 3: Cross-Task Reference**

1. Create a wiki page without a project
2. Link tasks from different projects that share a common dependency or context
3. The page acts as a cross-project reference document
