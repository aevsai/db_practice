import asyncio
from datetime import datetime, time
from typing import List
import streamlit as st
import pandas as pd
import numpy as np
from app.data.access import persons, movies, genres, creators, countries
from app.database import engine_, Base


def row2dict(r): return {c.name: str(getattr(r, c.name))
                         for c in r.__table__.columns}


person_dao = persons.PersonDAO()
movies_dao = movies.MovieDAO()
genres_dao = genres.GenresDAO()
creators_dao = creators.CreatorDAO()
countries_dao = countries.CountryDAO()


Base.metadata.create_all(engine_)
st.success("Database connected", icon="🟢")
st.title('Database Access Interface')
st.subheader('Made by Artem Evsikov – @aevsai')
tab_names = ['Movies', 'Creators', 'Persons', 'Genres', 'Countries']
tab_list = list(st.tabs(tab_names))
tabs = {}

countries_list = countries_dao.get_all()
countries_names = [i.get('name') for i in countries_list]
countries_names.insert(0, '')
countries_codes = [i.get('code') for i in countries_list]

genres_list = genres_dao.get_all()
genres_names = [i.get('name') for i in genres_list]
genres_names.insert(0, '')

movies_list = movies_dao.get_all()
movies_names = [i['name'] for i in movies_list]
movies_names.insert(0, '')

person_list = person_dao.get_all()
person_names = [i['names']+' '+i['surname'] for i in person_list]
person_names.insert(0, '')

for n, name in enumerate(tab_names):
    tabs[name] = tab_list[n]


def get_country(code=None, name=None):
    countries_list = countries_dao.get_all()
    countries_names = [i.get('name') for i in countries_list]
    countries_codes = [i.get('code') for i in countries_list]

    if name:
        return countries_codes[countries_names.index(name)]

    if code:
        return countries_names[countries_codes.index(code)]


def update_person(): 
    st.session_state.person = person_dao.get(st.session_state.person_id)

def update_movie(): 
    st.session_state.movie = movies_dao.get(st.session_state.movie_id)

def update_genre(): 
    st.session_state.genre = genres_dao.get(st.session_state.genre_id)

def update_creator():
    st.session_state.creator = creators_dao.get(st.session_state.creator_id)

def is_dead():
    return bool(st.session_state.person.get('day_of_death') and st.session_state.person)

def render_movies():
    data = pd.DataFrame(movies_dao.get_all(filters={'name': st.session_state.movie_search}))
    if not data.empty:
        data['duration'] = data['duration'].map(lambda x: x.strftime(format='%H:%M'))
    st.dataframe(data, use_container_width=True)

def render_countries():
    st.dataframe(countries_dao.get_all(filters={'name': st.session_state.country_search}), use_container_width=True)

def render_creators():
    data = pd.DataFrame(creators_dao.get_all())
    if not data.empty:
        data['person'] = data['person'].map(lambda x: person_names[int(x)])
        data['movie'] = data['movie'].map(lambda x: movies_names[int(x)])
    st.dataframe(data, use_container_width=True)

with tabs['Movies'] as tab:
    st.subheader("Movies")
    
    search = st.text_input('Search by name', key='movie_search')

    render_movies()

    st.subheader('Edit Movie')
    st.number_input('Movie ID', step=1, key='movie_id', on_change=update_movie)

    if 'movie' not in st.session_state.keys():
        update_movie()

    if st.session_state.movie  or st.session_state.movie_id == 0:
        with st.form('movie_'):
            id = st.number_input('ID', step=1, value=st.session_state.movie.get('id') if st.session_state.movie else -1)
            name = st.text_input('Name', value=st.session_state.movie.get('name'))
            studio = st.text_input('Studio', value=st.session_state.movie.get('studio'))
            year = st.selectbox('Year', range(1900, 2101), index=int(st.session_state.movie.get('year')-1900) if st.session_state.movie else 100)
            country = st.selectbox(
                'Country',
                countries_names,
                index=countries_codes.index(st.session_state.movie.get('country'))+1 if st.session_state.movie else 0
            )
            duration = st.time_input('Duration', value=st.session_state.movie.get('duration') if st.session_state.movie else None)
            genre = st.selectbox('Genre', genres_names, index=st.session_state.movie.get('genre') if st.session_state.movie else 0)

            movie_action = st.selectbox('Action', ['Create', 'Update', 'Delete'])
            process_movie = st.form_submit_button('Save')

            if process_movie:

                form_movie = {
                    'id': id,
                    'name': name,
                    'studio': studio,
                    'year': year,
                    'country': get_country(name=country),
                    'duration': duration,
                    'genre': genres_names.index(genre)
                }
                
                if movie_action == 'Create':
                    mov = movies_dao.create(form_movie)
                elif form_movie.get('id'):
                    if movie_action == 'Update':
                        movies_dao.update(form_movie['id'], form_movie)
                    elif movie_action == 'Delete':
                        movies_dao.delete(form_movie.get('id'))
                else:
                    st.error('Movie id not specified, can\'t process request!', icon='🚨')


