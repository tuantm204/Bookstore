# 📚 BookStore Microservices - API Documentation

> **Base URL:** `http://localhost:8000/api`
>
> Tất cả request đều đi qua **API Gateway** (port 8000), gateway sẽ proxy tới service tương ứng.

---

## 📐 Kiến trúc tổng quan

```
Client  →  API Gateway (:8000)  →  Microservices (:8001-8011)  →  MySQL (:3306)
```

| Service | Port | Database | Prefix API |
|---------|------|----------|------------|
| Customer Service | 8001 | customer_db | `/api/customers/` |
| Staff Service | 8002 | staff_db | `/api/staffs/` |
| Manager Service | 8003 | manager_db | `/api/managers/` |
| Catalog Service | 8004 | catalog_db | `/api/catalogs/` |
| Book Service | 8005 | book_db | `/api/books/` |
| Cart Service | 8006 | cart_db | `/api/carts/`, `/api/cart-items/` |
| Order Service | 8007 | order_db | `/api/orders/`, `/api/order-items/` |
| Pay Service | 8008 | pay_db | `/api/payments/` |
| Ship Service | 8009 | ship_db | `/api/shipments/` |
| Comment & Rate Service | 8010 | comment_db | `/api/comments/` |
| Recommender AI Service | 8011 | recommend_db | `/api/recommendations/`, `/api/recommend/` |

---

## 🔗 Giao tiếp giữa các Services (Inter-service Communication)

```
Customer Service  ──POST /carts/──►  Cart Service      (Tự tạo giỏ hàng khi tạo customer)
Order Service     ──GET /carts/───►  Cart Service      (Lấy items trong giỏ hàng)
Order Service     ──GET /books/───►  Book Service      (Lấy giá sách)
Order Service     ──POST /payments/► Pay Service       (Tạo thanh toán tự động)
Order Service     ──POST /shipments/► Ship Service     (Tạo vận chuyển tự động)
Cart Item         ──GET /books/───►  Book Service      (Kiểm tra sách tồn tại)
Recommender AI    ──GET /books/───►  Book Service      (Lấy danh sách sách để gợi ý)
```

---

## 1. 👤 Customer Service

### 1.1 Lấy danh sách khách hàng
```
GET /api/customers/
```
**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "phone": "0901234567",
        "address": "Ha Noi",
        "created_at": "2026-03-09T10:00:00Z"
    }
]
```

### 1.2 Tạo khách hàng mới
```
POST /api/customers/
Content-Type: application/json
```
**Body:**
```json
{
    "name": "Nguyen Van A",
    "email": "a@gmail.com",
    "phone": "0901234567",
    "address": "Ha Noi"
}
```
**Response:** `201 Created`
> ⚡ **Side effect:** Tự động tạo Cart cho customer qua Cart Service.

### 1.3 Xem chi tiết khách hàng
```
GET /api/customers/{id}/
```
**Response:** `200 OK`

### 1.4 Cập nhật khách hàng
```
PUT /api/customers/{id}/
Content-Type: application/json
```
**Body:** (tất cả fields)
```json
{
    "name": "Nguyen Van B",
    "email": "b@gmail.com",
    "phone": "0909999999",
    "address": "HCM"
}
```

### 1.5 Cập nhật một phần
```
PATCH /api/customers/{id}/
Content-Type: application/json
```
**Body:** (chỉ field cần update)
```json
{
    "phone": "0908888888"
}
```

### 1.6 Xóa khách hàng
```
DELETE /api/customers/{id}/
```
**Response:** `204 No Content`

---

## 2. 👨‍💼 Staff Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| name | string | ✅ | max 255 |
| email | string | ✅ | unique |
| role | string | ❌ | default: "staff" |
| phone | string | ❌ | max 20 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/staffs/` | Danh sách staff |
| POST | `/api/staffs/` | Tạo staff |
| GET | `/api/staffs/{id}/` | Chi tiết staff |
| PUT | `/api/staffs/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/staffs/{id}/` | Cập nhật một phần |
| DELETE | `/api/staffs/{id}/` | Xóa staff |

**POST Body:**
```json
{
    "name": "Tran Thi B",
    "email": "staff_b@bookstore.com",
    "role": "cashier",
    "phone": "0912345678"
}
```

---

