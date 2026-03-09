"""
JWT Authentication Middleware for API Gateway.
Verifies JWT tokens and enforces role-based access control.
"""
import jwt
import json
from django.http import JsonResponse

# JWT Configuration (must match auth-service)
JWT_SECRET = 'bookstore-jwt-secret-key-2024-microservices'
JWT_ALGORITHM = 'HS256'

# Public routes that don't require authentication
PUBLIC_ROUTES = [
    '/',
    '/api/auth/login/',
    '/api/auth/register/',
    '/api/auth/refresh/',
    '/pages/login.html',
    '/pages/register.html',
]

# Public prefixes (static, admin, pages that load JS which then checks auth)
PUBLIC_PREFIXES = [
    '/static/',
    '/admin/',
]

# Role-based access control rules
# Format: { 'route_prefix': { 'methods': ['allowed_roles'] } }
ROLE_PERMISSIONS = {
    # Admin-only: user management
    '/api/auth/users/': {
        'GET': ['admin', 'manager'],
        'POST': ['admin'],
        'DELETE': ['admin'],
    },
    '/api/auth/assign-role/': {
        'POST': ['admin'],
    },
    # Staff management: admin & manager only
    '/api/staffs/': {
        'GET': ['admin', 'manager', 'staff'],
        'POST': ['admin', 'manager'],
        'PUT': ['admin', 'manager'],
        'PATCH': ['admin', 'manager'],
        'DELETE': ['admin'],
    },
    # Manager management: admin only
    '/api/managers/': {
        'GET': ['admin', 'manager'],
        'POST': ['admin'],
        'PUT': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    },
    # Catalog: staff+ can modify, all authenticated can read
    '/api/catalogs/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin', 'manager'],
    },
    # Books: staff+ can modify, all authenticated can read
    '/api/books/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin', 'manager'],
    },
    # Customer management: admin/manager/staff can manage, customer can view own
    '/api/customers/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff', 'customer'],
        'PATCH': ['admin', 'manager', 'staff', 'customer'],
        'DELETE': ['admin', 'manager'],
    },
    # Cart: all authenticated users
    '/api/carts/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff', 'customer'],
        'PATCH': ['admin', 'manager', 'staff', 'customer'],
        'DELETE': ['admin', 'manager', 'staff', 'customer'],
    },
    '/api/cart-items/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff', 'customer'],
        'PATCH': ['admin', 'manager', 'staff', 'customer'],
        'DELETE': ['admin', 'manager', 'staff', 'customer'],
    },
    # Orders: all authenticated
    '/api/orders/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin'],
    },
    '/api/order-items/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin'],
    },
    # Payment: staff+ can manage
    '/api/payments/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin'],
    },
    # Shipment: staff+ can manage
    '/api/shipments/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin'],
    },
    # Comments: all authenticated
    '/api/comments/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff', 'customer'],
        'PUT': ['admin', 'manager', 'staff', 'customer'],
        'PATCH': ['admin', 'manager', 'staff', 'customer'],
        'DELETE': ['admin', 'manager', 'staff', 'customer'],
    },
    # Recommendations: all authenticated can view, staff+ can manage
    '/api/recommendations/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
        'POST': ['admin', 'manager', 'staff'],
        'PUT': ['admin', 'manager', 'staff'],
        'PATCH': ['admin', 'manager', 'staff'],
        'DELETE': ['admin', 'manager'],
    },
    '/api/recommend/': {
        'GET': ['admin', 'manager', 'staff', 'customer'],
    },
}


class JWTAuthMiddleware:
    """
    Middleware that:
    1. Allows public routes without authentication
    2. Verifies JWT token from Authorization header or cookie
    3. Enforces role-based access control on API routes
    4. Passes user info to views via request.META
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Allow public routes
        if path in PUBLIC_ROUTES or any(path.startswith(p) for p in PUBLIC_PREFIXES):
            return self.get_response(request)

        # Allow page routes (HTML pages) - auth checked client-side via JS
        if path.startswith('/pages/'):
            return self.get_response(request)

        # For API routes, check JWT token
        if path.startswith('/api/'):
            # Auth service routes (except protected ones) are public
            if path.startswith('/api/auth/') and path not in [
                '/api/auth/users/',
                '/api/auth/assign-role/',
            ] and not path.startswith('/api/auth/users/'):
                return self.get_response(request)

            # Extract token from Authorization header
            token = None
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]

            if not token:
                return JsonResponse(
                    {'error': 'Authentication required. Please provide a valid JWT token.',
                     'detail': 'Add header: Authorization: Bearer <your_token>'},
                    status=401
                )

            # Verify token
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                if payload.get('type') != 'access':
                    return JsonResponse(
                        {'error': 'Invalid token type. Use access token.'},
                        status=401
                    )
            except jwt.ExpiredSignatureError:
                return JsonResponse(
                    {'error': 'Token has expired. Please login again or refresh token.'},
                    status=401
                )
            except jwt.InvalidTokenError:
                return JsonResponse(
                    {'error': 'Invalid token.'},
                    status=401
                )

            # Store user info in request for downstream use
            request.META['USER_ID'] = str(payload.get('user_id', ''))
            request.META['USER_ROLE'] = payload.get('role', '')
            request.META['USERNAME'] = payload.get('username', '')

            # Check role-based permissions
            user_role = payload.get('role', '')
            method = request.method

            for route_prefix, permissions in ROLE_PERMISSIONS.items():
                if path.startswith(route_prefix):
                    allowed_roles = permissions.get(method, [])
                    if allowed_roles and user_role not in allowed_roles:
                        return JsonResponse(
                            {
                                'error': 'Permission denied.',
                                'detail': f'Role "{user_role}" does not have {method} access to this resource.',
                                'required_roles': allowed_roles,
                            },
                            status=403
                        )
                    break

        return self.get_response(request)
