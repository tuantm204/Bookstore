#!/usr/bin/env python3
"""Write polished orders.html with bug fix and professional UI."""
import os

BASE = '/Users/truongmanhtuan/django_project/assgn05v1/bookstore-micro05/api-gateway/templates'

orders_html = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Đơn hàng - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:#f1f5f9;color:#1e293b;display:flex;min-height:100vh}
a{text-decoration:none;color:inherit}

/* Sidebar */
.sidebar{width:260px;background:#0f172a;color:#94a3b8;display:flex;flex-direction:column;position:fixed;top:0;left:0;bottom:0;z-index:100}
.sidebar-brand{padding:20px 24px;display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;color:#fff;border-bottom:1px solid #1e293b}
.sidebar-brand i{color:#3b82f6}
.sidebar-menu{flex:1;padding:16px 12px;overflow-y:auto}
.menu-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:16px 12px 8px;color:#475569}
.menu-item{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:8px;font-size:14px;color:#94a3b8;transition:all .2s;margin-bottom:2px}
.menu-item:hover{background:#1e293b;color:#e2e8f0}
.menu-item.active{background:#1d4ed8;color:#fff}
.menu-item i{width:20px;text-align:center}
.sidebar-footer{padding:16px;border-top:1px solid #1e293b}
.user-card{display:flex;align-items:center;gap:10px;padding:8px}
.user-avatar{width:36px;height:36px;border-radius:8px;background:#3b82f6;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px}
.user-info .name{font-size:13px;font-weight:600;color:#e2e8f0}
.user-info .role{font-size:11px;color:#64748b}

/* Main */
.main{flex:1;margin-left:260px}
.topbar{background:#fff;padding:16px 28px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,.06);position:sticky;top:0;z-index:50}
.topbar h1{font-size:20px;font-weight:700;display:flex;align-items:center;gap:8px}
.topbar h1 i{color:#2563eb}
.topbar-actions{display:flex;gap:12px;align-items:center}
.topbar-actions a,.topbar-actions button{background:none;border:none;color:#64748b;font-size:14px;cursor:pointer;display:flex;align-items:center;gap:6px;font-family:inherit;transition:color .2s}
.topbar-actions a:hover,.topbar-actions button:hover{color:#1e293b}
.btn-store{background:#eff6ff!important;color:#2563eb!important;padding:8px 16px;border-radius:8px;font-weight:600}
.btn-store:hover{background:#dbeafe!important}
.content{padding:28px}

/* Stats Cards */
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:24px}
.stat-card{background:#fff;border-radius:14px;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,.06);display:flex;align-items:center;gap:16px;transition:transform .2s,box-shadow .2s}
.stat-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.1)}
.stat-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px}
.stat-icon.blue{background:#dbeafe;color:#2563eb}
.stat-icon.amber{background:#fef3c7;color:#d97706}
.stat-icon.green{background:#dcfce7;color:#16a34a}
.stat-icon.red{background:#fee2e2;color:#dc2626}
.stat-info h4{font-size:24px;font-weight:800;line-height:1}
.stat-info p{font-size:12px;color:#64748b;font-weight:500;margin-top:4px}

/* Cards */
.card{background:#fff;border-radius:14px;box-shadow:0 1px 3px rgba(0,0,0,.06);margin-bottom:24px;overflow:hidden}
.card-header{padding:20px 24px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;justify-content:space-between}
.card-header h3{font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px}
.card-body{padding:24px}

/* Form */
.form-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.form-field{display:flex;flex-direction:column;gap:6px}
.form-field label{font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.5px}
.form-field input,.form-field select{padding:10px 14px;border:2px solid #e2e8f0;border-radius:10px;font-size:14px;font-family:inherit;transition:border-color .2s,box-shadow .2s}
.form-field input:focus,.form-field select:focus{outline:none;border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,.1)}

/* Buttons */
.btn{padding:10px 20px;border:none;border-radius:10px;cursor:pointer;font-size:14px;font-weight:600;font-family:inherit;display:inline-flex;align-items:center;gap:6px;transition:all .2s}
.btn-primary{background:#2563eb;color:#fff}
.btn-primary:hover{background:#1d4ed8;box-shadow:0 4px 12px rgba(37,99,235,.3)}
.btn-danger{background:#ef4444;color:#fff}
.btn-danger:hover{background:#dc2626}
.btn-success{background:#16a34a;color:#fff}
.btn-success:hover{background:#15803d}
.btn-warning{background:#f59e0b;color:#fff}
.btn-warning:hover{background:#d97706}
.btn-info{background:#0ea5e9;color:#fff}
.btn-info:hover{background:#0284c7}
.btn-secondary{background:#64748b;color:#fff}
.btn-secondary:hover{background:#475569}
.btn-sm{padding:7px 14px;font-size:12px;border-radius:8px}
.btn-ghost{background:transparent;color:#64748b;border:2px solid #e2e8f0}
.btn-ghost:hover{background:#f8fafc;border-color:#cbd5e1}

/* Table */
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse}
th{text-align:left;padding:12px 20px;font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.5px;background:#f8fafc;border-bottom:2px solid #e2e8f0}
td{padding:14px 20px;font-size:14px;border-bottom:1px solid #f1f5f9}
tr{transition:background .15s}
tr:hover td{background:#f8fafc}
.empty-state{text-align:center;padding:48px 20px;color:#94a3b8}
.empty-state i{font-size:48px;margin-bottom:12px;display:block;opacity:.5}
.empty-state p{font-size:15px}

/* Badges */
.badge{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600}
.badge-pending{background:#fef3c7;color:#92400e}
.badge-paid{background:#dbeafe;color:#1e40af}
.badge-completed{background:#dcfce7;color:#166534}
.badge-shipped{background:#e0e7ff;color:#3730a3}
.badge-in_transit{background:#dbeafe;color:#1e40af}
.badge-delivered{background:#d1fae5;color:#065f46}
.badge-cancelled{background:#fee2e2;color:#991b1b}
.badge-failed{background:#fee2e2;color:#991b1b}
.badge-preparing{background:#fef3c7;color:#92400e}

/* Status dots */
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot-pending{background:#f59e0b}
.dot-paid{background:#3b82f6}
.dot-completed,.dot-delivered{background:#16a34a}
.dot-shipped,.dot-in_transit{background:#6366f1}
.dot-cancelled,.dot-failed{background:#ef4444}
.dot-preparing{background:#f59e0b}

/* Select */
select.status-select{padding:7px 12px;border:2px solid #e2e8f0;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit;background:#fff;transition:border-color .2s}
select.status-select:focus{outline:none;border-color:#2563eb}

/* Messages */
.msg{padding:12px 16px;border-radius:10px;margin-bottom:16px;display:none;font-size:14px;font-weight:500;align-items:center;gap:8px}
.msg.ok{background:#dcfce7;color:#166534;display:flex}
.msg.err{background:#fee2e2;color:#991b1b;display:flex}

/* Modal */
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,.6);backdrop-filter:blur(4px);z-index:1000;justify-content:center;align-items:center}
.modal-overlay.active{display:flex}
.modal{background:#fff;border-radius:20px;padding:0;width:90%;max-width:600px;max-height:85vh;overflow:hidden;box-shadow:0 25px 60px rgba(0,0,0,.25);animation:modalIn .25s ease-out}
@keyframes modalIn{from{opacity:0;transform:scale(.95) translateY(10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.modal-header{padding:24px 28px 20px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;justify-content:space-between}
.modal-header h3{font-size:18px;font-weight:700;display:flex;align-items:center;gap:10px}
.modal-close{width:36px;height:36px;border-radius:10px;border:none;background:#f1f5f9;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;color:#64748b;transition:all .2s}
.modal-close:hover{background:#e2e8f0;color:#1e293b}
.modal-body{padding:24px 28px;overflow-y:auto;max-height:calc(85vh - 140px)}
.modal-footer{padding:16px 28px;border-top:1px solid #f1f5f9;display:flex;justify-content:flex-end;gap:10px}

/* Order info grid */
.order-info{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.info-item{padding:14px 16px;background:#f8fafc;border-radius:12px;border:1px solid #f1f5f9}
.info-item .info-label{font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.info-item .info-value{font-size:16px;font-weight:700;color:#1e293b}
.info-item .info-value.price{color:#dc2626}

/* Order items in detail */
.section-title{font-size:13px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.order-item{display:flex;align-items:center;gap:14px;padding:14px 16px;background:#f8fafc;border-radius:12px;margin-bottom:10px;border:1px solid #f1f5f9;transition:background .15s}
.order-item:hover{background:#f1f5f9}
.order-item .book-cover{width:50px;height:68px;border-radius:8px;object-fit:cover;border:1px solid #e2e8f0;flex-shrink:0;background:#f1f5f9}
.order-item .book-placeholder{width:50px;height:68px;border-radius:8px;background:linear-gradient(135deg,#e0e7ff,#dbeafe);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.order-item .oi-info{flex:1;min-width:0}
.order-item .oi-title{font-weight:600;color:#1e293b;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.order-item .oi-sub{font-size:12px;color:#64748b;margin-top:2px}
.order-item .oi-right{text-align:right;flex-shrink:0}
.order-item .oi-price{font-weight:700;color:#dc2626;font-size:15px}
.order-item .oi-qty{font-size:11px;color:#94a3b8;margin-top:2px}

/* Toolbar */
.toolbar{display:flex;align-items:center;gap:12px;padding:0 24px 16px}
.search-box{display:flex;align-items:center;background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:0 14px;transition:border-color .2s;flex:1;max-width:360px}
.search-box:focus-within{border-color:#2563eb;background:#fff}
.search-box i{color:#94a3b8;font-size:14px}
.search-box input{border:none;background:transparent;padding:10px;font-size:14px;font-family:inherit;outline:none;flex:1}
.filter-select{padding:10px 14px;border:2px solid #e2e8f0;border-radius:10px;font-size:13px;font-weight:500;font-family:inherit;background:#fff;cursor:pointer}
.filter-select:focus{outline:none;border-color:#2563eb}

/* Loading skeleton */
.skeleton{background:linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:6px;height:16px}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* Order total summary */
.order-summary{background:linear-gradient(135deg,#1e293b,#334155);color:#fff;border-radius:12px;padding:16px 20px;margin-top:16px;display:flex;align-items:center;justify-content:space-between}
.order-summary .sum-label{font-size:14px;color:#94a3b8}
.order-summary .sum-value{font-size:22px;font-weight:800}
</style>
</head>
<body>

<aside class="sidebar">
<div class="sidebar-brand"><i class="fas fa-book-open"></i> BookStore</div>
<nav class="sidebar-menu">
<div class="menu-label">Tổng quan</div>
<a class="menu-item" href="/pages/admin.html"><i class="fas fa-gauge-high"></i> Dashboard</a>
<div class="menu-label">Quản lý</div>
<a class="menu-item" href="/pages/books.html"><i class="fas fa-book"></i> Sách</a>
<a class="menu-item" href="/pages/catalogs.html"><i class="fas fa-layer-group"></i> Danh mục</a>
<a class="menu-item" href="/pages/customers.html"><i class="fas fa-users"></i> Khách hàng</a>
<a class="menu-item active" href="/pages/orders.html"><i class="fas fa-box"></i> Đơn hàng</a>
<a class="menu-item" href="/pages/cart.html"><i class="fas fa-shopping-cart"></i> Giỏ hàng</a>
<div class="menu-label">Tài chính & Vận chuyển</div>
<a class="menu-item" href="/pages/payments.html"><i class="fas fa-credit-card"></i> Thanh toán</a>
<a class="menu-item" href="/pages/shipments.html"><i class="fas fa-truck"></i> Vận chuyển</a>
<div class="menu-label">Nội dung</div>
<a class="menu-item" href="/pages/comments.html"><i class="fas fa-comments"></i> Bình luận</a>
<a class="menu-item" href="/pages/recommender.html"><i class="fas fa-robot"></i> Gợi ý AI</a>
<div class="menu-label">Nhân sự</div>
<a class="menu-item" href="/pages/staffs.html"><i class="fas fa-user-tie"></i> Nhân viên</a>
<a class="menu-item" href="/pages/managers.html"><i class="fas fa-user-shield"></i> Quản lý</a>
</nav>
<div class="sidebar-footer"><div class="user-card">
<div class="user-avatar" id="sideAvatar">A</div>
<div class="user-info"><div class="name" id="sideName">Admin</div><div class="role" id="sideRole">admin</div></div>
</div></div>
</aside>

<div class="main">
<div class="topbar">
<h1><i class="fas fa-box"></i> Quản lý Đơn hàng</h1>
<div class="topbar-actions">
<a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a>
<button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button>
</div>
</div>

<div class="content">
<div id="msg" class="msg"></div>

<!-- Stats -->
<div class="stats-row">
<div class="stat-card"><div class="stat-icon blue"><i class="fas fa-box"></i></div><div class="stat-info"><h4 id="statTotal">-</h4><p>Tổng đơn hàng</p></div></div>
<div class="stat-card"><div class="stat-icon amber"><i class="fas fa-clock"></i></div><div class="stat-info"><h4 id="statPending">-</h4><p>Chờ xử lý</p></div></div>
<div class="stat-card"><div class="stat-icon green"><i class="fas fa-check-circle"></i></div><div class="stat-info"><h4 id="statCompleted">-</h4><p>Hoàn thành</p></div></div>
<div class="stat-card"><div class="stat-icon red"><i class="fas fa-dollar-sign"></i></div><div class="stat-info"><h4 id="statRevenue">-</h4><p>Tổng doanh thu</p></div></div>
</div>

<!-- Create Order -->
<div class="card">
<div class="card-header"><h3><i class="fas fa-plus-circle" style="color:#2563eb"></i> Tạo đơn hàng mới</h3></div>
<div class="card-body">
<div class="form-grid">
<div class="form-field"><label>Customer ID</label><input type="number" id="customer_id" placeholder="Nhập ID khách hàng"></div>
</div>
<div style="margin-top:16px;display:flex;align-items:center;gap:12px">
<button class="btn btn-primary" onclick="createOrder()"><i class="fas fa-shopping-bag"></i> Tạo từ giỏ hàng</button>
<span style="color:#94a3b8;font-size:13px">Tự động tạo đơn từ giỏ hàng hiện tại của khách.</span>
</div>
</div></div>

<!-- Orders Table -->
<div class="card">
<div class="card-header">
<h3><i class="fas fa-list-ul" style="color:#2563eb"></i> Danh sách đơn hàng</h3>
<button class="btn btn-ghost btn-sm" onclick="load()"><i class="fas fa-refresh"></i> Tải lại</button>
</div>
<div class="toolbar">
<div class="search-box"><i class="fas fa-search"></i><input type="text" id="searchInput" placeholder="Tìm kiếm theo ID, khách hàng..." oninput="filterTable()"></div>
<select class="filter-select" id="statusFilter" onchange="filterTable()">
<option value="">Tất cả trạng thái</option>
<option value="pending">Chờ xử lý</option>
<option value="paid">Đã thanh toán</option>
<option value="completed">Hoàn thành</option>
<option value="shipped">Đã gửi</option>
<option value="delivered">Đã giao</option>
<option value="cancelled">Đã hủy</option>
</select>
</div>
<div class="table-wrap">
<table>
<thead><tr>
<th style="width:60px">ID</th>
<th>Khách hàng</th>
<th>Sản phẩm</th>
<th>Tổng tiền</th>
<th>Trạng thái</th>
<th>Ngày tạo</th>
<th style="width:130px">Thao tác</th>
</tr></thead>
<tbody id="tbl">
<tr><td colspan="7"><div class="empty-state"><i class="fas fa-spinner fa-spin"></i><p>Đang tải dữ liệu...</p></div></td></tr>
</tbody>
</table>
</div>
</div>
</div>
</div>

<!-- Detail Modal -->
<div class="modal-overlay" id="detailModal">
<div class="modal">
<div class="modal-header">
<h3><i class="fas fa-receipt" style="color:#2563eb"></i> Đơn hàng #<span id="detail_order_id"></span></h3>
<button class="modal-close" onclick="closeModal()"><i class="fas fa-times"></i></button>
</div>
<div class="modal-body">
<div class="order-info">
<div class="info-item"><div class="info-label">Khách hàng</div><div class="info-value">#<span id="detail_customer"></span></div></div>
<div class="info-item"><div class="info-label">Ngày đặt</div><div class="info-value"><span id="detail_date"></span></div></div>
<div class="info-item"><div class="info-label">Trạng thái</div><div class="info-value"><span id="detail_status" class="badge"></span></div></div>
<div class="info-item"><div class="info-label">Tổng tiền</div><div class="info-value price">$<span id="detail_total"></span></div></div>
</div>
<div class="section-title"><i class="fas fa-shopping-bag"></i> Sản phẩm trong đơn (<span id="detail_item_count">0</span>)</div>
<div id="detail_items"><div class="skeleton" style="height:80px;margin-bottom:10px"></div><div class="skeleton" style="height:80px"></div></div>
<div id="detail_summary"></div>
</div>
<div class="modal-footer"><button class="btn btn-secondary" onclick="closeModal()">Đóng</button></div>
</div>
</div>

<script>
var TOKEN = localStorage.getItem('access_token');
if (!TOKEN) window.location.href = '/pages/login.html';

var _fetch = window.fetch;
window.fetch = function(url, opts) {
    opts = opts || {};
    opts.headers = Object.assign({}, opts.headers || {}, {'Authorization': 'Bearer ' + TOKEN});
    return _fetch(url, opts);
};

function showMsg(t, ok) {
    var e = document.getElementById('msg');
    e.innerHTML = '<i class="fas fa-' + (ok ? 'check-circle' : 'exclamation-circle') + '"></i> ' + t;
    e.className = 'msg ' + (ok ? 'ok' : 'err');
    setTimeout(function() { e.className = 'msg'; }, 3500);
}

function logout() { localStorage.clear(); window.location.href = '/pages/login.html'; }

try {
    var u = JSON.parse(localStorage.getItem('user') || '{}');
    document.getElementById('sideName').textContent = u.full_name || u.username || 'Admin';
    document.getElementById('sideRole').textContent = u.role || 'admin';
    document.getElementById('sideAvatar').textContent = (u.full_name || u.username || 'A')[0].toUpperCase();
    if (['admin', 'manager', 'staff'].indexOf(u.role) < 0) window.location.href = '/';
} catch (e) {}

var API = '/api';
var allOrders = [];
var bookCache = {};
var statusLabels = {
    'pending': 'Chờ xử lý', 'paid': 'Đã thanh toán', 'completed': 'Hoàn thành',
    'shipped': 'Đã gửi', 'in_transit': 'Đang vận chuyển', 'delivered': 'Đã giao',
    'cancelled': 'Đã hủy', 'failed': 'Thất bại', 'preparing': 'Đang chuẩn bị'
};
var statusIcons = {
    'pending': 'clock', 'paid': 'credit-card', 'completed': 'check-circle',
    'shipped': 'truck', 'in_transit': 'shipping-fast', 'delivered': 'box-open',
    'cancelled': 'times-circle', 'failed': 'exclamation-triangle', 'preparing': 'cog'
};

function getBookInfo(bookId) {
    if (bookCache[bookId]) return Promise.resolve(bookCache[bookId]);
    return fetch(API + '/books/' + bookId + '/').then(function(r) {
        if (r.ok) return r.json(); return null;
    }).then(function(b) {
        if (b) bookCache[bookId] = b; return b;
    }).catch(function() { return null; });
}

function updateStats(orders) {
    var total = orders.length;
    var pending = orders.filter(function(o) { return o.status === 'pending'; }).length;
    var completed = orders.filter(function(o) { return o.status === 'completed' || o.status === 'delivered'; }).length;
    var revenue = orders.reduce(function(s, o) { return s + parseFloat(o.total_amount || 0); }, 0);

    document.getElementById('statTotal').textContent = total;
    document.getElementById('statPending').textContent = pending;
    document.getElementById('statCompleted').textContent = completed;
    document.getElementById('statRevenue').textContent = '$' + revenue.toFixed(2);
}

function load() {
    var tb = document.getElementById('tbl');
    tb.innerHTML = '<tr><td colspan="7"><div class="empty-state"><i class="fas fa-spinner fa-spin"></i><p>Đang tải dữ liệu...</p></div></td></tr>';

    fetch(API + '/orders/').then(function(r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
    }).then(function(d) {
        allOrders = Array.isArray(d) ? d : (d.results || []);
        updateStats(allOrders);
        renderOrders(allOrders);
    }).catch(function(err) {
        console.error('Load orders error:', err);
        tb.innerHTML = '<tr><td colspan="7"><div class="empty-state"><i class="fas fa-exclamation-triangle" style="color:#ef4444"></i><p>Không thể tải danh sách đơn hàng</p><p style="font-size:12px;margin-top:4px">' + err.message + '</p></div></td></tr>';
    });
}

function renderOrders(orders) {
    var tb = document.getElementById('tbl');
    if (!orders.length) {
        tb.innerHTML = '<tr><td colspan="7"><div class="empty-state"><i class="fas fa-box-open"></i><p>Chưa có đơn hàng nào</p></div></td></tr>';
        return;
    }

    tb.innerHTML = orders.map(function(o) {
        var itemCount = (o.items && o.items.length) || 0;
        var statusOpts = ['pending', 'paid', 'completed', 'shipped', 'delivered', 'cancelled'].map(function(s) {
            return '<option value="' + s + '"' + (s === o.status ? ' selected' : '') + '>' + (statusLabels[s] || s) + '</option>';
        }).join('');

        var statusIcon = statusIcons[o.status] || 'circle';
        var dateStr = new Date(o.created_at).toLocaleDateString('vi-VN', {day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'});

        return '<tr data-id="' + o.id + '" data-customer="' + o.customer_id + '" data-status="' + o.status + '">' +
            '<td><strong style="color:#2563eb">#' + o.id + '</strong></td>' +
            '<td><div style="display:flex;align-items:center;gap:8px"><div style="width:32px;height:32px;border-radius:8px;background:#eff6ff;display:flex;align-items:center;justify-content:center"><i class="fas fa-user" style="color:#2563eb;font-size:12px"></i></div><span>Khách #' + o.customer_id + '</span></div></td>' +
            '<td><span class="badge" style="background:#f1f5f9;color:#475569"><i class="fas fa-cube"></i> ' + itemCount + ' sản phẩm</span></td>' +
            '<td><strong style="color:#dc2626;font-size:15px">$' + parseFloat(o.total_amount).toFixed(2) + '</strong></td>' +
            '<td><select class="status-select" onchange="updateStatus(' + o.id + ',this.value)" style="border-color:transparent;background:#f8fafc">' + statusOpts + '</select></td>' +
            '<td><span style="color:#64748b;font-size:13px">' + dateStr + '</span></td>' +
            '<td><div style="display:flex;gap:6px">' +
            '<button class="btn btn-info btn-sm" onclick="viewDetail(' + o.id + ')" title="Xem chi tiết"><i class="fas fa-eye"></i></button>' +
            '<button class="btn btn-danger btn-sm" onclick="del(' + o.id + ')" title="Xóa"><i class="fas fa-trash"></i></button>' +
            '</div></td></tr>';
    }).join('');
}

function filterTable() {
    var search = document.getElementById('searchInput').value.toLowerCase();
    var statusF = document.getElementById('statusFilter').value;
    var filtered = allOrders.filter(function(o) {
        var matchSearch = !search || ('#' + o.id).toLowerCase().indexOf(search) >= 0 || ('' + o.customer_id).indexOf(search) >= 0;
        var matchStatus = !statusF || o.status === statusF;
        return matchSearch && matchStatus;
    });
    renderOrders(filtered);
}

function createOrder() {
    var cid = document.getElementById('customer_id').value;
    if (!cid) { showMsg('Vui lòng nhập Customer ID', false); return; }

    fetch(API + '/orders/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({customer_id: parseInt(cid)})
    }).then(function(r) {
        return r.json().then(function(d) {
            if (r.ok) {
                showMsg('Đơn hàng #' + d.id + ' đã tạo thành công! Tổng: $' + d.total_amount, true);
                document.getElementById('customer_id').value = '';
                load();
            } else {
                showMsg(d.error || d.detail || JSON.stringify(d), false);
            }
        });
    }).catch(function(e) { showMsg('Lỗi kết nối: ' + e.message, false); });
}

function updateStatus(id, newStatus) {
    fetch(API + '/orders/' + id + '/', {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: newStatus})
    }).then(function(r) {
        if (r.ok) {
            showMsg('Đã cập nhật trạng thái đơn #' + id + ' → ' + (statusLabels[newStatus] || newStatus), true);
            // Update local data
            allOrders.forEach(function(o) { if (o.id === id) o.status = newStatus; });
            updateStats(allOrders);
        } else {
            showMsg('Lỗi cập nhật trạng thái', false);
        }
    });
}

function viewDetail(id) {
    // Find order in cached data first
    var order = allOrders.find(function(o) { return o.id === id; });

    var modal = document.getElementById('detailModal');
    document.getElementById('detail_order_id').textContent = id;
    document.getElementById('detail_items').innerHTML = '<div class="skeleton" style="height:80px;margin-bottom:10px"></div><div class="skeleton" style="height:80px"></div>';
    document.getElementById('detail_summary').innerHTML = '';
    modal.classList.add('active');

    var showDetail = function(o) {
        document.getElementById('detail_customer').textContent = o.customer_id;
        document.getElementById('detail_total').textContent = parseFloat(o.total_amount).toFixed(2);

        var st = document.getElementById('detail_status');
        var icon = statusIcons[o.status] || 'circle';
        st.innerHTML = '<span class="status-dot dot-' + o.status + '"></span> ' + (statusLabels[o.status] || o.status);
        st.className = 'badge badge-' + o.status;

        document.getElementById('detail_date').textContent = new Date(o.created_at).toLocaleDateString('vi-VN', {day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'});

        var items = o.items || [];
        document.getElementById('detail_item_count').textContent = items.length;

        if (!items.length) {
            document.getElementById('detail_items').innerHTML = '<div class="empty-state" style="padding:24px"><i class="fas fa-box-open"></i><p>Không có sản phẩm trong đơn</p></div>';
            return;
        }

        // Fetch book info for all items
        var promises = items.map(function(item) {
            return getBookInfo(item.book_id).then(function(book) { return {item: item, book: book}; });
        });

        Promise.all(promises).then(function(results) {
            var html = results.map(function(r) {
                var item = r.item;
                var book = r.book;
                var imgHtml = book && book.image_url
                    ? '<img class="book-cover" src="' + book.image_url + '" onerror="this.parentElement.innerHTML=\'<div class=book-placeholder>📖</div>\'">'
                    : '<div class="book-placeholder">📖</div>';
                var title = book ? book.title : 'Sách #' + item.book_id;
                var author = book ? (book.author || '') : '';
                var lineTotal = (parseFloat(item.price || 0) * (item.quantity || 1)).toFixed(2);

                return '<div class="order-item">' + imgHtml +
                    '<div class="oi-info"><div class="oi-title">' + title + '</div>' +
                    '<div class="oi-sub">' + (author ? author + ' · ' : '') + '$' + parseFloat(item.price || 0).toFixed(2) + ' × ' + item.quantity + '</div></div>' +
                    '<div class="oi-right"><div class="oi-price">$' + lineTotal + '</div>' +
                    '<div class="oi-qty">SL: ' + item.quantity + '</div></div></div>';
            }).join('');

            document.getElementById('detail_items').innerHTML = html;

            // Summary
            document.getElementById('detail_summary').innerHTML =
                '<div class="order-summary"><span class="sum-label">Tổng thanh toán</span><span class="sum-value">$' + parseFloat(o.total_amount).toFixed(2) + '</span></div>';
        });
    };

    if (order) {
        showDetail(order);
    } else {
        fetch(API + '/orders/' + id + '/').then(function(r) { return r.json(); }).then(showDetail)
        .catch(function() { showMsg('Lỗi tải chi tiết đơn hàng', false); });
    }
}

function closeModal() { document.getElementById('detailModal').classList.remove('active'); }

function del(id) {
    if (!confirm('Bạn có chắc muốn xóa đơn hàng #' + id + '?')) return;
    fetch(API + '/orders/' + id + '/', {method: 'DELETE'}).then(function(r) {
        if (r.ok || r.status === 204) {
            showMsg('Đã xóa đơn hàng #' + id, true);
            load();
        } else {
            showMsg('Lỗi khi xóa đơn hàng', false);
        }
    });
}

document.getElementById('detailModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// Load data
load();
</script>
</body>
</html>'''

path = os.path.join(BASE, 'orders.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(orders_html)
print("✅ orders.html written successfully!")
