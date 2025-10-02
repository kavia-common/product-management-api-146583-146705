from marshmallow import Schema, fields


class ProductSchema(Schema):
    """Schema for a product entity."""
    id = fields.UUID(required=True, description="Product ID (UUID)")
    name = fields.Str(required=True, description="Product name")
    price = fields.Float(required=True, description="Product price")
    quantity = fields.Int(required=True, description="Quantity in stock")
    created_at = fields.DateTime(required=True, description="Creation timestamp")
    updated_at = fields.DateTime(required=True, description="Last update timestamp")


class ProductCreateSchema(Schema):
    """Schema for creating a product."""
    name = fields.Str(required=True, description="Product name")
    price = fields.Float(required=True, description="Product price")
    quantity = fields.Int(required=True, description="Quantity in stock")


class ProductUpdateSchema(Schema):
    """Schema for partially updating a product."""
    name = fields.Str(description="Product name")
    price = fields.Float(description="Product price")
    quantity = fields.Int(description="Quantity in stock")


class PaginationMetadataSchema(Schema):
    """Schema representing pagination metadata."""
    total = fields.Int(required=True)
    total_pages = fields.Int(required=True)
    first_page = fields.Int(required=True)
    last_page = fields.Int(required=True)
    page = fields.Int(required=True)
    previous_page = fields.Int(allow_none=True)
    next_page = fields.Int(allow_none=True)


class ProductListSchema(Schema):
    """Schema for a paginated list of products."""
    items = fields.List(fields.Nested(ProductSchema), required=True)
    meta = fields.Nested(PaginationMetadataSchema, required=True)


class TotalBalanceSchema(Schema):
    """Schema for total balance response."""
    total_balance = fields.Float(required=True, description="Sum of price * quantity for all products")
