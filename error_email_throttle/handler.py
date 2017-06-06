import logging
from django.apps import apps
from django.views.debug import ExceptionReporter
from django.utils.log import AdminEmailHandler


class AdminEmailThrottler(AdminEmailHandler):
    def __init__(self, include_html=False, email_backend=None):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend

    def emit(self, record):
        request = record.request
        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        if self._can_send_email(reporter, record):
            super(AdminEmailThrottler, self).emit(record)

    def _can_send_email(self, reporter, record):
        ErrorReport = apps.get_model('error_email_throttle', 'ErrorReport')
        return ErrorReport.objects.add_error_log(reporter, record)
