import streamlit as st
from api_func import *
from graph import *
import json as JSON
import time
from htbuilder import HtmlElement, div, br, hr, a, img, styles, classes, fonts
from htbuilder import p as P
from htbuilder.units import percent
from htbuilder.units import px as pix

st.title("Film Comparison App 📽️")
st.markdown("###### Please be aware that this app using IMDb API, in order to have smooth process please kindly compare the film that can be found at IMDb")

###-----------------------Choosing Film to Compare-----------------------###
id1 = st.text_input("",label_visibility="hidden",disabled=False,
                    placeholder="Insert 1st IMDb URL here"
                    )
film1,desc1 = st.columns((5,5))

with film1:
    if id1 != "":
        film_id1 = get_film_id(id1)
        image_url1, film_title1, year1, running_time1, ftype1, episodes1 = get_movie_detail(film_id1)
        good1, bad1, avg_rate1 = get_param(film_id1)
        st.image(image_url1)


with desc1:
    if id1 != "":
        st.markdown("")
        st.title(film_title1)
        st.markdown(f"### ⭐{avg_rate1}/10")
        st.markdown("")
        st.markdown("")
        st.subheader(f"✨ Type : {ftype1}")
        st.subheader(f"📅 Year : {year1}")
        st.subheader(f"🎞️ Episodes : {episodes1}")
        st.subheader(f"⏳ Duration : {running_time1} minutes")



id2 = st.text_input("",label_visibility="hidden",disabled=False,
                    placeholder="Insert 2nd IMDb URL here"
                    )
desc2,film2 = st.columns((5,5))
with film2:
    if id2 != "":
        film_id2 = get_film_id(id2)
        image_url2, film_title2, year2, running_time2, ftype2, episodes2 = get_movie_detail(film_id2)
        good2, bad2, avg_rate2 = get_param(film_id2)   
        st.image(image_url2)


with desc2:
    if id2 != "":
        st.markdown("")
        st.title(film_title2)
        st.markdown(f"### ⭐{avg_rate2}/10")
        st.markdown("")
        st.markdown("")
        st.subheader(f"✨ Type : {ftype2}")
        st.subheader(f"📅 Year : {year2}")
        st.subheader(f"🎞️ Episodes : {episodes2}")
        st.subheader(f"⏳ Duration : {running_time2} minutes")

###-----------------------Bayesian Comparison-----------------------###
if (id1 != "") and (id2 != ""):
    st.header("Bayesian Comparison on Both Movie Ratings")

    alpha1 = good1/(good1+bad1)
    beta1 = bad1/(good1+bad1)
    alpha2 = good2/(good2+bad2)
    beta2 = bad2/(good2+bad2)

    fig, probability_1_more_than_2, probability_2_more_than_1 = get_beta_dist(alpha1=alpha1,
                                                                            beta1=beta1,
                                                                            alpha2=alpha2,
                                                                            beta2=beta2,
                                                                            film_name1=film_title1,
                                                                            film_name2=film_title2
                                                                            )

    st.plotly_chart(fig)
    st.write(f"""
             Based on the sampling rating from distribution, probability you like {film_title1} more than {film_title2} is {round(probability_1_more_than_2*100,1)}%, 
             while probability you like {film_title2} more than {film_title1} is {round(probability_2_more_than_1*100,1)}%"""
             )
    winner = np.where(probability_1_more_than_2 > probability_2_more_than_1, film_title1, film_title2)
    st.markdown(f"#### Thus, from the user ratings ✨{winner}✨ is better 🏆")

