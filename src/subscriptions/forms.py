from django import forms
from subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
	"""docstring for SubscriptionForm"""
	class Meta:
		"""docstring for Meta"""
		model = Subscription
		exclude = ('created_at',)