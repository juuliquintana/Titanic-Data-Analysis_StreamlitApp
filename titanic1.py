import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components


st.set_page_config(page_title="Titanic", layout="wide" , initial_sidebar_state="expanded" , page_icon="🚢")

@st.cache_resource
def cargar_datos():
    return pd.read_csv('csv/titanic_clean.csv')

def cargar_datos_originales():
    return pd.read_csv('csv/titanic.csv')

# load the data
datos = cargar_datos()
datos_originales = cargar_datos_originales()

#make the sidebar
st.sidebar.image('fotos/titanic_original.jpg', width=300)
opcion = st.sidebar.radio(
    "Select a section:",
    ["Welcome","Inicio","Dataset","Passengers","Age", "Survivor", "Fare","Conclusion"]
)
st.sidebar.header("Filtros")

st.markdown(
    """
    <style>
    .title {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: white;
        text-align: center;
        font-size: 4em;
        margin-bottom: 0.5em;
    }
    .header {
        font-family: 'Calibri', sans-serif;
        color: #6A5ACD;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .subheader {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: beige;
        text-align: center;
        font-size: 2em;
        margin-bottom: 0.5em;
    }
    .subsubheader {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: #778899;
        text-align: center;
        font-size: 1.5em;
        margin-bottom: 0.5em;
    }
    .subsubheader_sidebar {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: #778899;
        font-size: 1.5em;
        margin-bottom: 0.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# add "Todos" to the list of options
def agregar_todos(lista): 
    return ["Todos"] + list(lista)

filtros = { 
    'Sex': st.sidebar.multiselect("Sex:", options=agregar_todos(datos['Sex'].unique()), default=["Todos"]),
    'Title': st.sidebar.multiselect("Title:", options=agregar_todos(datos['Title'].unique()), default=["Todos"])
    
}

# function to apply the filters
def aplicar_filtros(df, filtros): 
    for col, val in filtros.items():
        if "Todos" not in val:
            df = df[df[col].isin(val)]
        else :
            df = df
    return df

datos_filtrados = aplicar_filtros(datos, filtros) 


def portada():
    st.markdown('<div class="title"> Welcome to a analysis from the </div>', unsafe_allow_html=True)
    st.image('fotos/titulo.jpg', use_column_width=True, width=500)
    
def mostrar_inicio(): 
    st.markdown('<div class="title">TITANIC</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">And no, its not about James Cameron movie</div>', unsafe_allow_html=True)
    st.image('fotos/titanicpeli.jpg', use_column_width=False, width=500)
    st.markdown('<div class="subheader">Its a data analysis from the real passengers of the titanic</div>', unsafe_allow_html=True)
    st.image('fotos/titanic_original.jpg', use_column_width=False, width=500)
    
def mostrar_ambos_datasets():
    tab1, tab2, tab3, tab4 = st.tabs(["Original dataset", "Columns transformation", "Null values", "Modified dataset"])
    with tab1:
        st.markdown('<div class="subheader">Original dataset</div>', unsafe_allow_html=True)
        st.dataframe(datos_originales)  

    with tab2:
        st.markdown('<div class="subheader">Columns transformation</div>', unsafe_allow_html=True)
        st.text("Build the following columns:")
        st.text("- Title: Extracted from the Name column, and then the values were grouped into Miss, Mrs and Mr categories")
        st.code("""
        df["Title"]=df["Name"].apply(lambda x: x.split(',')[1].split('.')[0])
        unique_titles = df['Title'].unique()
        df.replace(to_replace = [' Mlle', ' Ms',' Miss'], value = 'Miss', inplace = True)
        df.replace(to_replace = [' Mme', ' Mrs'], value = 'Mrs', inplace = True)
        df.replace(to_replace = [' Don',' Sir',' Mr'],value='Mr',inplace=True)
                """, language="python")
        st.text("- FamilySize: Sum of SibSp and Parch columns, plus 1 and then drop the SibSp and Parch columns")
        st.code("""
        df["FamilySize"] = df["SibSp"] + df["Parch"] + 1 
        df = df.drop(columns = ["SibSp", "Parch"])
                """, language="python")
        st.text("- Update_fare: Multiply the Fare column by 98.4 and round it to 1 decimal place, to convert it to actual currency")
        st.code("""df["Update_fare"]=df["Fare"].apply(lambda x: x * 98.4).round(1)""", language="python")
        st.text("- Survived: Se cambió el valor de 1 y 0 por Yes y No")
        st.code("""df["Survived"] = df["Survived"].replace({0: "No", 1: "Yes"})""", language="python")
        
    with tab3:
        st.markdown('<div class="subheader">Handling null values</div>', unsafe_allow_html=True)
        st.text("The following changes were made to the dataset:")
        st.text("- The Cabin and Embarked columns were filled with the value 'Unknown'")
        st.code("""
                df.fillna({'Cabin':'Unknown'}, inplace=True)
                df,fillna({'Embarked':'Unknown'}, inplace=True) """, language="python")
        st.text("- The Age column was filled with the median value of the Title group")
        st.code("""
        median_ages = df.groupby('Title')['Age'].median()
        #define a function that will impute the age of the missing values
        def impute_age(row):
            if pd.isna(row['Age']):
                title = row['Title']
                return median_ages[title]
            else:
                return row['Age']
        
        df['Age'] = df.apply(impute_age, axis=1)""", language="python")
    
    with tab4:
        st.markdown('<div class="subheader">Modified dataset</div>', unsafe_allow_html=True)
        st.dataframe(datos_filtrados) 



# function to show the passengers
def mostrar_pasajeros():
    # Insert containers separated into tabs:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Number of passengers",
                                "By class",
                            "By sex",
                            "By title",
                            "They travel alone?"])
    
    with tab1:    
        fig = go.Figure()
        area = go.Indicator( mode = "number", value = datos_filtrados["PassengerId"].count(), name = "Passenger on the Titanic" )
        fig.add_trace(area)
        fig.update_layout(template = "plotly_dark")
        st.plotly_chart(fig, use_container_width=False, width=400)

    with tab2:
        
        datos_filtrados['Pclass'] = datos_filtrados['Pclass'].astype(str)
        total_passengers_by_class = datos_filtrados.groupby(['Pclass']).size().reset_index(name='Total Passengers')
        fig = px.bar(total_passengers_by_class, x='Pclass', y='Total Passengers', 
                title='Total passengers by class', 
                labels={'Pclass':'Class', 'Total Passengers':'Total passengers'}, 
                template='plotly_dark',
                color='Pclass',
                color_discrete_map= {"1":"#48C9B0 ", "2":"#5499C7", "3":"#AF7AC5 "})
        st.plotly_chart(fig, use_container_width=True)    
        
        
        col1, col2, col3 = st.columns([1,3,1])
        with col1:
                st.write("")
            
        with col2:
                with open ('fotos/passengers_by_class.html', encoding="utf-8") as file6:
                            html_str6 = file6.read()
                components.html(html_str6, height=600, scrolling=False)
            
        with col3:
                st.write("")
    
    with tab3:
        
        col1, col2, col3 = st.columns([1,3,1])

        with col1:
            st.write("")

        with col2:
            
            with open('fotos/passxsex.html', encoding="utf-8") as file7:
                html_str7 = file7.read()
            components.html(html_str7, height=700, scrolling=False)

        with col3:
            st.write("")
                
    
    with tab4: 
        
        with open('fotos/passxtitulo.html', encoding="utf-8") as file1:
            html_str1 = file1.read()
        components.html(html_str1, height=1000, scrolling=False)
        
    
    with tab5:
        
        total_passengers_by_family_size = datos_filtrados.groupby('FamilySize').size().reset_index(name='Total Passengers').sort_values(by='Total Passengers', ascending=False).head(8)
        fig = px.bar(total_passengers_by_family_size, x="FamilySize", y="Total Passengers",
                title="They travell alone?", labels={"FamilySize":"Family size", "Total Passengers":"Number of passengers"},
                template="plotly_dark", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
 
# function to show the ages   
def mostrar_edades():
    
    with open('fotos/histograma.html', encoding="utf-8") as file8:
        html_str8 = file8.read()  
    components.html(html_str8, height=600, scrolling=False)
    
    
    
    with open('fotos/edadvstitulo.html', encoding="utf-8") as file2:
            html_str2 = file2.read()
    components.html(html_str2, height=600, scrolling=False)

# function to show the survivors 
def mostrar_sobrevivientes():
    st.markdown('<div class="subheader">Survivors</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Survivors",
                                    "By sex",
                                    "By title",
                                    "By class"])
    with tab1:
        
        with open('fotos/sobrevivientes.html', encoding="utf-8") as file9:
            html_str9 = file9.read()
        components.html(html_str9, height=600, scrolling=False)
        
    
    with tab2:
        
        fig = px.treemap(datos_filtrados, path=["Survived", "Sex"], title="Distribution of passengers survived by sex", 
                    template="plotly_dark", width=800, height=600, color="Survived", 
                    color_discrete_map = {"No":"#707B7C" , "Yes":"#1ABC9C" })
        st.plotly_chart(fig, use_container_width=True)
        
    
    with tab3:
        
        fig = px.treemap(datos_filtrados, path=["Survived","Title"], title="Distribution of passengers survived by title", template="plotly_dark",
                width=1000, height=800, color="Survived", color_discrete_map = {"No":"#707B7C" , "Yes":"#1ABC9C" })
        st.plotly_chart(fig, use_container_width=True)
        
    
    with tab4:
        
        with open('fotos/sobrevivientesxclase.html', encoding="utf-8") as file12:
            html_str12 = file12.read()
        components.html(html_str12, height=400, scrolling=False)
        
        
        with open('fotos/pie_chart_class.html', encoding="utf-8") as file10:
            html_str10 = file10.read()
        components.html(html_str10, height=400, scrolling=False)
    
# function to show the fares   
def mostrar_tarifas():
    st.markdown('<div class="subheader">Fares</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Max and min fare", "By class"])
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            st.header("Max value of fare")
            df_pagado = datos_filtrados[(datos_filtrados["Update_fare"] > 0)]
            max_fare = df_pagado["Update_fare"].max()
            fig = go.Figure()
            area = go.Indicator(
                            mode = "number",
                            value = max_fare,
                            number = {"prefix": "£", "valueformat": ".0f"},  
                            name = "Max fare"
                            )
            fig.add_trace(area)
            fig.update_layout(template = "plotly_dark")
            st.plotly_chart(fig, use_container_width=False, width=400)
        
        with col2:
            st.header("Min value of fare")
            fig = go.Figure()
            area = go.Indicator( mode = "number", value = df_pagado["Update_fare"].min(), name = "Min fare", number = {"prefix": "£", "valueformat": ".0f"}  )
            fig.add_trace(area)
            fig.update_layout(template = "plotly_dark")
            st.plotly_chart(fig, use_container_width=False, width=400)
    
    with tab2:
        
        with open('fotos/farexclass.html', encoding="utf-8") as file13:
            html_str13 = file13.read()
        components.html(html_str13, height=600, scrolling=False)
        st.plotly_chart(fig, use_container_width=True)
    
    
def conclusion():
    st.markdown('<div class="subheader">Conlusion</div>', unsafe_allow_html=True)
    st.write("When we think of the Titanic, iconic and often somber images come to mind. Yet, the stories of the individuals aboard this ship over 112 years ago remain relatively unknown. Today, we have explored some of these stories and uncovered intriguing facts about this tragic voyage.")
    st.write("Our analysis, based on the dataset from Kaggle, provided insights into the demographics and fate of the Titanic passengers. We discovered that the dataset, while comprehensive, does not encompass all passengers aboard the ship. Nevertheless, it allowed us to answer fundamental questions: How many passengers were there? How many survived? Were there more men than women? What happened to the children?")
    st.write("Interestingly, we found that a famous phrase about ships holds true here, underscoring the realities of maritime disasters. Through data analysis and visualization, we commemorated the lives lost and gained a deeper understanding of the events surrounding the Titanic’s voyage.")
    st.write("In conclusion, this exploration serves as a reminder of the human stories behind historical events, shedding light on the lives affected by one of the most notable maritime disasters in history.")
    st.image('fotos/memorial.jpg', use_column_width=True, width=500)
    
# dictionary to call the functions
opciones = {
    "Welcome": portada,
    "Inicio": mostrar_inicio,
    "Passengers": mostrar_pasajeros,
    "Age": mostrar_edades, 
    "Survivor": mostrar_sobrevivientes,
    "Fare": mostrar_tarifas,
    "Dataset": (mostrar_ambos_datasets),
    "Conclusion": conclusion
}

opciones[opcion]() # call the function


