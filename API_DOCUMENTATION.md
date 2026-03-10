# 📚 BookStore Microservices - API Documentation

> **Base URL:** `http://localhost:8000/api`
>
> Tất cả request đều đi qua **API Gateway** (port 8000), gateway sẽ proxy tới service tương ứng.
> Tất cả API endpoints (trừ Auth login/register/refresh) đều yêu cầu **JWT Bearer Token** trong header.

---

## 📐 Kiến trúc tổng quan

```
Client  →  API Gateway (:8000)  →  JWT Middleware  →  Microservices (:8001-8012)  →  MySQL (:3306)
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
| **Auth Service** | **8012** | **auth_db** | **`/api/auth/`** |

---

## 🔐 Authentication (JWT)

Hệ thống sử dụng **JWT (JSON Web Token)** với thuật toán **HS256** để xác thực và phân quyền.

### Authentication Flow

```
1. Client gửi POST /api/auth/login/ {username, password}
2. Auth Service xác thực → Trả về {access_token, refresh_token}
3. Client lưu tokens vào localStorage
4. Mọi API request gửi kèm header: Authorization: Bearer <access_token>
5. JWT Middleware tại Gateway:
   a) Decode token (HS256, secret key)
   b) Kiểm tra token type = 'access' và chưa hết hạn
   c) Kiểm tra role có đủ quyền cho endpoint + HTTP method
   d) Nếu OK → proxy request đến backend service
   e) Nếu FAIL → trả 401 (Unauthorized) hoặc 403 (Forbidden)
6. Khi access_token hết hạn → POST /api/auth/refresh/ với refresh_token
```

### Vai trò & Phân quyền (RBAC)

| Role | Quyền hạn |
|------|-----------|
| **admin** | Toàn quyền trên mọi resource, quản lý users, gán vai trò |
| **manager** | Đọc/ghi hầu hết resources, xem users, không gán vai trò |
| **staff** | Đọc/ghi sách, đơn hàng, khách hàng; không quản lý managers |
| **customer** | Đọc sách/catalog, tạo đơn hàng, bình luận, xem thông tin cá nhân |

### Ma trận phân quyền chi tiết

| Resource | Admin | Manager | Staff | Customer |
|----------|-------|---------|-------|----------|
| Auth Users (GET) | ✅ | ✅ | ❌ | ❌ |
| Assign Role | ✅ | ❌ | ❌ | ❌ |
| Staffs (CRUD) | ✅ Full | ✅ R/W | ✅ Read | ❌ |
| Managers (CRUD) | ✅ Full | ✅ Read | ❌ | ❌ |
| Books (CRUD) | ✅ Full | ✅ R/W/Del | ✅ R/W | ✅ Read |
| Catalogs (CRUD) | ✅ Full | ✅ R/W/Del | ✅ R/W | ✅ Read |
| Customers (CRUD) | ✅ Full | ✅ R/W/Del | ✅ R/W | ✅ R/W |
| Orders (CRUD) | ✅ Full | ✅ R/W | ✅ R/W | ✅ Read/Create |
| Payments | ✅ Full | ✅ R/W | ✅ R/W | ✅ Read/Create |
| Comments (CRUD) | ✅ Full | ✅ Full | ✅ Full | ✅ Full |

### Tài khoản mặc định (Seed Accounts)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| staff1 | staff123 | staff |
| staff2 | staff123 | staff |
| manager1 | manager123 | manager |
| manager2 | manager123 | manager |

---

## 🔗 Giao tiếp giữa các Services (Inter-service Communication)

```
Gateway           ──JWT verify──────►  Auth Service       (Xác thực token mỗi request)
Customer Service  ──POST /carts/────►  Cart Service       (Tự tạo giỏ hàng khi tạo customer)
Order Service     ──GET /carts/─────►  Cart Service       (Lấy items trong giỏ hàng)
Order Service     ──GET /books/─────►  Book Service       (Lấy giá sách)
Order Service     ──POST /payments/─►  Pay Service        (Tạo thanh toán tự động)
Order Service     ──POST /shipments/►  Ship Service       (Tạo vận chuyển tự động)
Cart Item         ──GET /books/─────►  Book Service       (Kiểm tra sách tồn tại)
Recommender AI    ──GET /books/─────►  Book Service       (Lấy danh sách sách để gợi ý)
```

---

## 0. 🔐 Auth Service

### User Model
| Field | Type | Required | Note |
|-------|------|----------|------|
| username | string | ✅ | max 150, unique |
| email | string | ✅ | unique |
| password | string | ✅ | Hashed SHA-256 + salt |
| full_name | string | ✅ | max 255 |
| role | string | ❌ | `admin` / `manager` / `staff` / `customer` (default: customer) |
| is_active | boolean | ❌ | default: true |

### Endpoints

| Method | URL | Auth | Mô tả |
|--------|-----|------|--------|
| POST | `/api/auth/register/` | ❌ | Đăng ký tài khoản mới |
| POST | `/api/auth/login/` | ❌ | Đăng nhập, trả JWT tokens |
| POST | `/api/auth/refresh/` | ❌ | Refresh access token |
| POST | `/api/auth/verify/` | ❌ | Xác thực token hợp lệ |
| GET | `/api/auth/me/` | ✅ | Thông tin user hiện tại |
| POST | `/api/auth/change-password/` | ✅ | Đổi mật khẩu |
| POST | `/api/auth/assign-role/` | ✅ Admin | Gán vai trò cho user |
| GET | `/api/auth/users/` | ✅ Admin/Manager | Danh sách tất cả users |
| POST | `/api/auth/users/{id}/deactivate/` | ✅ Admin | Vô hiệu hóa user |
| POST | `/api/auth/users/{id}/reset-password/` | ✅ Admin | Reset mật khẩu user |

### Đăng ký
```
POST /api/auth/register/
Content-Type: application/json
```
**Body:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword",
    "full_name": "Nguyen Van A"
}
```
**Response:** `201 Created`
```json
{
    "message": "Registration successful",
    "user": {
        "id": 6,
        "username": "newuser",
        "email": "newuser@example.com",
        "full_name": "Nguyen Van A",
        "role": "customer",
        "is_active": true
    }
}
```

