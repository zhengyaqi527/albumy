import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from albumy.models import Photo, User
from albumy.extensions import db

fake = Faker()

def fake_admin():
    admin = User(
        name='Yaqi Zheng',
        username='zhengyaqi',
        email='yaqi.zheng@guokr.com',
        bio=fake.sentence(),
        website='https://zhengyaqi527.github.io/struggle_everyday',
        confirmed=True
    )
    admin.set_password('1233211234567')
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for i in range(count):
        user = User(
            username=fake.name(),
            confirmed=True,
            bio=fake.sentence(),
            website=fake.url(),
            location=fake.city(),
            member_since=fake.date_this_decade(),
            email=fake.email()
        )
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        filename = 'random_%d.jpg' %i
        r = lambda: random.randint(128, 255)
        img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_this_year()
        )
        db.session.add(photo)
    db.session.commit()