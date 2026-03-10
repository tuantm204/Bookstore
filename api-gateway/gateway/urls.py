from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Auth page routes
    path('pages/login.html', views.login_page, name='login-page'),
    path('pages/register.html', views.register_page, name='register-page'),
    # Customer storefront routes
    path('pages/store.html', views.store_page, name='store-page'),
    path('pages/book-detail.html', views.book_detail_page, name='book-detail-page'),
    path('pages/my-cart.html', views.my_cart_page, name='my-cart-page'),
    path('pages/my-orders.html', views.my_orders_page, name='my-orders-page'),
    path('pages/my-profile.html', views.my_profile_page, name='my-profile-page'),
    path('pages/checkout.html', views.checkout_page, name='checkout-page'),
    # Admin routes
    path('pages/admin.html', views.admin_page, name='admin-page'),
    # Legacy page routes
    path('pages/books.html', views.books_page, name='books-page'),
    path('pages/cart.html', views.cart_page, name='cart-page'),
    path('pages/customers.html', views.customers_page, name='customers-page'),
    path('pages/staffs.html', views.staffs_page, name='staffs-page'),
    path('pages/managers.html', views.managers_page, name='managers-page'),
    path('pages/catalogs.html', views.catalogs_page, name='catalogs-page'),
    path('pages/orders.html', views.orders_page, name='orders-page'),
    path('pages/payments.html', views.payments_page, name='payments-page'),
    path('pages/shipments.html', views.shipments_page, name='shipments-page'),
    path('pages/comments.html', views.comments_page, name='comments-page'),
    path('pages/recommender.html', views.recommender_page, name='recommender-page'),
    # Auth API proxy routes (must be before general proxy)
    re_path(r'^api/auth/(?P<path>.*)$', views.auth_proxy, name='auth-proxy'),
    # API proxy routes
    re_path(r'^api/(?P<service>[\w-]+)/(?P<path>.*)$', views.proxy, name='proxy'),
    re_path(r'^api/(?P<service>[\w-]+)/$', views.proxy, name='proxy-root'),
]
