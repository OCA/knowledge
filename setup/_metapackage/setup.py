import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-attachment_attach_non_editable',
        'odoo10-addon-document_page',
        'odoo10-addon-document_page_approval',
        'odoo10-addon-document_page_tags',
        'odoo10-addon-knowledge',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
