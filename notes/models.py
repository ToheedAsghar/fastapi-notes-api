from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(10000), nullable=False)
    is_arhived = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("User")
