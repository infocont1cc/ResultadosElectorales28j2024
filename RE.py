
import streamlit as st
st.set_page_config(layout="centered")
import re
import base64
pattern=r"^\d{9}\.\d{2}\.\d\.\d{4}!(\d+,){37}\d+(!\d+){2}$"
output_text=""
output_text_w=""
#spc=" "
def insertar(instr):
    global output_text
    output_text +="> "+instr + "  \n"
    
def insertarw(instr,cret=True):
    global output_text_w
    if cret:
        output_text_w +=instr + "\n"
    else:
        output_text_w +=instr
def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
    
# Inject custom CSS
st.markdown(
    """
    <style>
    /* Change background color */
    body {
        background-color: #f0f2f6;
    }

    /* Style headers */
    h1 {
        color: #ff4b4b;
        text-align: left;
        font-family: 'Arial', sans-serif;
    }   
        
       .stForm {
    background-color: #b0e4cc; /* Light blue background for the form */
    padding: 20px; /* Add some space inside the form */
    border-radius: 10px; /* Rounded corners */
    border: 1px solid #ddd; /* Add a light border */
    }
    button[data-testid="stBaseButton-primaryFormSubmit"]{
		background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 16px;
        border: 2px solid #4CAF50;
    }


    button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
        background-color: white;
        color: #4CAF50;
		}
    button[data-testid="stBaseButton-secondaryFormSubmit"]{
    background-color: #008CBA !important; /* Blue */
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 16px;
        border: 2px solid #4CAF50;
        transition: background-color 0.3s ease;
    }

    button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
    background-color: white !important ;
        color: #008CBA;
    }
     #text_input_1{
    font-size: 15px;
    background-color: #e5edff;
    }
    [data-testid="stSidebar"] a {
        background-color: #f0f0f5;
        padding: 20px;        
        color: #333;
        user-select: auto;         
        text-decoration: none;
    }
   
    a:link {
    color: red;
    }
    a:visited {
    color: green;
    }
    a:hover {
    color: #FF7F50;
    text-transform: uppercase;    
    }
     a:active {
    color: blue;
    }
     [data-testid="stMarkdownContainer"] a button {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 20px;
        width: 100%;
        border: 2px solid #ffffff;
    }

    /* Hover effect */
    [data-testid="stMarkdownContainer"] a button:hover {
        background-color: #45a049;
        color: yellow;
    }
    [data-testid="stMarkdownContainer"] a#bumd button{
    background-color: red;
    }
    [data-testid="stMarkdownContainer"] a#bini button{
    background-color: #008cba;
    }
    [data-testid="stMarkdownContainer"] a#res button{
    background-color: #df89dc;
    }
    div[data-testid="InputInstructions"] > span:nth-child(1) {
    visibility: hidden;    
    }
     table {
        border-collapse: collapse;
        width: 40%;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    /* Apply a different background color to odd rows */
    tbody tr:nth-child(odd) {
        background-color: #f0f2f6;
    }
    /* Optional: Style the header row */
    th {
        background-color: #0e1117; 
        color: white;
    }
    .custom-table {
    border: 2px solid red;
    width: 70%;
    }
    .align-left {
    text-align: left;
    }
    .align-right {
    text-align: right;
    }
    tfoot.total-row tr {
    background-color: #ffb3b3; /* A distinct color for the total row */
    font-weight: bold; /* Optional: make the total row bold */
    }
    tbody tr:hover {
    background-color: #ddd; /* Optional: highlight row on hover */
    }
    tfoot.total-row tr:hover {
    background-color: #e1ebf2; /* A distinct color for the total row */
    
    }
    </style>
    """,
    unsafe_allow_html=True
)

