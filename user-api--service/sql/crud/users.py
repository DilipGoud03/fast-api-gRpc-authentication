from sql.models.users import User
from sqlalchemy.orm import Session
import bcrypt


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user) -> User:
    user = User(
        name=user.get("name"),
        email=user.get("email"),
        password=_encoded_password(user.get("password")),
        created_at=user.get("created_at"),
        updated_at=user.get("updated_at")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, existing_user: User,  user_data: dict) -> User:

    name = user_data.get("name", "")
    if name != "":
        existing_user.name = user_data["name"]

    email = user_data.get("email", "")
    if email != "":
        existing_user.email = user_data["email"]

    password = user_data.get("password", "")
    if password != "":
        existing_user.password = _encoded_password(password)
    # db.commit()
    # db.refresh(existing_user)
    return existing_user


def delete_user(db: Session, user: User) -> bool:
    db.delete(user)
    db.commit()
    return True


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def _encoded_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password, "utf-8"), salt)


def _check_password(password, hashed_password) -> bool:
    h_password = bytes(hashed_password, "utf-8")
    _password = bytes(password, "utf-8")
    return bcrypt.checkpw(_password, h_password)

def _check_email(db:Session, email: str, id:int):
    user = db.query(User).filter(User.email==email, User.id!=id).first()
    if user:
        return True
    