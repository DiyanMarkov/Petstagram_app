from django import forms

from petstagram.common.models import PhotoLike, PhotoComment
from petstagram.pets.forms import DisabledFormMixin
from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'user')


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'photo',)


class PhotoDeleteForm(DisabledFormMixin, PhotoBaseForm):

    disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()

    def save(self, commit=True):
        if commit:
            self.instance.tagged_pets.clear()  # clear() when many-to-many
            PhotoLike.objects.filter(photo_id=self.instance.id).delete() # one-to-many relation
            PhotoComment.objects.filter(photo_id=self.instance.id).delete()  # one-to-many relation
            self.instance.delete()
        else:
            pass

        return self.instance


