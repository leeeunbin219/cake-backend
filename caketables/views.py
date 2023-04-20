from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from django.shortcuts import get_object_or_404


from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import UserTable, Visitor

from .serializers import (
    CreateTableSerializer,
    UserMiniSerializer,
    UserTableSerializer,
    VisitorMiniSerializer,
    VisitorUpdateSerializer,
    TableShowSerializer,
    VisitorSerializer,VisitorLetterSerializer,
)


# 사용자의 테이블 (모두가 볼 수 있음)
class TableShowView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        caketables = UserTable.objects.all()
        caketables_serializer = TableShowSerializer(caketables, many=True)

        response_data = "caketables", caketables_serializer.data

        return Response(response_data, status=HTTP_200_OK)


# 사용자의 테이블 생성 (로그인 한 사람만 가능)
class NewTable(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get(self, request):
    #     new_table = UserTable.objects.all()
    #     serializer = CreateTableSerializer(new_table, many=True)
    #     return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = CreateTableSerializer(data=request.data)
        if serializer.is_valid():
            new_table = serializer.save(
                owner=request.data.get("owner"),
            )
            serializer = UserTableSerializer(new_table)
            serializer.save()
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


# 케이크 생성 (visitor)
class PickCakeView(APIView):
    def get(self, request):
        visitor = Visitor.objects.all()
        serializer = VisitorSerializer(visitor, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = VisitorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "입력하신 정보를 다시 확인해주세요."},
                status=HTTP_400_BAD_REQUEST,
            )


# 케이크 수정(visitor) / 삭제(table owner, visitor)
class LetterView(APIView):
    # letter 는 table_user랑 작성한 visitor만 조회 가능
    def get(self, request, pk, format=None):
        visitor = get_object_or_404(Visitor, pk=pk)
        visitor_password = request.query_params.get("visitor_password", None)

        if request.user.is_admin or request.user == visitor.visitor_name or (visitor.visitor_password == visitor_password):
            serializer = VisitorLetterSerializer(visitor)
            return Response(serializer.data)
        else:
            return Response({"error": "비밀번호가 잘못되었습니다."}, status=HTTP_403_FORBIDDEN)


    # letter 작성은 비밀번호를 입력한 visitor만 가능
    def post(self, request, format=None):
        serializer = VisitorSerializer(data=request.data)
        visitor_password = request.data.get("visitor_password", None)

        if serializer.is_valid():
            if visitor_password:
                serializer.save(visitor_password=visitor_password)
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response({"error": "비밀번호가 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # letter 수정은 작성한 visitor만 가능
    def put(self, request, pk, format=None):
        visitor = get_object_or_404(Visitor, pk=pk)
        visitor_password = request.data.get("visitor_password", None)
        
        if visitor.visitor_password == visitor_password:
            serializer = VisitorSerializer(visitor, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "비밀번호가 잘못되었습니다."}, status=HTTP_403_FORBIDDEN)
    
    # letter 삭제는 table 주인, 작성한 visitor, 관리자(admin)만 가능
    def delete(self, request, pk, format=None):
        visitor = get_object_or_404(Visitor, pk=pk)
        visitor_password = request.data.get("visitor_password", None)
        
        if request.user.is_admin or request.user == visitor.visitor_name or (visitor.visitor_password == visitor_password):
            visitor.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "비밀번호가 잘못되었습니다."}, status=HTTP_403_FORBIDDEN)