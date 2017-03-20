import functools

from .context_manager import enabled_macros


def enable_macros(model):
    """
    Decorator for enabling macros inside of some function

    :param model: Model
    :type model: django.db.models.Model
    :return: function in which body macros for specified model will enabled
    :rtype: func
    """
    def _enable_macros(func):
        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            with enabled_macros(model):
                return func(*args, **kwargs)
        return _wrap
    return _enable_macros
