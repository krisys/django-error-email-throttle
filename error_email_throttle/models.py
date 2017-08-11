from __future__ import unicode_literals

import json
import hashlib
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


def _get_error_hash(filename, lineno, function, context_line):
    key = filename + str(lineno) + function + context_line
    return hashlib.sha256(key.encode('utf8')).hexdigest()


class ErrorReportManager(models.Manager):
    def add_error_log(self, reporter, record):
        lastframe = reporter.get_traceback_data()['lastframe']
        url = record.request.get_full_path()
        filename = lastframe.get('filename')
        lineno = lastframe.get('lineno')
        context_line = lastframe.get('context_line')
        function = lastframe.get('function')

        error_hash = _get_error_hash(filename, lineno, function, context_line)
        error_report = ErrorReport.objects.filter(
            error_hash=error_hash
        ).first()

        if error_report:
            time_diff = (timezone.now() - error_report.last_emailed)
            send_email = False
            time_diff_allowed = getattr(
                settings, 'ERROR_EMAIL_THROTTLING_TIME', 15) * 60
            if time_diff.total_seconds() > time_diff_allowed:
                send_email = True

            error_report.update_stats(url=url, send_email=send_email)
            return send_email

        urls = json.dumps([url])
        ErrorReport.objects.create(
            error_date=timezone.now().date(),
            latest_error=timezone.now(),
            error_count=1,
            function=function,
            filename=filename,
            lineno=lineno,
            error_hash=error_hash,
            context_line=context_line,
            urls=urls,
            stack_trace=reporter.get_traceback_text(),
            last_emailed=timezone.now()
        )

        return True


class ErrorReport(models.Model):
    stack_trace = models.TextField()
    error_date = models.DateField()
    latest_error = models.DateTimeField(default=timezone.now)
    error_count = models.IntegerField(default=0)
    last_emailed = models.DateTimeField(null=True, blank=True)

    function = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    lineno = models.IntegerField()
    context_line = models.TextField(null=True, blank=True)
    error_hash = models.CharField(max_length=200, unique=True)

    urls = models.TextField()

    objects = ErrorReportManager()

    def __unicode__(self):
        return '%s - Line no: %d (Error count: %d)' % (
            self.filename, self.lineno, self.error_count
        )

    def update_stats(self, url, send_email):
        urls = []
        if self.urls:
            urls = json.loads(self.urls)

        urls.append(url)
        urls = list(set(urls))

        if send_email:
            self.last_emailed = timezone.now()

        self.urls = json.dumps(urls)
        self.error_count += 1
        self.latest_error = timezone.now()
        self.save()

    @property
    def affected_urls(self):
        if self.urls:
            return len(json.loads(self.urls))
        return 0
