import re

from django import forms


PATTERN = re.compile(r'^\d{10}$')


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=(('0', False),
                                                   ('1', True)
                                                   )
                                          )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=(('0', False),
                                                ('1', True)
                                                )
                                       )

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if not data.isdigit():
            raise forms.ValidationError('Номер телефона должен содержатьтолько цифры')
        if not PATTERN.match(data):
            raise forms.ValidationError('Неверный формат номера')

        return data



# first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control',
    #                'placeholder': 'Введите Ваше имя',
    #                }
    #     )
    # )
    #
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control',
    #                'placeholder': 'Введите Вашу фамилию',
    #                }
    #     )
    # )
    #
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control',
    #                'placeholder': 'Введите Ваш телефон',
    #                }
    #     )
    # )
    #
    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=(('0', False),
    #              ('1', True)
    #              ),
    #     initial=0,
    # )
    #
    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control',
    #                'id': 'delivery-address',
    #                'rows': 2,
    #                'placeholder': 'Введите адрес доставки',
    #                }
    #     ),
    #     required=False,
    # )
    #
    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=(('0', False),
    #              ('1', True)
    #              ),
    #     initial='card',
    # )
