# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# © 2017 ThinkOpen Solutions <https://tkobr.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import io
import logging
import subprocess
from StringIO import StringIO

import pyPdf
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
_MARKER_PHRASE = '[[waiting for OCR]]'
OCR_LANGUAGE = [('afr', 'Afrikaans'),
                ('amh', 'Amharic'),
                ('ara', 'Arabic'),
                ('asm', 'Assamese'),
                ('aze', 'Azerbaijani'),
                ('aze_cyrl', 'Azerbaijani - Cyrilic'),
                ('bel', 'Belarusian'),
                ('ben', 'Bengali'),
                ('bod', 'Tibetan'),
                ('bos', 'Bosnian'),
                ('bul', 'Bulgarian'),
                ('cat', 'Catalan; Valencian'),
                ('ceb', 'Cebuano'),
                ('ces', 'Czech'),
                ('chi_sim', 'Chinese - Simplified'),
                ('chi_tra', 'Chinese - Traditional'),
                ('chr', 'Cherokee'),
                ('cym', 'Welsh'),
                ('dan', 'Danish'),
                ('dan_frak', 'Danish - Fraktur'),
                ('deu', 'German'),
                ('deu_frak', 'German - Fraktur'),
                ('dzo', 'Dzongkha'),
                ('ell', 'Greek, Modern (1453-)'),
                ('eng', 'English'),
                ('enm', 'English, Middle (1100-1500)'),
                ('epo', 'Esperanto'),
                ('equ', 'Math / equation detection module'),
                ('est', 'Estonian'),
                ('eus', 'Basque'),
                ('fas', 'Persian'),
                ('fin', 'Finnish'),
                ('fra', 'French'),
                ('frk', 'Frankish'),
                ('frm', 'French, Middle (ca.1400-1600)'),
                ('gle', 'Irish'),
                ('glg', 'Galician'),
                ('grc', 'Greek, Ancient (to 1453)'),
                ('guj', 'Gujarati'),
                ('hat', 'Haitian; Haitian Creole'),
                ('heb', 'Hebrew'),
                ('hin', 'Hindi'),
                ('hrv', 'Croatian'),
                ('hun', 'Hungarian'),
                ('iku', 'Inuktitut'),
                ('ind', 'Indonesian'),
                ('isl', 'Icelandic'),
                ('ita', 'Italian'),
                ('ita_old', 'Italian - Old'),
                ('jav', 'Javanese'),
                ('jpn', 'Japanese'),
                ('kan', 'Kannada'),
                ('kat', 'Georgian'),
                ('kat_old', 'Georgian - Old'),
                ('kaz', 'Kazakh'),
                ('khm', 'Central Khmer'),
                ('kir', 'Kirghiz; Kyrgyz'),
                ('kor', 'Korean'),
                ('kur', 'Kurdish'),
                ('lao', 'Lao'),
                ('lat', 'Latin'),
                ('lav', 'Latvian'),
                ('lit', 'Lithuanian'),
                ('mal', 'Malayalam'),
                ('mar', 'Marathi'),
                ('mkd', 'Macedonian'),
                ('mlt', 'Maltese'),
                ('msa', 'Malay'),
                ('mya', 'Burmese'),
                ('nep', 'Nepali'),
                ('nld', 'Dutch; Flemish'),
                ('nor', 'Norwegian'),
                ('ori', 'Oriya'),
                ('osd', 'Orientation and script detection module'),
                ('pan', 'Panjabi; Punjabi'),
                ('pol', 'Polish'),
                ('por', 'Portuguese'),
                ('pus', 'Pushto; Pashto'),
                ('ron', 'Romanian; Moldavian; Moldovan'),
                ('rus', 'Russian'),
                ('san', 'Sanskrit'),
                ('sin', 'Sinhala; Sinhalese'),
                ('slk', 'Slovak'),
                ('slk_frak', 'Slovak - Fraktur'),
                ('slv', 'Slovenian'),
                ('spa', 'Spanish; Castilian'),
                ('spa_old', 'Spanish; Castilian - Old'),
                ('sqi', 'Albanian'),
                ('srp', 'Serbian'),
                ('srp_latn', 'Serbian - Latin'),
                ('swa', 'Swahili'),
                ('swe', 'Swedish'),
                ('syr', 'Syriac'),
                ('tam', 'Tamil'),
                ('tel', 'Telugu'),
                ('tgk', 'Tajik'),
                ('tgl', 'Tagalog'),
                ('tha', 'Thai'),
                ('tir', 'Tigrinya'),
                ('tur', 'Turkish'),
                ('uig', 'Uighur; Uyghur'),
                ('ukr', 'Ukrainian'),
                ('urd', 'Urdu'),
                ('uzb', 'Uzbek'),
                ('uzb_cyrl', 'Uzbek - Cyrilic'),
                ('vie', 'Vietnamese'),
                ('yid', 'Yiddish'), ]


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    language = fields.Selection(OCR_LANGUAGE, 'Language',
                                default=lambda self:
                                self.env['ir.config_parameter'].get_param(
                                    'document_ocr.language', 'eng'))
    # We need to redefine index_content field to be able to update it
    # on the onchange_language()
    index_content = fields.Text('Indexed Content',
                                readonly=False,
                                prefetch=False)
    index_content_rel = fields.Text(related='index_content',
                                    string='Indexed Content Rel')

    @api.onchange('language')
    def onchange_language(self):
        process = subprocess.Popen(['tesseract', '--list-langs'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if self.language not in stderr.split('\n'):
            raise UserError(_(
                "Language not installed."
                " Please ask your system administrator to"
                " install tesseract '%s' language." %
                self.language))
        if self.store_fname:
            bin_data = self._file_read(self.store_fname)
        else:
            bin_data = self.db_datas
        if bin_data:
            index_content = self._index(
                bin_data.decode('base64'), self.datas_fname, self.mimetype)
            return {'value': {
                'index_content': index_content}}
        return {'value': {}}

    @api.model
    def _index(self, bin_data, datas_fname, mimetype):
        content = super(IrAttachment, self)._index(
            bin_data, datas_fname, mimetype)
        if not content or content == 'image':
            has_synchr_param = self.env['ir.config_parameter'].get_param(
                'document_ocr.synchronous', 'False') == 'True'
            has_force_flag = self.env.context.get('document_ocr_force')
            synchr = has_synchr_param or has_force_flag
            if synchr:
                content = self._index_ocr(bin_data)
            else:
                content = _MARKER_PHRASE
        return content

    def _index_ocr(self, bin_data):
        _logger.info('OCR IMAGE "%s"...', self.datas_fname)
        process = subprocess.Popen(
            ['tesseract', 'stdin', 'stdout', '-l', self.language],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(bin_data)
        if stderr:
            _logger.error('Error during OCR: %s', stderr)
        return stdout

    def _index_pdf(self, bin_data):

        def convert_bin_to_image(self, bin_data):
            dpi = int(self.env['ir.config_parameter'].get_param(
                'document_ocr.dpi', '500'))
            quality = int(self.env['ir.config_parameter'].get_param(
                'document_ocr.quality', '100'))
            process = subprocess.Popen(
                ['convert', '-density', str(dpi),
                 '-quality', str(quality),
                 '-', '-append', 'png32:-'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(bin_data)
            if stderr:
                _logger.error('Error converting PDF to image: %s', stderr)
            return stdout

        def _convert_pdf_page_to_image(self, pdf, pagenum):
            dst_pdf = pyPdf.PdfFileWriter()
            dst_pdf.addPage(pdf.getPage(pagenum))
            pdf_bytes = io.BytesIO()
            dst_pdf.write(pdf_bytes)
            pdf_bytes.seek(0)
            return convert_bin_to_image(self, pdf_bytes.read())

        has_synchr_param = self.env['ir.config_parameter'].get_param(
            'document_ocr.synchronous', 'False') == 'True'
        has_force_flag = self.env.context.get('document_ocr_force')
        synchr = has_synchr_param or has_force_flag
        if synchr:
            buf = super(IrAttachment, self)._index_pdf(bin_data)
            if len(buf.split('\n')) < 2 and bin_data.startswith('%PDF-'):
                # If we got less than 2 lines,
                # run OCR anyway and append to existent text
                try:
                    f = StringIO(bin_data)
                    pdf = pyPdf.PdfFileReader(f)
                    if pdf.getNumPages() > 1:
                        for pagenum in range(0, pdf.getNumPages()):
                            _logger.info('OCR PDF "%s" page %d/%d...',
                                         self.datas_fname,
                                         pagenum + 1,
                                         pdf.getNumPages())
                            pdf_image = _convert_pdf_page_to_image(self, pdf,
                                                                   pagenum)
                            index_content = self._index_ocr(pdf_image)
                            buf = u'%s\n-- %d --\n%s' % (
                                buf, pagenum + 1, index_content.decode('utf8'))
                    else:
                        pdf_image = convert_bin_to_image(self, bin_data)
                        index_content = self._index_ocr(pdf_image)
                        buf = u'%s\n%s' % (buf, index_content.decode('utf8'))
                except Exception as e:
                    _logger.error('Error converting PDF to image: %s', e)
                    pass
        else:
            buf = _MARKER_PHRASE
        return buf

    @api.model
    def _ocr_cron(self):
        for this in self.with_context(document_ocr_force=True).search(
                [('index_content', '=', _MARKER_PHRASE)]):
            if not this.datas:
                continue
            index_content = this._index(
                this.datas.decode('base64'), this.datas_fname, this.mimetype)
            this.write({
                'index_content': index_content,
            })
