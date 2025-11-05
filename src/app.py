import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from validate_docbr import CPF
from database import Database

# Configuração da página
st.set_page_config(
    page_title="Sane Aqui - Pesquisa de Saneamento",
    page_icon="🏠",
    layout="wide"
)

# Inicializa banco
db = Database()
db.create_table()

# Validador de CPF
cpf_validator = CPF()

# Sidebar para navegação
st.sidebar.title("📋 Menu")
page = st.sidebar.radio(
    "Navegação",
    ["Formulário de Pesquisa", "Painel Estatístico"]
)

# ==================== PÁGINA 1: FORMULÁRIO ====================
if page == "Formulário de Pesquisa":
    st.title("🏠 Sane Aqui - Pesquisa de Saneamento Básico")
    st.markdown("---")
    
    with st.form("formulario_pesquisa"):
        col1, col2 = st.columns(2)
        
        with col1:
            cpf = st.text_input(
                "CPF *",
                max_chars=14,
                placeholder="000.000.000-00",
                help="Digite apenas números"
            )
            endereco = st.text_input("Endereço *", placeholder="Rua, Avenida, etc.")
            bairro = st.text_input("Bairro", placeholder="Nome do bairro")
            cidade = st.text_input("Cidade *", placeholder="Nome da cidade")
        
        with col2:
            estado = st.selectbox(
                "Estado *",
                ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                 "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                 "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
            )
            moradores = st.number_input(
                "Número de Moradores *",
                min_value=1,
                max_value=50,
                value=1
            )
            rede_esgoto = st.radio("Possui Rede de Esgoto? *", ["Sim", "Não"])
            agua_tratada = st.radio("Possui Água Tratada? *", ["Sim", "Não"])
        
        submitted = st.form_submit_button("📤 Enviar Pesquisa", use_container_width=True)
        
        if submitted:
            # Validações
            errors = []
            
            # Remove formatação do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            if not cpf_limpo or not cpf_validator.validate(cpf_limpo):
                errors.append("❌ CPF inválido")
            
            if not endereco:
                errors.append("❌ Endereço é obrigatório")
            
            if not cidade:
                errors.append("❌ Cidade é obrigatória")
            
            if not estado:
                errors.append("❌ Estado é obrigatório")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Salva no banco
                data = {                    
                    'cpf': cpf_limpo,
                    'endereco': endereco,
                    'bairro': bairro,
                    'cidade': cidade,
                    'estado': estado,
                    'moradores': moradores,
                    'rede_esgoto': rede_esgoto == "Sim",
                    'agua_tratada': agua_tratada == "Sim"
                }
                
                if db.insert_pesquisa(data):
                    st.success("✅ Pesquisa enviada com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ Erro ao salvar. Tente novamente.")

# ==================== PÁGINA 2: DASHBOARD ====================
elif page == "Painel Estatístico":
    st.title("📊 Painel de Estatísticas")
    st.markdown("---")
    
    stats = db.get_statistics()
    
    if stats and not stats['total'].empty:
        total_registros = int(stats['total']['total'].iloc[0])
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Pesquisas", f"{total_registros:,}")
        
        with col2:
            media_moradores = float(stats['moradores']['media_moradores'].iloc[0])
            st.metric("Média de Moradores", f"{media_moradores:.1f}")
        
        with col3:
            perc_esgoto = (stats['infra']['com_esgoto'].iloc[0] / total_registros) * 100
            st.metric("Com Rede de Esgoto", f"{perc_esgoto:.1f}%")
        
        with col4:
            perc_agua = (stats['infra']['com_agua'].iloc[0] / total_registros) * 100
            st.metric("Com Água Tratada", f"{perc_agua:.1f}%")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Distribuição por Estado")
            fig_estado = px.bar(
                stats['por_estado'],
                x='estado',
                y='total',
                color='total',
                labels={'total': 'Quantidade', 'estado': 'Estado'},
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_estado, use_container_width=True)
        
        with col2:
            st.subheader("🏙️ Top 10 Cidades")
            fig_cidade = px.pie(
                stats['por_cidade'],
                values='total',
                names='cidade',
                hole=0.4
            )
            st.plotly_chart(fig_cidade, use_container_width=True)
        
        # Gráfico de infraestrutura
        st.subheader("🚰 Infraestrutura de Saneamento")
        infra_data = pd.DataFrame({
            'Tipo': ['Rede de Esgoto', 'Água Tratada'],
            'Com Acesso': [
                int(stats['infra']['com_esgoto'].iloc[0]),
                int(stats['infra']['com_agua'].iloc[0])
            ],
            'Sem Acesso': [
                total_registros - int(stats['infra']['com_esgoto'].iloc[0]),
                total_registros - int(stats['infra']['com_agua'].iloc[0])
            ]
        })
        
        fig_infra = go.Figure(data=[
            go.Bar(name='Com Acesso', x=infra_data['Tipo'], y=infra_data['Com Acesso'], marker_color='green'),
            go.Bar(name='Sem Acesso', x=infra_data['Tipo'], y=infra_data['Sem Acesso'], marker_color='red')
        ])
        fig_infra.update_layout(barmode='stack')
        st.plotly_chart(fig_infra, use_container_width=True)
        
    else:
        st.info("📭 Nenhuma pesquisa cadastrada ainda. Comece preenchendo o formulário!")
