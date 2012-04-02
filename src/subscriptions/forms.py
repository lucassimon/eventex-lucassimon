# encoding: utf-8 
from django import forms
from django.utils.translation import ugettext_lazy as _
from subscriptions.validators import CpfValidator
from subscriptions.models import Subscription
from django.core.validators import EMPTY_VALUES

class PhoneWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widget = (
			forms.TextInput(attrs={'size':'2', 'maxlength':'2'}),
            forms.TextInput(attrs={'size':'15', 'maxlength':'9'}))
        super(PhoneWidget, self).__init__(widget, attrs)

    def decompress(self, value):
        if not value:
            return [None, None]

        return value.split('-')

class PhoneField(forms.MultiValueField):
	widget = PhoneWidget

	def __init__(self, *args, **kwargs):
		fields = (
        	forms.IntegerField(),
			forms.IntegerField())
		super(PhoneField, self).__init__(fields, *args, **kwargs)
	def compress(self, data_list):
		if not data_list:
			return None

		if data_list[0] in EMPTY_VALUES:
			raise forms.ValidationError(u'DDD inválido.')

		if data_list[1] in EMPTY_VALUES:
			raise forms.ValidationError(u'Número inválido.')
		return '%s-%s' % tuple(data_list)

class SubscriptionForm(forms.ModelForm):
	"""docstring for SubscriptionForm"""

	phone = PhoneField(label=_('Teleasdasdasdfone'), required=False)

	class Meta:
		"""docstring for Meta"""
		model = Subscription
		exclude = ('created_at','paid')

	# Para usar com o forms.Form
	# name =: forms.CharField(label=_('Nome'), max_length=100,)
	# cpf = forms.CharField(label=_('CPf:'), max_length=11, min_length=11, validators=[CpfValidator])
	# email = forms.EmailField(label=_('Email'))
	# phone = forms.CharField(label=_('Telefone'), max_length=100, required=False,)
	


	def _unique_check(self, fieldname, error_message=''):
		param = { fieldname: self.cleaned_data[fieldname]}
		try:
			s = Subscription.objects.get(**param)
		except Subscription.DoesNotExist:
			return self.cleaned_data[fieldname]
		raise forms.ValidationError(error_message)

	def clean_cpf(self):
		return self._unique_check('cpf',_(u'CPF ja inscrito.'))

	def clean_email(self):
		return self._unique_check('email',_(u'E-mail ja inscrito.'))

	def clean(self):
		super(SubscriptionForm,self).clean()

		if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
			raise forms.ValidationError(
				_(u'Voce precisa informar seu e-mail ou seu telefone.')
			)
		return self.cleaned_data
