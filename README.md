# django-error-email-throttle
Throttles the error emails that get sent via Django

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

