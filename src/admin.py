import os
from flask_admin import Admin
from models import db, User, Planet, Character, Vehicle
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class UserAdmin(ModelView):
        form_ajax_refs = {
            'favorite_characters': {
                'fields': ['name'],
                'page_size': 10,
            },
            'favorite_planets': {
                'fields': ['name'],
                'page_size': 10,
            },
            'favorite_vehicles': {
                'fields': ['name'],
                'page_size': 10,
            },
        }

    admin.add_view(UserAdmin(User, db.session))

    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