## 3. 👔 Manager Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| name | string | ✅ | max 255 |
| email | string | ✅ | unique |
| department | string | ❌ | max 100 |
| phone | string | ❌ | max 20 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/managers/` | Danh sách manager |
| POST | `/api/managers/` | Tạo manager |
| GET | `/api/managers/{id}/` | Chi tiết |
| PUT | `/api/managers/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/managers/{id}/` | Cập nhật một phần |
| DELETE | `/api/managers/{id}/` | Xóa |

**POST Body:**
```json
{
    "name": "Le Van C",
    "email": "manager_c@bookstore.com",
    "department": "Sales",
    "phone": "0923456789"
}
```

---

## 4. 📂 Catalog Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| name | string | ✅ | max 255 |
| description | string | ❌ | text |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/catalogs/` | Danh sách catalog |
| POST | `/api/catalogs/` | Tạo catalog |
| GET | `/api/catalogs/{id}/` | Chi tiết |
| PUT | `/api/catalogs/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/catalogs/{id}/` | Cập nhật một phần |
| DELETE | `/api/catalogs/{id}/` | Xóa |

**POST Body:**
```json
{
    "name": "Fiction",
    "description": "Sách tiểu thuyết, truyện"
}
```

---

## 5. 📖 Book Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| title | string | ✅ | max 255 |
| author | string | ✅ | max 255 |
| price | decimal | ✅ | max_digits=10, decimal_places=2 |
| stock | integer | ❌ | default: 0 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/books/` | Danh sách sách |
| POST | `/api/books/` | Tạo sách |
| GET | `/api/books/{id}/` | Chi tiết sách |
| PUT | `/api/books/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/books/{id}/` | Cập nhật một phần |
| DELETE | `/api/books/{id}/` | Xóa sách |

**POST Body:**
```json
{
    "title": "Dune",
    "author": "Frank Herbert",
    "price": "15.99",
    "stock": 50
}
```

---

## 6. 🛒 Cart Service

### Cart Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khách hàng |

### CartItem Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| cart | integer | ✅ | Cart ID (FK) |
| book_id | integer | ✅ | ID sách (sẽ verify qua Book Service) |
| quantity | integer | ❌ | default: 1 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/carts/` | Danh sách giỏ hàng |
| POST | `/api/carts/` | Tạo giỏ hàng |
| GET | `/api/carts/{id}/` | Chi tiết giỏ (kèm items) |
| GET | `/api/carts/customer/{customer_id}/` | ⭐ Lấy giỏ hàng theo Customer ID |
| GET | `/api/cart-items/` | Danh sách cart items |
| POST | `/api/cart-items/` | Thêm sách vào giỏ |
| GET | `/api/cart-items/{id}/` | Chi tiết item |
| PUT | `/api/cart-items/{id}/` | Cập nhật item |
| DELETE | `/api/cart-items/{id}/` | Xóa item khỏi giỏ |

**POST Cart Body:**
```json
{
    "customer_id": 1
}
```

**POST CartItem Body:**
```json
{
    "cart": 1,
    "book_id": 1,
    "quantity": 2
}
```
> ⚡ **Validation:** Khi thêm cart-item, service sẽ gọi Book Service kiểm tra sách tồn tại.

**GET /api/carts/{id}/ Response:**
```json
{
    "id": 1,
    "customer_id": 1,
    "items": [
        {
            "id": 1,
            "cart": 1,
            "book_id": 1,
            "quantity": 2
        }
    ],
    "created_at": "2026-03-09T10:00:00Z"
}
```

---

## 7. 📦 Order Service

### Order Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khách hàng |
| total_amount | decimal | auto | Tính tự động |
| status | string | auto | pending/paid/shipped/delivered/cancelled |

### OrderItem Fields
| Field | Type | Note |
|-------|------|------|
| order | integer | Order ID (FK) |
| book_id | integer | ID sách |
| quantity | integer | Số lượng |
| price | decimal | Giá tại thời điểm đặt |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/orders/` | Danh sách đơn hàng |
| POST | `/api/orders/` | ⭐ Tạo đơn hàng từ giỏ hàng |
| GET | `/api/orders/{id}/` | Chi tiết đơn (kèm items) |
| PUT | `/api/orders/{id}/` | Cập nhật đơn |
| PATCH | `/api/orders/{id}/` | Cập nhật trạng thái |
| DELETE | `/api/orders/{id}/` | Xóa đơn |
| GET | `/api/order-items/` | Danh sách order items |

**POST Order Body:**
```json
{
    "customer_id": 1,
    "address": "123 Nguyen Hue, HCM"
}
```

> ⚡ **Workflow khi tạo Order:**
> 1. Lấy giỏ hàng của customer từ Cart Service
> 2. Lấy giá sách từ Book Service cho mỗi item
> 3. Tính tổng tiền, tạo Order + OrderItems
> 4. Gọi Pay Service tạo Payment tự động
> 5. Gọi Ship Service tạo Shipment tự động

**Response:**
```json
{
    "id": 1,
    "customer_id": 1,
    "total_amount": "31.98",
    "status": "pending",
    "items": [
        {
            "id": 1,
            "order": 1,
            "book_id": 1,
            "quantity": 2,
            "price": "15.99"
        }
    ],
    "created_at": "2026-03-09T10:30:00Z"
}
```

---

## 8. 💳 Payment Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| order_id | integer | ✅ | ID đơn hàng |
| amount | decimal | ✅ | Số tiền |
| method | string | ❌ | `cash` / `credit_card` / `bank_transfer` (default: cash) |
| status | string | ❌ | `pending` / `completed` / `failed` (default: pending) |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/payments/` | Danh sách thanh toán |
| POST | `/api/payments/` | Tạo thanh toán |
| GET | `/api/payments/{id}/` | Chi tiết |
| PUT | `/api/payments/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/payments/{id}/` | Cập nhật trạng thái |
| DELETE | `/api/payments/{id}/` | Xóa |

