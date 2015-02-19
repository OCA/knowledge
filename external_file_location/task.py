# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import sys
from openerp import models, fields

class Task(models.Model):
    _name = 'ir.location.task'
    _description = 'Description'
    
    name = fields.Char()
    # method = fields.Selection([
    #     ('ftp_import', 'FTP import'),
    #     ('ftp_export', 'FTP export'),
    #     ('sftp_import', 'SFTP import'),
    #     ('sftp_export', 'SFTP export'),
    #     ('filestore_import', 'Filestore import'),
    #     ('filestore_export', 'Filestore export'),
    #     ])
    method = fields.Selection(selection='_get_method')
    filename = fields.Char()
    filepath = fields.Char()
    location_id = fields.Many2one('ir.location', string='Location')

    def _get_method(self):
        res = []
        for cls in itersubclasses(AbstractTask):
            if cls._synchronize_type:
                cls_info = (cls._key + cls._synchronize_type, cls._name + cls._synchronize_type)
                res.append(cls_info)
        return res

    def run(self):
        connection_class = ...

        method_class = getattr(sys.modules[__name__], self.method)
        config = {
                'host': self.location_id.address,
                'user': self.location_id.login,
                'pwd': self.location_id.password,
                'port': self.location_id.port,
                'allow_dir_creation': False,
                'filename': self.filename,
                'path': self.filepath
                }
        conn = method_class(config)
        conn.run()


def itersubclasses(cls, _seen=None):
    """
    itersubclasses(cls)
    Generator over all subclasses of a given class, in depth first order.
    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>>
    >>> for cls in itersubclasses(A):
    ... print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
               'new-style classes, not %.100r' % cls
               )
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub
