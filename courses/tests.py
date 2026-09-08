from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, TrainerProfile
from courses.models import Category, Course, Comment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def trainer_user():
    user = User.objects.create_user(
        email="trainer@example.com", password="pass12345",
        first_name="Ali", last_name="Rezaei", role="trainer",
    )
    TrainerProfile.objects.create(user=user)
    return user


@pytest.fixture
def other_trainer_user():
    user = User.objects.create_user(
        email="other@example.com", password="pass12345",
        first_name="Sara", last_name="Ahmadi", role="trainer",
    )
    TrainerProfile.objects.create(user=user)
    return user


@pytest.fixture
def category():
    return Category.objects.create(name="Web Development")


@pytest.fixture
def course(trainer_user, category):
    return Course.objects.create(
        title="Website Design",
        category=category,
        trainer=trainer_user.trainer_profile,
        description="Learn web design",
        price=169.00,
        status=True,
    )


@pytest.mark.django_db
class TestCourseList:
    def test_list_shows_only_published_courses(self, api_client, course):
        draft = Course.objects.create(
            title="Draft Course",
            trainer=course.trainer,
            description="not published",
            price=100,
            status=False,
        )
        url = reverse("course-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        titles = [c["title"] for c in response.data]
        assert "Website Design" in titles
        assert "Draft Course" not in titles

    def test_anonymous_user_can_list_courses(self, api_client, course):
        url = reverse("course-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseCreate:
    def test_trainer_can_create_course(self, api_client, trainer_user, category):
        api_client.force_authenticate(user=trainer_user)
        url = reverse("course-list")
        response = api_client.post(url, {
            "title": "New Course",
            "category": category.id,
            "description": "desc",
            "price": "99.00",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["trainer"] == trainer_user.trainer_profile.id

    def test_student_cannot_create_course(self, api_client, category):
        student = User.objects.create_user(
            email="student@example.com", password="pass12345",
            first_name="Reza", last_name="M", role="student",
        )
        api_client.force_authenticate(user=student)
        url = reverse("course-list")
        response = api_client.post(url, {
            "title": "New Course",
            "category": category.id,
            "description": "desc",
            "price": "99.00",
        })
        assert response.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def test_anonymous_cannot_create_course(self, api_client, category):
        url = reverse("course-list")
        response = api_client.post(url, {
            "title": "New Course",
            "category": category.id,
            "description": "desc",
            "price": "99.00",
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCourseUpdate:
    def test_owner_trainer_can_update(self, api_client, trainer_user, course):
        api_client.force_authenticate(user=trainer_user)
        url = reverse("course-detail", kwargs={"slug": course.slug})
        response = api_client.patch(url, {"title": "Updated Title"})

        assert response.status_code == status.HTTP_200_OK
        course.refresh_from_db()
        assert course.title == "Updated Title"

    def test_other_trainer_cannot_update(self, api_client, other_trainer_user, course):
        api_client.force_authenticate(user=other_trainer_user)
        url = reverse("course-detail", kwargs={"slug": course.slug})
        response = api_client.patch(url, {"title": "Hacked Title"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        course.refresh_from_db()
        assert course.title != "Hacked Title"


@pytest.mark.django_db
class TestCourseViewCount:
    def test_retrieve_increments_view_count(self, api_client, course):
        url = reverse("course-detail", kwargs={"slug": course.slug})
        assert course.counted_views == 0

        api_client.get(url)
        course.refresh_from_db()
        assert course.counted_views == 1

        api_client.get(url)
        course.refresh_from_db()
        assert course.counted_views == 2


@pytest.mark.django_db
class TestComments:
    def test_anonymous_can_post_comment(self, api_client, course):
        url = reverse("course-comments", kwargs={"course_slug": course.slug})
        response = api_client.post(url, {
            "name": "Reza",
            "email": "reza@example.com",
            "message": "Great course!",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(course=course, name="Reza").exists()

    def test_comment_starts_unapproved(self, api_client, course):
        url = reverse("course-comments", kwargs={"course_slug": course.slug})
        api_client.post(url, {
            "name": "Reza", "email": "reza@example.com", "message": "hi",
        })
        comment = Comment.objects.get(name="Reza")
        assert comment.status is False