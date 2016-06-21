# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import subprocess
from PIL import Image
from StringIO import StringIO
from openerp import api, models

_logger = logging.getLogger(__name__)
_MARKER_PHRASE = '[[waiting for OCR]]'


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def _index(self, data, datas_fname, file_type):
        mimetype, content = super(IrAttachment, self)._index(
            data, datas_fname, file_type)
        if not content or content == 'image':
            has_synchr_param = self.env['ir.config_parameter'].get_param(
                'document_ocr.synchronous', 'False') == 'True'
            has_force_flag = self.env.context.get('document_ocr_force')
            if has_synchr_param or has_force_flag:
                content = self._index_ocr(mimetype, data, datas_fname,
                                          file_type)
            else:
                content = _MARKER_PHRASE

        return mimetype, content

    @api.model
    def _index_ocr(self, mimetype, data, datas_fname, file_type):
        dpi = int(
            self.env['ir.config_parameter'].get_param(
                'document_ocr.dpi', '500'))
        top_type, sub_type = mimetype.split('/', 1)
        if hasattr(self, '_index_ocr_get_data_%s' % sub_type):
            image_data = getattr(self, '_index_ocr_get_data_%s' % sub_type)(
                data, datas_fname, file_type, dpi)
        else:
            image_data = StringIO()
            try:
                Image.open(StringIO(data)).save(image_data, 'tiff',
                                                dpi=(dpi, dpi))
            except IOError:
                _logger.exception('Failed to OCR image')
                return None
        process = subprocess.Popen(
            ['tesseract', 'stdin', 'stdout'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(image_data.getvalue())
        if stderr:
            _logger.error('Error during OCR: %s', stderr)
        return stdout

    @api.model
    def _index_ocr_get_data_pdf(self, data, datas_fname, file_type, dpi):
        process = subprocess.Popen(
            ['convert', '-density', str(dpi), '-', '-append', 'png32:-'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(data)
        if stderr:
            _logger.error('Error converting to PDF: %s', stderr)
        return StringIO(stdout)

    @api.model
    def _ocr_cron(self):
        for this in self.with_context(document_ocr_force=True).search([
            ('index_content', '=', _MARKER_PHRASE),
        ]):
            if not this.datas:
                continue
            file_type, index_content = this._index(
                this.datas.decode('base64'), this.datas_fname, this.file_type)
            this.write({
                'file_type': file_type,
                'index_content': index_content,
            })