def showresults(): 
    global lcandidatos
    global partidos
    global qr
    global output_text
    global output_text_w
    output_text=""
    #global table_html
    qr=st.session_state.text_input   
    arrQR=qr.split('!')
    lvotos=arrQR[1].split(',')
    votos=[int(item) for item in lvotos]
    sgtos=arrQR[0].split('.')
    IDcen=sgtos[0]
    mesa=sgtos[1]
    if mesa[0]=='0':
        mesa=mesa[1]
    if IDcen[0]=='0':
        IDcen=IDcen[-8:]
    dato=(IDcen,)
    cur.execute(myquery,dato)
    res=cur.fetchone()
    #print(res)
    edo,mpio,pqia,centro,cenID=res
    if edo=="CAPITAL":
        edo="DISTRITO CAPITAL"
    partidos=[]
    for i in range(38):      
        partidos.append(Partido(lpartidos[i],votos[i]))
    partidos[28].abrev="ADC"     
    n=0
    candidatos=[]
    for i in range(10):   
        candidatos.append(Candidato(lcandidatos[i],imgs[i],partidos[n:n+numali[i]]))
        n+=numali[i]   
    qr=qr.strip() 
    st.markdown(f"## :blue[Resultados en la mesa {mesa} , {centro}]")
    st.markdown(f"## :red[Parroquia: {pqia}, Municipio: {mpio}]")
    st.markdown(f"## :violet[Estado: {edo}]")
    st.markdown("### :green[Votos por candidato y partido según el orden del código QR:]\n")    
    insertarw("*_Código QR introducido:_*")
    insertarw(f"*_{qr}_*")    
    insertarw(f" *Resultados en la mesa {mesa} , {centro}*")
    insertarw(f"_Parroquia: {pqia}, Municipio: {mpio}_")
    insertarw(f"*Estado: {edo}*")
    insertarw("*Votos por candidato y partido según el orden del código QR:*")
    insertarw('```')
    #insertar(f" **Código QR introducido:{qr}**")
    insertar("**Código QR introducido:**  ")
    #insertar("<br/>")
    insertar(f"***{qr}***")
    insertar(f"## Resultados en la mesa {mesa} , {centro}")
    insertar(f"## Parroquia: {pqia}, Municipio: {mpio}")
    insertar(f"## Estado: {edo}")
    insertar(" ")
    insertar("## Votos por candidato y partido según el orden del código QR")      
    #for i in range(10):    
    for candidato in candidatos:
            table_html = """
            <table  border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; " >
             """
            table_html += f"<th><img src='data:image/jpg;base64,{candidato.imagen}'    width='50'></img></th><th>{candidato.nombre}</th><th class='align-right' >{candidato.votos}</th>"
            insertarw('_'*23)          
            insertarw(candidato.nombre.ljust(17)+str(candidato.votos).rjust(5))
            insertarw('_'*23)
            insertar('_'*29)         
            insertar(f"|  {candidato.nombre}| {candidato.votos} |")
            insertar("| ----- | ----: |")
            #insertar('_'*29) 
            for partido in candidato.partidos:
                table_html += f"<tr ><td colspan='2' contenteditable='false'>{partido.nombre}</td><td class='align-right' >{partido.votos}</td></tr>"   
                pnom=partido.nombre
                if hasattr(partido, 'abrev'):
                    pnom=partido.abrev
                insertarw(spc+pnom.ljust(13)+str(partido.votos).rjust(4))
                insertar(f"|{partido.nombre} | {str(partido.votos)} |")  
            table_html += "</table>"
            insertarw('_'*23)
            insertarw(" ")
            #insertar('_'*29)
            #insertar(" ")
            st.markdown(table_html, unsafe_allow_html=True)   
    insertarw('```')             
    totalValidos=sum(votos)
    vParcia=arrQR[2]
    vNulos=arrQR[3]
    tVotos=totalValidos+int(vParcia)+int(vNulos)
    nVal=int(vParcia)+int(vNulos)
    pctNval=round(nVal/tVotos*100,2)
    candidatos_ord = sorted(candidatos, key=lambda x: x.votos,reverse=True)
    st.sidebar.markdown(
    '<a id="res" href="#resumen-principal" target="_self"><button>Resumen principal</button></a>',     unsafe_allow_html=True
                )
    st.markdown("## :orange[Resumen principal]")
    st.markdown("# Resultados de candidatos ordenados por votos:")     
    insertarw("*Resumen de resultados de candidatos ordenados por votos:*") 
    insertarw('-'*35)
    insertarw('```')
    insertarw('-'*35)
    insertar("# Resumen de resultados de candidatos ordenados por votos:")    
    insertar('-'*35)
    insertar("|Candidato|Votos|%|")
    insertar("| ----- | ----: |-----:|")    
    table_html2 = """
    <table class='custom-table' border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; " >
     """
    table_html2+="<tr><th colspan='2' style='text-align: center;'>Candidato</th><th>Votos</th><th>Porcentaje</th></tr>"
    for candidato in candidatos_ord:
            table_html2 +=f"<tr><td><img src='data:image/jpg;base64,{candidato.imagen}' width='35'></td><td>{candidato.nombre}</td><td class='align-right' >{candidato.votos}</td><td class='align-right'>{format(candidato.votos/totalValidos,'.2%')}</td></tr>"
            insertarw(candidato.nombre.ljust(20)+str(candidato.votos).rjust(4)+spc+format(candidato.votos/totalValidos,".2%").rjust(6))
            insertar(f"|{candidato.nombre}| {str(candidato.votos)}|{format(candidato.votos/totalValidos,'.2%')}|")
    table_html2 += f"<tfoot class='total-row' ><tr><td colspan='2'>Total votos válidos</td><td class='align-right' >{str(totalValidos)}</td><td class='align-right'>100%</td></tr>"
    table_html2 += f"<tr><td colspan='2'>No válidos</td><td class='align-right' >{nVal}</td><td class='align-right' >{pctNval}%</td></tr>"
    table_html2 += f"<tr><td colspan='2'>TOTAL VOTOS</td><td class='align-right' >{tVotos}</td><td class='align-right' >100%</td></tr></tfoot>"
    table_html2 += "</table>"
    st.markdown(table_html2, unsafe_allow_html=True)  
    insertarw('-'*35)
    insertarw('-'*35)
    insertarw("TOTAL VOTOS VÁLIDOS".ljust(20)+str(totalValidos).rjust(4)+sp4+"100.00%".rjust(7))
    insertarw("VOTOS PARCIALES".ljust(20)+arrQR[2].rjust(4)+sp4)
    insertarw("VOTOS NULOS".ljust(21)+arrQR[3].rjust(4))
    insertarw('-'*35)
    insertarw("TOTAL VOTOS".ljust(20)+str(tVotos).rjust(4))
    insertarw('-'*35)
    insertarw('```')
    insertar(f"|***TOTAL VOTOS VÁLIDOS*** |***{str(totalValidos)}***|***100.00%***|") 
    #insertar(f"|VOTOS PARCIALES|{arrQR[2]}|&nbsp;|")
    #insertar(f"|VOTOS NULOS|{arrQR[3]}|&nbsp;|")
    #insertar('-'*35)
    pctnval=format(nVal/tVotos,'.2%')
    pctval=format(totalValidos/tVotos,'.2%')
    insertar(f"|*No válidos*|*{nVal}*|*{pctnval}*")
    insertar(f"|***TOTAL VOTOS***|***{str(tVotos)}***|***100.00%***|")
    insertar('-'*35)    
    st.header("Seccion WhatsApp")    
    st.sidebar.markdown(
    '<a href="#seccion-whats-app" target="_self"><button>Sección Whatsapp</button></a>', 
    unsafe_allow_html=True
                )
    st.markdown(' :blue-background[Copie este código en posts WhatsApp]',help="Para Copiar en posts Wahtsapp, busque el simbolo parecido a ⧉ , en el extremo superior derecho y haga click en él  ")      
    st.code(output_text_w, language=None)
    st.header("Seccion Markdown")    
    st.sidebar.markdown(
    '<a id="bumd" href="#seccion-markdown" target="_self"><button >Sección Markdown</button></a>', 
    unsafe_allow_html=True)
    st.markdown(':orange-background[Copie este código en sitios Markdown]',help="Para Copiar en posts markdown, busque el simbolo parecido a ⧉ , en el extremo superior derecho y haga click en él  ") 
    st.code(output_text,language="markdown")    
