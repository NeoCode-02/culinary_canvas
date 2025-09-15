from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.core.cache import cache
from .models import CustomUser
from .serializers import UserRegisterSerializer, VerifyEmailSerializer, ResendCodeSerializer, LoginSerializer, UserProfileSerializer
from .tasks import send_verification_email

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_verified=False)
        send_verification_email.delay(user.id)

        return Response(
            {"message": "Registration code sent to your email. Check your email for a verification code."},
            status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer  
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")

        if not email or not code:
            return Response(
                {"error": "Email and code are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response({"message": "Email is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the code from the cache using the user's ID
            cached_code = cache.get(f"verification_code_{user.id}")

            if cached_code and cached_code == code:
                user.is_verified = True
                user.save()
                # Delete the code from the cache after successful verification
                cache.delete(f"verification_code_{user.id}")
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ResendVerificationCodeView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResendCodeSerializer

    def post(self, request, *args, **kwargs):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        email = sz.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # do NOT reveal whether the e-mail exists
            return Response(
                {"detail": "If the e-mail is registered, a new code has been sent."},
                status=status.HTTP_200_OK
            )

        if user.is_verified:
            return Response(
                {"detail": "E-mail is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # optional: simple rate-limit – 1 resend per minute
        rate_limit_key = f"resend_limit_{user.id}"
        if cache.get(rate_limit_key):
            return Response(
                {"detail": "Please wait a minute before requesting a new code."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        cache.set(rate_limit_key, True, 60)  # 60 s

        # delete any previous code and send a fresh one
        cache.delete(f"verification_code_{user.id}")
        send_verification_email.delay(user.id)   # same task you already wrote

        return Response(
            {"detail": "A new verification code has been sent to your e-mail."},
            status=status.HTTP_200_OK
        )


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def update(self, request, *args, **kwargs):
        # Handle file upload
        if 'profile_picture' in request.FILES:
            # Remove old profile picture if exists
            user = self.get_object()
            if user.profile_picture:
                user.profile_picture.delete(save=False)
        
        return super().update(request, *args, **kwargs)