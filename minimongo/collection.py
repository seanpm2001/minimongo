# -*- coding: utf-8 -*-

from pymongo.collection import Collection as PyMongoCollection

class Collection(PyMongoCollection):
    '''A wrapper around :class:`pymongo.collection.Collection` that
    provides the same functionality, but stores the document class of
    the collection we're working with. So that
    :meth:`pymongo.collection.Collection.find` and
    :meth:`pymongo.collection.Collection.find_one` can return the right
    classes instead of plain :class:`dict`.
    '''

    #: A reference to the model class, which uses this collection.
    document_class = None

    def __init__(self, *args, **kwargs):
        self.document_class = kwargs.pop('document_class')
        super(Collection, self).__init__(*args, **kwargs)

    def find(self, *args, **kwargs):
        '''Same as :meth:`pymongo.collection.Collection.find`, except
        it returns the right document class.
        '''
        kwargs['as_class'] = self.document_class
        return super(Collection, self).find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        '''Same as :meth:`pymongo.collection.Collection.find_one`, except
        it returns the right document class.
        '''
        kwargs['as_class'] = self.document_class
        return super(Collection, self).find_one(*args, **kwargs)

    def from_dbref(self, dbref):
        '''Given a :class:`pymongo.dbref.DBRef`, dereferences it and
        returns a corresponding document, wrapped in an appropriate model
        class.

        .. note:: If a given `dbref` point to a different database and
                  / or collection, :exc:`ValueError` is raised.
        '''
        # Making sure a given DBRef points to a proper collection
        # and database.
        if not dbref.collection == self.name:
            raise ValueError('DBRef points to an invalid collection.')
        elif dbref.database and not dbref.database == self.database.name:
            raise ValueError('DBRef points to an invalid database.')
        else:
            return self.find_one(dbref.id)