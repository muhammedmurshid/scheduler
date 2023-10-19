from odoo import api, fields, models, _
import base64
from io import BytesIO
from pdf2docx import parse


class FacultySearchWizard(models.TransientModel):
    _name = 'faculty.search.wizard'
    _description = 'Faculty Search Wizard'

    def action_faculty_search(self):
        active_id = self.env.context.get('active_id')
        print(active_id, 'active_id')
        rec = self.env['class.scheduler'].browse(active_id)
        print(rec, 'rec_id')
        ids = []
        for i in rec.record_ids:

            user = self.env['res.users'].search([])
            for j in user:
                if i.faculty_id:
                    if j.id == i.faculty_id.id:
                        ids.append(j.id)
        print(ids, 'ids')
        domain = [('id', 'in', ids)]
        return domain

    faculty_id = fields.Many2one('res.users', string='Faculty', domain=action_faculty_search, required=True)
    time_table = fields.Binary('Excel File')
    record_id = fields.Many2one('class.scheduler', string='Record', readonly=True)

    def action_download(self):
        template = self.env.ref('scheduler.month_time_table_for_faculty')
        html_content = template._render_qweb_pdf([self.id])[0]
        outfile = open('/tmp/temp.pdf', 'wb')
        outfile.write(html_content)
        outfile.close()

        open('/tmp/temp.docx', 'w')
        parse('/tmp/temp.pdf', '/tmp/temp.docx')
        self.time_table = base64.b64encode(open('/tmp/temp.pdf', 'rb').read())
        return {
            'name': 'Time Table For Faculty',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=faculty.search.wizard&id={}&field=time_table&filename_field=filename&download=true'.format(
                self.id
            ),
            'target': 'self',
        }


