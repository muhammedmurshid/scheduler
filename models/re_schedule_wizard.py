from odoo import fields, models, api, _


class ReScheduleWizard(models.TransientModel):
    _name = 're.schedule.wizard'
    _description = 'Re Schedule Reason Wizard'

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day')
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)])
    subject_id = fields.Many2one('subject.details', string='Subject')
    exam = fields.Char(string='Exam')

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

    parent_id = fields.Integer('Parent Id')
    child_id = fields.Integer('Child Id')

    def action_re_scheduler(self):
        print('pp')
        reschedule = []
        for rec in self:
            record = {
                'date': rec.date,
                'day': rec.day,
                'time_from': rec.time_from,
                'time_to': rec.time_to,
                'faculty_id': rec.faculty_id.id,
                'subject_id': rec.subject_id.id,

            }
            reschedule.append((0, 0, record))
            print(rec.id, 'rec id')

        schedule = self.env['class.records.scheduler'].search([('id', '=', self.child_id)])
        schedule.re_scheduled = True
        dd = self.env['class.scheduler'].search([])
        for rec in dd:

            if self.parent_id == rec.id:
                print('yes')
                rec.re_scheduler_ids = reschedule
            else:
                # rec.re_scheduler_ids = reschedule
                print('no')
        # fac = self.env['faculty.details'].search([])
        # for i in fac:
        #     if i.name.id == self.faculty_id.id:
        #
        #         for rec in i.scheduled_ids:
        #             if rec.record_id == self.id:
        #                 rec.unlink()
        #                 print('yes fac')
        #                 i.scheduled_ids = reschedule
        #             else:
        #                 print('no fac')
        #
        # print('oooi')

