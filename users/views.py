from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from .permissions import IsAccountOwner
from rest_framework import generics


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def update(self, request, *args, **kwargs):
        user_instance = self.get_object()
        new_pass = request.data.pop("password")
        if new_pass:
            user_instance.set_password(new_pass)
            user_instance.save()
        return super().update(request, *args, **kwargs)
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "pk"
