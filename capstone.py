import streamlit as st
from chatbot import predict_class, get_response, intents 


st.title("Asistente Virtual - Venta de Verduras") 

if "mesagges" not in st.session_state:
    st.session_state.mesagges = [] ## se almacena el historial del chatbot.
if "first_mesagge" not in st.session_state:
    st.session_state.first_mesagge = True ## Si es la primera vez que se utiliza por algun cliente el chatbot.
    
for mesagge in st.session_state.mesagges:
    with st.chat_message(mesagge["role"]): ## define el rol del chat entre USER y CHATBOT.
        st.markdown(mesagge["content"])

if st.session_state.first_mesagge:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿Como puedo ayudarte?")

        st.session_state.mesagges.append({"role": "assistant", "content": "Hola, ¿Como puedo ayudarte?"})  ##Se utiliza append por cada vez que se registre un mensaje y este quede en el historial
        st.session_state.first_mesagge = False
 
if prompt := st.chat_input("¿Como puedo ayudarte?"):  ##Se creara el prompt
    
    with st.chat_message("user"):  
        st.markdown(prompt)
    st.session_state.mesagges.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)
    
    with st.chat_message("assistant"):
        st.markdown(res)  
    st.session_state.mesagges.append({"role": "asistant", "content": res})
    