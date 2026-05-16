import locale

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication


def load_translations(app : QApplication) -> None:
    translator = QTranslator(app)
    locale_map: dict = {
        'zh_CN': 'zh_CN.qm',
        'en_US': 'en.qm',
        'en_GB': 'en.qm',
        'de_DE': 'de.qm',
        'fr_FR': 'fr.qm',
        'es_ES': 'es.qm'
    }

    default = locale.getdefaultlocale()
    lang_code = default[0] if default and default[0] else None

    if lang_code and locale_map.get(lang_code):
        if translator.load(locale_map[lang_code]):
            app.installTranslator(translator)
            return

    #当找不到语言时用英语
    if translator.load('en.qm'):
        app.installTranslator(translator)