**POST Body:**
```json
{
    "order_id": 1,
    "amount": "31.98",
    "method": "credit_card",
    "status": "pending"
}
```

**PATCH (cập nhật trạng thái):**
```json
{
    "status": "completed"
}
```

---

## 9. 🚚 Shipment Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| order_id | integer | ✅ | ID đơn hàng |
| address | string | ✅ | Địa chỉ giao |
| status | string | ❌ | `preparing` / `shipped` / `in_transit` / `delivered` |
| tracking_number | string | ❌ | Mã vận đơn |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/shipments/` | Danh sách vận chuyển |
| POST | `/api/shipments/` | Tạo vận chuyển |
| GET | `/api/shipments/{id}/` | Chi tiết |
| PUT | `/api/shipments/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/shipments/{id}/` | Cập nhật trạng thái |
| DELETE | `/api/shipments/{id}/` | Xóa |

**POST Body:**
```json
{
    "order_id": 1,
    "address": "123 Nguyen Hue, HCM",
    "tracking_number": "VN123456789"
}
```

**PATCH (cập nhật trạng thái):**
```json
{
    "status": "shipped"
}
```

---

## 10. ⭐ Comment & Rate Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khách hàng |
| book_id | integer | ✅ | ID sách |
| content | string | ✅ | Nội dung bình luận |
| rating | integer | ❌ | 1-5, default: 5 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/comments/` | Danh sách bình luận |
| POST | `/api/comments/` | Tạo bình luận |
| GET | `/api/comments/{id}/` | Chi tiết |
| PUT | `/api/comments/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/comments/{id}/` | Cập nhật một phần |
| DELETE | `/api/comments/{id}/` | Xóa |

**POST Body:**
```json
{
    "customer_id": 1,
    "book_id": 1,
    "content": "Sách rất hay, nội dung hấp dẫn!",
    "rating": 5
}
```

---

## 11. 🤖 Recommender AI Service

### Recommendation Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khách hàng |
| book_id | integer | ✅ | ID sách |
| score | float | ❌ | 0.0-1.0, default: 0.0 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/recommend/` | ⭐ Gợi ý sách ngẫu nhiên (max 5 cuốn) |
| GET | `/api/recommendations/` | Danh sách recommendations đã lưu |
| POST | `/api/recommendations/` | Lưu recommendation |
| GET | `/api/recommendations/{id}/` | Chi tiết |
| DELETE | `/api/recommendations/{id}/` | Xóa |

**GET /api/recommend/ Response:**
```json
{
    "recommended_books": [
        {
            "id": 1,
            "title": "Dune",
            "author": "Frank Herbert",
            "price": "15.99",
            "stock": 50
        },
        {
            "id": 3,
            "title": "1984",
            "author": "George Orwell",
            "price": "12.50",
            "stock": 30
        }
    ]
}
```

**POST Recommendation Body:**
```json
{
    "customer_id": 1,
    "book_id": 1,
    "score": 0.95
}
```

---

## 🔥 Luồng nghiệp vụ chính (Business Flow)

```
1. Tạo Customer    POST /api/customers/        → Auto tạo Cart
2. Thêm Sách       POST /api/books/            → Nhập kho sách
3. Thêm vào Giỏ    POST /api/cart-items/        → Chọn sách vào giỏ
4. Đặt hàng        POST /api/orders/            → Tạo Order + Payment + Shipment
5. Thanh toán       PATCH /api/payments/{id}/    → Cập nhật status = completed
6. Vận chuyển       PATCH /api/shipments/{id}/   → Cập nhật status = delivered
7. Đánh giá         POST /api/comments/          → Khách đánh giá sách
8. Gợi ý           GET /api/recommend/           → AI gợi ý sách
```

---

## ⚠️ Error Responses

| Status | Ý nghĩa |
|--------|---------|
| 400 | Bad Request - Dữ liệu không hợp lệ |
| 404 | Not Found - Không tìm thấy resource |
| 503 | Service Unavailable - Không kết nối được service |
| 504 | Gateway Timeout - Service phản hồi quá lâu |

```json
{
    "error": "Cart not found"
}
```

```json
{
    "email": ["This field must be unique."]
}
```
