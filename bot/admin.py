from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Lesson, Video, Test

# =========================
# User Admin
# =========================
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "id",
        "username",
        "full_name",
        "phone",
        "chat_id",
        "is_staff",
        "has_paid",
        "is_watched",
    )
    search_fields = ("full_name", "username", "chat_id", "phone", "is_staff")
    list_filter = ("has_paid", "is_staff", "is_watched")
    list_editable = ("has_paid", "is_watched")
    readonly_fields = ("id", "username", "chat_id", "full_name", "phone")
    ordering = ("-date_joined",)
    list_display_links = ("full_name", "username")
    list_per_page = 25


# =========================
# Video Admin
# =========================
from django.utils.html import format_html

@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ("id", "title", "short_description", "url", "lesson_link")
    search_fields = ("title", "description", "url")
    readonly_fields = ("id",)
    ordering = ("id",)
    list_display_links = ("title",)

    def lesson_link(self, obj):
        if hasattr(obj, 'lesson'):
            return obj.lesson.title
        return "-"
    lesson_link.short_description = "Lesson"

    def short_description(self, obj):
        if obj.description:
            return (obj.description[:50] + "...") if len(obj.description) > 50 else obj.description
        return "-"
    short_description.short_description = "Description"



# =========================
# Test Admin
# =========================
@admin.register(Test)
class TestAdmin(ModelAdmin):
    list_display = (
        "id",
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_option",
        "lessons_list"
    )
    search_fields = ("question", "option_a", "option_b", "option_c", "option_d")
    list_filter = ("correct_option",)
    ordering = ("id",)
    list_display_links = ("question",)

    def lessons_list(self, obj):
        return ", ".join([lesson.title for lesson in obj.lessons.all()])
    lessons_list.short_description = "Lessons"


# =========================
# Lesson Admin
# =========================
@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ("id", "title", "video_title", "tests_list")
    search_fields = ("title",)
    readonly_fields = ("id",)
    ordering = ("id",)
    list_display_links = ("title",)

    def video_title(self, obj):
        if obj.video:
            return obj.video.title
        return "-"
    video_title.short_description = "Video"

    def tests_list(self, obj):
        return ", ".join([t.question for t in obj.tests.all()])
    tests_list.short_description = "Tests"
