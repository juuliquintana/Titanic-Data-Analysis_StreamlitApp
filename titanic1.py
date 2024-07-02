import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(page_title="Titanic", layout="wide" , initial_sidebar_state="expanded" , page_icon="🚢")

st.markdown('<div class="title">Titanic Dataset Analysis</div>', unsafe_allow_html=True)

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
    ["Welcome","Dataset","Passengers","Age", "Survivor", "Fare", "Conclusion"]
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
        font-size: 3em;
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
        color: white;
        text-align: center;
        font-size: 1.5em;
        margin-bottom: 0.5em;
    }
    .subsheader {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: #778899;
        text-align: center;
        font-size: 1.25em;
        margin-bottom: 0.5em;
    }
    .subsubheader {
        font-family: 'Calibri', sans-serif;
        font-weight: bold;
        color: #778899;
        text-align: center;
        font-size: 1em;
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
    
    st.markdown("""
        <div class="subsheader">
        In this app, we are going to learn more about the real passengers of the Titanic. Many of us know about the movie, but it's important to remember what happened to the real passengers. Who were they? What were their stories?
        <br>
        Come and discover this journey together!
        </div>
        """, unsafe_allow_html=True)


    st.image("fotos/titulo.jpg", use_column_width=True, width=220)



# function to show the passengers
def mostrar_pasajeros():
    # Insert containers separated into tabs:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Number of passengers",
                                "By class",
                            "By sex",
                            "By title",
                            "¿They travel alone?"])
    
    with tab1: 
        st.markdown('<div class="subsubheader">How many passangers were there?</div>', unsafe_allow_html=True)
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
            datos_filtrados['Pclass'] = datos_filtrados['Pclass'].astype(str)
            fig= px.pie(datos_filtrados, names="Pclass", title="Passengers by class", template='plotly_dark', color="Pclass", color_discrete_map= {"1":"#48C9B0 ", "2":"#5499C7", "3":"#AF7AC5 "})
            fig.update_traces(textfont=dict(color="black"))
            fig.update_layout(width=500, height=500)
            fig.write_html("passengers_by_class.html")
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
                st.markdown("""
    <div class="subsubheader">
        In this section, we can see the distribution of passengers by class. The majority of passengers were in third class, followed by first and second class.
    </div>
""", unsafe_allow_html=True)

    
    with tab3:
        
        col1, col2, col3 = st.columns([1,3,1])

        with col1:
            st.write("")

        with col2:
            
            fig = px. pie(datos_filtrados,names="Sex", title="Distribution of passengers by sex", template="plotly_dark",
                            width=500, height=500,color="Sex" ,color_discrete_map = {"male":"#F4D03F" , "female":"#58D68D " })
            fig.update_traces(textfont=dict(color="black"))
            fig.write_html("passxsex.html")
            fig

        with col3:
            st.markdown('<div class="subsubheader">We can see that the majority of passengers was male.</div>', unsafe_allow_html=True)
    
    with tab4: 
        col1, col2 = st.columns([4,1])
        with col1:
            total_passengers_by_title = datos_filtrados.groupby('Title').size().reset_index(name='Total Passengers').sort_values(by='Total Passengers', ascending=False). head(8)

            fig = px.bar(total_passengers_by_title, x='Title', y='Total Passengers', 
                            title="Number of passengers by title", 
                        labels={'Title':'Title', 'Total Passengers':'Total passengers'},
                        template='plotly_dark',
                        color='Title',
                        color_discrete_sequence= ['#d78f88', '#7f7287', '#5b7a8e', 'silver', 'gold', 'lightblue', 'lightgreen', 'lightcoral'], height=600, width=800)
            fig.write_html("passxtitulo.html")
            fig
        with col2:
            st.markdown("")

    
    with tab5:
        
        total_passengers_by_family_size = datos_filtrados.groupby('FamilySize').size().reset_index(name='Total Passengers').sort_values(by='Total Passengers', ascending=False).head(8)
        fig = px.bar(total_passengers_by_family_size, x="FamilySize", y="Total Passengers",
                title="¿They travell alone?", labels={"FamilySize":"Family size", "Total Passengers":"Number of passengers"},
                template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel1)
        st.plotly_chart(fig, use_container_width=True)

