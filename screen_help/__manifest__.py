{
    "name": "Screen Help",
    "summary": "Contextual help on actions, editable in Odoo or shipped as Markdown",
    "version": "19.0.1.0.0",
    "development_status": "Alpha",
    "category": "Knowledge Management",
    "website": "https://github.com/OCA/knowledge",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["bealdav"],
    "license": "AGPL-3",
    "depends": ["base_setup"],
    "external_dependencies": {"python": ["markdown"]},
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/help_section.xml",
        "views/res_config_settings.xml",
        "report/help.xml",
    ],
    "demo": ["data/demo.xml", "data/demo_section.xml"],
    "post_init_hook": "post_init_hook",
    "assets": {
        "web.assets_backend": [
            "screen_help/static/src/**/*",
        ],
    },
}