### Đăng nhập
```
POST /api/auth/login/
Content-Type: application/json
```
**Body:**
```json
{
    "username": "admin",
    "password": "admin123"
}
```
**Response:** `200 OK`
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@bookstore.com",
        "full_name": "Administrator",
        "role": "admin",
        "is_active": true
    },
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Refresh Token
```
POST /api/auth/refresh/
Content-Type: application/json
```
**Body:**
```json
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```
**Response:** `200 OK`
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...(new)"
}
```

### Gán vai trò (Admin only)
```
POST /api/auth/assign-role/
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```
**Body:**
```json
{
    "user_id": 6,
    "role": "staff"
}
```

---

## 1. 👤 Customer Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| full_name | string | ✅ | max 255 |
| email | string | ✅ | unique |
| phone | string | ❌ | max 20 |
| job | string | ❌ | max 255, nghề nghiệp |
| street | string | ❌ | max 500, địa chỉ đường |
| city | string | ❌ | max 255, thành phố |
| state | string | ❌ | max 255, tỉnh/bang |
| zip_code | string | ❌ | max 20, mã bưu chính |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/customers/` | Danh sách khách hàng |
| POST | `/api/customers/` | Tạo khách hàng mới |
| GET | `/api/customers/{id}/` | Chi tiết khách hàng |
| PUT | `/api/customers/{id}/` | Cập nhật toàn bộ |
| PATCH | `/api/customers/{id}/` | Cập nhật một phần |
| DELETE | `/api/customers/{id}/` | Xóa khách hàng |

### 1.1 Lấy danh sách khách hàng
```
GET /api/customers/
Authorization: Bearer <access_token>
```
**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "full_name": "Nguyen Van A",
        "email": "a@gmail.com",
        "phone": "0901234567",
        "job": "Engineer",
        "street": "123 Nguyen Hue",
        "city": "Ho Chi Minh",
        "state": "HCM",
        "zip_code": "70000",
        "created_at": "2026-03-09T10:00:00Z",
        "updated_at": "2026-03-09T10:00:00Z"
    }
]
```

### 1.2 Tạo khách hàng mới
```
POST /api/customers/
Authorization: Bearer <access_token>
Content-Type: application/json
```
**Body:**
```json
{
    "full_name": "Nguyen Van A",
    "email": "a@gmail.com",
    "phone": "0901234567",
    "job": "Engineer",
    "street": "123 Nguyen Hue",
    "city": "Ho Chi Minh",
    "state": "HCM",
    "zip_code": "70000"
}
```
**Response:** `201 Created`

> ⚡ **Side effect:** Tự động tạo Cart cho customer qua Cart Service.

### 1.3 Xem chi tiết khách hàng
```
GET /api/customers/{id}/
Authorization: Bearer <access_token>
```
**Response:** `200 OK`

### 1.4 Cập nhật khách hàng
```
PUT /api/customers/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```
**Body:** (tất cả fields)
```json
{
    "full_name": "Nguyen Van B",
    "email": "b@gmail.com",
    "phone": "0909999999",
    "job": "Designer",
    "street": "456 Le Loi",
    "city": "Ha Noi",
    "state": "HN",
    "zip_code": "10000"
}
```

### 1.5 Cập nhật một phần
```
PATCH /api/customers/{id}/
Authorization: Bearer <access_token>
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
Authorization: Bearer <access_token>
```
**Response:** `204 No Content`

> 🔒 **Auth:** Admin full, Manager R/W/Del, Staff R/W, Customer R/W own.

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

> 🔒 **Auth:** Admin full access, Manager read/write, Staff read only, Customer no access.

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

> 🔒 **Auth:** Admin full access, Manager read only, Staff/Customer no access.

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
    "description": "Sach tieu thuyet, truyen"
}
```

