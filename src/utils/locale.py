from PySide6.QtCore import QTranslator
import locale

from PySide6.QtWidgets import QApplication


def on_locale(app : QApplication):
    translator = QTranslator()
    olocale = {'zh_CN' : 'zh_CN.qm', 'en_US' : 'en.qm', 'en_GB' : 'en.qm', 'de_DE' : 'de.qm', 'fr_FR' : 'fr.qm', 'es_ES' : 'es.qm'}
    lang_code, _ = locale.getdefaultlocale()
    if olocale.get(lang_code):
        if translator.load(olocale[lang_code]):
            app.installTranslator(translator)

    else:
        if translator.load('en.qm'):
            app.installTranslator(translator)
