#!/usr/bin/env python3
"""Write all updated admin HTML files with field labels, image_url for books, book info in order details."""
import os

BASE = '/Users/truongmanhtuan/django_project/assgn05v1/bookstore-micro05/api-gateway/templates'

# Common CSS for field labels
LABEL_CSS = """
.form-field{display:flex;flex-direction:column;gap:4px}
.form-field label{font-size:12px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:.5px}
.form-field input,.form-field select,.form-field textarea{padding:10px 14px;border:2px solid #e2e8f0;border-radius:8px;font-size:14px;font-family:inherit}
.form-field input:focus,.form-field select:focus,.form-field textarea:focus{outline:none;border-color:#2563eb}
.img-preview{width:48px;height:48px;border-radius:8px;object-fit:cover;border:1px solid #e2e8f0}
.img-preview-lg{width:100%;max-width:200px;max-height:120px;border-radius:8px;object-fit:cover;margin-top:4px;border:1px solid #e2e8f0}
"""

# ============================
# SIDEBAR TEMPLATE
# ============================
def sidebar(active):
    items = [
        ('Tổng quan', [('admin.html','fa-gauge-high','Dashboard')]),
        ('Quản lý', [('books.html','fa-book','Sách'),('catalogs.html','fa-layer-group','Danh mục'),('customers.html','fa-users','Khách hàng'),('orders.html','fa-box','Đơn hàng'),('cart.html','fa-shopping-cart','Giỏ hàng')]),
        ('Tài chính & Vận chuyển', [('payments.html','fa-credit-card','Thanh toán'),('shipments.html','fa-truck','Vận chuyển')]),
        ('Nội dung', [('comments.html','fa-comments','Bình luận'),('recommender.html','fa-robot','Gợi ý AI')]),
        ('Nhân sự', [('staffs.html','fa-user-tie','Nhân viên'),('managers.html','fa-user-shield','Quản lý')]),
    ]
    html = '<aside class="sidebar"><div class="sidebar-brand"><i class="fas fa-book-open"></i> BookStore</div><nav class="sidebar-menu">'
    for label, links in items:
        html += f'<div class="menu-label">{label}</div>'
        for href, icon, name in links:
            ac = ' active' if href == active else ''
            html += f'<a class="menu-item{ac}" href="/pages/{href}"><i class="fas {icon}"></i> {name}</a>'
    html += '</nav><div class="sidebar-footer"><div class="user-card"><div class="user-avatar" id="sideAvatar">A</div><div class="user-info"><div class="name" id="sideName">Admin</div><div class="role" id="sideRole">admin</div></div></div></div></aside>'
    return html

