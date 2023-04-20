from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import UserTable, Visitor

from rest_framework import serializers


# User 간단히 조회 및 선택 시 사용
class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ("nickname",)


# visitor 간단히 조회
class VisitorMiniSerializer(ModelSerializer):
    class Meta:
        model = Visitor
        fields = ("visitor_name",)


# 모두가 볼 수 있는 user table
# [get]
class TableShowSerializer(ModelSerializer):
    # visitor = VisitorMiniSerializer()

    class Meta:
        model = UserTable
        fields = (
            "pk",
            "nickname",
            "tablecolor",
            # "visitor",
        )
        read_only_fields = "__all__"


# 유저가 테이블 생성할 때 사용
# [post]
class CreateTableSerializer(ModelSerializer):
    # owner_id = serializers.IntegerField(read_only=True)  # owner_id 필드를 추가하고, write_only=True로 설정

    class Meta:
        model = UserTable
        fields = ("id", "nickname", "tablecolor")
        read_only_fields = ("id",)


# 유저가 테이블 조회 및 삭제할 때 사용
# [get / delete]
class UserTableSerializer(ModelSerializer):
    total_visitor = SerializerMethodField()

    class Meta:
        model = UserTable
        fields = (
            "pk",
            "nickname",
            "tablecolor",
            "total_visitor",
        )
        read_only_fields = (
            "pk",
            "total_visitor",
        )

    def get_total_visitor(self, obj):
        return obj.visitors.count()


# visitor 가 테이블에 방문할 때 사용
# [get / post]
class VisitorSerializer(ModelSerializer):
    owner = UserMiniSerializer(read_only=True)

    class Meta:
        model = Visitor
        fields = (
            "pk",
            "owner",
            "pickcake",
            "letter",
            "visitor_name",
        )
        read_only_fields = ("pk",)


# visitor 가 편지를 수정 및 삭제할 때 사용
# [put / delete]
class VisitorUpdateSerializer(ModelSerializer):
    class Meta:
        model = Visitor
        fields = (
            "pk",
            "pickcake",
            "letter",
            "visitor_name",
            "visitor_password",
        )
        read_only_fields = (
            "pk",
            "pickcake",
        )


# 테이블 수정 및 삭제 시 사용
class TableSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ("nickname",)


# 편지 수정 및 삭제 시 사용
class VisitorLetterSerializer(ModelSerializer):
    owner = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = Visitor
        fields = ("id", "owner", "letter", "visitor_name")
