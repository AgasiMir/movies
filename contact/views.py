from django.views.generic import CreateView

from contact.forms import ContactForm

from .models import Contact


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/mistake.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