###-----------------------OpenAI API Comparison-----------------------###
if (id1 != "") and (id2 != ""):
    st.header("🤔 Still Can't Decide? Let's ask GPT from OpenAI")
    st.write("")

    user_key_prompt = "Enter your OpenAI API key to get started. Keep it safe, as it'll be your key to coming back. \n\n**Friendly reminder:** GPT Lab works best with pay-as-you-go API keys. Free trial API keys are limited to 3 requests a minute. For more information on OpenAI API rate limits, check [this link](https://platform.openai.com/docs/guides/rate-limits/overview).\n\n- Don't have an API key? No worries! Create one [here](https://platform.openai.com/account/api-keys).\n- Want to upgrade your free-trial API key? Just enter your billing information [here](https://platform.openai.com/account/billing/overview)."
    placeholder = "Paste your OpenAI API key here (sk-...)"
    
    with st.container():
        st.markdown("\n")
        st.info(user_key_prompt)
        api_key_placeholder = st.text_input("Enter your OpenAI API Key", key="user_key_input", type="password", autocomplete="current-password", placeholder=placeholder)

    if api_key_placeholder != "":
        with st.spinner('Wait for it ⏱️...'):
            answer = get_chatgpt_ans(get_prompt1(film1=film_title1,film2=film_title2),api_key=api_key_placeholder)
            my_dict = JSON.loads(answer,strict=False)
            time.sleep(1)
        str1, str2 = st.columns((5,5))
        with str1:
            st.markdown(f'#### {film_title1}')
            st.markdown(f'<div style="text-align: justify;">{my_dict["synopsis1"]}</div>', unsafe_allow_html=True)
        with str2:
            st.markdown(f'#### {film_title2}')
            st.markdown(f'<div style="text-align: justify;">{my_dict["synopsis2"]}</div>', unsafe_allow_html=True)

        ###----------------------------------------Preferences Form----------------------------------------###
        st.write("")
        st.write("")
        st.header("We understand that if you still can't decided, so fill out this preferences form so we can decide which film is the most suited for you")
        
        with st.form("my_form"):
            st.header("Your Film Preferences 🤩")
            family_friendly = st.select_slider("Content of the Film",
                                            options=['Kid-Friendly','Neutral','Adult-Focused'],
                                            value='Neutral')
            tone = st.select_slider("Tone of the Film",
                                    options=['Dark','Neutral','Uplifting'],
                                    value='Neutral')
            paced = st.select_slider("Pace of the Film",
                                    options=['Slow','Neutral','Fast'],
                                    value='Neutral')
            fun = st.select_slider("Atmosphere of the Film",
                                options=['Serious','Neutral','Entertaining'],
                                value='Neutral')
            popularity = st.select_slider("Popularity of the Film",
                                        options=['Niche','Neutral','Blockbuster'],
                                        value='Neutral')
            runtime = st.select_slider("Runtime of the Film",
                                    options=['Lengthy','Neutral','Quick'],
                                    value='Neutral')
            plot = st.select_slider("Plot of the Film",
                                    options=['Simple','Neutral','Complex'],
                                    value='Neutral')
            visual = st.select_slider("Visual of the Film",
                                    options=['Minimalist','Neutral','Visually Stunning'],
                                    value='Neutral')
            submitted = st.form_submit_button("Submit")
            if submitted:
                user_preferences = {'family_friendly':family_friendly,
                                    'tone':tone,
                                    'paced':paced,
                                    'fun':fun,
                                    'popularity':popularity,
                                    'runtime':runtime,
                                    'visual':visual,
                                    'plot':plot}
            else:
                user_preferences = {}
        
        if user_preferences != {}:
            with st.spinner('Our recomendation for you is.... 🥁🥁🥁'):
                answer1 = get_chatgpt_ans(get_prompt2(film1=film_title1,
                                                    film2=film_title2,
                                                    family_friendly=user_preferences['family_friendly'],
                                                    tone=user_preferences['tone'],
                                                    paced=user_preferences['paced'],
                                                    fun=user_preferences['fun'],
                                                    popularity=user_preferences['popularity'],
                                                    runtime=user_preferences['runtime'],
                                                    plot=user_preferences['plot'],
                                                    visual=user_preferences['visual']),api_key=api_key_placeholder)
                my_dict1 = JSON.loads(answer1,strict=False)
                time.sleep(1)
            
            st.header(f'{my_dict1["film"]}🏆')
            st.markdown(f'<div style="text-align: justify;">{my_dict1["explanation"]}</div>', unsafe_allow_html=True)


###------------------------Footer------------------------###
#Footer


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style), _class='small-image')


def link(link, text, **style):
    return a(href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility:hidden;}
     .stApp { bottom: 80px;}
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=pix(0, 0, 0, 0),
        width=percent(100),
        color="grey",
        text_align="center",
        height=10,
        opacity=1
    )

    body = P()
    foot = div(
        style=style_div
    )(
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made with ❤️ by Baja Stephanus RS",
        br(),
        link("https://www.kaggle.com/bajasiagian/code", image('https://storage.scolary.com/storage/file/public/71b68248-ba0a-4b26-b15f-0c77cdf341cd.svg',width=pix(25), height=pix(25))),
        "                                                                                                ",
        link("https://www.linkedin.com/in/bajastephanus/", image('https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/2048px-LinkedIn_icon.svg.png',width=pix(25), height=pix(25))),
    ]
    layout(*myargs)
footer()
    