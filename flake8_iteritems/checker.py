from .version import __version__
from ast import walk, Call, Name, Dict, Attribute

class IteritemsChecker(object):
    name = 'flake8_iteritems'
    version = __version__

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in walk(self.tree):
            if not isinstance(node, Call):
                continue
            # if isinstance(node.func, Name) and node.func.id in ('iteritems', 'iterkeys', 'itervalues',):
            #     # no need to check top-level iteritems() etc, they are not bound methods
            #     pass
            if isinstance(node.func, Attribute) and isinstance(node.func.value, (Name, Dict)) and node.func.attr in ('iteritems', 'iterkeys', 'itervalues',):
                pass
            else:
                continue
            if len(node.args) > 0:
                continue
            if isinstance(node.func.value, Name):
                varName = node.func.value.id
            else:
                varName = '{}'  # todo: better print str(node.func.value)
            yield node.lineno, node.col_offset, 'ITI010 %s.%s() needs to be migrated to six.%s(%s)' % (varName, node.func.attr, node.func.attr, varName), type(self)
