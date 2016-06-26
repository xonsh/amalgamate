==========
amalgamate
==========
A package-based, source code amalgamater for collapseing Python packages into
a single module.

The amalgamate utility enables the possibility of speeding up startup time for
Python packages at low-to-no run time cost. If this sounds too good to be true,
read on for the details!

The big idea here is to glue most of the source files in a package or subpackage
together into a single module, called ``__amalgam__.py``. Combined with some hooks
in the ``__init__.py``, this should dramatically reduce the number of files that
are being searched for inside of the package.  This is critical in larger
projects where import times are the major startup time cost.

The ``amalgamate.py`` script automatically creates the ``__amalgamate__.py`` file
for a package. This will create and solve a dependency graph of all modules in
the package. It then will go through each module and glue it into the
``__amalgamate__.py``, removing duplicate imports as it goes.

Additionally, the ``amalgamate.py`` script will automatically make most
non-package imports lazy. This lets developers write as many imports as they
want, without having to worry about startup times. Non-package modules
aren't actually imported in ``__amalgam__.py`` until they are used (ie an
attribute is accessed).

This has some funny side effects such as,

1. All of the modules that are amalgamated share the same globals (so be
   careful about naming things),
2. Debugging makes most things looks like code comes from ``__amalgam__``,
   unless an environment variable is set prior to import.
3. Not all imports are able to be lazy.

**********
Imports
**********
The way the code amalgamater works is that other modules
that are in the same package (and amalgamated) should be imported from-imports,
without an ``as``-clause.  For example, suppose that ``z`` is a module in the
package ``pkg``, that depends on ``x`` and ``y`` in the same package.  ``z``
should exlucively use imports like the following::

    from pkg.x import a, c, d
    from pkg.y import e, f, g

These from-imports simulate all of the ``x``, ``y``, and ``z`` modules having
the same ``gloabls()``.
This is because the amalgamater puts all such modules in the same globals(),
which is effectively what the from-imports do. For example, ``xonsh.ast`` and
``xonsh.execer`` are both in the same package (``xonsh``). Thus they should use
the above from from-import syntax.

Alternatively, for modules outside of the current package (or modules that are
not amalgamated) the import statement should be either ``import pkg.x`` or
``import pkg.x as name``. This is because these are the only cases where the
amalgamater is able to automatically insert lazy imports in way that is guarantted
to be safe. Say we are back in ``z`` and depend on ``dep``, ``collections.abc``,
and modules in a subpackage, ``pkg.sub``.  The following are all acceptable::

    import dep
    import collections.abc as abc
    import pkg.dep.mod0
    import pkg.dep.mod1 as mod1

The important thing here is to simply be consistent for such imports across all
modules in the package ``pkg``.

**WARNING:** You should not use the form ``from pkg.i import j`` for modules
outside of the amalgamted package. This is due to the ambiguity that
``from pkg.x import name`` may import a variable that cannot be lazily constructed
OR may import a module. The amalgamater is foreced to leave such import stametements
as they were written, which means that they cannot be automatically lazy or
eliminated.  They are thus forced to be imported at when ``__amalgam__.py`` is
imported/

So the simple rules to follow are that:

1. Import objects from modules in the same package directly in using from-import,
2. Import objects from moudules outside of the package via a direct import
   or import-as statement.

