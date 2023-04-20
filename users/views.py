import json
import bcrypt
import jwt
import requests

from datetime import timedelta
from config.settings import SECRET_KEY
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    SignupSerializer,
    UserDetailSerializer,
    UserSerializer,
    LoginSerializer,
)
from .models import User


# 회원가입
class SignUp(APIView):
    def get(self, request):
        return Response({"message": "이름, 이메일, 비밀번호, 생일을 입력해주세요."})

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        birthday = request.data.get("birthday")

        if not password or len(password) < 8:
            return Response({"message": "비밀번호를 8자 이상 입력해주세요."})
        serializer = SignupSerializer(data=request.data)
        
        if User.objects.filter(email=email).exists():
            return Response({"message": "이미 가입된 이메일입니다."})

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = SignupSerializer(user)

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입 성공",
                    "token": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                    },
                },
                status=HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 이메일 로그인
class Login(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            access_token = request.COOKIES.get("access")
            payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
            pk = payload.get("user_email")
            user = User.objects.get(email=pk)
            serializer = LoginSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료 시 토큰 갱신
            data = {"refresh": request.COOKIES.get("refresh", None)}
            serializer = TokenObtainPairSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get("access", None)
                refresh = serializer.data.get("refresh", None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
                pk = payload.get("user_email")
                user = get_object_or_404(User, pk=pk)
                serializer = LoginSerializer(user)
                res = Response(serializer.data, status=HTTP_200_OK)
                res.set_cookie("access", access, httponly=True)
                res.set_cookie("refresh", refresh, httponly=True)
                return res
            raise jwt.exceptions.InvalidTokenError

        except jwt.exceptions.InvalidTokenError:
            # 사용 불가능한 토큰일 때
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_401_UNAUTHORIZED)

    # 로그인
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None:
            return Response(
                {"message": "이메일과 비밀번호를 입력해주세요."}, status=HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = LoginSerializer(user)

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


# 로그아웃
class Logout(APIView):
    def post(self, request):

        # 쿠키에 저장 된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {"message": "로그아웃 되었습니다."},
            status=HTTP_202_ACCEPTED,
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


# 유저 리스트 조회
class UserList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


# 유저 정보 조회 및 삭제 (mypage)
class Mypage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)
