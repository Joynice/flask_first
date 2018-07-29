#encoding:utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from app import app
from models import User,Question,Answer
manager = Manager(app)

#使用Migrate 绑定app,db
migrate = Migrate(app,db)

#添加迁移脚本命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()