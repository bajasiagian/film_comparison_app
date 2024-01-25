import requests
import numpy as np
import fnmatch
from openai import OpenAI
import streamlit as st


###--------------------IMDb API/RapidAPI--------------------###
def get_film_id(url):
    film_id = fnmatch.filter(url.split("/"), 'tt*')
    
    return film_id[0]

def get_movie_detail(film_id):
    url = "https://imdb8.p.rapidapi.com/title/get-details"

    querystring = {"tconst":film_id}

    headers = {
        "X-RapidAPI-Key": st.secrets['RAPID_API_KEY'],
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    results = response.json()

    image_url = results['image']['url']
    film_title = results['title']
    year = results['year']
    running_time = results['runningTimeInMinutes']
    film_type = np.where((results['titleType']=='tvSeries') or (results['titleType']=='tvMiniSeries'),['TV Series'],['Movie'])

    if film_type[0] == "TV Series":
        episodes = results['numberOfEpisodes']
        ftype = "TV Series"
    else:
        episodes = '-'
        ftype = "Movie"

    return image_url, film_title, year, running_time, ftype, episodes


def get_param(film_id):
    url = "https://imdb8.p.rapidapi.com/title/get-ratings"

    querystring = {"tconst":film_id}

    headers = {
        "X-RapidAPI-Key": st.secrets['RAPID_API_KEY'],
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    result = response.json()
    review_count = result["ratingsHistograms"]["IMDb Users"]["histogram"]

    alpha = review_count['6']+review_count['7']+review_count['8']+review_count['9']+review_count['10']
    beta = review_count['1']+review_count['2']+review_count['3']+review_count['4']+review_count['5']

    average_rating = result['rating']

    return alpha,beta,average_rating


###--------------------GPT/OpenAI API--------------------###

def get_prompt1(film1, film2):
    prompt = f"""
            i want to know the synopsis for {film1} and {film2}
            
            please write the resluts in this format of python dictionary, and at least in 90 words, dont change the synopsis1 and synopsis2, make the output string and just in one line (no enter):
            {'{"synopsis1":synopsis and a glimpse of review for first film,"synopsis2":synopsis and a glimpse of review for second film}'}
        """

    return prompt.replace("\n", "")


def get_prompt2(film1,film2,family_friendly,tone,paced,fun,popularity,runtime,plot,visual):
    prompt = f"""
            between this two film : {film1} and {film2}, can you give me recomendation (you can only pick one),
            which film having more {family_friendly} content, more {tone} tone, more {paced} pace, more {fun}, 
            more {popularity} in popularity, more {runtime} in runtime, more {plot} in the plot, and more{visual} for the visual

            please give me your answer in this format of python dictionary and at least in 100 words, please kep the keys of dictionary same as i wrote,
            you just need fill out the title of your recomended movie as string and your explanation why you choose that film part! make the output string and just in one line (no enter):
            {'{"film":the title of your recomended movie as string, "explanation": elaborate  why you choose that film}'}
        """
    return prompt.replace("\n", "")



def get_chatgpt_ans(prompt,api_key):
    client = OpenAI(api_key = api_key)

    stream = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}],
        stream = True,
        )

    answer = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer += chunk.choices[0].delta.content
    
    return answer