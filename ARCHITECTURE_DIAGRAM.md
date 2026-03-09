# 📐 BookStore Microservices — Architecture Diagram

---

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph Client["🌐 Client Layer"]
        Browser["🖥️ Web Browser"]
        Postman["🧪 Postman"]
    end

    subgraph Gateway["⚡ API Gateway — port 8000"]
        GW["Django API Gateway<br/>SQLite<br/>Proxy + Static Pages"]
    end

    subgraph Services["🔧 Microservices Layer"]
        direction TB
        subgraph People["👥 People Management"]
            CS["👤 Customer Service<br/>:8001"]
            SS["👨‍💼 Staff Service<br/>:8002"]
            MS["👔 Manager Service<br/>:8003"]
        end
        subgraph Product["📦 Product Management"]
            CAS["📂 Catalog Service<br/>:8004"]
            BS["📖 Book Service<br/>:8005"]
        end
        subgraph Shopping["🛒 Shopping Flow"]
            CRS["🛒 Cart Service<br/>:8006"]
            OS["📦 Order Service<br/>:8007"]
        end
        subgraph Fulfillment["💰 Fulfillment"]
            PS["💳 Payment Service<br/>:8008"]
            SHS["🚚 Shipment Service<br/>:8009"]
        end
        subgraph Engagement["⭐ Engagement"]
            CMS["💬 Comment Service<br/>:8010"]
            RS["🤖 Recommender Service<br/>:8011"]
        end
    end

    subgraph Database["🗄️ MySQL 8.0 — port 3307"]
        DB[(MySQL Server)]
    end

    Browser -->|"HTTP :8000"| GW
    Postman -->|"HTTP :8000"| GW

    GW -->|"/api/customers/*"| CS
    GW -->|"/api/staffs/*"| SS
    GW -->|"/api/managers/*"| MS
    GW -->|"/api/catalogs/*"| CAS
    GW -->|"/api/books/*"| BS
    GW -->|"/api/carts/*"| CRS
    GW -->|"/api/orders/*"| OS
    GW -->|"/api/payments/*"| PS
    GW -->|"/api/shipments/*"| SHS
    GW -->|"/api/comments/*"| CMS
    GW -->|"/api/recommend/*"| RS

    CS --> DB
    SS --> DB
    MS --> DB
    CAS --> DB
    BS --> DB
    CRS --> DB
    OS --> DB
    PS --> DB
    SHS --> DB
    CMS --> DB
    RS --> DB
```

---

## 2. Inter-Service Communication

```mermaid
graph LR
    subgraph Gateway
        GW["⚡ API Gateway<br/>:8000"]
    end

    CS["👤 Customer<br/>:8001"]
    BS["📖 Book<br/>:8005"]
    CRS["🛒 Cart<br/>:8006"]
    OS["📦 Order<br/>:8007"]
    PS["💳 Payment<br/>:8008"]
    SHS["🚚 Shipment<br/>:8009"]
    RS["🤖 Recommender<br/>:8011"]

    CS -- "① POST /carts/<br/>auto-create cart" --> CRS
    CRS -- "② GET /books/{id}<br/>verify book exists" --> BS

    OS -- "③ GET /carts/customer/{id}<br/>fetch cart items" --> CRS
    OS -- "④ GET /books/{id}<br/>fetch book price" --> BS
    OS -- "⑤ POST /payments/<br/>create payment" --> PS
    OS -- "⑥ POST /shipments/<br/>create shipment" --> SHS

    RS -- "⑦ GET /books/<br/>fetch all books" --> BS

    style CS fill:#e1f5fe
    style BS fill:#fff3e0
    style CRS fill:#e8f5e9
    style OS fill:#fce4ec
    style PS fill:#f3e5f5
    style SHS fill:#fff8e1
    style RS fill:#e0f2f1
