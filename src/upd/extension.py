from PySide6.QtGui import QPixmap
from .exceptions import ToolNotComplete

class Tool:
    def __init__(self, *args, **kwargs):
        import importlib
        import pkgutil
        mod = '.'.join(self.__module__.split('.')[:-1])
        path = importlib.import_module(mod).__path__
        # for importer, modname, ispkg in pkgutil.iter_modules(path):
        #     importlib.import_module(f'{mod}.{modname}')

        self.init_tasks = []
        self.models = []
        self.main_panel_class = None

    def renderer(self, renderer_class):
        from .renderers import renderers
        renderers[renderer_class().name] = renderer_class()


    def init_task(self, task_function):
        self.init_tasks.append(task_function)

    def model(self, model_class):
        self.models.append(model_class)
        return model_class

    def get_icon(self):
        try:
            return QPixmap(f'plugins/{self.get_id()}/assets/icon.png')
        except:
            raise ToolNotComplete(self.__get_any_names__(), 'get_icon')

    def get_name(self):
        return 'unnamed-tool'

    def get_id(self):
        raise ToolNotComplete(self.__get_any_names__(), 'get_id')

    def __get_any_names__(self):
        return self.get_name() or self.get_id() or self.__class__.__name__

    def main_panel(self, main_panel_class: type):
        self.main_panel_class = main_panel_class
        return main_panel_class

    def get_main_panel(self):
        return self.main_panel_class()

    def settings(self, **kwargs):
        from .conf import settings
        settings.add_category(self.get_id(), **kwargs)
