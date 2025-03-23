from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(String, ForeignKey("category.id"), nullable=False)
    branch_id = Column(String, ForeignKey("branch.id"), nullable=False)

    category = relationship("Category", back_populates="menu_items")
    branch = relationship("Branch", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