```

---

## 3. Database Architecture (Database per Service)

```mermaid
graph TB
    subgraph MySQL["🗄️ MySQL 8.0 Server (port 3307)"]
        direction LR
        DB1[(customer_db)]
        DB2[(staff_db)]
        DB3[(manager_db)]
        DB4[(catalog_db)]
        DB5[(book_db)]
        DB6[(cart_db)]
        DB7[(order_db)]
        DB8[(pay_db)]
        DB9[(ship_db)]
        DB10[(comment_db)]
        DB11[(recommend_db)]
    end

    CS["👤 Customer :8001"] --> DB1
    SS["👨‍💼 Staff :8002"] --> DB2
    MS["👔 Manager :8003"] --> DB3
    CAS["📂 Catalog :8004"] --> DB4
    BS["📖 Book :8005"] --> DB5
    CRS["🛒 Cart :8006"] --> DB6
    OS["📦 Order :8007"] --> DB7
    PS["💳 Payment :8008"] --> DB8
    SHS["🚚 Shipment :8009"] --> DB9
    CMS["💬 Comment :8010"] --> DB10
    RS["🤖 Recommender :8011"] --> DB11
```

---

## 4. Docker Network Topology

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            Docker Network: bookstore-net                                 │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                         🌐  API Gateway (api-gateway:8000)                          │  │
│  │                         Django 4.2 + SQLite + HTML Templates                        │  │
│  │                         Exposed → localhost:8000                                     │  │
│  └────────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬────┘  │
│           │       │       │       │       │       │       │       │       │       │       │
│    ┌──────▼──┐┌───▼───┐┌──▼────┐┌─▼─────┐┌▼──────┐┌▼─────┐┌▼─────┐┌▼─────┐┌▼─────┐┌▼───┐│
│    │Customer ││ Staff ││Manager││Catalog││ Book  ││ Cart ││Order ││ Pay  ││ Ship ││Comm││
│    │ :8001   ││ :8002 ││ :8003 ││ :8004 ││ :8005 ││ :8006││ :8007││ :8008││ :8009││entd││
│    └───┬─────┘└──┬────┘└──┬────┘└──┬────┘└──┬────┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬─┘│
│        │         │        │        │        │        │       │       │       │       │   │
│  ┌─────▼─────────▼────────▼────────▼────────▼────────▼───────▼───────▼───────▼───────▼─┐ │
│  │                        🗄️  MySQL 8.0 (mysql:3306)                                   │ │
│  │                        Exposed → localhost:3307                                      │ │
│  │    11 databases: customer_db | staff_db | manager_db | catalog_db | book_db          │ │
│  │                   cart_db | order_db | pay_db | ship_db | comment_db | recommend_db  │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  ┌──────────────────────┐                                                                │
│  │ 🤖 Recommender :8011 │  (also on same network)                                       │
│  └──────────────────────┘                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Request Flow — Order Creation (Business Workflow)

```mermaid
sequenceDiagram
    participant C as 🖥️ Client
    participant GW as ⚡ Gateway :8000
    participant OS as 📦 Order :8007
    participant CRS as 🛒 Cart :8006
    participant BS as 📖 Book :8005
    participant PS as 💳 Payment :8008
    participant SHS as 🚚 Shipment :8009

    C->>GW: POST /api/orders/<br/>{customer_id, address}
    GW->>OS: Proxy → POST /orders/

    Note over OS: Step 1: Fetch Cart
    OS->>CRS: GET /carts/customer/{customer_id}/
    CRS-->>OS: {id, customer_id, items: [{book_id, qty}]}

    Note over OS: Step 2: Get Book Prices
    loop For each cart item
        OS->>BS: GET /books/{book_id}/
        BS-->>OS: {id, title, price, stock}
    end

    Note over OS: Step 3: Calculate & Save
    OS->>OS: total = Σ(price × qty)<br/>Create Order + OrderItems

    Note over OS: Step 4: Create Payment
    OS->>PS: POST /payments/<br/>{order_id, amount, method}
    PS-->>OS: {id, status: "pending"}

    Note over OS: Step 5: Create Shipment
    OS->>SHS: POST /shipments/<br/>{order_id, address}
    SHS-->>OS: {id, status: "processing"}

    OS-->>GW: 201 {order + items}
    GW-->>C: 201 Created
