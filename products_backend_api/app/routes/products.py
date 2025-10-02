from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import func
from uuid import UUID

from app.db import db, Product
from app.schemas import (
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
    ProductListSchema,
    TotalBalanceSchema,
)

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/products",
    description="CRUD operations for product resources",
)


def parse_uuid(value: str):
    try:
        return UUID(value)
    except Exception:
        abort(400, message="Invalid product ID format. Must be a UUID.")


@blp.route("/")
class ProductsList(MethodView):
    @blp.arguments(ProductCreateSchema)
    @blp.response(201, ProductSchema)
    def post(self, data):
        """Create a new product.
        Request JSON:
          - name: string
          - price: float
          - quantity: int
        Returns: Created product.
        """
        try:
            product = Product(**data)
            db.session.add(product)
            db.session.commit()
            return product
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Invalid product data or duplicate constraint violation.")
        except DataError:
            db.session.rollback()
            abort(400, message="Invalid product data types provided.")

    @blp.response(200, ProductListSchema)
    def get(self):
        """List products with pagination.
        Query params:
          - page: int (default 1)
          - page_size: int (default 20, max 100)
        Returns: items + pagination metadata.
        """
        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 20))
        except ValueError:
            abort(400, message="page and page_size must be integers.")

        page = 1 if page < 1 else page
        page_size = 1 if page_size < 1 else min(page_size, 100)

        query = Product.query
        total = query.count()
        items = (
            query.order_by(Product.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        total_pages = (total + page_size - 1) // page_size if page_size else 1
        meta = {
            "total": total,
            "total_pages": total_pages,
            "first_page": 1 if total > 0 else 0,
            "last_page": total_pages if total_pages > 0 else 0,
            "page": page,
            "previous_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page < total_pages else None,
        }
        return {"items": items, "meta": meta}


@blp.route("/total_balance")
class ProductsTotalBalance(MethodView):
    @blp.response(200, TotalBalanceSchema)
    def get(self):
        """Returns the sum of price * quantity for all products in stock."""
        # Compute sum(price * quantity) in the database for efficiency
        result = db.session.query(func.coalesce(func.sum(Product.price * Product.quantity), 0.0)).scalar()
        # Ensure float type for JSON serialization
        total_balance = float(result or 0.0)
        return {"total_balance": total_balance}


@blp.route("/<string:product_id>")
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id: str):
        """Get a product by ID."""
        pid = parse_uuid(product_id)
        product = Product.query.get(pid)
        if not product:
            abort(404, message="Product not found.")
        return product

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def patch(self, data, product_id: str):
        """Partially update a product."""
        pid = parse_uuid(product_id)
        product = Product.query.get(pid)
        if not product:
            abort(404, message="Product not found.")

        for k, v in data.items():
            setattr(product, k, v)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Invalid product update data.")
        except DataError:
            db.session.rollback()
            abort(400, message="Invalid product data types provided.")
        return product

    @blp.response(204)
    def delete(self, product_id: str):
        """Delete a product."""
        pid = parse_uuid(product_id)
        product = Product.query.get(pid)
        if not product:
            abort(404, message="Product not found.")
        db.session.delete(product)
        db.session.commit()
        return ""
