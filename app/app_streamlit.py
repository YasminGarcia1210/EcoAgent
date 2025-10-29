"""
Aplicación Streamlit para EcoAgent
==================================

Interfaz de usuario para interactuar con el EcoAgent.
Proporciona una interfaz amigable para consultas sobre devoluciones,
verificación de elegibilidad y generación de etiquetas.

Autor: EcoAgent Team
Fecha: 2024
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
from typing import Dict, Any

# Importaciones locales
from agente import create_eco_agent, EcoAgent

# Configuración de la página
st.set_page_config(
    page_title="EcoAgent - Devoluciones Inteligentes",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stats-container {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class EcoAgentApp:
    """Clase principal de la aplicación Streamlit."""
    
    def __init__(self):
        """Inicializar la aplicación."""
        self.agent = None
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializar el estado de la sesión."""
        if 'agent_initialized' not in st.session_state:
            st.session_state.agent_initialized = False
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'stats' not in st.session_state:
            st.session_state.stats = {
                "total_queries": 0,
                "successful_queries": 0,
                "errors": 0
            }
    
    def initialize_agent(self):
        """Inicializar el agente."""
        try:
            with st.spinner("🤖 Inicializando EcoAgent..."):
                # Obtener API key de OpenAI
                openai_api_key = st.session_state.get('openai_api_key')
                
                # Crear agente
                self.agent = create_eco_agent(openai_api_key)
                st.session_state.agent_initialized = True
                
                st.success("✅ EcoAgent inicializado correctamente!")
                return True
                
        except Exception as e:
            st.error(f"❌ Error al inicializar EcoAgent: {str(e)}")
            return False
    
    def render_header(self):
        """Renderizar el encabezado de la aplicación."""
        st.markdown('<h1 class="main-header">🤖 EcoAgent</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">Asistente Inteligente para Devoluciones</h2>', unsafe_allow_html=True)
        
        # Información del agente
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estado", "🟢 Activo" if st.session_state.agent_initialized else "🔴 Inactivo")
        
        with col2:
            st.metric("Consultas Totales", st.session_state.stats["total_queries"])
        
        with col3:
            success_rate = (st.session_state.stats["successful_queries"] / 
                          max(st.session_state.stats["total_queries"], 1)) * 100
            st.metric("Tasa de Éxito", f"{success_rate:.1f}%")
    
    def render_sidebar(self):
        """Renderizar la barra lateral."""
        st.sidebar.title("⚙️ Configuración")
        
        # Configuración de API
        st.sidebar.subheader("🔑 Configuración de API")
        openai_api_key = st.sidebar.text_input(
            "OpenAI API Key",
            value=st.session_state.get('openai_api_key', ''),
            type="password",
            help="Ingresa tu clave API de OpenAI para usar modelos reales"
        )
        
        if openai_api_key != st.session_state.get('openai_api_key'):
            st.session_state.openai_api_key = openai_api_key
            st.session_state.agent_initialized = False
        
        # Botón de inicialización
        if not st.session_state.agent_initialized:
            if st.sidebar.button("🚀 Inicializar EcoAgent", type="primary"):
                self.initialize_agent()
        else:
            if st.sidebar.button("🔄 Reinicializar EcoAgent"):
                st.session_state.agent_initialized = False
                st.rerun()
        
        # Información del agente
        if st.session_state.agent_initialized and self.agent:
            st.sidebar.subheader("📊 Información del Agente")
            stats = self.agent.get_stats()
            
            st.sidebar.write(f"**Modelo:** {stats['model_type']}")
            st.sidebar.write(f"**Herramientas:** {stats['tools_available']}")
            st.sidebar.write(f"**RAG:** {'✅' if stats['rag_available'] else '❌'}")
            st.sidebar.write(f"**Interacciones:** {stats['total_interactions']}")
        
        # Ejemplos de consultas
        st.sidebar.subheader("💡 Ejemplos de Consultas")
        example_queries = [
            "¿Puedo devolver un smartphone comprado hace 20 días?",
            "Necesito una etiqueta de devolución para PROD001",
            "¿Cuáles son las políticas de devolución?",
            "¿Cómo funciona el proceso de devolución?"
        ]
        
        for query in example_queries:
            if st.sidebar.button(f"📝 {query}", key=f"example_{query}"):
                st.session_state.example_query = query
        
        # Limpiar historial
        if st.sidebar.button("🗑️ Limpiar Historial"):
            st.session_state.chat_history = []
            st.rerun()
    
    def render_chat_interface(self):
        """Renderizar la interfaz de chat."""
        st.subheader("💬 Consulta al EcoAgent")
        
        # Campo de entrada
        user_input = st.text_area(
            "Escribe tu consulta:",
            value=st.session_state.get('example_query', ''),
            height=100,
            placeholder="Ejemplo: ¿Puedo devolver un producto que compré hace 15 días?"
        )
        
        # Limpiar query de ejemplo después de usarla
        if 'example_query' in st.session_state:
            del st.session_state.example_query
        
        # Botón de envío
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("🚀 Enviar", type="primary", disabled=not st.session_state.agent_initialized):
                if user_input.strip():
                    self.process_user_query(user_input.strip())
        
        with col2:
            if st.button("🔄 Limpiar"):
                st.rerun()
    
    def process_user_query(self, query: str):
        """Procesar consulta del usuario."""
        if not st.session_state.agent_initialized or not self.agent:
            st.error("❌ EcoAgent no está inicializado. Por favor, inicialízalo primero.")
            return
        
        try:
            # Actualizar estadísticas
            st.session_state.stats["total_queries"] += 1
            
            # Mostrar spinner
            with st.spinner("🤖 EcoAgent está procesando tu consulta..."):
                # Procesar consulta
                result = self.agent.process_query(query)
            
            # Actualizar estadísticas
            if result["agent_status"] == "success":
                st.session_state.stats["successful_queries"] += 1
            else:
                st.session_state.stats["errors"] += 1
            
            # Agregar al historial
            st.session_state.chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": result["response"],
                "status": result["agent_status"]
            })
            
            # Mostrar respuesta
            self.display_response(result)
            
        except Exception as e:
            st.error(f"❌ Error al procesar consulta: {str(e)}")
            st.session_state.stats["errors"] += 1
    
    def display_response(self, result: Dict[str, Any]):
        """Mostrar la respuesta del agente."""
        st.markdown("---")
        
        if result["agent_status"] == "success":
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### ✅ Respuesta del EcoAgent")
            st.write(result["response"])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("### ❌ Error en la Consulta")
            st.write(result["response"])
            if "error" in result:
                st.write(f"**Detalles del error:** {result['error']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Mostrar metadatos
        with st.expander("📊 Información de la Consulta"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Timestamp:** {result['timestamp']}")
                st.write(f"**Estado:** {result['agent_status']}")
                st.write(f"**Herramientas disponibles:** {result['tools_available']}")
            
            with col2:
                if 'stats' in result:
                    stats = result['stats']
                    st.write(f"**Interacciones totales:** {stats['total_interactions']}")
                    st.write(f"**Interacciones exitosas:** {stats['successful_interactions']}")
                    st.write(f"**Errores:** {stats['errors']}")
    
    def render_chat_history(self):
        """Renderizar el historial de chat."""
        if st.session_state.chat_history:
            st.subheader("📜 Historial de Conversación")
            
            # Mostrar historial en orden inverso (más reciente primero)
            for i, entry in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"💬 Consulta {len(st.session_state.chat_history) - i}: {entry['query'][:50]}..."):
                    st.write(f"**Consulta:** {entry['query']}")
                    st.write(f"**Respuesta:** {entry['response']}")
                    st.write(f"**Estado:** {entry['status']}")
                    st.write(f"**Timestamp:** {entry['timestamp']}")
    
    def render_agent_info(self):
        """Renderizar información del agente."""
        if st.session_state.agent_initialized and self.agent:
            st.subheader("🤖 Información del EcoAgent")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🛠️ Herramientas Disponibles")
                tools_info = [
                    "✅ Verificar Elegibilidad de Producto",
                    "✅ Generar Etiqueta de Devolución", 
                    "✅ Consultar Políticas de Devolución",
                    "✅ Consulta RAG (Recuperación de Información)"
                ]
                for tool in tools_info:
                    st.write(tool)
            
            with col2:
                st.markdown("### 📈 Estadísticas del Agente")
                stats = self.agent.get_stats()
                
                st.metric("Interacciones Totales", stats['total_interactions'])
                st.metric("Tasa de Éxito", f"{(stats['successful_interactions'] / max(stats['total_interactions'], 1)) * 100:.1f}%")
                st.metric("Tipo de Modelo", stats['model_type'])
                st.metric("RAG Disponible", "✅" if stats['rag_available'] else "❌")
    
    def run(self):
        """Ejecutar la aplicación."""
        # Renderizar componentes
        self.render_header()
        self.render_sidebar()
        
        # Contenido principal
        if st.session_state.agent_initialized:
            # Interfaz de chat
            self.render_chat_interface()
            
            # Historial de chat
            self.render_chat_history()
            
            # Información del agente
            self.render_agent_info()
        else:
            # Pantalla de bienvenida
            st.markdown("""
            <div class="info-box">
                <h3>👋 ¡Bienvenido a EcoAgent!</h3>
                <p>EcoAgent es tu asistente inteligente especializado en devoluciones de productos.</p>
                <p><strong>¿Qué puede hacer EcoAgent?</strong></p>
                <ul>
                    <li>✅ Verificar si un producto es elegible para devolución</li>
                    <li>🏷️ Generar etiquetas de devolución automáticamente</li>
                    <li>📋 Consultar políticas y procedimientos de devolución</li>
                    <li>🔍 Responder preguntas usando información contextual</li>
                </ul>
                <p><strong>Para comenzar:</strong></p>
                <ol>
                    <li>Configura tu API Key de OpenAI en la barra lateral (opcional)</li>
                    <li>Haz clic en "Inicializar EcoAgent"</li>
                    <li>¡Comienza a hacer consultas!</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar ejemplos
            st.subheader("💡 Ejemplos de Consultas")
            
            examples = [
                {
                    "title": "Verificar Elegibilidad",
                    "query": "¿Puedo devolver un smartphone que compré hace 20 días?",
                    "description": "Verifica si un producto cumple con los criterios de devolución"
                },
                {
                    "title": "Generar Etiqueta",
                    "query": "Necesito una etiqueta de devolución para el producto PROD001 del cliente CLI001",
                    "description": "Genera una etiqueta completa con instrucciones de envío"
                },
                {
                    "title": "Consultar Políticas",
                    "query": "¿Cuáles son las políticas de devolución para electrónicos?",
                    "description": "Obtiene información detallada sobre políticas específicas"
                },
                {
                    "title": "Proceso General",
                    "query": "¿Cómo funciona el proceso de devolución?",
                    "description": "Explica el proceso completo paso a paso"
                }
            ]
            
            for i, example in enumerate(examples):
                with st.expander(f"📝 {example['title']}"):
                    st.write(f"**Consulta:** {example['query']}")
                    st.write(f"**Descripción:** {example['description']}")


def main():
    """Función principal de la aplicación."""
    app = EcoAgentApp()
    app.run()


if __name__ == "__main__":
    main()
