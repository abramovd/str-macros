import re


class MacrosMixin(object):
    """
    Use macros for your model.CharField.
    All macro labels should be inside of [], e.g.,
    [rb-mail-banner_id].

    MACRO_FIELDS - tuple of fields for which macros should
    be checked
    MACRO_MAP - map of a macro pattern and a function that
        should be called when such pattern is found
        Such functions should expected one param - self, which
        is an object of your class for which macros are enabled.
        Patterns in MACRO_MAP should be defines without []
        E.g. MACRO_MAP = {
            'rb_mail-banner_id':
                lambda self: str(self.banner_id)
            }
    """

    MACRO_FIELDS = ()
    MACRO_MAP = {}
    _enabled_macros = False
    _parent_getattribute = object.__getattribute__

    @classmethod
    def start_macros(cls):
        """
        Start checking macros by overwriting __getattribute__ method,
        but store parent __getattribute__ method for future rollback

        :return:
        """
        def __getattribute__(self, name):
            """
            Before return value, check if it is in MACRO_FIELDS,

            :param self: current object
            :type self: MacrosModelMixin
            :param name: field name
            :type name: str or unicode
            :return:
            """
            parent_getattribute = super(MacrosMixin, self).__getattribute__
            value = parent_getattribute(name)

            if name not in parent_getattribute('MACRO_FIELDS'):
                return value
            else:
                return self._process_macros(value)

        if cls._enabled_macros:
            return

        cls._enabled_macros = True
        if cls.MACRO_MAP:
            cls._parent_getattribute = super(MacrosMixin, cls).__getattribute__
            setattr(cls, '__getattribute__', __getattribute__)
        else:
            raise AttributeError(
                'You need to specify MACRO_MAP on your class definition'
            )

    @classmethod
    def is_macros_enabled(cls):
        """
        Get current state: either macros are enabled now or not

        :return: are macros enabled?
        :rtype: bool
        """
        return cls._enabled_macros

    @classmethod
    def stop_macros(cls):
        """
        Disable macros, but rolling back __getattirbute__ method

        :return:
        """

        if cls._enabled_macros:
            setattr(cls, '__getattribute__', cls._parent_getattribute)
            cls._enabled_macros = False

    def _process_macros(self, value):
        """
        Process macro patterns which are inside of [] and
        defined as keys in MACRO_MAP. If such pattern is found
        then call function which is defined as a value for this key
        in MACRO_MAP.


        :param value:
        :return:
        """
        if not value:
            return value

        macro_map = self.MACRO_MAP

        search_pattern = '\[' + '\]|\['.join(macro_map.keys()) + '\]'

        pattern = re.compile(search_pattern)

        return pattern.sub(
            lambda label: str(macro_map[label.group()[1:-1]](self)),
            value
        )