# function to show the ages   
def mostrar_edades():
    
    col1, col2 = st.columns([3,1])
    with col1:
            fig = px.histogram(datos_filtrados, x='Age', title='Age distribution of passengers', template='plotly_dark',
                    width=800, height=600, color_discrete_sequence=px.colors.qualitative.Light24_r, marginal='box')
            fig.write_html("histograma.html")
            fig
            
    with col2:
            st.markdown("""
    <div class="subsubheader">
        While analyzing the ages of the Titanic passengers, it's interesting to consider the life expectancy during that era. At the beginning of the 20th century, life expectancy was around 47 years for men and 50 years for women, significantly lower than today's average. This context can influence how we interpret the ages of the passengers and their life expectancies in that historical context.
    </div>
""", unsafe_allow_html=True)
            

    fig = px.box(datos_filtrados, x= "Title",y="Age", title="Age distribution by title", 
            template="plotly_dark", width=800, height=600, color="Title", 
            color_discrete_sequence= ['#d78f88', '#7f7287', '#5b7a8e', 'silver', 'gold', 'lightblue', 'lightgreen', 'lightcoral'])
    colT1, colT2 = st.columns([10,90])
    with colT2:
        fig.write_html("edadvstitulo.html")
        fig

# function to show the survivors 
def mostrar_sobrevivientes():
    
    tab1, tab2, tab3, tab4 = st.tabs(["Survivors",
                                    "By sex",
                                    "By title",
                                    "By class"])
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            fig= px.pie(datos_filtrados, names="Survived", title="Survived passengers", template="plotly_dark", width=800, height=600, color="Survived", color_discrete_map = {"No":"#707B7C" , "Yes":"#1ABC9C "})
            fig.update_traces(textfont=dict(color="black"))
            fig.update_layout(width=500, height=500)
            fig.write_html("sobrevivientes.html")
            fig
        
        with col2:
            st.markdown('<div class="subsubheader">The majority of passengers did not survive the Titanic disaster. The number of survivors was significantly lower than the number of passengers who perished. This is a reminder of the tragic events that occurred on that fateful night..</div>', unsafe_allow_html=True)

    
    with tab2:
        st.markdown('<div class="subsubheader">In the following chart, we can see the distribution of passengers who survived. Many of us are familiar with the phrase "Children and women first" from the movie, which was based on the real events that unfolded that night. This protocol reflected the prioritization given to women and children during the evacuation of the Titanic, highlighting the heroic efforts and sacrifices made during the tragic event.</div>', unsafe_allow_html=True)

        fig = px.treemap(datos_filtrados, path=["Survived", "Sex"], title="Distribution of passengers survived by sex", 
                    template="plotly_dark", width=800, height=600, color="Survived", 
                    color_discrete_map = {"No":"#707B7C" , "Yes":"#1ABC9C" })
        st.plotly_chart(fig, use_container_width=True)
        
    
    with tab3:

        st.markdown('<div class="subsubheader">A curious fact is that the famous phrase "the captain goes down with the ship" was followed by Captain Edward Smith of the Titanic. He was last seen on the bridge of the ship, and his body was never recovered. This serves as a poignant reminder of the tragic events that unfolded that night and the heroic efforts made by the crew and passengers to save as many lives as possible. In the following chart, we can observe the distribution of passengers who survived by title. Notably, the captain was among those who did not survive.</div>', unsafe_allow_html=True)

        fig = px.treemap(datos_filtrados, path=["Survived","Title"], title="Distribution of passengers survived by title", template="plotly_dark",
                width=1000, height=800, color="Survived", color_discrete_map = {"No":"#707B7C" , "Yes":"#1ABC9C" })
        st.plotly_chart(fig, use_container_width=True)
        
    
    with tab4:
        st.markdown('<div class="subsubheader">In the following chart, we can see the distribution of passengers who survived by class. The majority of survivors were from first class, followed by second and third class. This reflects the prioritization given to first-class passengers during the evacuation of the Titanic, as they were the first to board the lifeboats. This is a reminder of the social hierarchy that existed during that era and the impact it had on the tragic events that unfolded that night.</div>', unsafe_allow_html=True)
        fig = px.histogram(datos_filtrados, x="Pclass", color="Survived", 
                            barmode="group", 
                            category_orders={"Pclass": [1, 2, 3], "Survived": ["No", "Yes"]},
                    labels={"Pclass": "Class", "Survived": "Survived"},
                    title="Survived by Class",
                    color_discrete_map= {"No":"#707B7C" , "Yes":"#1ABC9C" }, template="plotly_dark")
        fig.write_html("sobrevivientesxclase.html")
        fig
        
        colT1, colT2 = st.columns([10,90])
        with colT2:
            with open('fotos/pie_chart_class.html', encoding="utf-8") as file10:
                html_str10 = file10.read()
            components.html(html_str10, height=400, scrolling=False)
    
