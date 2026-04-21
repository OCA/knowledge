This module extends the document page (wiki) functionality by allowing you to link them directly to project tasks.

## Main Features

* **Link Wiki Pages to Multiple Tasks**: Allows associating document pages to one or more project tasks via a Many2many relationship
* **Automatic Project Filling**: When all linked tasks share the same project, it is automatically filled on the document
* **Consistency Validation**: If a project is defined on the wiki page, all linked tasks must belong to that project
* **Smart Filtering**: When a project is selected, only tasks from that project are displayed for selection
* **Page Counter**: Displays the number of wiki pages linked to each task directly in the task view

## Benefits

* Organize project documentation hierarchically (Project → Tasks → Wiki)
* A single wiki page can document multiple related tasks (e.g., a spec shared by several tasks)
* A task can reference multiple wiki pages for different aspects of its work
* Keep documentation close to the work context (tasks)
* Quickly access all documentation related to a specific task

## Dependencies

This module requires:
* `document_page_project`: Module that links document pages to projects
* `project`: Odoo's project management module
