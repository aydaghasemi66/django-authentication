from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, StudentProfile, TrainerProfile
from courses.models import Category, Course
from order.models import Order, OrderItem, Enrollment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user():
    user = User.objects.create_user(
        email="student@example.com", password="pass12345",
        first_name="Reza", last_name="M", role="student",
    )
    StudentProfile.objects.create(user=user)
    return user


@pytest.fixture
def trainer_user():
    user = User.objects.create_user(
        email="trainer@example.com", password="pass12345",
        first_name="Ali", last_name="Rezaei", role="trainer",
    )
    TrainerProfile.objects.create(user=user)
    return user


@pytest.fixture
def course(trainer_user):
    category = Category.objects.create(name="Web Development")
    return Course.objects.create(
        title="Website Design",
        category=category,
        trainer=trainer_user.trainer_profile,
        description="Learn web design",
        price=169.00,
        status=True,
    )


@pytest.fixture
def another_course(trainer_user):
    return Course.objects.create(
        title="SEO Basics",
        trainer=trainer_user.trainer_profile,
        description="Learn SEO",
        price=99.00,
        status=True,
    )


@pytest.mark.django_db
class TestAddItem:
    def test_student_can_add_item(self, api_client, student_user, course):
        api_client.force_authenticate(user=student_user)
        url = reverse("order-add-item")
        response = api_client.post(url, {"course_id": course.id})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["total_price"] == "169.00"
        assert Order.objects.filter(student=student_user.student_profile).exists()

    def test_trainer_cannot_add_item(self, api_client, trainer_user, course):
        api_client.force_authenticate(user=trainer_user)
        url = reverse("order-add-item")
        response = api_client.post(url, {"course_id": course.id})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_add_same_course_twice(self, api_client, student_user, course):
        api_client.force_authenticate(user=student_user)
        url = reverse("order-add-item")
        api_client.post(url, {"course_id": course.id})
        response = api_client.post(url, {"course_id": course.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reuses_existing_pending_order(self, api_client, student_user, course, another_course):
        api_client.force_authenticate(user=student_user)
        url = reverse("order-add-item")
        api_client.post(url, {"course_id": course.id})
        api_client.post(url, {"course_id": another_course.id})

        orders = Order.objects.filter(student=student_user.student_profile)
        assert orders.count() == 1
        assert orders.first().items.count() == 2

    def test_invalid_course_id_rejected(self, api_client, student_user):
        api_client.force_authenticate(user=student_user)
        url = reverse("order-add-item")
        response = api_client.post(url, {"course_id": 9999})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_add_already_enrolled_course(self, api_client, student_user, course):
        Enrollment.objects.create(student=student_user.student_profile, course=course)
        api_client.force_authenticate(user=student_user)
        url = reverse("order-add-item")
        response = api_client.post(url, {"course_id": course.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCheckout:
    def test_checkout_marks_order_paid_and_creates_enrollment(self, api_client, student_user, course):
        api_client.force_authenticate(user=student_user)
        api_client.post(reverse("order-add-item"), {"course_id": course.id})
        order = Order.objects.get(student=student_user.student_profile)

        url = reverse("order-checkout", kwargs={"pk": order.id})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == "paid"
        assert Enrollment.objects.filter(
            student=student_user.student_profile, course=course
        ).exists()

    def test_cannot_checkout_empty_order(self, api_client, student_user):
        order = Order.objects.create(student=student_user.student_profile)
        api_client.force_authenticate(user=student_user)

        url = reverse("order-checkout", kwargs={"pk": order.id})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_checkout_already_paid_order(self, api_client, student_user, course):
        api_client.force_authenticate(user=student_user)
        api_client.post(reverse("order-add-item"), {"course_id": course.id})
        order = Order.objects.get(student=student_user.student_profile)

        url = reverse("order-checkout", kwargs={"pk": order.id})
        api_client.post(url)  # اولین چک‌اوت
        response = api_client.post(url)  # دومین تلاش

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_checkout_other_students_order(self, api_client, student_user, course):
        other_student = User.objects.create_user(
            email="other@example.com", password="pass12345", role="student",
        )
        StudentProfile.objects.create(user=other_student)

        api_client.force_authenticate(user=student_user)
        api_client.post(reverse("order-add-item"), {"course_id": course.id})
        order = Order.objects.get(student=student_user.student_profile)

        api_client.force_authenticate(user=other_student)
        url = reverse("order-checkout", kwargs={"pk": order.id})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMyEnrollments:
    def test_lists_only_own_enrollments(self, api_client, student_user, course):
        other_student = User.objects.create_user(
            email="other@example.com", password="pass12345", role="student",
        )
        StudentProfile.objects.create(user=other_student)
        Enrollment.objects.create(student=other_student.student_profile, course=course)
        Enrollment.objects.create(student=student_user.student_profile, course=course)

        api_client.force_authenticate(user=student_user)
        url = reverse("my-enrollments")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1