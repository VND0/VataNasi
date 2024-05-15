from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .tables import User, Category, Base, Word


class DataBase:
    """Набор внешних интерфейсов для взаимодействия с БД."""

    def __init__(self, path: str) -> None:
        """
        Инициализация движка БД.
        :param path: Путь к файлу с базой данных
        """
        self.engine = create_engine(f"sqlite:///{path}")
        self.Session = sessionmaker(self.engine)

    def create_tables_if_not_exist(self) -> None:
        Base.metadata.create_all(self.engine)

    def is_username_new(self, username: str) -> bool:
        session = self.Session()
        try:
            all_users = list(session.query(User).filter(User.username == username).all())
            return not all_users
        finally:
            session.close()

    def new_user(self, username: str, password_hash: str) -> int:
        """
        Добавление нового пользователя в БД.
        :param username: уникальное имя пользователя
        :param password_hash: хэш пароля нового пользователя
        :return: id нового пользователя в БД
        """
        session = self.Session()
        try:
            new_user = User(username, password_hash)
            session.add(new_user)
            session.commit()
            return new_user.id
        finally:
            session.close()

    def get_categories_of_user(self, user_id: int) -> list[str]:
        """
        Получение категорий слов, относящихся к конкретному пользователю.
        :param user_id: id пользователя, к которому относятся категории
        :return: итератор строк БД
        """
        session = self.Session()
        try:
            categories = session.query(Category).filter(Category.user_id == user_id).all()
            return [x.name for x in categories]
        finally:
            session.close()

    def get_user(self, username: str, password_hash: str) -> User | None:
        session = self.Session()
        try:
            return session.query(User).filter(
                User.username == username and User.password_hash == password_hash).one_or_none()
        finally:
            session.close()

    def select_user_by_id(self, id: int) -> User | None:
        session = self.Session()
        try:
            return session.query(User).filter(User.id == id).one()
        finally:
            session.close()

    def delete_user(self, username: str) -> None:
        with self.Session() as session:
            user = session.query(User).filter(User.username == username).one()
            categories = session.query(Category).filter(Category.user == user).all()
            for category in categories:
                words = session.query(Word).filter(Word.category == category).all()
                for word in words:
                    session.delete(word)
                session.delete(category)
            session.delete(user)

            session.commit()

    def change_passwd(self, username: str, new_passwd_hash: str) -> None:
        with self.Session() as session:
            session.query(User).filter(User.username == username).update({User.password_hash: new_passwd_hash})
            session.commit()

    def delete_category(self, user_id: int, category_name: str) -> None:
        with self.Session() as session:
            category = session.query(Category).filter(
                Category.user_id == user_id and Category.name == category_name
            ).one()
            session.delete(category)
            session.commit()