```

---

## 6. Customer Registration Flow

```mermaid
sequenceDiagram
    participant C as 🖥️ Client
    participant GW as ⚡ Gateway :8000
    participant CS as 👤 Customer :8001
    participant CRS as 🛒 Cart :8006

    C->>GW: POST /api/customers/<br/>{name, email, phone, address}
    GW->>CS: Proxy → POST /customers/
    CS->>CS: Save customer to DB

    Note over CS: Auto-create empty cart
    CS->>CRS: POST /carts/<br/>{customer_id: new_id}
    CRS-->>CS: {id, customer_id}

    CS-->>GW: 201 {customer data}
    GW-->>C: 201 Created
```

---

## 7. Technology Stack

```
┌────────────────────────────────────────────────────────────────────┐
│                      🏗️  TECHNOLOGY STACK                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │   Frontend    │  │  API Gateway │  │      Backend (×11)       │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────────────────┤ │
│  │ HTML5 / CSS3 │  │ Django 4.2   │  │ Django 4.2               │ │
│  │ Bootstrap 5  │  │ SQLite       │  │ Django REST Framework    │ │
│  │ JavaScript   │  │ Requests lib │  │ 3.15.1                   │ │
│  │ Fetch API    │  │ URL Proxy    │  │ MySQL 8.0                │ │
│  └──────────────┘  └──────────────┘  │ mysqlclient              │ │
│                                       └──────────────────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │Infrastructure│  │   Language   │  │       Pattern            │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────────────────┤ │
│  │ Docker       │  │ Python 3.11  │  │ API Gateway Pattern      │ │
│  │ Docker       │  │              │  │ Database per Service     │ │
│  │  Compose     │  │              │  │ Synchronous REST calls   │ │
│  │ MySQL 8.0    │  │              │  │ Service Orchestration    │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## 8. Port Mapping Summary

| Service | Container Name | Internal Port | External Port | Database |
|---------|---------------|---------------|---------------|----------|
| MySQL | mysql | 3306 | **3307** | — |
| API Gateway | api-gateway | 8000 | **8000** | SQLite |
| Customer | customer-service | 8001 | 8001 | customer_db |
| Staff | staff-service | 8002 | 8002 | staff_db |
| Manager | manager-service | 8003 | 8003 | manager_db |
| Catalog | catalog-service | 8004 | 8004 | catalog_db |
| Book | book-service | 8005 | 8005 | book_db |
| Cart | cart-service | 8006 | 8006 | cart_db |
| Order | order-service | 8007 | 8007 | order_db |
| Payment | pay-service | 8008 | 8008 | pay_db |
| Shipment | ship-service | 8009 | 8009 | ship_db |
| Comment | comment-service | 8010 | 8010 | comment_db |
| Recommender | recommender-service | 8011 | 8011 | recommend_db |

---

## 9. Service Routing Table (Gateway)

```
Client Request                      →  Gateway Proxy Target
─────────────────────────────────────────────────────────────
/api/customers/*                    →  http://customer-service:8001/customers/*
/api/staffs/*                       →  http://staff-service:8002/staffs/*
/api/managers/*                     →  http://manager-service:8003/managers/*
/api/catalogs/*                     →  http://catalog-service:8004/catalogs/*
/api/books/*                        →  http://book-service:8005/books/*
/api/carts/*                        →  http://cart-service:8006/carts/*
/api/cart-items/*                   →  http://cart-service:8006/cart-items/*
/api/orders/*                       →  http://order-service:8007/orders/*
/api/order-items/*                  →  http://order-service:8007/order-items/*
/api/payments/*                     →  http://pay-service:8008/payments/*
/api/shipments/*                    →  http://ship-service:8009/shipments/*
/api/comments/*                     →  http://comment-service:8010/comments/*
/api/recommendations/*              →  http://recommender-service:8011/recommendations/*
/api/recommend/*                    →  http://recommender-service:8011/recommend/*
```

---

> 💡 **Tip**: Các Mermaid diagram có thể xem trực tiếp trên **GitHub**, **GitLab**, hoặc dùng [Mermaid Live Editor](https://mermaid.live) để render.
