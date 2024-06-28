import pymysql

# 替换django默认底层mysql
pymysql.install_as_MySQLdb()