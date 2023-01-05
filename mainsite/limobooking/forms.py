from django import forms


class ReservationForm(forms.Form):
    """ This class creates the form for the reservations """

    destination = forms.CharField(
        label='Destination', max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control'}),
    )

    departureDate = forms.DateField(
        label='Date de départ:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            })
    )

    hoursList = [
        ('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'),
        ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'),
        ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'),
        ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
        ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'),
        ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')
    ]
    hour = forms.ChoiceField(
        label='Heure:',
        choices=hoursList,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            })
    )

    minutesList = [('00', '00'), ('20', '20'), ('40', '40')]
    minute = forms.ChoiceField(
        label='Minutes:',
        choices=minutesList,
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            })
    )

    sharingList = [('Oui', 'Oui'), ('Non', 'Non')]
    sharing = forms.ChoiceField(
        label='Partage de course:',
        choices=sharingList,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            })
    )

    firstname = forms.CharField(
        label='Prénom:',
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'size': '25',
            })
    )

    lastname = forms.CharField(
        label='Nom de famille:',
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'size': '25',
            })
    )

    email = forms.EmailField(
        label='Email:',
        max_length=40,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'size': '30',
            })
    )


class SearchForm(forms.Form):
    """ This class creates a form to find a booking """

    departureDate = forms.DateField(
        label='Date de départ:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            })
    )

    email = forms.EmailField(
        label='Email:',
        max_length=40,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'size': '30',
            })
    )


