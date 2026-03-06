# 统一导入，确保 SQLAlchemy 能发现所有 Model
from app.models.brand import Brand
from app.models.tag import Tag
from app.models.product import Product, product_tag_table
from app.models.order import Order, OrderItem
