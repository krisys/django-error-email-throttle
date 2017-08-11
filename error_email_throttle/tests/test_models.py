from django.test import TestCase, RequestFactory

from error_email_throttle.models import ErrorReport

request_factory = RequestFactory()


class MockReporter(object):
    def get_traceback_data(self):
        return {
            'lastframe': {
                'filename': 'foo.py',
                'lineno': 42,
                'context_line': 'bar',
                'function': 'foobar',
            }
        }

    def get_traceback_text(self):
        return 'foobar'


class MockRecord(object):
    request = request_factory.get('/')


class TestErrorReportManager(TestCase):
    def test_add_error_log(self):
        reporter = MockReporter()
        record = MockRecord()
        ErrorReport.objects.add_error_log(reporter, record)