> 🔒 **Auth:** Admin/Manager/Staff can create/edit, Customer read only.

---

## 5. 📖 Book Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| title | string | ✅ | max 255 |
| author | string | ✅ | max 255 |
| price | decimal | ✅ | max_digits=10, decimal_places=2 |
| stock | integer | ❌ | default: 0 |
| catalog_id | integer | ❌ | ID danh muc (cross-service ref, nullable) |
| image_url | string | ❌ | URL anh bia sach (max 500, default: "") |

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
    "stock": 50,
    "catalog_id": 1,
    "image_url": "https://covers.openlibrary.org/b/id/12345-L.jpg"
}
```

**Response:**
```json
{
    "id": 1,
    "title": "Dune",
    "author": "Frank Herbert",
    "price": "15.99",
    "stock": 50,
    "catalog_id": 1,
    "image_url": "https://covers.openlibrary.org/b/id/12345-L.jpg",
    "created_at": "2026-03-09T10:00:00Z"
}
```

> 🔒 **Auth:** Admin/Manager can delete, Admin/Manager/Staff can create/edit, Customer read only.

---

## 6. 🛒 Cart Service

### Cart Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khach hang (unique) |

### CartItem Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| cart | integer | ✅ | Cart ID (FK) |
| book_id | integer | ✅ | ID sach (se verify qua Book Service) |
| quantity | integer | ❌ | default: 1 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/carts/` | Danh sach gio hang |
| POST | `/api/carts/` | Tao gio hang |
| GET | `/api/carts/{id}/` | Chi tiet gio (kem items) |
| GET | `/api/carts/customer/{customer_id}/` | ⭐ Lay gio hang theo Customer ID |
| GET | `/api/cart-items/` | Danh sach cart items |
| POST | `/api/cart-items/` | Them sach vao gio |
| GET | `/api/cart-items/{id}/` | Chi tiet item |
| PUT | `/api/cart-items/{id}/` | Cap nhat item |
| DELETE | `/api/cart-items/{id}/` | Xoa item khoi gio |

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
> ⚡ **Validation:** Khi them cart-item, service se goi Book Service kiem tra sach ton tai.

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
| customer_id | integer | ✅ | ID khach hang |
| total_amount | decimal | auto | Tinh tu dong |
| status | string | auto | pending/paid/shipped/delivered/cancelled |

### OrderItem Fields
| Field | Type | Note |
|-------|------|------|
| order | integer | Order ID (FK) |
| book_id | integer | ID sach |
| quantity | integer | So luong |
| price | decimal | Gia tai thoi diem dat |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/orders/` | Danh sach don hang |
| POST | `/api/orders/` | ⭐ Tao don hang tu gio hang |
| GET | `/api/orders/{id}/` | Chi tiet don (kem items) |
| PUT | `/api/orders/{id}/` | Cap nhat don |
| PATCH | `/api/orders/{id}/` | Cap nhat trang thai |
| DELETE | `/api/orders/{id}/` | Xoa don |
| GET | `/api/order-items/` | Danh sach order items |

**POST Order Body:**
```json
{
    "customer_id": 1
}
```

> ⚡ **Workflow khi tao Order:**
> 1. Lay gio hang cua customer tu Cart Service
> 2. Lay gia sach tu Book Service cho moi item
> 3. Tinh tong tien, tao Order + OrderItems
> 4. Goi Pay Service tao Payment tu dong
> 5. Goi Ship Service tao Shipment tu dong

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

> 🔒 **Auth:** Admin/Manager/Staff full CRUD, Customer can read own orders and create.

---

## 8. 💳 Payment Service

### Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| order_id | integer | ✅ | ID don hang |
| amount | decimal | ✅ | So tien |
| method | string | ❌ | `cash` / `credit_card` / `bank_transfer` (default: cash) |
| status | string | ❌ | `pending` / `completed` / `failed` (default: pending) |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/payments/` | Danh sach thanh toan |
| POST | `/api/payments/` | Tao thanh toan |
| GET | `/api/payments/{id}/` | Chi tiet |
| PUT | `/api/payments/{id}/` | Cap nhat toan bo |
| PATCH | `/api/payments/{id}/` | Cap nhat trang thai |
| DELETE | `/api/payments/{id}/` | Xoa |

**POST Body:**
```json
{
    "order_id": 1,
    "amount": "31.98",
    "method": "credit_card",
    "status": "pending"
}
```

