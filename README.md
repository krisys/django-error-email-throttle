# django-error-email-throttle
Throttles the error emails that get sent via Django. To ensure that error emails of only one error type is throttled, we generate a hash of file, function, line number and the line contents.

## Quickstart
Add error_email_throttle to installed apps
```
INSTALLED_APPS = [
    ...
    'error_email_throttle',
]
```

Add error_email_throttle.handler.AdminEmailThrottler to Logging config
```
'handlers': {
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'error_email_throttle.handler.AdminEmailThrottler'
    }
}
```

A value of 15 minutes is used as the default, i.e. emails are not triggered for the same error within the next 15 minutes. One can override this setting by adding the following to settings.py

```
ERROR_EMAIL_THROTTLING_TIME = 30
```

For instances where DB instance itself could be down. In such cases, error_email_throttle provides a File based fallback approach. You can enable this by adding the following to settings.py

```
ERROR_EMAIL_THROTTLING_FILE_FALLBACK = True
```


One could find a list of all errors and the number of times it has occured by visiting the following page in admin.

```/admin/error_email_throttle/```

