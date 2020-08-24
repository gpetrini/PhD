from distutils.core import setup

setup(
    name='pyqca',
    version='2.1.12',
    author='Gabriel Petrini',
    author_email='gpetrinidasilveira@gmail.com',
    py_modules=['libfsqca','fuzzy','dataset','pptable','gtt','concov','acqlib', 
                'kirqlib','kirq_resources_rc','kirq_ui'],
    scripts=['bin/nec','bin/suf', 'bin/consist', 'bin/bq', 'bin/gtt',
             'bin/concov','bin/kirq'],
    data_files=[('man/man1', ['man/man1/nec.1',
                              'man/man1/suf.1',
                              'man/man1/consist.1',
                              'man/man1/bq.1',
                              'man/man1/gtt.1',
                              'man/man1/concov.1',
                              'man/man1/kirq.1'])],
    url='http://github/gpetrini/pyqca/',
    packages=['numpy', 'pandas','xlrd','openpyxl','openpyxl.reader','openpyxl.shared','openpyxl.shared.compat','openpyxl.tests','openpyxl.writer'],
    description='Qualitative Comparative Analysis',
)
