import streamlit as st


def render_creators():

    st.markdown(""" 
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="../css/style.css">
        <link href='https://fonts.googleapis.com/css?family=Allerta Stencil' rel='stylesheet'>
    <style>
            h1{font-display: aligncenter;
                font-family: 'Allerta Stencil';
                color: white;}
    </style>
    <h1><center>Ozone Creators</center></h1>
    </head>
    </html>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader('Rayane Mazari')
        st.image('imgs/rayane.jpg')
    with col2:
        st.subheader('Chaymae Mesbahi')
        st.image('imgs/Chaymae.jpg')
    with col3:
        st.subheader('Riyad Mazari')
        st.image('imgs/Riyad.jpg')
    with col4:
        st.subheader('Yahya Laraqui')
        st.image('imgs/yahya.jpg')

    reveal = st.button('Reveal')

    if reveal:
        st.markdown(""" 
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="../css/style.css">
        <link href='https://fonts.googleapis.com/css?family=Allerta Stencil' rel='stylesheet'>
    <style>
            h1{font-display: aligncenter;
                font-family: 'Allerta Stencil';
                color: white;}
    </style>
    <h1><center>Website QR Code</center></h1>
    </head>
    </html>
    """, unsafe_allow_html=True)
        st.balloons()
        col1, col2, col3 = st.columns([1,2,1])

        col2.image('imgs/qr-code.png')