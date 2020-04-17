from datetime import datetime
from hobbit_core.db import Column, BaseModel, reference_col, SurrogatePK
from sqlalchemy.orm import relationship, exc

from app.exts import bcrypt, db
# from app.models import Role # (ORM之间的model不需要互相导入，可以直接使用)


# class SubMenu(db.Model, SurrogatePK):
#     __tablename__ = 'submenus'
#     child_id = Column(db.Integer, db.ForeignKey('menus.id'), primary_key=True)
#     # child_id = reference_col('menus', nullable=False)
#     parent_id = Column(db.Integer, db.ForeignKey('menus.id'), primary_key=True)
#     # parent_id = reference_col('menus', nullable=False)
#     def __init__(self, **kwargs):
#         db.Model.__init__(self, **kwargs)


# class Menu(BaseModel):
#     __tablename__ = 'menus'
#     exclude_columns = ['created_at', 'updated_at']
#     auth_name = Column(db.String(32), nullable=False, index=True)
#     path = Column(db.String(256), nullable=False)

#     children = relationship('SubMenu',
#                             foreign_keys=[SubMenu.parent_id],
#                             backref = db.backref('parent', lazy='joined'),
#                             lazy = 'dynamic',
#                             cascade = 'all, delete-orphan'
#                             )

#     parents = relationship('SubMenu',
#                             foreign_keys=[SubMenu.child_id],
#                             backref = db.backref('child', lazy='joined'),
#                             lazy = 'dynamic',
#                             cascade = 'all, delete-orphan'
#                             )
#     def add_child(self, menu):
#         if not self.is_sub_menu(menu):
#             sub_menu = SubMenu(parent=self, child=menu)
#             db.session.add(sub_menu)
    
#     def remove_child(self, menu):
#         sub_menu = self.children.filter_by(child_id=menu.id).first()
#         if sub_menu:
#             db.session.delete(sub_menu)

#     def is_sub_menu(self, menu):
#         return self.children.filter_by(child_id=menu.id).first() is not None    
    

#     def __init__(self, auth_name, path, **kwargs):
#         db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)

# class Menu(BaseModel):
#     __tablename__ = 'menus'
#     # exclude_columns = ['created_at', 'updated_at']
#     auth_name = Column(db.String(32), nullable=False, index=True)
#     path = Column(db.String(256), nullable=False)
#     level = Column(db.Integer, nullable=True)
#     # children = relationship("SubMenu", backref='parent')

#     def __init__(self, auth_name, path, **kwargs):
#         db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)


# class SubMenu(BaseModel):
#     __tablename__ = 'submenus'
#     exclude_columns = ['created_at', 'updated_at']
#     auth_name = Column(db.String(32), nullable=False, index=True)
#     path = Column(db.String(256), nullable=False)
#     level = Column(db.Integer, nullable=True)
#     parent_id = Column(db.Integer, db.ForeignKey('menus.id'))
#     parent = relationship('Menu', backref=db.backref('children', order_by=auth_name))

#     def __init__(self, auth_name, path, **kwargs):
#         db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)

association_table = db.Table('association',
    # Column('menu_id', db.Integer, db.ForeignKey('menus.id', ondelete='CASCADE')),
    # Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
    Column('menu_id', db.Integer, db.ForeignKey('menus.id')),
    Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key = True)
    exclude_columns = ['created_at', 'updated_at']
    auth_name = Column(db.String(32), nullable=False, index=True)
    path = Column(db.String(256), nullable=False)
    level = Column(db.Integer, nullable=True)
    created_at = Column(db.Date, nullable=True, default=datetime.now)
    updated_at = Column(db.Date, nullable=True, default=datetime.now)
    parent_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    children = db.relationship('Menu', back_populates='parent')
    parent = db.relationship('Menu', back_populates='children', remote_side=[id])

    # role_id = Column(db.Integer, db.ForeignKey('roles.id'))
    # role = relationship('Role', backref=db.backref('menus', order_by=id))
    # roles = relationship('Role', secondary=association_table, back_populates="menus")
    # 将back_populates修改为db.backref() 指定 lazy = 'dynamic' 参数，关系两侧返回的查询都可接受额外的过滤器
    roles = relationship('Role', secondary=association_table, backref=db.backref("menus", lazy='dynamic'))


    def __init__(self, auth_name, path, **kwargs):
        db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)


# association_table = Table('association', db.Model.metadata,
#     Column('menu_id', db.Integer, ForeignKey('menus.id')),
#     Column('role_id', db.Integer, ForeignKey('roles.id'))
# )