with tabs['Persons'] as tab:

    st.subheader("Persons")
    pdg = st.dataframe(person_dao.get_all(), use_container_width=True)

    st.subheader('Edit Person')
    st.number_input('User ID', step=1, key='person_id', on_change=update_person)

    if 'person' not in st.session_state.keys():
        update_person()

    if st.session_state.person  or st.session_state.person_id == 0:
        with st.form("person_"):

            id = st.number_input('id', step=1, value=st.session_state.person.get('id') if st.session_state.person else -1)
            surname = st.text_input('surname', value=st.session_state.person.get('surname'))
            names = st.text_input('names', value=st.session_state.person.get('names'))
            country = st.selectbox(
                'Country',
                countries_names,
                index=countries_codes.index(st.session_state.person.get('country'))+1 if st.session_state.person else 0
            )
            birthday = st.date_input('birthday', value=datetime.strptime(str(st.session_state.person.get('birthday')), '%Y-%m-%d') if st.session_state.person else None)
            dead = st.checkbox('dead', value=True if is_dead() else False)
            date_of_death = st.date_input(
                'date_of_death', 
                disabled=not bool(is_dead()), 
                value=datetime.strptime(str(st.session_state.person.get('day_of_death')), '%Y-%m-%d') if dead else None)

            person_action = st.selectbox('Action', ['Create', 'Update', 'Delete'])
            process_person = st.form_submit_button('Save')

            if process_person:

                form_per = {
                    'id': id if person_action != 'Create' else None,
                    'surname': surname,
                    'names': names,
                    'country': get_country(name=country),
                    'birthday': birthday,
                    'day_of_death': date_of_death if dead else None
                }
                
                if person_action == 'Create':
                    pers = person_dao.create(form_per)
                elif form_per.get('id'):
                    if person_action == 'Update':
                        person_dao.update(form_per['id'], form_per)
                    elif person_action == 'Delete':
                        person_dao.delete(form_per.get('id'))
                else:
                    st.error('User id not specified, can\'t process request!', icon='🚨')


with tabs['Countries']:
    st.subheader("Countries")

    search = st.text_input('Search by name', key='country_search')
    render_countries()

with tabs['Creators']:
    st.subheader("Creators")
    render_creators()

    st.subheader('Edit Creator')
    st.number_input('Creator ID', step=1, key='creator_id', on_change=update_creator)

    if 'creator' not in st.session_state.keys():
        update_creator()

    if st.session_state.creator or st.session_state.creator_id == 0:

        with st.form("creator_"):

            id = st.number_input('id', step=1, value=st.session_state.creator.get('id') if st.session_state.creator else -1)
            movie = st.selectbox(
                'Movie',
                movies_names,
                index=st.session_state.creator.get('movie') if st.session_state.creator else 0
            )
            person = st.selectbox(
                'Person',
                person_names,
                index=st.session_state.creator.get('person') if st.session_state.creator else 0
            )
            job_title = st.text_input('Job title', value=st.session_state.creator.get('job_title'))
            role = st.text_input('Role', value=st.session_state.creator.get('role'))

            creator_action = st.selectbox('Action', ['Create', 'Update', 'Delete'])
            process_creator = st.form_submit_button('Save')

            if process_creator:

                form_creator = {
                    'id': id,
                    'movie': movies_names.index(movie),
                    'person': person_names.index(person),
                    'job_title': job_title,
                    'role': role,
                }
                
                if creator_action == 'Create':
                    pers = creators_dao.create(form_creator)
                elif form_creator.get('id'):
                    if creator_action == 'Update':
                        creators_dao.update(form_creator['id'], form_creator)
                    elif creator_action == 'Delete':
                        creators_dao.delete(form_creator.get('id'))
                else:
                    st.error('Creator id not specified, can\'t process request!', icon='🚨')


with tabs['Genres']:

    st.subheader("Genres")
    st.dataframe(genres_dao.get_all(), use_container_width=True)
    
    st.subheader("Edit Genre")
    st.number_input('Genre ID', step=1, key='genre_id', on_change=update_genre)

    if 'genre' not in st.session_state.keys():
        update_genre()

    if st.session_state.genre  or st.session_state.genre_id == 0:
        with st.form("genre_"):

            id = st.number_input('ID', step=1, value=st.session_state.genre.get('id') if st.session_state.genre else -1)
            name = st.text_input('Name', value=st.session_state.genre.get('name'))

            genre_action = st.selectbox('Action', ['Create', 'Update', 'Delete'])
            process_genre = st.form_submit_button('Save')

            if process_genre:

                form_genre = {
                    'id': id if genre_action != 'Create' else None,
                    'name': name
                }

                if genre_action == 'Create':
                    genres_dao.create(form_genre)
                elif form_genre.get('id'):
                    if genre_action == 'Update':
                        genres_dao.update(form_genre['id'], form_genre)
                    elif genre_action == 'Delete':
                        genres_dao.delete(form_genre['id'])
                else:
                    st.error('Genre id not specified, can\'t process request!', icon='🚨')
