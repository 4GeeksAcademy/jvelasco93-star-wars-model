import os
from flask_admin import Admin
from models import db, User, Planet, Character, Vehicle
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class UserAdmin(ModelView):
        pass

    class CharacterAdmin(ModelView):
        column_list = ('id', 'name', 'hair_color', 'eye_color',
                       'birth_year', 'favorited_by')

    class PlanetAdmin(ModelView):
        column_list = ('id', 'name', 'climate', 'population',
                       'favorited_by')

    class VehicleAdmin(ModelView):
        column_list = ('id', 'name', 'model', 'passengers',
                       'favorited_by')

    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(CharacterAdmin(Character, db.session))
    admin.add_view(PlanetAdmin(Planet, db.session))
    admin.add_view(VehicleAdmin(Vehicle, db.session))