**PATCH (cap nhat trang thai):**
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
| order_id | integer | ✅ | ID don hang |
| address | string | ✅ | Dia chi giao |
| status | string | ❌ | `preparing` / `shipped` / `in_transit` / `delivered` |
| tracking_number | string | ❌ | Ma van don |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/shipments/` | Danh sach van chuyen |
| POST | `/api/shipments/` | Tao van chuyen |
| GET | `/api/shipments/{id}/` | Chi tiet |
| PUT | `/api/shipments/{id}/` | Cap nhat toan bo |
| PATCH | `/api/shipments/{id}/` | Cap nhat trang thai |
| DELETE | `/api/shipments/{id}/` | Xoa |

**POST Body:**
```json
{
    "order_id": 1,
    "address": "123 Nguyen Hue, HCM",
    "tracking_number": "VN123456789"
}
```

**PATCH (cap nhat trang thai):**
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
| customer_id | integer | ✅ | ID khach hang |
| book_id | integer | ✅ | ID sach |
| content | string | ✅ | Noi dung binh luan |
| rating | integer | ❌ | 1-5, default: 5 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/comments/` | Danh sach binh luan |
| POST | `/api/comments/` | Tao binh luan |
| GET | `/api/comments/{id}/` | Chi tiet |
| PUT | `/api/comments/{id}/` | Cap nhat toan bo |
| PATCH | `/api/comments/{id}/` | Cap nhat mot phan |
| DELETE | `/api/comments/{id}/` | Xoa |

**POST Body:**
```json
{
    "customer_id": 1,
    "book_id": 1,
    "content": "Sach rat hay, noi dung hap dan!",
    "rating": 5
}
```

> 🔒 **Auth:** All roles have full access to comments.

---

## 11. 🤖 Recommender AI Service

### Recommendation Fields
| Field | Type | Required | Note |
|-------|------|----------|------|
| customer_id | integer | ✅ | ID khach hang |
| book_id | integer | ✅ | ID sach |
| score | float | ❌ | 0.0-1.0, default: 0.0 |

### Endpoints
| Method | URL | Mô tả |
|--------|-----|--------|
| GET | `/api/recommend/` | ⭐ Goi y sach ngau nhien (max 5 cuon) |
| GET | `/api/recommendations/` | Danh sach recommendations da luu |
| POST | `/api/recommendations/` | Luu recommendation |
| GET | `/api/recommendations/{id}/` | Chi tiet |
| DELETE | `/api/recommendations/{id}/` | Xoa |

**GET /api/recommend/ Response:**
```json
{
    "recommended_books": [
        {
            "id": 1,
            "title": "Dune",
            "author": "Frank Herbert",
            "price": "15.99",
            "stock": 50,
            "catalog_id": 1,
            "image_url": "https://covers.openlibrary.org/b/id/12345-L.jpg"
        },
        {
            "id": 3,
            "title": "1984",
            "author": "George Orwell",
            "price": "12.50",
            "stock": 30,
            "catalog_id": 1,
            "image_url": ""
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

## 🔥 Luong nghiep vu chinh (Business Flow)

```
0. Dang nhap       POST /api/auth/login/        -> Nhan JWT tokens -> Luu localStorage
1. Tao Customer    POST /api/customers/          -> Auto tao Cart
2. Them Sach       POST /api/books/              -> Nhap kho sach (voi catalog_id + image_url)
3. Them vao Gio    POST /api/cart-items/         -> Chon sach vao gio (verify book exists)
4. Dat hang        POST /api/orders/             -> Tao Order + Payment + Shipment
5. Thanh toan      PATCH /api/payments/{id}/     -> Cap nhat status = completed
6. Van chuyen      PATCH /api/shipments/{id}/    -> Cap nhat status = delivered
7. Danh gia        POST /api/comments/           -> Khach danh gia sach (1-5 sao)
8. Goi y           GET /api/recommend/           -> AI goi y sach
```

---

## ⚠️ Error Responses

| Status | Y nghia |
|--------|---------|
| 400 | Bad Request - Du lieu khong hop le |
| 401 | Unauthorized - Token khong hop le hoac het han |
| 403 | Forbidden - Khong du quyen (role khong phu hop) |
| 404 | Not Found - Khong tim thay resource |
| 503 | Service Unavailable - Khong ket noi duoc service |
| 504 | Gateway Timeout - Service phan hoi qua lau |

**Token het han:**
```json
{
    "error": "Token has expired"
}
```

**Khong du quyen:**
```json
{
    "error": "Forbidden: insufficient role permissions"
}
```

**Du lieu khong hop le:**
```json
{
    "email": ["This field must be unique."]
}
```

**Service khong kha dung:**
```json
{
    "error": "Cart not found"
}
```
