import logging
import time
import os

from django.apps import apps
from copy import copy
from django.conf import settings
from django.views.debug import ExceptionReporter
from django.utils.log import AdminEmailHandler
from django.db.utils import OperationalError


class AdminEmailThrottler(AdminEmailHandler):
    def __init__(self, include_html=False, email_backend=None):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend

    def emit(self, record):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (
            self.format(no_exc_record), reporter.get_traceback_text()
        )
        html_message = reporter.get_traceback_html() if self.include_html else None
        if self._can_send_email(reporter, record):
            self.send_mail(
                subject, message, fail_silently=True, html_message=html_message
            )

    def _can_send_email(self, reporter, record):
        ErrorReport = apps.get_model('error_email_throttle', 'ErrorReport')

        # Disallowed host email etc may not have a stack trace to analyse.
        try:
            return ErrorReport.objects.add_error_log(reporter, record)
        except OperationalError:
            if getattr(settings, 'ERROR_EMAIL_THROTTLING_FILE_FALLBACK', False):
                self.timestamp_file = os.path.join(
                    settings.BASE_DIR, 'error_throttle_last_email_sent.txt')
                if not os.path.exists(self.timestamp_file):
                    self.write_last_email_sent_to_file()
                    return True
                else:
                    with open(self.timestamp_file, 'r') as f:
                        contents = f.read().strip()

                    if contents:
                        last_emailed_timestamp = float(contents)
                        time_since = (time.time() - last_emailed_timestamp) / 60
                        if time_since < getattr(settings, 'ERROR_EMAIL_THROTTLING_TIME', 15):
                            return False

                    self.write_last_email_sent_to_file()
                    return True
        except Exception:
            return True

    def write_last_email_sent_to_file(self):
        with open(self.timestamp_file, 'w') as f:
            f.write(str(time.time()))

