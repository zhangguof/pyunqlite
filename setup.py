from distutils.core import setup, Extension

_unqlite = Extension('_unqlite',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = ['src'],
                    #libraries = ['tcl83'],
                    #library_dirs = ['/usr/local/lib'],
                    sources = ['wrap_unqlite.c','src/unqlite.c'])

setup (name = '_unqlite',
       version = '0.1',
       description = 'This is a python bind unqlite',
       author = 'zhangguofeng',
       author_email = 'zhangguof@gmail.com',
       url = '',
       ext_modules = [_unqlite])