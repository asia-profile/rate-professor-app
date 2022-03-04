from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect


class RateForm(forms.Form):
    professor_id = forms.CharField(required=True, max_length=20, label='Professor Id')
    module_code = forms.CharField(max_length=200, label='Module Code')
    rating = forms.IntegerField(required=True, label="Rating")
    message = forms.CharField(widget=forms.Textarea)


#does this part counts as client? idk, that was to be command line, so probably not
def rate(request, professor_id, module_code, year, semester, rating):
    submitted = False
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = RateForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'contact/rate_professor.html', {'form': form, 'submitted': submitted}
                  )