from django import forms
from .models import Pokemon, Treinador

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ["nome", "tipo", "peso", "altura"]
        
class TreinadorForm(forms.ModelForm):
    class Meta:
        model = Treinador
        fields = ["nome", "idade"]
        

        
        
        