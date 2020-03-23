from hobbit_core.db import Column, BaseModel, reference_col, SurrogatePK
from sqlalchemy.orm import relationship, exc

from app.exts import bcrypt, db


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
#     exclude_columns = ['created_at', 'updated_at']
#     auth_name = Column(db.String(32), nullable=False, index=True)
#     path = Column(db.String(256), nullable=False)
#     level = Column(db.Integer, nullable=True)
#     children = relationship("SubMenu", backref='parent')

#     def __init__(self, auth_name, path, **kwargs):
#         db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)


# class SubMenu(BaseModel):
#     __tablename__ = 'submenus'
#     exclude_columns = ['created_at', 'updated_at']
#     parent_id = Column(db.Integer, db.ForeignKey('menus.id'))

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key = True)
    exclude_columns = ['created_at', 'updated_at']
    auth_name = Column(db.String(32), nullable=False, index=True)
    path = Column(db.String(256), nullable=False)
    level = Column(db.Integer, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    sub_menu = db.relationship('Menu', back_populates='parent_menu')
    parent_menu = db.relationship('Menu', back_populates='sub_menu', remote_side=[id, auth_name, path])

    def __init__(self, auth_name, path, **kwargs):
        db.Model.__init__(self, auth_name=auth_name, path=path, **kwargs)
