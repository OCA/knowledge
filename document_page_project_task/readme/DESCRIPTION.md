This module extends the document page (wiki) functionality by allowing you to link them directly to project tasks.

## Main Features

* **Link Wiki Pages to Tasks**: Allows associating document pages to specific project tasks
* **Automatic Project Filling**: When a task is selected, the related project is automatically filled
* **Consistency Validation**: Ensures that the wiki page's project is always the same as the linked task's project
* **Smart Filtering**: When a project is defined, only tasks from that project are displayed for selection
* **Page Counter**: Displays the number of wiki pages linked to each task directly in the task view

## Benefits

* Organize project documentation hierarchically (Project → Task → Wiki)
* Keep documentation close to the work context (tasks)
* Avoid inconsistencies between projects and tasks through automatic validations
* Quickly access documentation related to a specific task

## Dependencies

This module requires:
* `document_page_project`: Module that links document pages to projects
* `project`: Odoo's project management module
