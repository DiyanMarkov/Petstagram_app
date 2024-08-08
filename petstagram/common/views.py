from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
import pyperclip

from petstagram.common.forms import PhotoCommentForm, SearchPhotosForm
from petstagram.common.models import PhotoLike
from petstagram.common.utils import get_photo_url
from petstagram.core.photo_utils import apply_likes_count, apply_user_liked_photo
from petstagram.photos.models import Photo


def index(request):
    search_form = SearchPhotosForm(request.GET)
    search_pattern = None

    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['user_name']

    photos = Photo.objects.all()
    comment_form = PhotoCommentForm()

    if search_pattern:
        # photos = photos.filter(tagged_pets__name__icontains=search_pattern)
        photos = photos.filter(user__username__icontains=search_pattern)

    photos = [apply_likes_count(photo) for photo in photos]
    photos = [apply_user_liked_photo(photo) for photo in photos]

    context = {
        'photos': photos,
        'comment_form': comment_form,
        'search_form': search_form,

    }
    return render(request, 'common/home-page.html', context=context)


@login_required
def like_photo(request, photo_id):
    user_liked_photos = PhotoLike.objects.filter(
        photo_id = photo_id,
        user_id=request.user.pk
    )

    if user_liked_photos:
        user_liked_photos.delete()

    else:
        PhotoLike.objects.create(
            photo_id=photo_id,
            user_id=request.user.pk,
        )

    return redirect(get_photo_url(request, photo_id))


@login_required
def share_photo(request, photo_id):

    relative_url = resolve_url('details photo', photo_id)
    absolute_url = request.build_absolute_uri(relative_url)
    pyperclip.copy(absolute_url)

    return redirect(get_photo_url(request, photo_id))


# @login_required
# def comment_photo(request, photo_id):
#
#     photo = Photo.objects.filter(pk=photo_id).get()
#
#     form = PhotoCommentForm(request.POST)
#
#     if form.is_valid():
#         comment = form.save(commit=False) # Does not save to DataBase because of comment=False and only returns us the object
#         comment.photo = photo
#         comment.user = request.user
#         comment.save()
#
#     return redirect('index')


@login_required
def comment_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.method == 'POST':
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            return redirect('index')

    return redirect('index')