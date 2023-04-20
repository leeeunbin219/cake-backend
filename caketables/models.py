from colorfield.fields import ColorField
from django.core.validators import RegexValidator

from django.db import models
from users.models import User


# 생일자가 고르는 테이블
class UserTable(models.Model):
    owner = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        blank=False,
        related_name="usertables",
    )

    nickname = models.CharField(
    max_length=7,
    default="",
    blank=False,
    null=False,
    )

    tablecolor = ColorField(
        default="#000000",
        help_text="케이크를 전시할 테이블 색상을 선택하세요.",
    )

    
    def total_visitor(self):
        return self.visitors.count()

    def __str__(self):
        return f"{self.owner}"


# 방문자의 케이크 선택 및 편지 작성
class Visitor(models.Model):
    owner = models.ForeignKey(
        "UserTable",
        on_delete=models.CASCADE,
        # blank=False,
        related_name="visitors",
    )

    pickcake = models.PositiveIntegerField(
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
            (11, "11"),
            (12, "12"),
        ],
        default=1,
        blank=False,
        null=False,
    )

    letter = models.TextField(
        max_length=50,
        blank=False,
        null=False,
        help_text="생일 축하 메세지를 입력하세요.",
    )
    
    visitor_name = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        help_text="방문자의 이름을 입력하세요.",
    )

    visitor_password = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        validators=[RegexValidator(r"^\d{4}$", "비밀번호는 4자리 숫자로 이루어져야합니다.")],
        help_text="비밀번호는 4자리 숫자로 이루어져야합니다.",
    )

    def __str__(self) -> str:
        return self.visitor_name