#variables que no cambian
myquery='''
SELECT Estados.estado, Municipios.municipio, Parroquias.parroquia, Centros.centro, Centros.centroID
FROM ((Estados INNER JOIN Municipios ON Estados.estadoID = Municipios.estadoID) 
INNER JOIN Parroquias ON Municipios.municipioID = Parroquias.municipioID) 
INNER JOIN Centros ON Parroquias.parroquiaID = Centros.parroquiaID
WHERE Centros.centroID=?;
'''
spc=" " * 5
sp4=" "*4
lcandidatos=[
        "NICOLÁS MADURO",
        "LUIS MARTÍNEZ",
        "JAVIER BERTUCCI",
        "JOSÉ BRITO",
        "ANTONIO ECARRI",
        "CLAUDIO FERMÍN",
        "DANIEL CEBALLOS",
        "EDMUNDO GONZÁLEZ",
        "ENRIQUE MÁRQUEZ",
        "BENJAMÍN RAUSSEO"]
lpartidos=[
        "PSUV",
        "PCV",
        "TUPAMARO",
        "PPT",
        "MSV",
        "PODEMOS",
        "MEP",
        "APC",
        "ORA",
        "UPV",
        "EV",
        "PVV",
        "PTV",
        "AD",
        "COPEI",
        "MR",
        "BR",
        "DDP",
        "UNE",
        "EL CAMBIO",
        "PV",
        "VU",
        "UVV",
        "MPJ",
        "AP",
        "MOVEV",
        "CMC",
        "FV",
        "ALIANZA DEL CAMBIO",
        "MIN UNIDAD",
        "SPV",
        "VPA",
        "AREPA",
        "UNTC",
        "MPV",
        "MUD",
        "CENTRADOS",
        "CONDE"]
