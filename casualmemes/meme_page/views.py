from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from .models import Genre, Meme, Reaction, Report, Avatar, REACTIONS
from .forms import CreateMemeForm, AddUserForm, AvatarChange
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def meme_cleaning(memes):
    """
    use it to change meme queryset into custom dict
    """
    clean_memes = []
    counter = 1
    for meme in memes:
        avatar = Avatar.objects.filter(owner=meme.creator)
        try:
            avatar = avatar[0]
        except IndexError:
            avatar = "static_avatar"
        clean_reactions = [
            [
                f"{REACTIONS[0][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[0][0]).count()}",
                REACTIONS[0][1],
            ],
            [
                f"{REACTIONS[1][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[1][0]).count()}",
                REACTIONS[1][1],
            ],
            [
                f"{REACTIONS[2][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[2][0]).count()}",
                REACTIONS[2][1],
            ],
            [
                f"{REACTIONS[3][1]} {Reaction.objects.filter(reaction_to=meme).filter(reaction=REACTIONS[3][0]).count()}",
                REACTIONS[3][1],
            ],
        ]

        all_genres = ["All"]
        for genre in meme.genres.all():
            all_genres.append(genre.name)

        clean_memes.append(
            {
                "avatar": avatar,
                "clean_reactions": clean_reactions,
                "meme": meme,
                "page_number": counter,
                "meme_genres": all_genres,
            }
        )
        counter += 1
    return clean_memes


def paginating(page, memes):
    """
    use it to prepare paginated page from meme queryset
    """
    clean_memes = meme_cleaning(memes)
    paginator = Paginator(clean_memes, 1)
    try:
        dict_memes = paginator.page(page)
    except PageNotAnInteger:
        dict_memes = paginator.page(1)
    except EmptyPage:
        dict_memes = paginator.page(paginator.num_pages)

    return dict_memes


class RedirectView(View):
    """
    redirects to main menu
    """

    def get(self, request):
        return redirect("menu", genre="All")


class MenuView(View):
    """
    main menu view
    """

    def get(self, request, genre):
        memes = Meme.objects.all().order_by("-added")
        genres = Genre.objects.all()
        page = request.GET.get("page", 1)
        dict_memes = paginating(page, memes)

        context = {
            "dict_memes": dict_memes,
            "genres": genres,
            "genre": genre,
        }

        return render(request, "meme_page/menu.html", context)

    def post(self, request, genre):
        if "filters_applied" in request.POST:
            try:
                genre_filter = Genre.objects.get(name=request.POST.get("genre_filter"))
                genre = genre_filter
            except ObjectDoesNotExist:
                genre = "All"

        if "react_meme_id" in request.POST:
            meme = Meme.objects.get(pk=request.POST.get("react_meme_id"))
            reactions_dict = dict(REACTIONS)
            reaction = ""
            for reaction_type in reactions_dict:
                if reactions_dict[reaction_type] in request.POST:
                    reaction = reaction_type
                    break
            try:
                react = Reaction.objects.get(
                    reaction_from=request.user, reaction_to=meme
                )
                react = Reaction.objects.filter(
                    reaction_from=request.user, reaction_to=meme
                )
                react.delete()
            except MultipleObjectsReturned:
                react = Reaction.objects.filter(
                    reaction_from=request.user, reaction_to=meme
                )
                react.delete()
            except ObjectDoesNotExist:
                pass
            except TypeError:
                return redirect("login")
            react = Reaction.objects.create(
                reaction_from=request.user, reaction_to=meme, reaction=reaction
            )

            page = int(request.POST.get("react_meme_page"))
        return redirect("menu", genre)


class MemeCreateView(PermissionRequiredMixin, View):
    """
    use it to create new memes
    """

    permission_required = "meme_page.add_meme"

    def get(self, request):
        form = CreateMemeForm()
        ctx = {"form": form}
        return render(request, "meme_page/meme_create.html", ctx)

    def post(self, request):
        form = CreateMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = Meme.objects.create(
                title=form.cleaned_data["title"],
                image=form.cleaned_data["image"],
                creator=request.user,
            )
            meme.genres.set(form.cleaned_data["genres"])
            meme.save()
            return redirect("index")
        ctx = {"form": form}
        return render(request, "meme_page/meme_create.html", ctx)


class AddUserView(FormView):
    """
    use it to create new user
    """

    form_class = AddUserForm
    template_name = "meme_page/user_add.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        group = Group.objects.get(name="Any User")
        group.user_set.add(user)
        return super().form_valid(form)


class CreateReportView(FormView):
    """
    use it to report meme
    """

    def get(self, request, report_id):
        ctx = {"report_id": report_id}
        return render(request, "meme_page/report_create.html", ctx)

    def post(self, request, report_id):
        message = request.POST["report_message"]
        reported_meme = Meme.objects.get(pk=report_id)
        Report.objects.create(message=message, reported=reported_meme)
        return redirect("index")


class AvatarChangeView(FormView):
    """
    use it to change or add avatar
    """

    def get(self, request):
        form = AvatarChange()
        ctx = {"form": form}
        return render(request, "meme_page/avatar_form.html", ctx)

    def post(self, request):
        form = AvatarChange(request.POST, request.FILES)
        if form.is_valid():
            old_avatars = Avatar.objects.filter(owner=request.user)
            old_avatars.delete()
            Avatar.objects.create(
                image=form.cleaned_data["image"],
                owner=request.user,
            )
            return redirect("index")
        ctx = {"form": form}
        return render(request, "meme_page/avatar_form.html", ctx)
