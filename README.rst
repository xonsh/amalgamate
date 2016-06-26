==========
amalgamate
==========
A package-based, source code amalgamater for collapsing Python packages into
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
should exclusively use imports like the following::

    from pkg.x import a, c, d
    from pkg.y import e, f, g

These from-imports simulate all of the ``x``, ``y``, and ``z`` modules having
the same ``globals()``.
This is because the amalgamater puts all such modules in the same globals(),
which is effectively what the from-imports do. For example, ``xonsh.ast`` and
``xonsh.execer`` are both in the same package (``xonsh``). Thus they should use
the above from from-import syntax.

Alternatively, for modules outside of the current package (or modules that are
not amalgamated) the import statement should be either ``import pkg.x`` or
``import pkg.x as name``. This is because these are the only cases where the
amalgamater is able to automatically insert lazy imports in way that is guaranteed
to be safe. Say we are back in ``z`` and depend on ``dep``, ``collections.abc``,
and modules in a subpackage, ``pkg.sub``.  The following are all acceptable::

    import dep
    import collections.abc as abc
    import pkg.dep.mod0
    import pkg.dep.mod1 as mod1

The important thing here is to simply be consistent for such imports across all
modules in the package ``pkg``.

**WARNING:** You should not use the form ``from pkg.i import j`` for modules
outside of the amalgamated package. This is due to the ambiguity that
``from pkg.x import name`` may import a variable that cannot be lazily constructed
OR may import a module. The amalgamater is forced to leave such import statements
as they were written, which means that they cannot be automatically lazy or
eliminated.  They are thus forced to be imported at when ``__amalgam__.py`` is
imported/

So the simple rules to follow are that:

1. Import objects from modules in the same package directly in using from-import,
2. Import objects from modules outside of the package via a direct import
   or import-as statement.


*********************
``__init__.py`` Hooks
*********************
To make this all work, the ``__init__.py`` for the package needs a predefined
space for ``amalgamate.py`` to write hooks into.  In its simplest form, this
is defined by the lines::

    # amalgamate exclude
    # amalgamate end

The ``amalgamate.py`` script will fill in between these two line and will over
write them as needed.  The initial exclude line accepts a space-separated list
of module names in the package to exclude from amalgamation::

    # amalgamate exclude foo bar baz
    # amalgamate end

You may also provide as many exclude lines as you want, though there should
only be one end line::

    # amalgamate exclude foo
    # amalgamate exclude bar
    # amalgamate exclude baz
    # amalgamate end

Also note that all modules whose names start with a double underscore, like
``__init__.py`` and ``__main__.py`` are automatically excluded.


**********************
Command Line Interface
**********************
The command line interface is a list of package names to amalgamate::

    $ amalgamate.py pkg pkg.sub0 pkg.sub1

You may also provide the ``--debug=NAME`` name to declare the environment
variable name for import debugging::

    $ amalgamate.py --debug=PKG_DEBUG pkg pkg.sub0 pkg.sub1

By default, this environment variable is simply called ``DEBUG``. If this
environment variable exists and is set to a non-empty string, then all
amalgamated imports are skipped and the modules in the package are imported
normally.  For example, suppose you have a script that imports your package
and you would like to see the module names, you could run the script with::

    $ env PKG_DEBUG=1 python script.py

to suppress the amalgamated imports.

**************
Setup Hooks
**************
We recommend running ``amalgamate.py`` every time that setup.py is executed.
This keeps ``__amalgam__.py`` and ``__init__.py`` in sync with the rest of
the package.  Feel free to use the following hook function in your project::

    def amalgamate_source():
        """Amalgamates source files."""
        try:
            import amalgamate
        except ImportError:
            print('Could not import amalgamate, skipping.', file=sys.stderr)
            return
        amalgamate.main(['amalgamate', '--debug=PKG_DEBUG', 'pkg'])

Additionally, feel free to copy the ``amalgamate.py`` script to your project.
It is only a single file!

**************
Dark Wizardry
**************
This is implemented via a syntax tree transformation so developers could write
mostly normal Python without having to worry about import speed. That accounts for
the wizardry.

The darkness comes from a project called
`JsonCpp <https://github.com/open-source-parsers/jsoncpp>`_. JsonCpp has an
`amalgamate script <https://github.com/open-source-parsers/jsoncpp/blob/master/amalgamate.py>`_,
that glues the whole project into a single header and single source file.
This is an amazing idea.  The kicker is that JsonCpp's amalgamate is written in
Python :)
