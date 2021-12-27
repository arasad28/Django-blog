from django import forms
from core.models import Comments,Post
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content=forms.CharField(widget=CKEditorWidget(attrs={
        'required':False,
        'col':'30',
        'rows':'10'
    }))
    class Meta:
        model=Post
        fields=Post
        fields=('title','overview','content','category')

class CommentForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'id':'exampleFormControlTextarea6',
        'placeholder':"Write something here...",
        'rows':'5'
    }))
    
    class Meta:
        model=Comments
        fields=('content',)



