from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Follow

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='999526',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date(),
                 avatar='/bird.png')
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()

def follows(count=100):
    user_count = User.query.count()
    for i in range(count):
        u1 = User.query.offset(randint(0, user_count - 1)).first()
        u2 = User.query.offset(randint(0, user_count - 1)).first()
        if not u1.is_following(u2) and u1 is not u2:
            pf = Follow(fan=u1, up=u2)
            db.session.add(pf)
            try:
                db.session.commit()
                i += 1
            except IntegrityError:
                db.session.rollback()
