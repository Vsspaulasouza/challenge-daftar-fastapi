from sqlalchemy import Column, Integer, String

from src.infra.database import Base


class Stories(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    text = Column(String, nullable=False)
