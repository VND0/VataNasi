from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Класс, реализующий данные пользователя в БД."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    categories = relationship("Category", back_populates="user_id")

    def __init__(self, username: str, password_hash: str) -> None:
        """
        Создание строки в таблице.
        :param username: уникальное имя пользователя
        :param password_hash: хэш пароля
        """
        self.username = username
        self.password_hash = password_hash


class Category(Base):
    """Класс, реализующий категорию слов в БД. Имеет связь с юзером и словами."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))
    words = relationship("Word", back_populates="category_id")

    def __init__(self, name: str, user_id: int) -> None:
        """
        Создание строки в таблице.
        :param name: уникальное название категории
        :param user_id: id пользователя, который создал категорию
        """
        self.name = name
        self.user_id = user_id


class Word(Base):
    """Класс, реализующий пару "слово-перевод". Связан с категорией, к которой относится."""
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    translation = Column(String)
    category_id = ForeignKey(Category.id)

    def __init__(self, value: str, translation: str, category_id: int) -> None:
        """
        Создание строки в таблице.
        :param value: оригинальное слово
        :param translation: перевод слова
        :param category_id: id категории, к которой относится слово
        """
        self.value = value
        self.translation = translation
        self.category_id = category_id