numali = [13, 6, 1, 4, 6, 1, 2, 3, 1, 1]
limgs=['nm','lem','jb','jbrito','ae','cf','dc','eg','em','br']
imgs=[get_base64_image(item+'.jpg') for item in limgs]
class Partido:
    def __init__(self,nombre,votos):
        self.nombre=nombre
        self.votos=votos
class Candidato:
    def __init__(self, nombre,imagen, lista_partidos):
        self.nombre = nombre  # Usa el parámetro recibido
        self.partidos = lista_partidos  # Asigna la lista recibida
        # Calcula la suma basándose en la lista de partidos
        self.imagen=imagen
        self.votos = sum(p.votos for p in self.partidos)        
import sqlite3
conn = sqlite3.connect('RE.db')
cur = conn.cursor()
    
st.title("Interpretar código QR, Elecciones Venezuela 2024")
st.sidebar.markdown("## 📌 Navegación")
#st.sidebar.markdown("[INICIO](#96bbc1db)", unsafe_allow_html=True)
st.sidebar.markdown(
    '<a id="bini" href="#interpretar-codigo-qr-elecciones-venezuela-2024" target="_self"><button>INICIO</button></a>', 
    unsafe_allow_html=True )
  
def clear_text():
    #st.session_state['text_content'] = ""
    st.session_state.text_input = ""
# Initialize session state
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
with st.form(key='my_form', enter_to_submit=True, clear_on_submit=False):
    st.markdown(":rainbow[Coloque en el cuadro anexo el código QR y luego pulse ENTER o click en el botón izquierdo]")
    
    st.text_input(
        label ="hidden_label",
        placeholder="Pegue aquí su código Qr",
        key="text_input",
        label_visibility="collapsed")
        
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Enviar código para ver resultados electorales",type="primary")
    with col2:
        clear_button = st.form_submit_button(label="Limpiar cuadro ,para enviar otro código QR",on_click=clear_text, type="secondary")    
# st.markdown("## :rainbow[Area para introducir código QR]")
# # Text area bound to session state
# st.text_area(
    # label="hidden_label",
    # placeholder="Pegue aquí su código Qr",
    # key="text_input",
    # height=100,
    # label_visibility="collapsed"
# )

# Submit button
if submit_button:
    if st.session_state.text_input.strip():
        st.success(f"Usted introdujo:\n\n{st.session_state.text_input}")
        qr=st.session_state.text_input
        match1 = re.search(pattern, qr)
        if match1:
            #st.markdown(":green-background[El código QR está bien conformado]")
            st.success("✅ Texto introducido constituye un código QR bien conformado!")
            showresults()
        else:            
            #st.warning("El código QR no está bien conformado",icon="⚠️")
            st.error("❌ Texto introducido no es un código QR bien conformado")    
    else:
        #st.warning("Por favor introduzca el código antes de enviar.")
        st.error("❌ Por favor introduzca el código antes de enviar.")

    
