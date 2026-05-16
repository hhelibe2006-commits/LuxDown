import locale

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication


def on_locale(app : QApplication):
    translator = QTranslator()
    olocale = {
        'zh_CN': 'zh_CN.qm',
        'en_US': 'en.qm',
        'en_GB': 'en.qm',
        'de_DE': 'de.qm',
        'fr_FR': 'fr.qm',
        'es_ES': 'es.qm'
    }

    default = locale.getdefaultlocale()
    lang_code = default[0] if default and default[0] else None

    if lang_code and olocale.get(lang_code):
        if translator.load(olocale[lang_code]):
            app.installTranslator(translator)
            return

    #当找不到语言时用英语
    if translator.load('en.qm'):
        app.installTranslator(translator)