# Common head CSS (admin)
ADMIN_CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:#f1f5f9;color:#1e293b;display:flex;min-height:100vh}a{text-decoration:none;color:inherit}
.sidebar{width:260px;background:#0f172a;color:#94a3b8;display:flex;flex-direction:column;position:fixed;top:0;left:0;bottom:0;z-index:100}
.sidebar-brand{padding:20px 24px;display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;color:#fff;border-bottom:1px solid #1e293b}.sidebar-brand i{color:#3b82f6}
.sidebar-menu{flex:1;padding:16px 12px;overflow-y:auto}
.menu-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:16px 12px 8px;color:#475569}
.menu-item{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:8px;font-size:14px;color:#94a3b8;transition:all .2s;margin-bottom:2px}
.menu-item:hover{background:#1e293b;color:#e2e8f0}.menu-item.active{background:#1d4ed8;color:#fff}.menu-item i{width:20px;text-align:center}
.sidebar-footer{padding:16px;border-top:1px solid #1e293b}
.user-card{display:flex;align-items:center;gap:10px;padding:8px}
.user-avatar{width:36px;height:36px;border-radius:8px;background:#3b82f6;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px}
.user-info .name{font-size:13px;font-weight:600;color:#e2e8f0}.user-info .role{font-size:11px;color:#64748b}
.main{flex:1;margin-left:260px}
.topbar{background:#fff;padding:16px 28px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,.06);position:sticky;top:0;z-index:50}
.topbar h1{font-size:20px;font-weight:700;display:flex;align-items:center;gap:8px}.topbar h1 i{color:#2563eb}
.topbar-actions{display:flex;gap:12px;align-items:center}
.topbar-actions a,.topbar-actions button{background:none;border:none;color:#64748b;font-size:14px;cursor:pointer;display:flex;align-items:center;gap:6px;font-family:inherit}
.btn-store{background:#eff6ff!important;color:#2563eb!important;padding:8px 16px;border-radius:8px;font-weight:600}
.content{padding:28px}
.card{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);margin-bottom:24px}
.card-header{padding:20px 24px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;justify-content:space-between}
.card-header h3{font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px}
.card-body{padding:24px}
.form-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.btn{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600;font-family:inherit;display:inline-flex;align-items:center;gap:6px;transition:all .2s}
.btn-primary{background:#2563eb;color:#fff}.btn-primary:hover{background:#1d4ed8}
.btn-danger{background:#ef4444;color:#fff}.btn-danger:hover{background:#dc2626}
.btn-success{background:#16a34a;color:#fff}.btn-success:hover{background:#15803d}
.btn-warning{background:#f59e0b;color:#fff}.btn-warning:hover{background:#d97706}
.btn-info{background:#0ea5e9;color:#fff}.btn-info:hover{background:#0284c7}
.btn-secondary{background:#64748b;color:#fff}.btn-secondary:hover{background:#475569}
.btn-sm{padding:6px 12px;font-size:12px}
table{width:100%;border-collapse:collapse}
th{text-align:left;padding:12px 20px;font-size:12px;font-weight:700;color:#64748b;text-transform:uppercase;background:#f8fafc}
td{padding:12px 20px;font-size:14px;border-bottom:1px solid #f8fafc}
tr:hover td{background:#f8fafc}
.badge{display:inline-block;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:600}
.msg{padding:12px 16px;border-radius:8px;margin-bottom:16px;display:none;font-size:14px}
.msg.ok{background:#dcfce7;color:#166534;display:block}.msg.err{background:#fee2e2;color:#991b1b;display:block}
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:1000;justify-content:center;align-items:center}
.modal-overlay.active{display:flex}
.modal{background:#fff;border-radius:16px;padding:32px;width:90%;max-width:560px;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.modal h3{margin-bottom:20px;font-size:20px;display:flex;align-items:center;gap:8px}
.modal-actions{display:flex;gap:10px;margin-top:24px;justify-content:flex-end}
.stars{color:#f59e0b;font-size:14px}
select.status-select{padding:6px 10px;border:2px solid #e2e8f0;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit}
.badge-pending{background:#fef3c7;color:#92400e}.badge-paid,.badge-completed{background:#dcfce7;color:#166534}
.badge-shipped,.badge-in_transit{background:#dbeafe;color:#1e40af}.badge-delivered{background:#d1fae5;color:#065f46}
.badge-cancelled,.badge-failed{background:#fee2e2;color:#991b1b}.badge-preparing{background:#fef3c7;color:#92400e}
.order-item{display:flex;align-items:center;gap:12px;padding:12px 14px;background:#f8fafc;border-radius:8px;margin-bottom:8px;font-size:14px}
.order-item img{width:48px;height:64px;object-fit:cover;border-radius:6px;border:1px solid #e2e8f0}
.order-item .oi-info{flex:1}
.order-item .oi-info .oi-title{font-weight:600;color:#1e293b}.order-item .oi-info .oi-sub{font-size:12px;color:#64748b}
.order-item .oi-price{font-weight:700;color:#dc2626;white-space:nowrap}
"""

# Common auth JS block
AUTH_JS = """var TOKEN=localStorage.getItem('access_token');
if(!TOKEN)window.location.href='/pages/login.html';
var _fetch=window.fetch;window.fetch=function(url,opts){opts=opts||{};opts.headers=Object.assign({},opts.headers||{},{'Authorization':'Bearer '+TOKEN});return _fetch(url,opts)};
function showMsg(t,ok){var e=document.getElementById('msg');e.textContent=t;e.className='msg '+(ok?'ok':'err');setTimeout(function(){e.className='msg'},3000)}
function logout(){localStorage.clear();window.location.href='/pages/login.html'}
try{var u=JSON.parse(localStorage.getItem('user')||'{}');document.getElementById('sideName').textContent=u.full_name||u.username||'Admin';document.getElementById('sideRole').textContent=u.role||'admin';document.getElementById('sideAvatar').textContent=(u.full_name||u.username||'A')[0].toUpperCase();if(['admin','manager','staff'].indexOf(u.role)<0)window.location.href='/'}catch(e){}
var API='/api';"""


# ============================
# BOOKS.HTML
# ============================
books_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Sách - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('books.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-book"></i> Quản lý Sách</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a>
<button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card">
<div class="card-header"><h3><i class="fas fa-plus-circle"></i> Thêm sách mới</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Tên sách *</label><input type="text" id="title" placeholder="Nhập tên sách"></div>
<div class="form-field"><label>Tác giả *</label><input type="text" id="author" placeholder="Nhập tên tác giả"></div>
<div class="form-field"><label>Giá ($) *</label><input type="number" id="price" placeholder="0.00" step="0.01"></div>
<div class="form-field"><label>Số lượng kho</label><input type="number" id="stock" placeholder="0" min="0"></div>
<div class="form-field"><label>Danh mục</label><select id="catalog_id"><option value="">-- Chọn danh mục --</option></select></div>
<div class="form-field"><label>Ảnh bìa (URL)</label><input type="url" id="image_url" placeholder="https://example.com/image.jpg"></div>
</div><button class="btn btn-primary" style="margin-top:16px" onclick="addItem()"><i class="fas fa-plus"></i> Thêm sách</button>
</div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách sách</h3></div>
<table><thead><tr><th>Ảnh</th><th>ID</th><th>Tên sách</th><th>Tác giả</th><th>Danh mục</th><th>Giá</th><th>Kho</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="8">Đang tải...</td></tr></tbody></table></div>
</div></div>

<div class="modal-overlay" id="editModal"><div class="modal">
<h3><i class="fas fa-edit" style="color:#f59e0b"></i> Chỉnh sửa sách</h3>
<input type="hidden" id="edit_id">
<div class="form-grid">
<div class="form-field"><label>Tên sách</label><input type="text" id="edit_title"></div>
<div class="form-field"><label>Tác giả</label><input type="text" id="edit_author"></div>
<div class="form-field"><label>Giá ($)</label><input type="number" id="edit_price" step="0.01"></div>
<div class="form-field"><label>Số lượng kho</label><input type="number" id="edit_stock" min="0"></div>
<div class="form-field"><label>Danh mục</label><select id="edit_catalog_id"><option value="">-- Chọn danh mục --</option></select></div>
<div class="form-field"><label>Ảnh bìa (URL)</label><input type="url" id="edit_image_url" placeholder="https://..."><img id="edit_img_preview" class="img-preview-lg" style="display:none"></div>
</div>
<div class="modal-actions">
<button class="btn btn-secondary" onclick="closeModal()">Hủy</button>
<button class="btn btn-success" onclick="saveEdit()"><i class="fas fa-save"></i> Lưu</button>
</div></div></div>

<script>
{AUTH_JS}
var catalogMap={{}};
function loadCatalogs(){{
return fetch(API+'/catalogs/').then(function(r){{return r.json()}}).then(function(d){{
var items=Array.isArray(d)?d:(d.results||[]);catalogMap={{}};
var opts='';items.forEach(function(c){{catalogMap[c.id]=c.name;opts+='<option value="'+c.id+'">'+c.name+'</option>'}});
document.getElementById('catalog_id').innerHTML='<option value="">-- Chọn danh mục --</option>'+opts;
document.getElementById('edit_catalog_id').innerHTML='<option value="">-- Chọn danh mục --</option>'+opts;
}}).catch(function(){{}})}}
function load(){{
fetch(API+'/books/').then(function(r){{return r.json()}}).then(function(d){{
var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');
if(!items.length){{tb.innerHTML='<tr><td colspan="8">Chưa có sách</td></tr>';return}}
tb.innerHTML=items.map(function(b){{
var imgCell=b.image_url?'<img src="'+b.image_url+'" class="img-preview" onerror="this.src=\\'\\';this.alt=\\'No img\\'">':'<span style="color:#94a3b8">-</span>';
var catBadge=b.catalog_id?'<span class="badge" style="background:#ede9fe;color:#6d28d9">'+(catalogMap[b.catalog_id]||'#'+b.catalog_id)+'</span>':'<span style="color:#94a3b8">-</span>';
var stockStyle=b.stock>5?'background:#dcfce7;color:#166534':b.stock>0?'background:#fef9c3;color:#854d0e':'background:#fee2e2;color:#991b1b';
return '<tr><td>'+imgCell+'</td><td><strong>#'+b.id+'</strong></td><td>'+b.title+'</td><td>'+(b.author||'-')+'</td><td>'+catBadge+'</td><td style="font-weight:700;color:#dc2626">$'+parseFloat(b.price).toFixed(2)+'</td><td><span class="badge" style="'+stockStyle+'">'+b.stock+'</span></td><td><button class="btn btn-warning btn-sm" onclick="openEdit('+b.id+')"><i class="fas fa-edit"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+b.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('');
}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="8">Lỗi tải dữ liệu</td></tr>';}})}}
function addItem(){{
var data={{title:document.getElementById('title').value,author:document.getElementById('author').value,price:document.getElementById('price').value,stock:document.getElementById('stock').value||0,image_url:document.getElementById('image_url').value}};
var catId=document.getElementById('catalog_id').value;if(catId)data.catalog_id=parseInt(catId);
if(!data.title||!data.author||!data.price){{showMsg('Vui lòng điền Tên, Tác giả và Giá',false);return}}
fetch(API+'/books/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{
if(r.ok){{showMsg('Thêm sách thành công!',true);['title','author','price','stock','image_url'].forEach(function(id){{document.getElementById(id).value=''}});document.getElementById('catalog_id').value='';load()}}
else{{r.json().then(function(e){{showMsg(JSON.stringify(e),false)}})}}
}})}}
function openEdit(id){{
fetch(API+'/books/'+id+'/').then(function(r){{return r.json()}}).then(function(b){{
document.getElementById('edit_id').value=b.id;
document.getElementById('edit_title').value=b.title||'';
document.getElementById('edit_author').value=b.author||'';
document.getElementById('edit_price').value=b.price||'';
document.getElementById('edit_stock').value=b.stock!=null?b.stock:0;
document.getElementById('edit_catalog_id').value=b.catalog_id||'';
document.getElementById('edit_image_url').value=b.image_url||'';
var prev=document.getElementById('edit_img_preview');
if(b.image_url){{prev.src=b.image_url;prev.style.display='block'}}else{{prev.style.display='none'}}
document.getElementById('editModal').classList.add('active');
}}).catch(function(){{showMsg('Lỗi tải thông tin sách',false)}})}}
function closeModal(){{document.getElementById('editModal').classList.remove('active')}}
function saveEdit(){{
var id=document.getElementById('edit_id').value;if(!id)return;
var data={{title:document.getElementById('edit_title').value,author:document.getElementById('edit_author').value,price:document.getElementById('edit_price').value,stock:document.getElementById('edit_stock').value||0,image_url:document.getElementById('edit_image_url').value}};
var catId=document.getElementById('edit_catalog_id').value;if(catId)data.catalog_id=parseInt(catId);else data.catalog_id=null;
fetch(API+'/books/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{
if(r.ok){{showMsg('Cập nhật sách thành công!',true);closeModal();load()}}
else{{r.json().then(function(e){{showMsg('Lỗi: '+JSON.stringify(e),false)}})}}
}})}}
function del(id){{if(!confirm('Xóa sách #'+id+'?'))return;fetch(API+'/books/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('editModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
document.getElementById('edit_image_url').addEventListener('input',function(){{var prev=document.getElementById('edit_img_preview');if(this.value){{prev.src=this.value;prev.style.display='block'}}else{{prev.style.display='none'}}}});
loadCatalogs().then(function(){{load()}});
</script></body></html>'''


# ============================
# CATALOGS.HTML
# ============================
catalogs_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Danh mục - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('catalogs.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-layer-group"></i> Quản lý Danh mục</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a><button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-plus-circle"></i> Thêm danh mục mới</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Tên danh mục *</label><input type="text" id="name" placeholder="Nhập tên danh mục"></div>
<div class="form-field"><label>Mô tả</label><input type="text" id="description" placeholder="Mô tả ngắn"></div>
</div><button class="btn btn-primary" style="margin-top:16px" onclick="addItem()"><i class="fas fa-plus"></i> Thêm</button></div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách danh mục</h3></div>
<table><thead><tr><th>ID</th><th>Tên</th><th>Mô tả</th><th>Ngày tạo</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="5">Đang tải...</td></tr></tbody></table></div></div></div>

<div class="modal-overlay" id="editModal"><div class="modal">
<h3><i class="fas fa-edit" style="color:#f59e0b"></i> Chỉnh sửa danh mục</h3>
<input type="hidden" id="edit_id">
<div class="form-grid">
<div class="form-field"><label>Tên danh mục</label><input type="text" id="edit_name"></div>
<div class="form-field"><label>Mô tả</label><input type="text" id="edit_description"></div>
</div>
<div class="modal-actions"><button class="btn btn-secondary" onclick="closeModal()">Hủy</button><button class="btn btn-success" onclick="saveEdit()"><i class="fas fa-save"></i> Lưu</button></div></div></div>

<script>
{AUTH_JS}
var SVC='catalogs';
function load(){{fetch(API+'/'+SVC+'/').then(function(r){{return r.json()}}).then(function(d){{var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');if(!items.length){{tb.innerHTML='<tr><td colspan="5">Chưa có danh mục</td></tr>';return}}tb.innerHTML=items.map(function(c){{return '<tr><td><strong>#'+c.id+'</strong></td><td><strong>'+c.name+'</strong></td><td>'+(c.description||'-')+'</td><td>'+new Date(c.created_at).toLocaleDateString('vi-VN')+'</td><td><button class="btn btn-warning btn-sm" onclick="openEdit('+c.id+')"><i class="fas fa-edit"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+c.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('')}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="5">Lỗi tải</td></tr>'}})}}
function addItem(){{var data={{name:document.getElementById('name').value,description:document.getElementById('description').value}};if(!data.name){{showMsg('Vui lòng nhập tên',false);return}}fetch(API+'/'+SVC+'/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Thêm thành công!',true);['name','description'].forEach(function(id){{document.getElementById(id).value=''}});load()}}else{{r.json().then(function(e){{showMsg(JSON.stringify(e),false)}})}}}})}}
function openEdit(id){{fetch(API+'/'+SVC+'/'+id+'/').then(function(r){{return r.json()}}).then(function(c){{document.getElementById('edit_id').value=c.id;document.getElementById('edit_name').value=c.name||'';document.getElementById('edit_description').value=c.description||'';document.getElementById('editModal').classList.add('active')}}).catch(function(){{showMsg('Lỗi',false)}})}}
function closeModal(){{document.getElementById('editModal').classList.remove('active')}}
function saveEdit(){{var id=document.getElementById('edit_id').value;if(!id)return;var data={{name:document.getElementById('edit_name').value,description:document.getElementById('edit_description').value}};fetch(API+'/'+SVC+'/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Cập nhật thành công!',true);closeModal();load()}}else{{r.json().then(function(e){{showMsg('Lỗi: '+JSON.stringify(e),false)}})}}}})}}
function del(id){{if(!confirm('Xóa #'+id+'?'))return;fetch(API+'/'+SVC+'/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('editModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
load();
</script></body></html>'''


# ============================
# STAFFS.HTML
# ============================
staffs_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Nhân viên - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('staffs.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-user-tie"></i> Quản lý Nhân viên</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a><button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-plus-circle"></i> Thêm nhân viên mới</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Họ tên *</label><input type="text" id="name" placeholder="Nhập họ tên"></div>
<div class="form-field"><label>Email *</label><input type="email" id="email" placeholder="email@example.com"></div>
<div class="form-field"><label>Số điện thoại</label><input type="text" id="phone" placeholder="0123456789"></div>
<div class="form-field"><label>Vai trò</label><select id="role"><option value="staff">Nhân viên (staff)</option><option value="manager">Quản lý (manager)</option></select></div>
</div><button class="btn btn-primary" style="margin-top:16px" onclick="addItem()"><i class="fas fa-plus"></i> Thêm</button></div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách nhân viên</h3></div>
<table><thead><tr><th>ID</th><th>Họ tên</th><th>Email</th><th>Vai trò</th><th>SĐT</th><th>Ngày tạo</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="7">Đang tải...</td></tr></tbody></table></div></div></div>

<div class="modal-overlay" id="editModal"><div class="modal">
<h3><i class="fas fa-edit" style="color:#f59e0b"></i> Chỉnh sửa nhân viên</h3>
<input type="hidden" id="edit_id">
<div class="form-grid">
<div class="form-field"><label>Họ tên</label><input type="text" id="edit_name"></div>
<div class="form-field"><label>Email</label><input type="email" id="edit_email"></div>
<div class="form-field"><label>Số điện thoại</label><input type="text" id="edit_phone"></div>
<div class="form-field"><label>Vai trò</label><select id="edit_role"><option value="staff">Nhân viên</option><option value="manager">Quản lý</option></select></div>
</div>
<div class="modal-actions"><button class="btn btn-secondary" onclick="closeModal()">Hủy</button><button class="btn btn-success" onclick="saveEdit()"><i class="fas fa-save"></i> Lưu</button></div></div></div>

<script>
{AUTH_JS}
var SVC='staffs';
function load(){{fetch(API+'/'+SVC+'/').then(function(r){{return r.json()}}).then(function(d){{var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');if(!items.length){{tb.innerHTML='<tr><td colspan="7">Chưa có nhân viên</td></tr>';return}}tb.innerHTML=items.map(function(s){{return '<tr><td><strong>#'+s.id+'</strong></td><td><strong>'+s.name+'</strong></td><td>'+s.email+'</td><td><span class="badge" style="background:#dcfce7;color:#166534">'+(s.role||'staff')+'</span></td><td>'+(s.phone||'-')+'</td><td>'+new Date(s.created_at).toLocaleDateString('vi-VN')+'</td><td><button class="btn btn-warning btn-sm" onclick="openEdit('+s.id+')"><i class="fas fa-edit"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+s.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('')}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="7">Lỗi</td></tr>'}})}}
function addItem(){{var data={{name:document.getElementById('name').value,email:document.getElementById('email').value,role:document.getElementById('role').value||'staff',phone:document.getElementById('phone').value}};if(!data.name||!data.email){{showMsg('Họ tên và Email là bắt buộc',false);return}}fetch(API+'/'+SVC+'/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Thêm thành công!',true);['name','email','phone'].forEach(function(id){{document.getElementById(id).value=''}});load()}}else{{r.json().then(function(e){{showMsg(JSON.stringify(e),false)}})}}}})}}
function openEdit(id){{fetch(API+'/'+SVC+'/'+id+'/').then(function(r){{return r.json()}}).then(function(s){{document.getElementById('edit_id').value=s.id;document.getElementById('edit_name').value=s.name||'';document.getElementById('edit_email').value=s.email||'';document.getElementById('edit_phone').value=s.phone||'';document.getElementById('edit_role').value=s.role||'staff';document.getElementById('editModal').classList.add('active')}}).catch(function(){{showMsg('Lỗi',false)}})}}
function closeModal(){{document.getElementById('editModal').classList.remove('active')}}
function saveEdit(){{var id=document.getElementById('edit_id').value;if(!id)return;var data={{name:document.getElementById('edit_name').value,email:document.getElementById('edit_email').value,phone:document.getElementById('edit_phone').value,role:document.getElementById('edit_role').value}};fetch(API+'/'+SVC+'/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Cập nhật thành công!',true);closeModal();load()}}else{{r.json().then(function(e){{showMsg('Lỗi: '+JSON.stringify(e),false)}})}}}})}}
function del(id){{if(!confirm('Xóa #'+id+'?'))return;fetch(API+'/'+SVC+'/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('editModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
load();
</script></body></html>'''


# ============================
# MANAGERS.HTML
# ============================
managers_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý viên - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('managers.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-user-shield"></i> Quản lý viên</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a><button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-plus-circle"></i> Thêm quản lý viên mới</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Họ tên *</label><input type="text" id="name" placeholder="Nhập họ tên"></div>
<div class="form-field"><label>Email *</label><input type="email" id="email" placeholder="email@example.com"></div>
<div class="form-field"><label>Phòng ban</label><input type="text" id="department" placeholder="Phòng ban"></div>
<div class="form-field"><label>Số điện thoại</label><input type="text" id="phone" placeholder="0123456789"></div>
</div><button class="btn btn-primary" style="margin-top:16px" onclick="addItem()"><i class="fas fa-plus"></i> Thêm</button></div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách quản lý viên</h3></div>
<table><thead><tr><th>ID</th><th>Họ tên</th><th>Email</th><th>Phòng ban</th><th>SĐT</th><th>Ngày tạo</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="7">Đang tải...</td></tr></tbody></table></div></div></div>

<div class="modal-overlay" id="editModal"><div class="modal">
<h3><i class="fas fa-edit" style="color:#f59e0b"></i> Chỉnh sửa quản lý viên</h3>
<input type="hidden" id="edit_id">
<div class="form-grid">
<div class="form-field"><label>Họ tên</label><input type="text" id="edit_name"></div>
<div class="form-field"><label>Email</label><input type="email" id="edit_email"></div>
<div class="form-field"><label>Phòng ban</label><input type="text" id="edit_department"></div>
<div class="form-field"><label>Số điện thoại</label><input type="text" id="edit_phone"></div>
</div>
<div class="modal-actions"><button class="btn btn-secondary" onclick="closeModal()">Hủy</button><button class="btn btn-success" onclick="saveEdit()"><i class="fas fa-save"></i> Lưu</button></div></div></div>

<script>
{AUTH_JS}
var SVC='managers';
function load(){{fetch(API+'/'+SVC+'/').then(function(r){{return r.json()}}).then(function(d){{var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');if(!items.length){{tb.innerHTML='<tr><td colspan="7">Chưa có quản lý viên</td></tr>';return}}tb.innerHTML=items.map(function(m){{return '<tr><td><strong>#'+m.id+'</strong></td><td><strong>'+m.name+'</strong></td><td>'+m.email+'</td><td>'+(m.department||'-')+'</td><td>'+(m.phone||'-')+'</td><td>'+new Date(m.created_at).toLocaleDateString('vi-VN')+'</td><td><button class="btn btn-warning btn-sm" onclick="openEdit('+m.id+')"><i class="fas fa-edit"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+m.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('')}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="7">Lỗi</td></tr>'}})}}
function addItem(){{var data={{name:document.getElementById('name').value,email:document.getElementById('email').value,department:document.getElementById('department').value,phone:document.getElementById('phone').value}};if(!data.name||!data.email){{showMsg('Họ tên và Email là bắt buộc',false);return}}fetch(API+'/'+SVC+'/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Thêm thành công!',true);['name','email','department','phone'].forEach(function(id){{document.getElementById(id).value=''}});load()}}else{{r.json().then(function(e){{showMsg(JSON.stringify(e),false)}})}}}})}}
function openEdit(id){{fetch(API+'/'+SVC+'/'+id+'/').then(function(r){{return r.json()}}).then(function(m){{document.getElementById('edit_id').value=m.id;document.getElementById('edit_name').value=m.name||'';document.getElementById('edit_email').value=m.email||'';document.getElementById('edit_department').value=m.department||'';document.getElementById('edit_phone').value=m.phone||'';document.getElementById('editModal').classList.add('active')}}).catch(function(){{showMsg('Lỗi',false)}})}}
function closeModal(){{document.getElementById('editModal').classList.remove('active')}}
function saveEdit(){{var id=document.getElementById('edit_id').value;if(!id)return;var data={{name:document.getElementById('edit_name').value,email:document.getElementById('edit_email').value,department:document.getElementById('edit_department').value,phone:document.getElementById('edit_phone').value}};fetch(API+'/'+SVC+'/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Cập nhật thành công!',true);closeModal();load()}}else{{r.json().then(function(e){{showMsg('Lỗi: '+JSON.stringify(e),false)}})}}}})}}
function del(id){{if(!confirm('Xóa #'+id+'?'))return;fetch(API+'/'+SVC+'/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('editModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
load();
</script></body></html>'''


# ============================
# COMMENTS.HTML
# ============================
comments_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Bình luận - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('comments.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-comments"></i> Quản lý Bình luận</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a><button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-plus-circle"></i> Thêm bình luận</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Customer ID *</label><input type="number" id="customer_id" placeholder="ID khách hàng"></div>
<div class="form-field"><label>Book ID *</label><input type="number" id="book_id" placeholder="ID sách"></div>
<div class="form-field"><label>Đánh giá</label><select id="rating"><option value="5">⭐⭐⭐⭐⭐ (5)</option><option value="4">⭐⭐⭐⭐ (4)</option><option value="3">⭐⭐⭐ (3)</option><option value="2">⭐⭐ (2)</option><option value="1">⭐ (1)</option></select></div>
</div><div style="margin-top:12px"><div class="form-field"><label>Nội dung *</label><input type="text" id="content" placeholder="Nội dung bình luận..."></div></div>
<button class="btn btn-primary" style="margin-top:16px" onclick="addItem()"><i class="fas fa-plus"></i> Gửi</button></div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách bình luận</h3></div>
<table><thead><tr><th>ID</th><th>Khách hàng</th><th>Sách</th><th>Đánh giá</th><th>Nội dung</th><th>Ngày</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="7">Đang tải...</td></tr></tbody></table></div></div></div>

<div class="modal-overlay" id="editModal"><div class="modal">
<h3><i class="fas fa-edit" style="color:#f59e0b"></i> Chỉnh sửa bình luận</h3>
<input type="hidden" id="edit_id">
<div class="form-grid">
<div class="form-field"><label>Đánh giá</label><select id="edit_rating"><option value="5">⭐⭐⭐⭐⭐ (5)</option><option value="4">⭐⭐⭐⭐ (4)</option><option value="3">⭐⭐⭐ (3)</option><option value="2">⭐⭐ (2)</option><option value="1">⭐ (1)</option></select></div>
</div><div style="margin-top:12px"><div class="form-field"><label>Nội dung</label><input type="text" id="edit_content" placeholder="Nội dung bình luận..."></div></div>
<div class="modal-actions"><button class="btn btn-secondary" onclick="closeModal()">Hủy</button><button class="btn btn-success" onclick="saveEdit()"><i class="fas fa-save"></i> Lưu</button></div></div></div>

<script>
{AUTH_JS}
var SVC='comments';
function starIcons(n){{var s='';for(var i=0;i<5;i++)s+=i<n?'<i class="fas fa-star"></i>':'<i class="far fa-star"></i>';return s}}
function load(){{fetch(API+'/'+SVC+'/').then(function(r){{return r.json()}}).then(function(d){{var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');if(!items.length){{tb.innerHTML='<tr><td colspan="7">Chưa có bình luận</td></tr>';return}}tb.innerHTML=items.map(function(c){{return '<tr><td><strong>#'+c.id+'</strong></td><td>#'+c.customer_id+'</td><td>#'+c.book_id+'</td><td class="stars">'+starIcons(c.rating)+'</td><td>'+c.content+'</td><td>'+new Date(c.created_at).toLocaleDateString('vi-VN')+'</td><td><button class="btn btn-warning btn-sm" onclick="openEdit('+c.id+')"><i class="fas fa-edit"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+c.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('')}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="7">Lỗi</td></tr>'}})}}
function addItem(){{var data={{customer_id:document.getElementById('customer_id').value,book_id:document.getElementById('book_id').value,rating:document.getElementById('rating').value,content:document.getElementById('content').value}};if(!data.customer_id||!data.book_id||!data.content){{showMsg('Customer ID, Book ID và Nội dung là bắt buộc',false);return}}fetch(API+'/'+SVC+'/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Thêm thành công!',true);['customer_id','book_id','content'].forEach(function(id){{document.getElementById(id).value=''}});load()}}else{{r.json().then(function(e){{showMsg(JSON.stringify(e),false)}})}}}})}}
function openEdit(id){{fetch(API+'/'+SVC+'/'+id+'/').then(function(r){{return r.json()}}).then(function(c){{document.getElementById('edit_id').value=c.id;document.getElementById('edit_rating').value=c.rating||5;document.getElementById('edit_content').value=c.content||'';document.getElementById('editModal').classList.add('active')}}).catch(function(){{showMsg('Lỗi',false)}})}}
function closeModal(){{document.getElementById('editModal').classList.remove('active')}}
function saveEdit(){{var id=document.getElementById('edit_id').value;if(!id)return;var data={{rating:parseInt(document.getElementById('edit_rating').value),content:document.getElementById('edit_content').value}};fetch(API+'/'+SVC+'/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{if(r.ok){{showMsg('Cập nhật thành công!',true);closeModal();load()}}else{{r.json().then(function(e){{showMsg('Lỗi: '+JSON.stringify(e),false)}})}}}})}}
function del(id){{if(!confirm('Xóa #'+id+'?'))return;fetch(API+'/'+SVC+'/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('editModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
load();
</script></body></html>'''


# ============================
# ORDERS.HTML - with book images/names in detail
# ============================
orders_html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quản lý Đơn hàng - BookStore Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>{ADMIN_CSS}{LABEL_CSS}</style></head>
<body>
{sidebar('orders.html')}
<div class="main">
<div class="topbar"><h1><i class="fas fa-box"></i> Quản lý Đơn hàng</h1>
<div class="topbar-actions"><a href="/" class="btn-store"><i class="fas fa-store"></i> Cửa hàng</a><button onclick="logout()"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button></div></div>
<div class="content"><div id="msg" class="msg"></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-plus-circle"></i> Tạo đơn hàng từ giỏ</h3></div>
<div class="card-body"><div class="form-grid">
<div class="form-field"><label>Customer ID</label><input type="number" id="customer_id" placeholder="ID khách hàng"></div>
</div><button class="btn btn-primary" style="margin-top:16px" onclick="createOrder()"><i class="fas fa-shopping-bag"></i> Tạo đơn hàng</button>
<p style="margin-top:8px;color:#94a3b8;font-size:13px">Tạo đơn hàng từ giỏ hàng của khách hàng.</p></div></div>
<div class="card"><div class="card-header"><h3><i class="fas fa-list"></i> Danh sách đơn hàng</h3></div>
<table><thead><tr><th>ID</th><th>Khách hàng</th><th>Tổng tiền</th><th>Trạng thái</th><th>Ngày tạo</th><th>Thao tác</th></tr></thead>
<tbody id="tbl"><tr><td colspan="6">Đang tải...</td></tr></tbody></table></div></div></div>

<div class="modal-overlay" id="detailModal"><div class="modal">
<h3><i class="fas fa-receipt" style="color:#2563eb"></i> Chi tiết đơn hàng #<span id="detail_order_id"></span></h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
<div><strong>Khách hàng:</strong> #<span id="detail_customer"></span></div>
<div><strong>Tổng tiền:</strong> $<span id="detail_total"></span></div>
<div><strong>Trạng thái:</strong> <span id="detail_status" class="badge"></span></div>
<div><strong>Ngày tạo:</strong> <span id="detail_date"></span></div>
</div>
<h4 style="margin-bottom:10px"><i class="fas fa-list"></i> Sản phẩm trong đơn</h4>
<div id="detail_items"><em style="color:#94a3b8">Đang tải...</em></div>
<div class="modal-actions"><button class="btn btn-secondary" onclick="closeModal()">Đóng</button></div></div></div>

<script>
{AUTH_JS}
var SVC='orders';
var statusLabels={{'pending':'Chờ xử lý','paid':'Đã thanh toán','completed':'Hoàn thành','shipped':'Đã gửi','in_transit':'Đang vận chuyển','delivered':'Đã giao','cancelled':'Đã hủy','failed':'Thất bại','preparing':'Đang chuẩn bị'}};
var bookCache={{}};
function getBookInfo(bookId){{
if(bookCache[bookId])return Promise.resolve(bookCache[bookId]);
return fetch(API+'/books/'+bookId+'/').then(function(r){{if(r.ok)return r.json();return null}}).then(function(b){{if(b)bookCache[bookId]=b;return b}}).catch(function(){{return null}})}}
function load(){{
fetch(API+'/'+SVC+'/').then(function(r){{return r.json()}}).then(function(d){{
var items=Array.isArray(d)?d:(d.results||[]);var tb=document.getElementById('tbl');
if(!items.length){{tb.innerHTML='<tr><td colspan="6">Chưa có đơn hàng</td></tr>';return}}
tb.innerHTML=items.map(function(o){{
var statusOpts=['pending','paid','completed','shipped','delivered','cancelled'].map(function(s){{return '<option value="'+s+'"'+(s===o.status?' selected':'')+'>'+(statusLabels[s]||s)+'</option>'}}).join('');
return '<tr><td><strong>#'+o.id+'</strong></td><td>#'+o.customer_id+'</td><td><strong>$'+parseFloat(o.total_amount).toFixed(2)+'</strong></td><td><select class="status-select" onchange="updateStatus('+o.id+',this.value)">'+statusOpts+'</select></td><td>'+new Date(o.created_at).toLocaleDateString('vi-VN')+'</td><td><button class="btn btn-info btn-sm" onclick="viewDetail('+o.id+')"><i class="fas fa-eye"></i></button> <button class="btn btn-danger btn-sm" onclick="del('+o.id+')"><i class="fas fa-trash"></i></button></td></tr>'}}).join('')
}}).catch(function(){{document.getElementById('tbl').innerHTML='<tr><td colspan="6">Lỗi</td></tr>'}})}}
function createOrder(){{var cid=document.getElementById('customer_id').value;if(!cid){{showMsg('Vui lòng nhập Customer ID',false);return}}fetch(API+'/'+SVC+'/',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{customer_id:parseInt(cid)}})}}).then(function(r){{return r.json().then(function(d){{if(r.ok){{showMsg('Đơn hàng #'+d.id+' đã tạo! Tổng: $'+d.total_amount,true);document.getElementById('customer_id').value='';load()}}else{{showMsg(JSON.stringify(d),false)}}}})}})}}
function updateStatus(id,newStatus){{fetch(API+'/'+SVC+'/'+id+'/',{{method:'PATCH',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{status:newStatus}})}}).then(function(r){{if(r.ok)showMsg('Đã cập nhật trạng thái đơn #'+id,true);else showMsg('Lỗi cập nhật',false)}})}}
function viewDetail(id){{
fetch(API+'/'+SVC+'/'+id+'/').then(function(r){{return r.json()}}).then(function(o){{
document.getElementById('detail_order_id').textContent=o.id;
document.getElementById('detail_customer').textContent=o.customer_id;
document.getElementById('detail_total').textContent=parseFloat(o.total_amount).toFixed(2);
var st=document.getElementById('detail_status');st.textContent=statusLabels[o.status]||o.status;st.className='badge badge-'+o.status;
document.getElementById('detail_date').textContent=new Date(o.created_at).toLocaleDateString('vi-VN');
var itemsDiv=document.getElementById('detail_items');
itemsDiv.innerHTML='<em style="color:#94a3b8">Đang tải sản phẩm...</em>';
fetch(API+'/order-items/?order='+id).then(function(ir){{return ir.json()}}).then(function(id2){{
var items=Array.isArray(id2)?id2:(id2.results||[]);
if(!items.length){{itemsDiv.innerHTML='<em style="color:#94a3b8">Không có sản phẩm</em>';return}}
var promises=items.map(function(item){{return getBookInfo(item.book_id).then(function(book){{return {{item:item,book:book}}}});}});
Promise.all(promises).then(function(results){{
itemsDiv.innerHTML=results.map(function(r){{
var item=r.item;var book=r.book;
var imgHtml=book&&book.image_url?'<img src="'+book.image_url+'" onerror="this.style.display=\'none\'">':'<div style="width:48px;height:64px;background:#f1f5f9;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:20px">📖</div>';
var titleHtml=book?book.title:'Sách #'+item.book_id;
var authorHtml=book?book.author:'';
return '<div class="order-item">'+imgHtml+'<div class="oi-info"><div class="oi-title">'+titleHtml+'</div><div class="oi-sub">'+(authorHtml?authorHtml+' · ':'')+'SL: '+item.quantity+'</div></div><div class="oi-price">$'+(item.price?parseFloat(item.price).toFixed(2):'N/A')+'</div></div>'}}).join('')}})
}}).catch(function(){{itemsDiv.innerHTML='<em style="color:#94a3b8">Không thể tải sản phẩm</em>'}});
document.getElementById('detailModal').classList.add('active');
}}).catch(function(){{showMsg('Lỗi tải chi tiết',false)}})}}
function closeModal(){{document.getElementById('detailModal').classList.remove('active')}}
function del(id){{if(!confirm('Xóa đơn hàng #'+id+'?'))return;fetch(API+'/'+SVC+'/'+id+'/',{{method:'DELETE'}}).then(function(){{showMsg('Đã xóa',true);load()}})}}
document.getElementById('detailModal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
load();
</script></body></html>'''


# Write all files
files = {
    'books.html': books_html,
    'catalogs.html': catalogs_html,
    'staffs.html': staffs_html,
    'managers.html': managers_html,
    'comments.html': comments_html,
    'orders.html': orders_html,
}

for name, content in files.items():
    path = os.path.join(BASE, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {name}")

print("\nAll admin pages written successfully!")
