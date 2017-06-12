"""
All Wrappers inherit from this base class, which has 4 responsibilities:

* Instantiates Class and storing wrapped element.
* Provides a ``unwrap()`` method, which returns the wrapped object.
* Provides access to all original methods and attributes of the
  wrapped object.
* Create a ``__repr__()`` method for consistent representation

Because access to original methods and properties is maintained, you can keep
the elements wrapped throughout your code. You would only need to unwrap when
when passing the element into function where the original Type is expected.

>>> wrapped = BaseObjectWrapper(SomeObject)
>>> wrapped
<RPW_BaseOBjectWrapper:>
>>> wrapped.unwrap()
SomeObject
>>> wrapped.SomeOriginalMethod()
# Method will run.

"""

import rpw
from rpw.exceptions import RPW_TypeError, RPW_Exception
from rpw.utils import logger


class BaseObject(object):

        def __init__(self, *args, **kwargs):
            pass

        def ToString(self, *args, **kwargs):
            """ Show correct repr on Dynamo """
            return self.__repr__(*args, **kwargs)

        # def __dir__(self):
        # TODO: Implement Dir on BaseOBject and BaseObjectWrapper for proper AC
            # return list(self.__dict__)

        def __repr__(self, data=''):
            return '<rpw:{class_name} | {data}>'.format(
                                        class_name=self.__class__.__name__,
                                        data=data)


class BaseObjectWrapper(BaseObject):
    """
    Arguments:
        element(APIObject): Revit Element to store
    """

    def __init__(self, revit_object):
        """
        Child classes can use self._revit_object to refer back to Revit Element
        NOTE: Any Wrapper that inherits and overrides __ini__ class MUST
        super to ensure _revit_object is created.
        BaseObjectWrapper must define a class variable _revit_object_class
        to define the object being wrapped.
        """
        _revit_object_class = self.__class__._revit_object_class

        if not isinstance(revit_object, _revit_object_class):
            raise RPW_TypeError(_revit_object_class, type(revit_object))

        object.__setattr__(self, '_revit_object', revit_object)

    def __getattr__(self, attr):
        """
        Getter for original methods and properties or the element.
        This method is only called if the attribute name does not
        already exists.
        """
        try:
            return getattr(self.__dict__['_revit_object'], attr)
        except AttributeError:
            # This lower/snake case to be converted.
            # This automatically gives acess to all names in lower case format
            # x.name (if was not already defined, will get x.Name)
            # Note: will not Work for setters, unless defined by wrapper
            attr_pascal_case = rpw.utils.coerce.to_pascal_case(attr)
            return getattr(self.__dict__['_revit_object'], attr_pascal_case)
        except KeyError:
            raise RPW_Exception('BaseObjectWrapper is missing _revit_object')

    def __setattr__(self, attr, value):
        """
        Setter allows setting of wrapped object properties, for example
        ```WrappedWall.Pinned = True``
        """
        if hasattr(self._revit_object, attr):
            self._revit_object.__setattr__(attr, value)
        else:
            object.__setattr__(self, attr, value)

    def unwrap(self):
        return self._revit_object

    def __repr__(self, data={}, to_string=None):
        """ ToString can be overriden for objects in which the method is
        not consistent - ie. XYZ.ToString returns pt tuple not Class Name """
        revit_object_name = to_string or self._revit_object.ToString()
        revit_object_name_chunks = revit_object_name.split('.')
        if revit_object_name_chunks > 2:
            revit_object_name = '..{}'.format('.'.join(revit_object_name_chunks[-2:]))

        data = ' '.join(['{0}:{1}'.format(k, v) for k, v in data.iteritems()])

        return '<rpw:{class_name} % {revit_object} | {data}>'.format(
                                    class_name=self.__class__.__name__,
                                    data=data,
                                    revit_object=revit_object_name,
                                    )
