# product-management-api-146583-146705

Products Backend API (Flask) providing CRUD operations on products with fields: id (UUID), name, price, quantity.

- Ocean Professional themed OpenAPI docs available at /docs
- Persistence via SQLAlchemy to the products_database (configure via environment variables)

## Run locally

1. Create a `.env` from `.env.example` and set DB connection variables.
2. Install dependencies:
   pip install -r products_backend_api/requirements.txt
3. Start the server:
   python -m products_backend_api.run

The API will listen on HOST:PORT (defaults: 0.0.0.0:3001).

## Endpoints

- GET /               -> Health
- GET /products       -> List products (page, page_size)
- POST /products      -> Create product
- GET /products/{id}  -> Get product by ID
- PATCH /products/{id}-> Update product partially
- DELETE /products/{id}-> Delete product

## Notes

- Provide DATABASE_URL or DB_* parts in the environment to connect to the products_database container.
- If no DB variables are provided, the API uses an in-memory SQLite fallback (for CI/dev only).
