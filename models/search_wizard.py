import json
import io
import xlsxwriter
from odoo import fields, models, api, _
from odoo.tools import date_utils


class SearchWizard(models.TransientModel):
    _name = 'search.class.timetable'
    _description = 'Search Wizard'

    faculty_id = fields.Many2one('res.users', domain=[('faculty_check', '=', True)], string='Faculty', required=True)
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    time_table = fields.Binary('Excel File')

    def action_search_inbetween_datas(self, data=None):
        aa = self.env['class.records.scheduler'].sudo().search([])
        report = []
        if self.faculty_id and self.from_date and self.to_date:
            for rec in aa:
                if self.faculty_id.id == rec.faculty_id.id:
                    if rec.state == 'scheduled':
                        if self.from_date <= rec.date <= self.to_date:

                            record = {
                                'date': rec.date,
                                'day': rec.day,
                                'from_date': rec.time_from,
                                'to_date': rec.time_to,
                                'subject': rec.subject_id.name,
                                # 'de_to': self.to_date,
                                'aa': aa,
                                'batch': rec.batch_id.name,
                                'branch': rec.branch_id.branch_name,
                                'topic': rec.topic,
                                # 'user': self.faculty_id.id,

                            }
                            report.append(record)

            data = {
                # 'date_from': self.date_from,
                'report': report,
                'aa': data,
                # 'report_tab': reporting,
                'faculty': self.faculty_id.name,
                'from_date': self.from_date,
                'to_date': self.to_date

            }

            print(aa, 'aa')
            return self.env.ref(
                'scheduler.inbetween_dates_time_table_for_faculty').report_action(None, data=data)
