from sqlalchemy import Column, Numeric, String, UnicodeText

from . import BASE, SESSION


class Like(BASE):
    __tablename__ = "zedlikes"
    chat_id = Column(String(14), primary_key=True)
    lik_id = Column(String(14), primary_key=True, nullable=False)
    f_name = Column(UnicodeText)
    f_user = Column(UnicodeText)

    def __init__(self, chat_id, lik_id, f_name, f_user):
        self.chat_id = str(chat_id)
        self.lik_id = str(lik_id)
        self.f_name = f_name
        self.f_user = f_user

    def __eq__(self, other):
        return bool(
            isinstance(other, Like)
            and self.chat_id == other.chat_id
            and self.lik_id == other.lik_id
        )


Like.__table__.create(bind=SESSION.get_bind(), checkfirst=True)


def get_like(chat_id, lik_id):
    try:
        return SESSION.query(Like).get((str(chat_id), str(lik_id)))
    finally:
        SESSION.close()


def get_likes(chat_id):
    try:
        return SESSION.query(Like).filter(Like.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_like(chat_id, lik_id, f_name, f_user):
    to_check = get_like(chat_id, lik_id)
    if not to_check:
        adder = Like(str(chat_id), str(lik_id), f_name, f_user)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Like).get((str(chat_id), str(lik_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Like(str(chat_id), str(lik_id), f_name, f_user)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_like(chat_id, lik_id):
    to_check = get_like(chat_id, lik_id)
    if not to_check:
        return False
    rem = SESSION.query(Like).get((str(chat_id), str(lik_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def remove_all_likes(chat_id):
    if saved_like := SESSION.query(Like).filter(Like.chat_id == str(chat_id)):
        saved_like.delete()
        SESSION.commit()
