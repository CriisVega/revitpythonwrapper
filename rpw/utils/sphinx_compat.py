class MockDB(object):

    BuiltInParameter = None
    BuiltInCategory = None
    ElementId = None

    def __init__(self, name=None):
        self.name = name

    def __getattr__(self, name, *args, **kwargs):
        return MockDB(name)

    def __repr__(self):
        return 'DB.' + self.name

DB = MockDB()
DB.__class__.__name__ = 'DB'
UI = MockDB()
UI.__class__.__name__ = 'UI'

doc = None
uidoc = None
version = None
List = None
Enum = None
wpf = None
Application = None
Window = object
