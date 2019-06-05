import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-attachment_action',
        'odoo8-addon-attachment_edit',
        'odoo8-addon-attachment_lock',
        'odoo8-addon-attachment_preview',
        'odoo8-addon-attachments_to_filesystem',
        'odoo8-addon-document_choose_directory',
        'odoo8-addon-document_no_unique_filenames',
        'odoo8-addon-document_ocr',
        'odoo8-addon-document_page',
        'odoo8-addon-document_page_approval',
        'odoo8-addon-document_page_partner_id',
        'odoo8-addon-document_page_tags',
        'odoo8-addon-document_reindex',
        'odoo8-addon-document_rtf_index',
        'odoo8-addon-document_sftp',
        'odoo8-addon-document_url',
        'odoo8-addon-document_wopi',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