# function to show the fares   
def mostrar_tarifas():
    
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
            st.plotly_chart(fig, use_container_width=False, width=300)
        
        with col2:
            st.header("Min value of fare")
            fig = go.Figure()
            area = go.Indicator( mode = "number", value = df_pagado["Update_fare"].min(), name = "Min fare", number = {"prefix": "£", "valueformat": ".0f"}  )
            fig.add_trace(area)
            fig.update_layout(template = "plotly_dark")
            st.plotly_chart(fig, use_container_width=False, width=300)
    
    with tab2:
        
        df_pagado = datos_filtrados[(datos_filtrados["Update_fare"] > 0)]
        fig=px.box(df_pagado.sort_values(by="Pclass"), x="Pclass", y="Update_fare", 
                    color="Pclass", 
                    title="Fare by Class", 
                    template="plotly_dark", 
                    labels={"Update_fare":"Fare updated in Libras", "Pclass":"Class"},
                    color_discrete_map = {"1":"#48C9B0 ", "2":"#5499C7", "3":"#AF7AC5 "})
        fig.write_html("farexclass.html")
        fig
    
    
def mostrar_ambos_datasets():
    tab1, tab2, tab3, tab4 = st.tabs(["Original dataset", "Columns transformation", "Null values", "Modified dataset"])
    with tab1:
        st.markdown('<div class="subheader">Original dataset</div>', unsafe_allow_html=True)
        st.markdown('<div class="subsubheader">The original dataset contains the following columns:</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="subsubheader">After the transformations, the dataset looks like this:</div>', unsafe_allow_html=True)
        st.dataframe(datos_filtrados) 
        st.markdown('<div class="subsubheader">To know more about the code and the transformations, you can check the notebook in my GitHub: [Titanic](https://github.com/juuliquintana/Titanic)</div>', unsafe_allow_html=True)

def conclusion():
    st.markdown('<div class="subheader">Conclusions</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="subsheader">
    Through data analysis, we remember the human stories behind the Titanic, gaining a deeper understanding of one of the most significant maritime disasters in history. The data allows us to explore the distribution of passengers by class, gender, and title, as well as the number of solo travelers. Additionally, we can observe the distribution of ages and titles of passengers, along with the count of survivors by gender, title, and class. Lastly, we also examined the range of fares paid by passengers, including the number of passengers who paid the maximum and minimum fares.
    <br><br>
    It's important not to forget the real story behind the beautiful movie.
</div>
""", unsafe_allow_html=True)

    st.image('fotos/memorial.jpg', use_column_width=True, width=500)

# dictionary to call the functions
opciones = {
    "Welcome": portada,
    #"Inicio": mostrar_inicio,
    "Passengers": mostrar_pasajeros,
    "Age": mostrar_edades, 
    "Survivor": mostrar_sobrevivientes,
    "Fare": mostrar_tarifas,
    "Dataset": (mostrar_ambos_datasets),
    "Conclusion": conclusion
}

opciones[opcion]() # call the function


