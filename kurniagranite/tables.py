from .models import *
from table import Table
from table.columns import Column
from table.utils import A
from table.columns import LinkColumn, Link
class MaterialTable(Table):
    id = Column(field='id', header=u'Id')
    namamaterial = Column(field='namamaterial', header=u'Nama Material')
    slug = Column(field='slug', header=u'Id')
    status = Column(field='is_active', header=u'Status')
    detail = LinkColumn(header=u"Detail Material", links=[Link(text=u"Detail", viewname="detailmaterial", args=(A('slug'),)),])
    aksi = LinkColumn(header=u"Aksi", links=[Link(text=u"Edit", viewname="materialhapus", args=(A('id'),)),])

    class Meta:
        model = Material
        pagination = True
        search = True