# Various shims to deal with node renames between astroid versions - astroid 2.0 renamed
# some of the nodes used by this library so for backwards compatibility, old names are
# translated to new.

try:
	from astroid import Call
except ImportError:
	from astroid import CallFunc as Call


try:
	from astroid import AssignName
except ImportError:
	from astroid import AssName as AssignName


