# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 00:40:13 2021

@author: Ronald Nyasha Kanyepi
@email : kanyepironald@gmail.com
"""
import os
from datetime import datetime

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from PIL import Image
from requests.exceptions import ConnectionError


def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'logo.ico'))
    st.set_page_config(page_title='COVID-DASHBOARD', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    st.balloons()
    # I want it to show balloon when it finished loading all the configs


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def list_of_countries():
    df = pd.read_csv("./components/csv/countries.csv")
    return df["Name"].tolist()


def covid_data_menu():
    st.subheader('Covid Data Menu')
    col1, col2, col3 = st.columns([4, 4, 4])
    with col1:
        st.text_input(label="Last Updated", value=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), disabled=True)
    with col2:
        pass
    with col3:
        option = st.selectbox('please select country?', (list_of_countries()), help="Please select country")

    try:
        response = requests.get("https://disease.sh/v3/covid-19/countries/" + option)
        data = response.json()

        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Country Info")
            country_data = data.pop("countryInfo")
            longitude, latitude = country_data["long"], country_data["lat"]
            country_data.update({"country": data["country"]})
            country_data.pop("lat")
            country_data.pop("long")
            # df = pd.DataFrame.from_dict(country_data, orient="index", dtype=str, columns=['Value'])
            # st.dataframe(df)
            remote_css("")
            st.markdown(f"""
               <table class="table table-borderless">
                    <tr>
                      <td>country</td>
                      <td>{country_data["country"]}</td>
                    </tr>
                     <tr>
                      <td>flag</td>
                      <td><img src="{country_data["flag"]}" style="width:20%;height:40%"></td>
                    </tr>
                    <tr>
                      <td>iso2</td>
                      <td>{country_data["iso2"]}</td>
                    </tr>
                    <tr>
                      <td>iso3</td>
                      <td>{country_data["iso3"]}</td>
                    </tr>
               </table></br>
            """, unsafe_allow_html=True)

            st.write("Covid Statistics")
            data.pop("country")
            df_1 = pd.DataFrame.from_dict(data, orient="index", dtype=str, columns=['Value'])
            st.write(df_1)

        with col2:
            st.write("Map")
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=latitude,
                    longitude=longitude,
                    zoom=4.7,
                    pitch=50,
                )
            ))

        with st.expander('Covid 19 Prevention Tips'):
            st.subheader("Here’s what you can do to protect yourself:")
            st.markdown(f"""<p>At International Medical Corps, we’re always preparing for the unexpected—whether it’s 
            an earthquake, a hurricane or an outbreak of infectious disease. As the COVID-19 outbreak grows, 
            it’s important to know that there are many actions we can take to protect ourselves, our loved ones and 
            our communities.</p>""", unsafe_allow_html=True)

            st.subheader("Here’s what you can do to protect yourself:")
            st.markdown(f""" <ul> <li>Wash your hands frequently with soap and water for at least 20 seconds.</li> 
            <li>If soap and water are not available, use an alcohol-based hand sanitizer with at least 60% 
            alcohol.</li> <li>Avoid close contact with people who are sick.</li> <li>Especially if you’re in a 
            high-risk group, consider limiting your exposure to others, using social distancing—for example, 
            avoid large gatherings, crowds of people and frequent trips to the store.</li>
            </li>Visit your state and local public-health websites for additional guidance specific to your area.</li>
             <li>Those at higher risk for serious illness should take additional precautions.</li>
              </ul> """,unsafe_allow_html=True)

            st.markdown(f"""</br> Reference for Tips : <a href="https://internationalmedicalcorps.org/emergency-response/covid-19/coronavirus-prevention-tips/">IMC</a>""",unsafe_allow_html=True)
    except ConnectionError as e:
        st.error("There is a connection error please retry later")


def other_tab():
    st.title("Other TAB")


def main():
    config()
    st.sidebar.subheader("COVID-19 DASHBOARD")
    menu = ["COVID-19 DATA","OTHER TAB"]
    choice = st.sidebar.selectbox("", menu)
    covid_data_menu() if (choice == "COVID-19 DATA") else other_tab()


if __name__ == '__main__':
    main()
