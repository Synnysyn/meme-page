from django.db.models.query import QuerySet
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
import pytest
from django.contrib.auth.models import User
from meme_page.models import Meme, Genre, Report, Avatar, REACTIONS

# Create your tests here.


@pytest.fixture
def user():
    u = User.objects.create_superuser(
        username="TrollUltimate", password="TrollUltimate123123"
    )
    return u


@pytest.fixture
def genre():
    g = Genre.objects.create(name="casual")
    return g


@pytest.fixture
def meme():
    u = User.objects.create_superuser(
        username="TrollUltimate", password="TrollUltimate123123"
    )
    g = Genre.objects.create(name="casual")
    m = Meme.objects.create(
        title="kappa",
        creator=u,
        image="test_meme.jpg",
    )
    m.genres.add(g)
    return m


# @pytest.fixture
# def group():
#   g = Group.objects.create(name="Any User")


@pytest.mark.django_db
def test_meme_menu(client):
    """
    testing Main menu View
    """
    response = client.get(reverse("menu", kwargs={"genre": "All"}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_meme_menu_post(meme, client):
    """
    testing Main menu View
    """
    context = {
        "filters_applied": True,
        "genre_filter": "casual",
        "react_meme_id": meme.id,
        "reaction": REACTIONS[0][1],
    }
    response = client.post(reverse("menu", kwargs={"genre": "All"}), context)
    assert response.status_code == 302


@pytest.mark.django_db
def test_meme_redirect(client):
    """
    testing Redirect View
    """
    response = client.get(reverse("index"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_meme_redirect_url(client):
    """
    testing Redirect View
    """
    response = client.get(reverse("index"))
    assert response.url == "/memes/All"


@pytest.mark.django_db
def test_meme_create_url(client):
    """
    testing Meme Create View
    """
    response = client.get(reverse("create-meme"))
    assert response.url == "/accounts/login/?next=/meme/create/"
    assert response.status_code == 302


@pytest.mark.django_db
def test_meme_create(client, user):
    """
    testing Meme create View
    """
    client.force_login(user)
    response = client.get(reverse("create-meme"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_meme_create_user(client):
    """
    testing User Create View
    """
    response = client.get(reverse("create-user"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_meme_create_new_user(client):
    """
    testing User Create View
    """
    Group.objects.create(name="Any User")
    context = {
        "username": "Troll",
        "password": "Troll123123",
        "repeat_password": "Troll123123",
        "email": "trolling@trl.tl",
    }
    response = client.post(reverse("create-user"), context)

    assert response.status_code == 302


@pytest.mark.django_db
def test_meme_create_report(meme, client):
    """
    testing Reporting View
    """
    response = client.get(reverse("create-report", kwargs={"report_id": meme.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_meme_create_new_report(meme, client):
    """
    testing Reporting View
    """
    context = {
        "report_message": "Troll",
    }
    response = client.post(
        reverse("create-report", kwargs={"report_id": meme.id}), context
    )

    r = Report.objects.filter(message="Troll", reported=meme)

    assert r != None
    assert response.status_code == 302


@pytest.mark.django_db
def test_meme_avatar(client, user):
    """
    testing Avatar change View
    """
    client.force_login(user)
    response = client.get(reverse("change-avatar"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_meme_wrong_avatar(user, client):
    """
    testing Avatar change View
    """
    context = {
        "owner": user,
        "image": "string",
    }
    avatar_count = Avatar.objects.count()
    assert avatar_count == 0

    client.force_login(user)
    response = client.post(reverse("change-avatar"), context)
    a = Avatar.objects.filter(owner=user, image="image")
    assert a.count() == 0
    assert avatar_count == 0
    assert response.status_code == 200
