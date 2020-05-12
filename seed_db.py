import uuid

from app import db, User, OAuth


def generate_id() -> str:
    return str(uuid.uuid4())


def seed():
    OAuth.query.delete()
    User.query.delete()

    authorized_users = [
        User(
            id=generate_id(),
            username="farooqamahmud@gmail.com",
            email="farooqamahmud@gmail.com",
            is_authorized=1,
        )
    ]

    try:
        db.session.add_all(authorized_users)
        db.session.commit()
    except Exception:
        db.session.rollback()
    finally:
        db.session.close()
