import pymysql
pymysql.install_as_MySQLdb()

# Permitir compatibilidad de Django con MySQL 8.0.x
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.check_database_version_supported = lambda self: None