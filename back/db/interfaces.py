from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .tables import User, Category, Base


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

    def check_unique_username(self, username: str) -> bool:
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

    def get_categories_of_user(self, user_id: int) -> Iterable[Category]:
        """
        Получение категорий слов, относящихся к конкретному пользователю.
        :param user_id: id пользователя, к которому относятся категории
        :return: итератор строк БД
        """
        session = self.Session()
        try:
            categories = session.query(Category).filter(Category.user_id == user_id)
            return categories
        finally:
            session.close()
