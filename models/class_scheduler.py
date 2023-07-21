from odoo import models, fields, api, _
from datetime import datetime, date
import calendar


class ClassScheduler(models.Model):
    _name = 'class.scheduler'
    _description = 'Class Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course_id'

    course_id = fields.Many2one('courses.details', string='Course', required=True)
    month_of_record = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'),
        ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        string='Month of Record', required=True)
    record_ids = fields.One2many('class.records.scheduler', 'record_id', string='Class Records')
    academic_head = fields.Many2one('hr.employee', string='Academic Head',
                                    related='class_teacher.employee_id.parent_id')
    class_teacher = fields.Many2one('res.users', string='Class Teacher', default=lambda self: self.env.user.id)
    re_scheduler_ids = fields.One2many('class.rescheduler', 're_schedule_id', string='Re Scheduler')
    reason_ids = fields.One2many('off.day.reasons', 'reason_id', string='Reason')
    state = fields.Selection([
        ('draft', 'Draft'), ('scheduled', 'Scheduled')
    ], string='Status', default='draft')

    def schedule(self):
        self.state = 'scheduled'
        abc = []
        ww = self.env['faculty.details'].search([])
        for jj in ww:
            for i in self.record_ids:
                print(i.day,'iday')
                abc.clear()
                if i.faculty_id.id == jj.name.id:
                    res_list = {
                        'date': i.date,
                        'day_class': i.day,
                        'faculty_id': i.faculty_id.id,
                        'time_from': i.time_from,
                        'time_to': i.time_to,
                        'subject_id': i.subject_id.id,
                    }
                    abc.append((0, 0, res_list))
                    jj.scheduled_ids = abc


class ClassRecordsScheduler(models.Model):
    _name = 'class.records.scheduler'
    _description = 'Class Records Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day')
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)])
    subject_id = fields.Many2one('subject.details', string='Subject')
    exam = fields.Char(string='Exam')
    record_id = fields.Many2one('class.scheduler', string='Class Records')
    get_day_from_date = fields.Char()

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


class ClassReScheduler(models.Model):
    _name = 'class.rescheduler'
    _description = 'Class Re Scheduler'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day', readonly=True)
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)])
    subject_id = fields.Many2one('subject.details', string='Subject')
    exam = fields.Char(string='Exam')

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
