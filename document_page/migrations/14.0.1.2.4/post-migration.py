from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    document_page_history = env["document.page.history"]
    for record in document_page_history.search([]):
        # Apply default HTML sanitize by reassigning the content
        record.content = record.content
