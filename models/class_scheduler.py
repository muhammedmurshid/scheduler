from odoo import models, fields, api, _
from datetime import datetime, date
import calendar
import base64
from io import BytesIO
from pdf2docx import parse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ClassScheduler(models.Model):
    _name = 'class.scheduler'
    _description = 'Class Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course_id'

    course_id = fields.Many2one('courses.details', string='Course', required=True)
    month_of_record = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'),
        ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month', required=True)
    record_ids = fields.One2many('class.records.scheduler', 'record_id', string='Class Records')
    academic_head = fields.Many2one('hr.employee', string='Academic Head',
                                    related='class_teacher.employee_id.parent_id')
    class_teacher = fields.Many2one('res.users', string='Class Teacher', default=lambda self: self.env.user.id,
                                    readonly=True)
    re_scheduler_ids = fields.One2many('class.rescheduler', 're_schedule_id', string='Re Scheduler')
    reason_ids = fields.One2many('off.day.reasons', 'reason_id', string='Reason')
    state = fields.Selection([
        ('draft', 'Draft'), ('head_approval', 'Head Approval'), ('scheduled', 'Scheduled'), ('rejected', 'Rejected')
    ], string='Status', default='draft')
    class_id = fields.Many2one('logic.base.class', string='Class', required=True, domain=[('state', '=', 'active')])

    def action_head_approval(self):
        for i in self:
            user_id = self.env.user.employee_id.parent_id.user_id.id
            i.activity_schedule('scheduler.mail_class_scheduler_for_heads', user_id=user_id,
                                note=f'{i.class_id.name} This Class schedule finalized. Approve This Class schedule.')
        self.state = 'head_approval'

    def action_reject(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
                'activity_type_id', '=', self.env.ref('scheduler.mail_class_scheduler_for_heads').id)])
        activity_id.action_feedback(feedback=f'Class schedule Rejected.')
        self.state = 'rejected'

    def schedule(self):
        activity_id = self.env['mail.activity'].sudo().search(
            [('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
                'activity_type_id', '=', self.env.ref('scheduler.mail_class_scheduler_for_heads').id)])
        activity_id.action_feedback(feedback=f'Class schedule Approved.')
        self.state = 'scheduled'
        abc = []
        ww = self.env['faculty.details'].sudo().search([])
        for jj in ww:
            for i in self.record_ids:
                print(i.day, 'iday')
                abc.clear()
                if i.faculty_id.id == jj.name.id:
                    res_list = {
                        'date': i.date,
                        'day': i.day,
                        'faculty_id': i.faculty_id.id,
                        'time_from': i.time_from,
                        'time_to': i.time_to,
                        'subject_id': i.subject_id.id,
                        'record_id': i.id
                    }
                    abc.append((0, 0, res_list))
                    jj.scheduled_ids = abc

    time_table = fields.Binary(string="Excel Report")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

    def action_print_report(self):
        print('ooooops')
        template = self.env.ref('scheduler.action_month_record_for_students')
        html_content = template._render_qweb_pdf([self.id])[0]
        outfile = open('/tmp/temp.pdf', 'wb')
        outfile.write(html_content)
        outfile.close()

        open('/tmp/temp.docx', 'w')
        parse('/tmp/temp.pdf', '/tmp/temp.docx')
        self.time_table = base64.b64encode(open('/tmp/temp.pdf', 'rb').read())
        return {
            'name': 'Time Table For Students',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=class.scheduler&id={}&field=time_table&filename_field=filename&download=true'.format(
                self.id
            ),
            'target': 'self',
        }

    def action_pdf_for_faculty(self):
        for i in self.record_ids:
            print(i.faculty_id, 'iddddddddddddddddddd')
        print('ooooops')
        return {
            'name': "Select Faculty",
            'type': "ir.actions.act_window",
            'res_model': "faculty.search.wizard",
            'view_mode': "form",
            'view_type': "form",
            'target': "new",
            'context': {'default_record_id': self.id}
        }

        # template = self.env.ref('scheduler.month_time_table_for_faculty')
        # html_content = template._render_qweb_pdf([self.id])[0]
        # outfile = open('/tmp/temp.pdf', 'wb')
        # outfile.write(html_content)
        # outfile.close()
        #
        # open('/tmp/temp.docx', 'w')
        # parse('/tmp/temp.pdf', '/tmp/temp.docx')
        # self.excel_file = base64.b64encode(open('/tmp/temp.pdf', 'rb').read())
        # return {
        #     'name': 'Time Table For Faculty',
        #     'type': 'ir.actions.act_url',
        #     'url': '/web/content/?model=class.scheduler&id={}&field=excel_file&filename_field=filename&download=true'.format(
        #         self.id
        #     ),
        #     'target': 'self',
        # }


class ClassRecordsScheduler(models.Model):
    _name = 'class.records.scheduler'
    _description = 'Class Records Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day')
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)], required=True)
    subject_id = fields.Many2one('subject.details', string='Subject', required=True)
    exam = fields.Char(string='Exam')
    record_id = fields.Many2one('class.scheduler', string='Class Records')
    get_day_from_date = fields.Char()
    re_scheduled = fields.Boolean(string='Re Scheduled')

    @api.onchange('date')
    def get_day_from_date(self):
        for record in self:
            if record.date:
                day = record.date.weekday()
                if day == 0:
                    record.day = 'Monday'
                elif day == 1:
                    record.day = 'Tuesday'
                elif day == 2:
                    record.day = 'Wednesday'
                elif day == 3:
                    record.day = 'Thursday'
                elif day == 4:
                    record.day = 'Friday'
                elif day == 5:
                    record.day = 'Saturday'
                elif day == 6:
                    record.day = 'Sunday'
                print(day, 'sss')

    def re_scheduler(self):
        print('pp')
        return {
            'name': 'Re Scheduler',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 're.schedule.wizard',
            'target': 'new',
            # 'view_id': self.env.ref
            # ('product_generation.product_generation_wizard_form').id,
            'context': {'default_parent_id': self.record_id.id, 'default_child_id': self.id,
                        'default_date': self.date, },
        }


class ClassReScheduler(models.Model):
    _name = 'class.rescheduler'
    _description = 'Class Re Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day', )
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)])
    subject_id = fields.Many2one('subject.details', string='Subject')
    exam = fields.Char(string='Exam')
    record_id = fields.Integer()

    re_schedule_id = fields.Many2one('class.scheduler', string='Class Records')

    @api.onchange('date')
    def get_day_from_date(self):
        for record in self:
            if record.date:
                day = record.date.weekday()
                if day == 0:
                    record.day = 'Monday'
                elif day == 1:
                    record.day = 'Tuesday'
                elif day == 2:
                    record.day = 'Wednesday'
                elif day == 3:
                    record.day = 'Thursday'
                elif day == 4:
                    record.day = 'Friday'
                elif day == 5:
                    record.day = 'Saturday'
                elif day == 6:
                    record.day = 'Sunday'
                print(day, 'sss')


class OffDayReasons(models.Model):
    _name = 'off.day.reasons'
    _description = 'Holiday'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    reason = fields.Text(string='Reason')
    reason_id = fields.Many2one('class.scheduler', string='Class Records')
