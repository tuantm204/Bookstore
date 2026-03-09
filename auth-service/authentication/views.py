import jwt
import datetime
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ChangePasswordSerializer, AssignRoleSerializer
)


def generate_tokens(user):
    """Generate access and refresh JWT tokens."""
    now = datetime.datetime.utcnow()
    access_payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'full_name': user.full_name,
        'type': 'access',
        'iat': now,
        'exp': now + datetime.timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRY),
    }
    refresh_payload = {
        'user_id': user.id,
        'username': user.username,
        'type': 'refresh',
        'iat': now,
        'exp': now + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRY),
    }
    access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return access_token, refresh_token


@api_view(['POST'])
def register(request):
    """Register a new user."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        access_token, refresh_token = generate_tokens(user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """Login with username and password."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is deactivated'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token, refresh_token = generate_tokens(user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_token(request):
    """Refresh access token using refresh token."""
    token = request.data.get('refresh_token')
    if not token:
        return Response(
            {'error': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get('type') != 'refresh':
            return Response(
                {'error': 'Invalid token type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            return Response(
                {'error': 'Account is deactivated'},
                status=status.HTTP_403_FORBIDDEN
            )

        access_token, new_refresh_token = generate_tokens(user)
        return Response({
            'access_token': access_token,
            'refresh_token': new_refresh_token,
        })
    except jwt.ExpiredSignatureError:
        return Response(
            {'error': 'Refresh token has expired. Please login again.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def verify_token(request):
    """Verify access token and return user info. Used by API Gateway."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Authorization header must be: Bearer <token>'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get('type') != 'access':
            return Response(
                {'error': 'Invalid token type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            return Response(
                {'error': 'Account is deactivated'},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            'valid': True,
            'user': UserSerializer(user).data,
        })
    except jwt.ExpiredSignatureError:
        return Response(
            {'error': 'Token has expired'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def me(request):
    """Get current user profile from token."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = User.objects.get(id=payload['user_id'])
        return Response(UserSerializer(user).data)
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['PUT'])
def change_password(request):
    """Change password for authenticated user."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def assign_role(request):
    """Assign a role to a user (admin only)."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        requesting_user = User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Only admin can assign roles
    if requesting_user.role != 'admin':
        return Response(
            {'error': 'Permission denied. Admin role required.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AssignRoleSerializer(data=request.data)
    if serializer.is_valid():
        try:
            target_user = User.objects.get(id=serializer.validated_data['user_id'])
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        target_user.role = serializer.validated_data['role']
        target_user.save()
        return Response({
            'message': f'Role updated to {target_user.role}',
            'user': UserSerializer(target_user).data,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_users(request):
    """List all users (admin/manager only)."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        requesting_user = User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if requesting_user.role not in ('admin', 'manager'):
        return Response(
            {'error': 'Permission denied. Admin or Manager role required.'},
            status=status.HTTP_403_FORBIDDEN
        )

    users = User.objects.all().order_by('-created_at')
    return Response(UserSerializer(users, many=True).data)


@api_view(['DELETE'])
def deactivate_user(request, user_id):
    """Deactivate a user (admin only)."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        requesting_user = User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if requesting_user.role != 'admin':
        return Response(
            {'error': 'Permission denied. Admin role required.'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if target_user.id == requesting_user.id:
        return Response(
            {'error': 'Cannot deactivate yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    target_user.is_active = False
    target_user.save()
    return Response({
        'message': f'User {target_user.username} has been deactivated',
        'user': UserSerializer(target_user).data,
    })
