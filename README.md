# 🍔 Food Delivery API

A production-style REST API backend for a food delivery platform, built with **FastAPI**, **MySQL**, and **SQLAlchemy**.

---

## 🚀 Tech Stack

| Layer        | Technology                  |
|--------------|-----------------------------|
| Framework    | FastAPI                     |
| Database     | MySQL 8                     |
| ORM          | SQLAlchemy                  |
| Auth         | JWT (python-jose) + bcrypt  |
| Migrations   | Alembic                     |
| Testing      | Pytest + httpx              |
| Docs         | Swagger / OpenAPI (built-in)|

---

## 📁 Project Structure

```
food-delivery-api/
├── app/
│   ├── main.py               # App entry point, middleware, router registration
│   ├── core/                 # Config, DB, security, constants, dependencies
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── api/v1/               # Route handlers (controllers)
│   ├── crud/                 # Direct DB operations
│   ├── services/             # Business logic layer
│   ├── utils/                # Helpers: pagination, file upload, validators
│   └── middleware/           # Logging, auth middleware
├── migrations/               # Alembic migration files
├── tests/                    # Pytest test suite
├── uploads/                  # Uploaded images
├── .env                      # Environment variables
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1. Clone & create virtual environment

```bash
git clone <your-repo-url>
cd food-delivery-api
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Edit `.env`:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/food_delivery_db
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start MySQL (via Docker)

```bash
docker-compose up -d db
```

Or use a local MySQL instance and create the database:
```sql
CREATE DATABASE food_delivery_db;
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

The app auto-creates all tables on startup via `Base.metadata.create_all()`.

### 5. Open Swagger docs

```
http://localhost:8000/docs
```

---

## 🗄️ Database Tables

| Table          | Description                          |
|----------------|--------------------------------------|
| `users`        | Customers, restaurant owners, admins |
| `restaurants`  | Restaurant profiles                  |
| `categories`   | Menu categories per restaurant       |
| `menu_items`   | Food items with price and image      |
| `cart`         | One cart per user                    |
| `cart_items`   | Items in a cart                      |
| `orders`       | Placed orders                        |
| `order_items`  | Snapshot of items per order          |
| `payments`     | Payment records per order            |
| `addresses`    | Delivery addresses per user          |
| `reviews`      | Ratings and reviews per restaurant   |
| `coupons`      | Discount codes                       |

---

## 🔐 Roles

| Role               | Permissions                                             |
|--------------------|---------------------------------------------------------|
| `admin`            | Full access: users, restaurants, coupons, orders        |
| `restaurant_owner` | Manage own restaurant, menu, and incoming orders        |
| `customer`         | Browse, cart, place orders, pay, review                 |

---

## 🌐 API Endpoints

### Auth
| Method | Endpoint                  | Description         |
|--------|---------------------------|---------------------|
| POST   | `/api/v1/auth/register`   | Register new user   |
| POST   | `/api/v1/auth/login`      | Login, get JWT      |
| GET    | `/api/v1/auth/me`         | Current user info   |

### Restaurants
| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| GET    | `/api/v1/restaurants/`            | List all restaurants     |
| GET    | `/api/v1/restaurants/{id}`        | Get restaurant details   |
| POST   | `/api/v1/restaurants/`            | Create restaurant        |
| PUT    | `/api/v1/restaurants/{id}`        | Update restaurant        |
| DELETE | `/api/v1/restaurants/{id}`        | Delete restaurant        |
| POST   | `/api/v1/restaurants/{id}/image`  | Upload restaurant image  |

### Menu
| Method | Endpoint                    | Description          |
|--------|-----------------------------|----------------------|
| GET    | `/api/v1/menu/?restaurant_id=` | List menu items   |
| POST   | `/api/v1/menu/`             | Create menu item     |
| PUT    | `/api/v1/menu/{id}`         | Update menu item     |
| DELETE | `/api/v1/menu/{id}`         | Delete menu item     |

### Cart
| Method | Endpoint                        | Description        |
|--------|---------------------------------|--------------------|
| GET    | `/api/v1/cart/`                 | View cart          |
| POST   | `/api/v1/cart/add`              | Add item to cart   |
| PUT    | `/api/v1/cart/update`           | Update quantity    |
| DELETE | `/api/v1/cart/remove/{item_id}` | Remove item        |

### Orders
| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| POST   | `/api/v1/orders/`     | Place order          |
| GET    | `/api/v1/orders/`     | List my orders       |
| GET    | `/api/v1/orders/{id}` | Get order detail     |
| PUT    | `/api/v1/orders/status` | Update order status|

### Payments
| Method | Endpoint                   | Description     |
|--------|----------------------------|-----------------|
| POST   | `/api/v1/payments/`        | Make payment    |
| GET    | `/api/v1/payments/{order_id}` | Get payment  |

### Reviews
| Method | Endpoint                        | Description          |
|--------|---------------------------------|----------------------|
| POST   | `/api/v1/reviews/`              | Post a review        |
| GET    | `/api/v1/reviews/{restaurant_id}` | Get reviews        |

### Coupons
| Method | Endpoint            | Description       |
|--------|---------------------|-------------------|
| POST   | `/api/v1/coupons/`  | Create coupon     |
| GET    | `/api/v1/coupons/`  | List valid coupons|

### Addresses
| Method | Endpoint                    | Description        |
|--------|-----------------------------|--------------------|
| GET    | `/api/v1/addresses/`        | List my addresses  |
| POST   | `/api/v1/addresses/`        | Add new address    |
| DELETE | `/api/v1/addresses/{id}`    | Delete address     |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🐳 Run Everything with Docker

```bash
docker-compose up --build
```

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

---

## 💡 Resume Highlights

- ✅ FastAPI with layered architecture (routes → services → crud → models)
- ✅ JWT authentication + bcrypt password hashing
- ✅ Role-based access control (Admin / Restaurant Owner / Customer)
- ✅ Full relational schema with One-to-One, One-to-Many, Many-to-Many
- ✅ Pagination & query filtering
- ✅ File uploads (restaurant & menu images)
- ✅ Swagger / OpenAPI docs auto-generated
- ✅ Alembic migrations ready
- ✅ Pytest test suite
- ✅ Docker Compose setup
