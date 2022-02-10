import datetime
from django import forms
from applications.alumniprofile.models import Profile, Constants, Batch
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from crispy_forms.bootstrap import InlineRadios
import re
# --------------------------------REGISTRATION FORMS FOR STUDENTS AND ALUMNI START--------------------------------------------------------
class Alumni_NewRegister(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
    )
    date_of_joining = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address', }
        ),
        max_length=4000,
        required=False,
    )
    country = forms.ChoiceField(widget=forms.Select(
        attrs={'id': 'countryId', 'class': 'countries order-alpha presel-IN custom-select', 'name': 'country'}))
    state = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'stateId', 'class': 'states order-alpha custom-select', 'name': 'state'}))
    city = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'cityId', 'class': 'cities order-alpha custom-select', 'name': 'city'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}), required=False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}), required=False)
    # checkbox_terms = forms.BooleanField(required=True)
    instagram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Instagram Username'}), required=False)
    checkbox_update = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Mother's Name"
        self.fields['spouse_name'].label = "Spouse's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
        # self.fields['checkbox_terms'].label = 'I abide by the Terms and Conditions of the SAC'
        self.fields[
            'checkbox_update'].label = 'I will update my information at regular intervals and will engage in the Alumni network actively.'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('name', css_class="form-control", wrapper_class='col-md-5'),
                Field('fathers_name', css_class="form-control", wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('sex', css_class="custom-select", wrapper_class="col-md-5"),
                Field('spouse_name', css_class="form-control", wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('alternate_email', css_class="form-control", wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('date_of_birth', css_class="form-control", wrapper_class='col-md-4'),
                Field('year_of_admission', css_class="custom-select", wrapper_class='col-md-4'),
                Field('batch', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('branch', css_class="custom-select", wrapper_class="col-md-5"),
                Field('programme', css_class="custom-select", wrapper_class="col-md-5"),
                css_class='form-row my-3',
            ),
            Div(
                Field('mobile1', css_class="form-control", wrapper_class='col-md-5'),
                Field('mobile2', css_class="form-control", wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            Div(
                Field('country', wrapper_class="col-md-4"),
                Field('state', wrapper_class="col-md-4"),
                Field('city', wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('permanent_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            InlineRadios('working_status'),
            Div(
                Field('current_position', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_organisation', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('date_of_joining', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('past_experience', css_class="form-control", wrapper_class="col-md-6 col-lg-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_course', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_university', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                css_class='form-row my-3',
            ),
            Div(
                Field('linkedin', css_class="form-control", wrapper_class='col-md-6'),
                Field('website', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('facebook', css_class="form-control", wrapper_class='col-md-6'),
                Field('instagram', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Field('profile_picture', css_class="w-100"),
            # 'profile_picture',
            'checkbox_update',
            Submit('submit', 'Register'),
        )

    def clean(self):
        super(Alumni_NewRegister, self).clean()  # if necessary
        del self._errors['country']
        del self._errors['city']
        del self._errors['state']
        return self.cleaned_data

    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'year_of_admission',
            'mobile1',
            'mobile2',
            'facebook',
            'instagram',
            'name',
            'fathers_name',
            'spouse_name',
            'sex',
            'alternate_email',
            'date_of_birth',
            'date_of_joining',
            'working_status',
            'branch',
            'programme',
            'batch',
            'current_address',
            'permanent_address',
            'current_position',
            'current_organisation',
            'past_experience',
            'current_course',
            'current_university',
            'linkedin',
            'website',
            'profile_picture',
            'checkbox_update']

        widgets = {
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }


class Student_NewRegister(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
    )
    date_of_joining = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address', }
        ),
        max_length=4000,
        required=False,
    )
    country = forms.ChoiceField(widget=forms.Select(
        attrs={'id': 'countryId', 'class': 'countries order-alpha presel-IN custom-select', 'name': 'country'}))
    state = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'stateId', 'class': 'states order-alpha custom-select', 'name': 'state'}))
    city = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'cityId', 'class': 'cities order-alpha custom-select', 'name': 'city'}))
    linkedin = forms.URLField(widget=forms.TextInput(
        attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(
        attrs={'placeholder': 'Website'}), required=False)
    facebook = forms.URLField(widget=forms.TextInput(
        attrs={'placeholder': 'Facebook URL'}), required=False)
    # checkbox_terms = forms.BooleanField(required=True)
    instagram = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Instagram Username'}), required=False)
    checkbox_update = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Mother's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
        # self.fields['checkbox_terms'].label = 'I abide by the Terms and Conditions of the SAC'
        self.fields[
            'checkbox_update'].label = 'I will update my information at regular intervals and will engage in the Alumni network actively.'
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            Div(
                Field('name', css_class="form-control",wrapper_class='col-md-5'),
                Field('fathers_name', css_class="form-control",wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('alternate_email', css_class="form-control",wrapper_class='col-md-5'),
                Field('sex', css_class="custom-select",wrapper_class="col-md-5"),
                css_class='form-row my-3',
            ),
            Div(
                Field('date_of_birth', css_class="form-control",
                      wrapper_class='col-md-4'),
                Field('year_of_admission', css_class="custom-select",
                      wrapper_class='col-md-4'),
                Field('batch', css_class="custom-select",
                      wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('branch', css_class="custom-select",
                      wrapper_class="col-md-5"),
                Field('programme', css_class="custom-select",
                      wrapper_class="col-md-5"),
                css_class='form-row my-3',
            ),
            Div(
                Field('mobile1', css_class="form-control",
                      wrapper_class='col-md-5'),
                Field('mobile2', css_class="form-control",
                      wrapper_class='col-md-5'),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_address', css_class="form-control",
                      wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            Div(
                Field('country', wrapper_class="col-md-4"),
                Field('state', wrapper_class="col-md-4"),
                Field('city', wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('permanent_address', css_class="form-control",
                      wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            Div(
                Field('linkedin', css_class="form-control",
                      wrapper_class='col-md-6'),
                Field('website', css_class="form-control",
                      wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('facebook', css_class="form-control",
                      wrapper_class='col-md-6'),
                Field('instagram', css_class="form-control",
                      wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Field('profile_picture', css_class="w-100"),
            # 'profile_picture',
            'checkbox_update',

            Submit('submit', 'Register'),
        )

    def clean(self):
        super(Student_NewRegister, self).clean()  # if necessary
        del self._errors['country']
        del self._errors['city']
        del self._errors['state']
        return self.cleaned_data

    class Meta:
        model = Profile

        fields = [
            'name',
            'city',
            'country',
            'state',
            'year_of_admission',
            'mobile1',
            'mobile2',
            'facebook',
            'instagram',
            'alternate_email',
            'fathers_name',
            'sex',
            'date_of_birth',
            'branch',
            'programme',
            'batch',
            'current_address',
            'checkbox_update',
            'permanent_address',
            'linkedin',
            'website',
            'profile_picture']

# --------------------------------REGISTRATION FORMS FOR STUDENTS AND ALUMNI END--------------------------------------------------------

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('batch', css_class='form-group col-md-4 mb-0'),
                Column('programme', css_class='form-group col-md-4 mb-0'),
                Column('branch', css_class='form-group col-md-4 mb-0'),
                css_class='form-row my-3'
            ),
            Submit('submit', 'Search', css_class=''),
        )

    class Meta:
        model = Profile
        fields = ['batch', 'programme', 'branch']


class ProfileEdit(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=True,
    )
    date_of_joining = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address', }
        ),
        max_length=4000,
        required=False,
    )
    country = forms.CharField(widget=forms.Select(
        attrs={'id': 'countryId', 'class': 'countries order-alpha custom-select', 'name': 'country'}))
    state = forms.CharField(
        widget=forms.Select(attrs={'id': 'stateId', 'class': 'states order-alpha custom-select', 'name': 'state'}))
    city = forms.CharField(
        widget=forms.Select(attrs={'id': 'cityId', 'class': 'cities order-alpha custom-selects', 'name': 'city'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}), required=False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}), required=False)
    instagram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Instagram Username'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Mother's Name"
        self.fields['spouse_name'].label = "Husband's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['phone_no'].label = 'Phone No.'
        self.fields['roll_no'].label = 'Roll No.'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('roll_no', css_class="form-control", wrapper_class='col-md-4'),
                Field('name', css_class="form-control", wrapper_class='col-md-4'),
                Field('sex', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('fathers_name', css_class="form-control", wrapper_class='col-md-6'),
                Field('spouse_name', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('date_of_birth', css_class="form-control", wrapper_class='col-md-4'),
                Field('year_of_admission', css_class="custom-select", wrapper_class='col-md-4'),
                Field('batch', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('branch', css_class="custom-select", wrapper_class="col-md-6"),
                Field('programme', css_class="custom-select", wrapper_class="col-md-6"),
                css_class='form-row my-3',
            ),
            Div(
                Field('mobile1', css_class="form-control", wrapper_class='col-md-4'),
                Field('mobile2', css_class="form-control", wrapper_class='col-md-4'),
                Field('phone_no', css_class="form-control", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('email', css_class="form-control", wrapper_class='col-md-6'),
                Field('alternate_email', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            Div(
                Field('country', wrapper_class="col-md-4"),
                Field('state', wrapper_class="col-md-4"),
                Field('city', wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('permanent_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            InlineRadios('working_status'),
            Div(
                Field('current_position', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_organisation', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('date_of_joining', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('past_experience', css_class="form-control", wrapper_class="col-md-6 col-lg-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_course', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_university', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                css_class='form-row my-3',
            ),
            Div(
                Field('linkedin', css_class="form-control", wrapper_class='col-md-6'),
                Field('website', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('facebook', css_class="form-control", wrapper_class='col-md-6'),
                Field('instagram', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Field('profile_picture', css_class="w-100"),
            # 'profile_picture',
            Submit('submit', 'Save Changes'),
        )
        # def clean(self):

    #     super(ProfileEdit, self).clean() #if necessary
    #     del self._errors['country']
    #     del self._errors['city']
    #     del self._errors['state']
    #     return self.cleaned_data

    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'year_of_admission',
            'alternate_email',
            'phone_no',
            'mobile1',
            'mobile2',
            'facebook',
            'instagram',
            'name',
            'fathers_name',
            'spouse_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'date_of_joining',
            'working_status',
            'branch',
            'programme',
            'batch',
            'current_address',
            'permanent_address',
            'phone_no',
            'current_position',
            'current_organisation',
            'past_experience',
            'current_course',
            'current_university',
            'linkedin',
            'website',
            'profile_picture']

        widgets = {
            # 'name': forms.TextInput(attrs={ 'readonly':'readonly'}),
            # 'sex': forms.TextInput(attrs={ 'readonly':'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'roll_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'year_of_admission': forms.TextInput(attrs={'readonly': 'readonly'}),
            'branch': forms.TextInput(attrs={'readonly': 'readonly'}),
            'programme': forms.TextInput(attrs={'readonly': 'readonly'}),
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }


class NewRegister(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
    )
    date_of_joining = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False,
    )
    current_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Address'}
        ),
        max_length=4000,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Enter Permanent Address', }
        ),
        max_length=4000,
        required=False,
    )
    country = forms.ChoiceField(widget=forms.Select(
        attrs={'id': 'countryId', 'class': 'countries order-alpha presel-IN custom-select', 'name': 'country'}))
    state = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'stateId', 'class': 'states order-alpha custom-select', 'name': 'state'}))
    city = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'cityId', 'class': 'cities order-alpha custom-select', 'name': 'city'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin URL'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Website'}), required=False)
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook URL'}), required=False)
    # checkbox_terms = forms.BooleanField(required=True)
    instagram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Instagram Username'}), required=False)
    checkbox_update = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fathers_name'].label = "Father/Mother's Name"
        self.fields['spouse_name'].label = "Husband's Name"
        self.fields['mobile1'].label = "Mobile No."
        self.fields['mobile2'].label = "Alternate Mobile No."
        self.fields['batch'].label = 'Year of Passing'
        self.fields['sex'].label = 'Gender'
        self.fields['phone_no'].label = 'Phone No.'
        self.fields['roll_no'].label = 'Roll No.'
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['year_of_admission'].label = 'Year of Admission'
        self.fields['alternate_email'].label = 'Alternate Email'
        # self.fields['checkbox_terms'].label = 'I abide by the Terms and Conditions of the Alumni Cell'
        self.fields[
            'checkbox_update'].label = 'I will update my information at regular intervals and will engage in the Alumni network actively.'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('roll_no', css_class="form-control", wrapper_class='col-md-4'),
                Field('name', css_class="form-control", wrapper_class='col-md-4'),
                Field('sex', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('fathers_name', css_class="form-control", wrapper_class='col-md-6'),
                Field('spouse_name', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('date_of_birth', css_class="form-control", wrapper_class='col-md-4'),
                Field('year_of_admission', css_class="custom-select", wrapper_class='col-md-4'),
                Field('batch', css_class="custom-select", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('branch', css_class="custom-select", wrapper_class="col-md-6"),
                Field('programme', css_class="custom-select", wrapper_class="col-md-6"),
                css_class='form-row my-3',
            ),
            Div(
                Field('mobile1', css_class="form-control", wrapper_class='col-md-4'),
                Field('mobile2', css_class="form-control", wrapper_class='col-md-4'),
                Field('phone_no', css_class="form-control", wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('email', css_class="form-control", wrapper_class='col-md-6'),
                Field('alternate_email', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            Div(
                Field('country', wrapper_class="col-md-4"),
                Field('state', wrapper_class="col-md-4"),
                Field('city', wrapper_class="col-md-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('permanent_address', css_class="form-control", wrapper_class='col-md'),
                css_class='form-row my-3',
            ),
            InlineRadios('working_status'),
            Div(
                Field('current_position', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_organisation', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('date_of_joining', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('past_experience', css_class="form-control", wrapper_class="col-md-6 col-lg-4"),
                css_class='form-row my-3',
            ),
            Div(
                Field('current_course', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                Field('current_university', css_class="form-control", wrapper_class='col-md-6 col-lg-4'),
                css_class='form-row my-3',
            ),
            Div(
                Field('linkedin', css_class="form-control", wrapper_class='col-md-6'),
                Field('website', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Div(
                Field('facebook', css_class="form-control", wrapper_class='col-md-6'),
                Field('instagram', css_class="form-control", wrapper_class='col-md-6'),
                css_class='form-row my-3',
            ),
            Field('profile_picture', css_class="w-100"),
            # 'profile_picture',
            'checkbox_update',
            Submit('submit', 'Register'),
        )

    def clean(self):
        super(NewRegister, self).clean()  # if necessary
        del self._errors['country']
        del self._errors['city']
        del self._errors['state']
        return self.cleaned_data

    class Meta:
        model = Profile

        fields = [
            'city',
            'country',
            'state',
            'year_of_admission',
            'alternate_email',
            'phone_no',
            'mobile1',
            'mobile2',
            'facebook',
            'instagram',
            'name',
            'fathers_name',
            'spouse_name',
            'sex',
            'email',
            'roll_no',
            'date_of_birth',
            'date_of_joining',
            'working_status',
            'branch',
            'programme',
            'batch',
            'current_address',
            'permanent_address',
            'phone_no',
            'current_position',
            'current_organisation',
            'past_experience',
            'current_course',
            'current_university',
            'linkedin',
            'website',
            'profile_picture']

        widgets = {
            'working_status': forms.RadioSelect(choices=Constants.WORKING_STATUS),
        }


class SignUp(UserCreationForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter your roll number'}))
    email = forms.EmailField(label='Enter email', widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email'}))
    password1 = forms.CharField(
        label='Enter password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Reenter your password'}))
    user_type = forms.ChoiceField(choices=(('A', 'Alumni'), ('S', 'Student')))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if re.findall("iiitdmj.ac.in$", email):
            raise ValidationError(
                "Institute email id is not accepted.Kindly enter your personal email id.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        r = User.objects.filter(username=username)
        match = re.search('20\w\w\w\d\d\d', username)
        match2 = re.search('20\d\d\d\d\d', username)
        if(match == match2 == None):
            raise ValidationError(
                'Please enter your institute roll number.'
            )
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
class PasswordResetRequestForm(forms.Form):
    roll_no = forms.IntegerField(label=("Roll No."))
    email = forms.CharField(label=("Email"), max_length=254)
