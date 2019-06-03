import sys

if sys.platform.startswith('win32'):
    import pymysql
    pymysql.install_as_MySQLdb()