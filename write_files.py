#!/usr/bin/env python3
import os

BASE = '/Users/truongmanhtuan/django_project/assgn05v1/bookstore-micro05'

# ===== STORE.HTML =====
store_html = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Cửa hàng sách - BookStore</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:#f8fafc;color:#1e293b}
a{text-decoration:none;color:inherit}
header{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08);position:sticky;top:0;z-index:100}
.header-wrap{max-width:1280px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:24px}
.logo{font-size:24px;font-weight:800;color:#2563eb;white-space:nowrap}.logo i{margin-right:6px}
.search-box{flex:1;max-width:520px;position:relative}
.search-box input{width:100%;padding:10px 44px 10px 16px;border:2px solid #e2e8f0;border-radius:10px;font-size:14px;font-family:inherit;transition:border .2s}
.search-box input:focus{outline:none;border-color:#2563eb}
.search-box button{position:absolute;right:4px;top:4px;bottom:4px;width:36px;border:none;background:#2563eb;color:#fff;border-radius:8px;cursor:pointer}
.header-actions{display:flex;align-items:center;gap:16px}
.header-actions a,.header-actions button{background:none;border:none;color:#64748b;font-size:14px;cursor:pointer;display:flex;align-items:center;gap:6px;font-family:inherit;white-space:nowrap;transition:color .2s}
.header-actions a:hover{color:#2563eb}
.cart-badge{position:relative}
.cart-badge .count{position:absolute;top:-6px;right:-10px;background:#ef4444;color:#fff;font-size:10px;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700}
.btn-login{background:#2563eb!important;color:#fff!important;padding:8px 20px;border-radius:8px;font-weight:600}
.breadcrumb{max-width:1280px;margin:0 auto;padding:16px 24px;font-size:13px;color:#94a3b8}
.breadcrumb a{color:#64748b}.breadcrumb a:hover{color:#2563eb}
.store-layout{max-width:1280px;margin:0 auto;padding:0 24px 48px;display:grid;grid-template-columns:250px 1fr;gap:24px}
.filter-sidebar{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.06);height:fit-content;position:sticky;top:80px}
.filter-title{font-size:16px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.filter-group{margin-bottom:20px}
.filter-group h4{font-size:13px;font-weight:600;color:#64748b;text-transform:uppercase;margin-bottom:10px}
.filter-group label{display:flex;align-items:center;gap:8px;padding:6px 0;font-size:14px;cursor:pointer;color:#475569}
.filter-group label:hover{color:#2563eb}
.filter-group input[type=checkbox]{accent-color:#2563eb;width:16px;height:16px}
.cat-count{font-size:12px;color:#94a3b8;margin-left:auto}
.price-inputs{display:flex;gap:8px;align-items:center}
.price-inputs input{width:80px;padding:6px 8px;border:1px solid #e2e8f0;border-radius:6px;font-size:13px;font-family:inherit}
.btn-filter{width:100%;padding:10px;background:#2563eb;color:#fff;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:8px}
.btn-filter:hover{background:#1d4ed8}
.btn-clear{width:100%;padding:8px;background:none;border:1px solid #e2e8f0;border-radius:8px;color:#64748b;cursor:pointer;font-family:inherit;margin-top:8px;font-size:13px}
.store-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.store-toolbar .results{font-size:14px;color:#64748b}.store-toolbar .results strong{color:#1e293b}
.sort-select{padding:8px 12px;border:1px solid #e2e8f0;border-radius:8px;font-size:13px;font-family:inherit;cursor:pointer}
.view-toggle{display:flex;gap:4px}
.view-toggle button{width:36px;height:36px;border:1px solid #e2e8f0;background:#fff;border-radius:8px;cursor:pointer;color:#64748b}
.view-toggle button.active{background:#2563eb;color:#fff;border-color:#2563eb}
.catalog-section{margin-bottom:32px}
.catalog-section h2{font-size:20px;font-weight:700;color:#1e293b;margin-bottom:16px;display:flex;align-items:center;gap:10px;padding-bottom:10px;border-bottom:2px solid #e2e8f0}
.catalog-section h2 i{color:#2563eb}
.catalog-section .cat-badge{background:#eff6ff;color:#2563eb;font-size:13px;padding:4px 12px;border-radius:20px;font-weight:600}
.book-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:20px}
.book-grid.list-view{grid-template-columns:1fr}
.book-card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06);transition:all .3s;border:1px solid #f1f5f9}
.book-card:hover{transform:translateY(-4px);box-shadow:0 8px 25px rgba(0,0,0,.12)}
.book-cover{height:200px;display:flex;align-items:center;justify-content:center;font-size:48px;position:relative;overflow:hidden;background:#f8fafc}
.book-cover img{width:100%;height:100%;object-fit:cover}
.stock-badge{position:absolute;top:10px;right:10px;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;z-index:2}
.stock-ok{background:#dcfce7;color:#166534}.stock-low{background:#fef9c3;color:#854d0e}.stock-out{background:#fee2e2;color:#991b1b}
.book-info{padding:16px}
.book-info h4{font-size:15px;font-weight:600;color:#1e293b;margin-bottom:4px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.book-info .author{font-size:13px;color:#64748b;margin-bottom:4px}
.book-info .book-catalog-tag{font-size:11px;color:#6d28d9;background:#ede9fe;padding:2px 8px;border-radius:10px;display:inline-block;margin-bottom:8px}
.book-info .price-row{display:flex;align-items:center;justify-content:space-between}
.book-info .price{font-size:18px;font-weight:700;color:#dc2626}
.btn-add{width:34px;height:34px;border-radius:8px;border:none;background:#2563eb;color:#fff;cursor:pointer;font-size:14px;transition:background .2s;display:flex;align-items:center;justify-content:center}
.btn-add:hover{background:#1d4ed8}
.list-view .book-card{display:grid;grid-template-columns:140px 1fr;height:auto}
.list-view .book-cover{height:100%;min-height:160px}
.list-view .book-info{display:flex;flex-direction:column;justify-content:center}
.list-view .book-info h4{font-size:17px;-webkit-line-clamp:unset}
.list-view .book-info .author{margin-bottom:8px}
.empty-state{text-align:center;padding:60px 20px;color:#94a3b8}
.empty-state i{font-size:48px;margin-bottom:16px;display:block}
.skeleton{background:linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);background-size:200% 100%;animation:shimmer 1.5s infinite}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
@media(max-width:768px){.store-layout{grid-template-columns:1fr}.filter-sidebar{position:static}}
#toast-container{position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column-reverse;gap:10px}
.toast{display:flex;align-items:center;gap:12px;padding:14px 20px;border-radius:12px;color:#fff;font-size:14px;font-weight:500;font-family:'Inter',sans-serif;box-shadow:0 8px 32px rgba(0,0,0,.18);animation:toastIn .4s ease;min-width:280px;max-width:420px}
.toast.success{background:linear-gradient(135deg,#16a34a,#15803d)}
.toast.error{background:linear-gradient(135deg,#dc2626,#b91c1c)}
.toast.info{background:linear-gradient(135deg,#2563eb,#1d4ed8)}
.toast i{font-size:18px;flex-shrink:0}.toast .toast-msg{flex:1}
.toast .toast-close{background:none;border:none;color:rgba(255,255,255,.7);cursor:pointer;font-size:16px;padding:0 0 0 8px}
.toast .toast-close:hover{color:#fff}
.toast.hide{animation:toastOut .3s ease forwards}
@keyframes toastIn{from{opacity:0;transform:translateX(80px) scale(.95)}to{opacity:1;transform:translateX(0) scale(1)}}
@keyframes toastOut{to{opacity:0;transform:translateX(80px) scale(.95)}}
</style>
</head>
<body>
<header><div class="header-wrap">
<a href="/" class="logo"><i class="fas fa-book-open"></i>BookStore</a>
<div class="search-box"><input type="text" id="searchInput" placeholder="Tìm kiếm sách, tác giả..." onkeydown="if(event.key==='Enter')doSearch()"><button onclick="doSearch()"><i class="fas fa-search"></i></button></div>
<div class="header-actions" id="headerActions"></div>
</div></header>
<div class="breadcrumb"><a href="/"><i class="fas fa-home"></i> Trang chủ</a> &rsaquo; <strong>Cửa hàng</strong></div>
<div class="store-layout">
<aside class="filter-sidebar">
<div class="filter-title"><i class="fas fa-sliders"></i> Bộ lọc</div>
<div class="filter-group"><h4>Danh mục</h4><div id="catFilters"><div class="skeleton" style="height:100px;border-radius:8px"></div></div></div>
<div class="filter-group"><h4>Khoảng giá</h4><div class="price-inputs"><input type="number" id="priceMin" placeholder="Từ" min="0"><span>—</span><input type="number" id="priceMax" placeholder="Đến" min="0"></div></div>
<div class="filter-group"><h4>Tình trạng</h4><label><input type="checkbox" id="inStock" checked> Còn hàng</label><label><input type="checkbox" id="outStock"> Hết hàng</label></div>
<button class="btn-filter" onclick="applyFilters()"><i class="fas fa-search"></i> Áp dụng</button>
<button class="btn-clear" onclick="clearFilters()"><i class="fas fa-times"></i> Xóa bộ lọc</button>
</aside>
<main class="store-main">
<div class="store-toolbar">
<div class="results" id="resultCount">Đang tải...</div>
<div style="display:flex;gap:12px;align-items:center">
<select class="sort-select" id="sortSelect" onchange="applyFilters()"><option value="newest">Mới nhất</option><option value="price-asc">Giá: Thấp → Cao</option><option value="price-desc">Giá: Cao → Thấp</option><option value="title">Tên A-Z</option></select>
<div class="view-toggle"><button class="active" id="gridBtn" onclick="setView('grid')"><i class="fas fa-grid-2"></i></button><button id="listBtn" onclick="setView('list')"><i class="fas fa-list"></i></button></div>
</div></div>
<div id="bookContainer"><div class="book-grid">
<div class="book-card"><div class="book-cover skeleton" style="height:200px"></div><div class="book-info"><div class="skeleton" style="height:20px;border-radius:4px;margin-bottom:8px"></div><div class="skeleton" style="height:14px;width:60%;border-radius:4px"></div></div></div>
<div class="book-card"><div class="book-cover skeleton" style="height:200px"></div><div class="book-info"><div class="skeleton" style="height:20px;border-radius:4px;margin-bottom:8px"></div><div class="skeleton" style="height:14px;width:60%;border-radius:4px"></div></div></div>
</div></div>
</main></div>
<div id="toast-container"></div>
<script>
function showToast(msg,type,duration){type=type||'success';duration=duration||3000;var t=document.createElement('div');t.className='toast '+type;var icons={success:'fa-circle-check',error:'fa-circle-xmark',info:'fa-circle-info'};t.innerHTML='<i class="fas '+(icons[type]||icons.info)+'"></i><span class="toast-msg">'+msg+'</span><button class="toast-close" onclick="this.parentElement.classList.add(\'hide\');setTimeout(function(){this.parentElement.remove()}.bind(this),300)"><i class="fas fa-times"></i></button>';document.getElementById('toast-container').appendChild(t);setTimeout(function(){if(t.parentElement){t.classList.add('hide');setTimeout(function(){t.remove()},300)}},duration)}
var API='/api',token=localStorage.getItem('access_token'),userStr=localStorage.getItem('user');
var currentUser=null,allBooks=[],allCatalogs=[],catalogMap={},viewMode='grid';
var coverColors=['#dbeafe','#fce7f3','#dcfce7','#fef9c3','#f3e8ff','#ffedd5','#e0f2fe','#fae8ff'];
var coverIcons=['\ud83d\udcd6','\ud83d\udcda','\ud83d\udcd8','\ud83d\udcd7','\ud83d\udcd5','\ud83d\udcd9','\ud83d\udcd3','\ud83d\udcd4'];
function authFetch(url,opts){opts=opts||{};if(token){opts.headers=Object.assign({},opts.headers||{},{'Authorization':'Bearer '+token})}return fetch(url,opts)}
(function(){
var el=document.getElementById('headerActions');
if(token&&userStr){try{currentUser=JSON.parse(userStr)}catch(e){}}
if(currentUser){el.innerHTML='<a href="/pages/my-cart.html" class="cart-badge"><i class="fas fa-shopping-cart fa-lg"></i><span class="count" id="cartCount">0</span></a><a href="/pages/my-profile.html" style="color:#2563eb;font-weight:600"><i class="fas fa-user-circle"></i> '+(currentUser.full_name||currentUser.username)+'</a><button onclick="localStorage.clear();location.href=\'/pages/login.html\'" style="color:#ef4444"><i class="fas fa-right-from-bracket"></i></button>';loadCartCount()}
else{el.innerHTML='<a href="/pages/my-cart.html" class="cart-badge"><i class="fas fa-shopping-cart fa-lg"></i></a><a href="/pages/login.html" class="btn-login">\u0110\u0103ng nh\u1eadp</a>'}
})();
function loadCartCount(){var cid=localStorage.getItem('customer_id');if(!cid)return;authFetch(API+'/carts/customer/'+cid+'/').then(function(r){if(r.ok)return r.json()}).then(function(d){if(d){var c=document.getElementById('cartCount');if(c)c.textContent=(d.items||[]).length}}).catch(function(){})}
var params=new URLSearchParams(location.search);
if(params.get('q'))document.getElementById('searchInput').value=params.get('q');
function doSearch(){var q=document.getElementById('searchInput').value;var p=new URLSearchParams(location.search);if(q)p.set('q',q);else p.delete('q');location.search=p.toString()}
function init(){
Promise.all([authFetch(API+'/books/'),authFetch(API+'/catalogs/')]).then(function(results){
return Promise.all([results[0].json(),results[1].json()])
}).then(function(data){
var bd=data[0];allBooks=Array.isArray(bd)?bd:(bd.results||[]);
var cd=data[1];allCatalogs=Array.isArray(cd)?cd:(cd.results||[]);
catalogMap={};allCatalogs.forEach(function(c){catalogMap[c.id]=c.name});
renderCatFilters();applyFilters();
}).catch(function(){document.getElementById('bookContainer').innerHTML='<div class="empty-state"><i class="fas fa-exclamation-triangle"></i>L\u1ed7i t\u1ea3i d\u1eef li\u1ec7u</div>'})}
function renderCatFilters(){
var selCat=params.get('cat');var catCounts={};var noCatCount=0;
allBooks.forEach(function(b){if(b.catalog_id&&catalogMap[b.catalog_id]){catCounts[b.catalog_id]=(catCounts[b.catalog_id]||0)+1}else{noCatCount++}});
var html=allCatalogs.map(function(c){return '<label><input type="checkbox" value="'+c.id+'" class="cat-cb" '+(selCat==c.id?'checked':'')+'>'+c.name+' <span class="cat-count">('+( catCounts[c.id]||0)+')</span></label>'}).join('');
if(noCatCount>0)html+='<label><input type="checkbox" value="none" class="cat-cb"> Ch\u01b0a ph\u00e2n lo\u1ea1i <span class="cat-count">('+noCatCount+')</span></label>';
document.getElementById('catFilters').innerHTML=html||'<span style="color:#94a3b8;font-size:13px">Ch\u01b0a c\u00f3 danh m\u1ee5c</span>'}
function applyFilters(){
var books=allBooks.slice();
var q=(document.getElementById('searchInput').value||'').toLowerCase();
if(q)books=books.filter(function(b){return (b.title||'').toLowerCase().indexOf(q)>=0||(b.author||'').toLowerCase().indexOf(q)>=0});
var checkedCats=Array.from(document.querySelectorAll('.cat-cb:checked')).map(function(cb){return cb.value});
if(checkedCats.length>0){books=books.filter(function(b){if(checkedCats.indexOf('none')>=0&&(!b.catalog_id||!catalogMap[b.catalog_id]))return true;return checkedCats.indexOf(String(b.catalog_id))>=0})}
var pmin=parseFloat(document.getElementById('priceMin').value);var pmax=parseFloat(document.getElementById('priceMax').value);
if(!isNaN(pmin))books=books.filter(function(b){return parseFloat(b.price)>=pmin});
if(!isNaN(pmax))books=books.filter(function(b){return parseFloat(b.price)<=pmax});
var inStk=document.getElementById('inStock').checked;var outStk=document.getElementById('outStock').checked;
if(inStk&&!outStk)books=books.filter(function(b){return b.stock>0});
if(!inStk&&outStk)books=books.filter(function(b){return b.stock<=0});
var sort=document.getElementById('sortSelect').value;
if(sort==='price-asc')books.sort(function(a,b){return parseFloat(a.price)-parseFloat(b.price)});
else if(sort==='price-desc')books.sort(function(a,b){return parseFloat(b.price)-parseFloat(a.price)});
else if(sort==='title')books.sort(function(a,b){return (a.title||'').localeCompare(b.title)});
else books.sort(function(a,b){return new Date(b.created_at)-new Date(a.created_at)});
document.getElementById('resultCount').innerHTML='Hi\u1ec3n th\u1ecb <strong>'+books.length+'</strong> s\u00e1ch';
if(checkedCats.length===0||checkedCats.length>1){renderBooksGrouped(books)}else{renderBooksFlat(books)}}
function renderBooksGrouped(books){
var container=document.getElementById('bookContainer');
if(!books.length){container.innerHTML='<div class="empty-state"><i class="fas fa-search"></i><p>Kh\u00f4ng t\u00ecm th\u1ea5y s\u00e1ch ph\u00f9 h\u1ee3p</p></div>';return}
var groups={};var uncategorized=[];
books.forEach(function(b){if(b.catalog_id&&catalogMap[b.catalog_id]){if(!groups[b.catalog_id])groups[b.catalog_id]=[];groups[b.catalog_id].push(b)}else{uncategorized.push(b)}});
var html='';
allCatalogs.forEach(function(cat){if(groups[cat.id]&&groups[cat.id].length>0){html+='<div class="catalog-section"><h2><i class="fas fa-layer-group"></i> '+cat.name+' <span class="cat-badge">'+groups[cat.id].length+' s\u00e1ch</span></h2><div class="book-grid '+(viewMode==='list'?'list-view':'')+'">'+groups[cat.id].map(function(b,i){return renderBookCard(b,i)}).join('')+'</div></div>'}});
if(uncategorized.length>0){html+='<div class="catalog-section"><h2><i class="fas fa-bookmark"></i> Ch\u01b0a ph\u00e2n lo\u1ea1i <span class="cat-badge">'+uncategorized.length+' s\u00e1ch</span></h2><div class="book-grid '+(viewMode==='list'?'list-view':'')+'">'+uncategorized.map(function(b,i){return renderBookCard(b,i)}).join('')+'</div></div>'}
container.innerHTML=html}
function renderBooksFlat(books){
var container=document.getElementById('bookContainer');
if(!books.length){container.innerHTML='<div class="empty-state"><i class="fas fa-search"></i><p>Kh\u00f4ng t\u00ecm th\u1ea5y s\u00e1ch</p></div>';return}
container.innerHTML='<div class="book-grid '+(viewMode==='list'?'list-view':'')+'">'+books.map(function(b,i){return renderBookCard(b,i)}).join('')+'</div>'}
function renderBookCard(b,i){
var color=coverColors[i%coverColors.length];var icon=coverIcons[i%coverIcons.length];
var sl=b.stock>5?'<span class="stock-badge stock-ok">C\u00f2n h\u00e0ng</span>':b.stock>0?'<span class="stock-badge stock-low">S\u1eafp h\u1ebft</span>':'<span class="stock-badge stock-out">H\u1ebft h\u00e0ng</span>';
var coverInner,coverStyle;
if(b.image_url){coverInner='<img src="'+b.image_url+'" alt="'+b.title+'" onerror="this.style.display=\'none\'">'+sl;coverStyle=''}
else{coverInner=icon+sl;coverStyle=' style="background:'+color+'"'}
var catTag=b.catalog_id&&catalogMap[b.catalog_id]?'<span class="book-catalog-tag"><i class="fas fa-tag"></i> '+catalogMap[b.catalog_id]+'</span>':'';
return '<a class="book-card" href="/pages/book-detail.html?id='+b.id+'"><div class="book-cover"'+coverStyle+'>'+coverInner+'</div><div class="book-info"><h4>'+b.title+'</h4><div class="author"><i class="fas fa-user-pen"></i> '+b.author+'</div>'+catTag+'<div class="price-row"><span class="price">$'+parseFloat(b.price).toFixed(2)+'</span><button class="btn-add" onclick="event.preventDefault();addToCart('+b.id+',this)"><i class="fas fa-cart-plus"></i></button></div></div></a>'}
function clearFilters(){document.getElementById('searchInput').value='';document.getElementById('priceMin').value='';document.getElementById('priceMax').value='';document.getElementById('inStock').checked=true;document.getElementById('outStock').checked=false;Array.from(document.querySelectorAll('.cat-cb')).forEach(function(cb){cb.checked=false});document.getElementById('sortSelect').value='newest';applyFilters()}
function setView(mode){viewMode=mode;Array.from(document.querySelectorAll('.book-grid')).forEach(function(g){if(mode==='list')g.classList.add('list-view');else g.classList.remove('list-view')});if(mode==='grid'){document.getElementById('gridBtn').classList.add('active');document.getElementById('listBtn').classList.remove('active')}else{document.getElementById('gridBtn').classList.remove('active');document.getElementById('listBtn').classList.add('active')}}
function addToCart(bookId,btn){
if(!token){location.href='/pages/login.html';return}
var cid=localStorage.getItem('customer_id');
if(!cid){showToast('Vui l\u00f2ng c\u1eadp nh\u1eadt h\u1ed3 s\u01a1 kh\u00e1ch h\u00e0ng','info');setTimeout(function(){location.href='/pages/my-profile.html'},1500);return}
authFetch(API+'/customers/'+cid+'/cart/add-item/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({book_id:bookId,quantity:1})}).then(function(r){if(r.ok){loadCartCount();showToast('\ud83d\uded2 \u0110\u00e3 th\u00eam v\u00e0o gi\u1ecf h\u00e0ng!','success');if(btn){btn.innerHTML='<i class="fas fa-check"></i>';btn.style.background='#16a34a';setTimeout(function(){btn.innerHTML='<i class="fas fa-cart-plus"></i>';btn.style.background=''},1500)}}else{r.json().then(function(d){showToast(d.error||'Kh\u00f4ng th\u1ec3 th\u00eam','error')})}}).catch(function(){showToast('L\u1ed7i k\u1ebft n\u1ed1i','error')})}
init();
</script>
</body>
</html>'''

with open(os.path.join(BASE, 'api-gateway/templates/store.html'), 'w', encoding='utf-8') as f:
    f.write(store_html)
print("store.html written OK")
