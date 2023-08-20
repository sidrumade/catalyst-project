from django import forms
from .models import Company
from allauth.account.forms import SignupForm
    
    
    
class CompanyModelForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['industry'] = forms.ChoiceField(choices=self.get_industry_choices())
        self.fields['size_range'] = forms.ChoiceField(choices=self.get_size_range_choices())
        self.fields['locality'] = forms.ChoiceField(choices=self.get_locality_choices())
        self.fields['country'] = forms.ChoiceField(choices=self.get_country_choices())
        
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['industry'].widget.attrs['class'] = 'form-select'
        self.fields['size_range'].widget.attrs['class'] = 'form-select'
        self.fields['locality'].widget.attrs['class'] = 'form-select'
        self.fields['country'].widget.attrs['class'] = 'form-select'
        
        
        
    def get_industry_choices(self):
        return [(industry, industry) for industry in Company.objects.values_list('industry', flat=True).distinct().filter(industry__startswith = 'information')]

    def get_size_range_choices(self):
        return [(size_range, size_range) for size_range in Company.objects.values_list('size_range', flat=True).distinct()]

    def get_locality_choices(self):
        return [(locality, locality) for locality in Company.objects.values_list('locality', flat=True).distinct().filter(locality__startswith = 'new')]

    def get_country_choices(self):
        return [(country, country) for country in Company.objects.values_list('country', flat=True).distinct().filter(country__startswith = 'united')]

    
    class Meta:
        model = Company
        fields = ["industry","size_range" , "locality" , "country","name"]
        






class CustomUserCreationForm(SignupForm):
    # Add any additional fields you want for user creation
    # For example:
    # phone_number = forms.CharField(max_length=15)

    def save(self, request):
        # Override the save method to create the user
        user = super().save(request)
        # Perform any additional actions if needed
        return user
