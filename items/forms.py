from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ("thumbnail", "item_name", "comment", "description")
        widgets = {
            "thumbnail": forms.ClearableFileInput(attrs={"formnovalidate":"formnovalidate", "class":"form-control", "id":"name", "placeholder":"商品画像", "data-validation-required-message":"Please enter your image."}),
            "item_name": forms.TextInput(attrs={"class":"form-control", "id":"name", "type":"text", "placeholder":"商品名(50文字)", "required":"required", "data-validation-required-message":"Please enter your name."}),
            "comment": forms.TextInput(attrs={"class":"form-control", "id":"name", "type":"text", "placeholder":"ひとこと紹介(50文字)", "required":"required", "data-validation-required-message":"Please enter your name."}),
            "description": forms.Textarea(attrs={"class":"form-control", "id":"message", "rows":"3", "placeholder":"詳しい商品説明", "required":"required", "data-validation-required-message":"Please enter your name."}),
        }
    
    def clean(self):
        item_name = self.cleaned_data.get("item_name")
        comment = self.cleaned_data.get("comment")
        description = self.cleaned_data.get("description")
        
        if not item_name:
            raise forms.ValidationError("商品名を入力してください")
        if not comment:
            raise forms.ValidationError("ひとこと紹介を入力してください")
        if not description:
            raise forms.ValidationError("詳しい商品説明を入力してください")
