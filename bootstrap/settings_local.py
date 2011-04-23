OAUTH = ('GwmJraHXvwyhyyHsjriA',
         'pRH2L42N7Jt0Q611tGGqBKGbrNDTbQoJlC8n2bKjOo',
         '17469965-KyfMtssZybCmy0x6upGZ1p41qKpGctQHLyBLh8NUY',
         'YaEQmC94GcXpbYOk85BL57FXDfOLeah2FLAbWyGs')


DATABASES = {
    'default': {
        'ENGINE': 'mysql2',
        'NAME': 'camelot',
        'USER': '',
        'PASSWORD': '',
        'HOST': '10.77.102.225',
        'PORT': '',
    },
    'slave01': {
        'ENGINE': 'mysql2',
        'NAME': 'camelot',
        'USER': '',
        'PASSWORD': '',
        'HOST': '10.118.190.255',
        'PORT': '',
    },
    'slave02': {
        'ENGINE': 'mysql2',
        'NAME': 'camelot',
        'USER': '',
        'PASSWORD': '',
        'HOST': '10.82.221.188',
        'PORT': '',
    },
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,
}

DEBUG = TEMPLATE_DEBUG = False

WOO=1
