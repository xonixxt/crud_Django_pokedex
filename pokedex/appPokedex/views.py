from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Pokemon, Treinador
from .forms import PokemonForm, TreinadorForm

import requests 


def home(request):
    return render(request, 'home.html')


def listarPokemons(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'listPokemon.html', {'pokemons': pokemons})

def criarPokemons(request):
    if request.method == "POST":
        form = PokemonForm(request.POST)
        if form.is_valid():
            novoPokemon = form.save(commit=False)
            
            nomePokemon = novoPokemon.nome.lower()
            
            url = f"https://pokeapi.co/api/v2/pokemon/{nomePokemon}/"
            response = requests.get(url)
            
            if response.status_code == 200:
                dadosPokemon = response.json()
               
                novoPokemon.imagemUrl = dadosPokemon['sprites']['front_default']
                novoPokemon.save()
                
                return redirect('listarPokemons')
            
            else:
                form.add_error('nome', f"Pokémon '{novoPokemon.nome}' não encontrado.")
                            
    else:
        form = PokemonForm()
    return render(request, 'createPokemon.html', {'form': form})


def deletarPokemon(request, pk):
    pokemon = Pokemon.objects.get(pk=pk)
    if request.method == 'POST':
        pokemon.delete()
        return redirect('listarPokemons')
    return render(request, 'confirmarDelete.html', {'pokemon': pokemon})

def atualizarPokemon(request, pk):
    pokemon = Pokemon.objects.get(pk=pk)
    if request.method == 'POST':
        form = PokemonForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('listarPokemons')
    else:
        form = PokemonForm(instance=pokemon)
        return render(request, 'createPokemon.html', {'form': form})
     
def buscarPokemons(request):
    pokemonNome = request.GET.get('nome', '').lower()
    context = {}

    if not pokemonNome:
        context['error'] = "Por favor, digite o nome de um Pokémon."
        return render(request, 'home.html', context)

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemonNome}/"
    response = requests.get(url)

    if response.status_code == 200:
        dadosPokemon = response.json()

        pokemon_data = {
            'nome': dadosPokemon['name'],
            'id': dadosPokemon['id'],
            'altura': dadosPokemon['height'] / 10.0,
            'peso': dadosPokemon['weight'] / 10.0,
            'sprite_url': dadosPokemon['sprites']['front_default'],
            'tipos': [tipo['type']['name'] for tipo in dadosPokemon['types']],
            'habilidades': [h['ability']['name'] for h in dadosPokemon['abilities']]
        }
        context['pokemon'] = pokemon_data
    else:
        context['error'] = f"Pokémon '{pokemonNome}' não encontrado. Tente novamente."

    return render(request, 'pokedex.html', context)

def listarTreinador(request):
    treinadores = Treinador.objects.all()
    return render(request, 'listTreinador.html', {'treinadores': treinadores})

def criarTreinador(request):
    if request.method == 'POST':
        form = TreinadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listarTreinador')
    else:
        form = TreinadorForm()
    return render(request, 'createTreinador.html', {'treinador': form})

def deletarTreinador(request, pk):
    treinador = Treinador.objects.get(pk=pk)
    if request.method == 'POST':
        treinador.delete()
        return redirect('listarTreinador')
    return render(request, 'confirmarDeleteTreinador.html', {'treinador': treinador})

def atualizarTreinador(request, pk):
    treinador = Treinador.objects.get(pk=pk)
    if request.method == 'POST':
        form = TreinadorForm(request.POST, instance=treinador)
        if form.is_valid():
            form.save()
            return redirect('listTreinador')
    else: 
        form = TreinadorForm(instance=treinador)
    return render(request, 'createTreinador.html', {'treinador': form})


    
    