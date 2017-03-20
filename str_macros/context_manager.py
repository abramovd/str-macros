from .mixins import MacrosMixin


class enabled_macros(object):
    """
    Inside of this context manager macros are
    enabled

    """

    def __init__(self, model):
        self.model = model
        if not issubclass(self.model, MacrosMixin):
            raise AttributeError('Model is not subclass of MacrosModelMixin')

    def __enter__(self):
        if issubclass(self.model, MacrosMixin):
            self.model.start_macros()
        return self.model

    def __exit__(self, *args):
        self.model.stop_macros()