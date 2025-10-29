"""
EcoAgent - Agente Inteligente para Devoluciones
===============================================

Este módulo implementa el agente principal que integra:
- Herramientas (Tools) para automatización
- Pipeline RAG para recuperación de información
- Sistema de logging y monitoreo
- Interfaz con el usuario

Autor: EcoAgent Team
Fecha: 2024
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Importaciones de LangChain
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.schema import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler

# Importaciones locales
from .tools import (
    verificar_elegibilidad_producto,
    generar_etiqueta_devolucion,
    consultar_politicas_devolucion
)
from .rag_pipeline import EcoRAGPipeline, create_rag_pipeline

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EcoAgentLogger(BaseCallbackHandler):
    """Callback handler personalizado para logging del agente."""
    
    def __init__(self, log_file: str = "logs/interacciones.log"):
        """
        Inicializar el logger del agente.
        
        Args:
            log_file (str): Archivo donde guardar los logs
        """
        self.log_file = log_file
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Asegura que el directorio de logs existe."""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def on_agent_action(self, action: AgentAction, **kwargs):
        """Callback cuando el agente ejecuta una acción."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_action",
            "tool": action.tool,
            "tool_input": action.tool_input,
            "log": action.log
        }
        self._write_log(log_entry)
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        """Callback cuando el agente termina."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_finish",
            "output": finish.return_values.get("output", ""),
            "log": finish.log
        }
        self._write_log(log_entry)
    
    def _write_log(self, log_entry: Dict[str, Any]):
        """Escribe una entrada de log al archivo."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Error al escribir log: {e}")


class EcoAgent:
    """
    Agente inteligente para manejo de devoluciones de productos.
    
    Integra herramientas de automatización, pipeline RAG y sistema de logging
    para proporcionar asistencia completa en procesos de devolución.
    """
    
    def __init__(self, openai_api_key: str = None, model_name: str = "gpt-4o-mini"):
        """
        Inicializar el EcoAgent.
        
        Args:
            openai_api_key (str): Clave API de OpenAI
            model_name (str): Nombre del modelo a utilizar
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.use_simulated_model = not bool(self.openai_api_key)
        
        # Inicializar componentes
        self.rag_pipeline = None
        self.tools = []
        self.agent = None
        self.logger = EcoAgentLogger()
        
        # Estadísticas del agente
        self.stats = {
            "total_interactions": 0,
            "tools_used": {},
            "successful_interactions": 0,
            "errors": 0
        }
        
        logger.info("EcoAgent inicializado")
    
    def initialize_rag_pipeline(self):
        """Inicializa el pipeline RAG."""
        try:
            logger.info("Inicializando pipeline RAG...")
            self.rag_pipeline = create_rag_pipeline(self.openai_api_key)
            logger.info("Pipeline RAG inicializado exitosamente")
        except Exception as e:
            logger.error(f"Error al inicializar pipeline RAG: {e}")
            raise
    
    def create_tools(self):
        """Crea las herramientas disponibles para el agente."""
        try:
            logger.info("Creando herramientas del agente...")
            
            # Herramienta RAG para consultas generales
            def rag_query(query: str) -> str:
                """Consulta información usando el pipeline RAG."""
                try:
                    result = self.rag_pipeline.query(query)
                    return result.get("result", "No se pudo obtener información.")
                except Exception as e:
                    return f"Error en consulta RAG: {str(e)}"
            
            # Definir herramientas
            self.tools = [
                Tool(
                    name="Verificar Elegibilidad de Producto",
                    func=verificar_elegibilidad_producto,
                    description="""Verifica si un producto puede devolverse según su ID y fecha de compra.
                    Parámetros: producto_id (string), fecha_compra (string en formato YYYY-MM-DD)
                    Ejemplo: Verificar Elegibilidad de Producto PROD001 2024-10-01"""
                ),
                Tool(
                    name="Generar Etiqueta de Devolución",
                    func=generar_etiqueta_devolucion,
                    description="""Genera una etiqueta de devolución para un producto y cliente específicos.
                    Parámetros: producto_id (string), cliente_id (string)
                    Ejemplo: Generar Etiqueta de Devolución PROD001 CLI001"""
                ),
                Tool(
                    name="Consultar Políticas de Devolución",
                    func=consultar_politicas_devolucion,
                    description="""Consulta las políticas de devolución según la categoría del producto.
                    Parámetros: categoria (string opcional)
                    Ejemplo: Consultar Políticas de Devolución Electrónicos"""
                ),
                Tool(
                    name="Consulta RAG",
                    func=rag_query,
                    description="""Consulta información general sobre políticas, procedimientos y datos de la empresa.
                    Parámetros: query (string)
                    Ejemplo: Consulta RAG ¿Cuáles son los procedimientos de calidad?"""
                )
            ]
            
            logger.info(f"Se crearon {len(self.tools)} herramientas")
            
        except Exception as e:
            logger.error(f"Error al crear herramientas: {e}")
            raise
    
    def initialize_llm(self):
        """Inicializa el modelo de lenguaje."""
        try:
            if not self.use_simulated_model:
                self.llm = ChatOpenAI(
                    model_name=self.model_name,
                    openai_api_key=self.openai_api_key,
                    temperature=0.1
                )
                logger.info(f"LLM inicializado: {self.model_name}")
            else:
                # LLM simulado para pruebas
                self.llm = self._create_simulated_llm()
                logger.info("LLM simulado inicializado")
                
        except Exception as e:
            logger.error(f"Error al inicializar LLM: {e}")
            self.use_simulated_model = True
            self.llm = self._create_simulated_llm()
    
    def _create_simulated_llm(self):
        """Crea un LLM simulado para pruebas."""
        class SimulatedLLM:
            def __init__(self):
                self.name = "SimulatedLLM"
            
            def __call__(self, prompt: str) -> str:
                """Simula respuesta del LLM."""
                prompt_lower = prompt.lower()
                
                if "devolución" in prompt_lower:
                    return "Para procesar una devolución, puedo ayudarte verificando la elegibilidad del producto y generando una etiqueta de devolución."
                elif "política" in prompt_lower:
                    return "Las políticas de devolución varían según la categoría. Puedo consultar las políticas específicas para ti."
                elif "ayuda" in prompt_lower or "soporte" in prompt_lower:
                    return "Soy EcoAgent, tu asistente especializado en devoluciones. ¿En qué puedo ayudarte?"
                else:
                    return "Soy EcoAgent. Puedo ayudarte con devoluciones, políticas y procedimientos. ¿Qué necesitas?"
        
        return SimulatedLLM()
    
    def create_agent(self):
        """Crea el agente principal con LangChain."""
        try:
            logger.info("Creando agente principal...")
            
            # Crear el agente
            self.agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                early_stopping_method="generate"
            )
            
            logger.info("Agente principal creado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al crear agente: {e}")
            raise
    
    def initialize_agent(self):
        """Inicializa completamente el agente."""
        try:
            logger.info("Inicializando EcoAgent completo...")
            
            # 1. Inicializar pipeline RAG
            self.initialize_rag_pipeline()
            
            # 2. Crear herramientas
            self.create_tools()
            
            # 3. Inicializar LLM
            self.initialize_llm()
            
            # 4. Crear agente
            self.create_agent()
            
            logger.info("EcoAgent inicializado completamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar agente: {e}")
            raise
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario.
        
        Args:
            user_input (str): Consulta del usuario
            
        Returns:
            Dict[str, Any]: Respuesta del agente y metadatos
        """
        try:
            logger.info(f"Procesando consulta: {user_input}")
            
            # Actualizar estadísticas
            self.stats["total_interactions"] += 1
            
            # Crear prompt contextual
            contextual_prompt = self._create_contextual_prompt(user_input)
            
            # Ejecutar agente
            if self.agent:
                response = self.agent.run(contextual_prompt)
            else:
                response = "Lo siento, el agente no está disponible en este momento."
            
            # Registrar interacción exitosa
            self.stats["successful_interactions"] += 1
            
            # Crear respuesta estructurada
            result = {
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "agent_status": "success",
                "tools_available": len(self.tools),
                "stats": self.stats.copy()
            }
            
            logger.info("Consulta procesada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error al procesar consulta: {e}")
            self.stats["errors"] += 1
            
            return {
                "response": f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "agent_status": "error",
                "error": str(e),
                "stats": self.stats.copy()
            }
    
    def _create_contextual_prompt(self, user_input: str) -> str:
        """Crea un prompt contextual para el agente."""
        context = f"""
Eres EcoAgent, un asistente inteligente especializado en devoluciones de productos.

CONTEXTO:
- Trabajas para EcoTech, una empresa eco-friendly
- Tienes acceso a herramientas para verificar elegibilidad y generar etiquetas
- Puedes consultar políticas y procedimientos usando RAG
- Siempre eres amable, profesional y útil

HERRAMIENTAS DISPONIBLES:
1. Verificar Elegibilidad de Producto: Para verificar si un producto puede devolverse
2. Generar Etiqueta de Devolución: Para crear etiquetas de devolución
3. Consultar Políticas de Devolución: Para obtener información sobre políticas
4. Consulta RAG: Para consultas generales sobre la empresa

INSTRUCCIONES:
- Responde de manera clara y profesional
- Usa las herramientas cuando sea apropiado
- Si el usuario pregunta sobre devoluciones, verifica elegibilidad primero
- Si necesita una etiqueta, genera una después de verificar elegibilidad
- Siempre explica el proceso paso a paso

CONSULTA DEL USUARIO: {user_input}

Responde de manera útil y profesional:
"""
        return context
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del agente."""
        return {
            "total_interactions": self.stats["total_interactions"],
            "successful_interactions": self.stats["successful_interactions"],
            "error_rate": self.stats["errors"] / max(self.stats["total_interactions"], 1),
            "tools_available": len(self.tools),
            "rag_available": self.rag_pipeline is not None,
            "model_type": "simulated" if self.use_simulated_model else "openai"
        }
    
    def reset_stats(self):
        """Reinicia las estadísticas del agente."""
        self.stats = {
            "total_interactions": 0,
            "tools_used": {},
            "successful_interactions": 0,
            "errors": 0
        }
        logger.info("Estadísticas reiniciadas")


# Función de conveniencia para crear el agente
def create_eco_agent(openai_api_key: str = None) -> EcoAgent:
    """
    Crea e inicializa un EcoAgent completo.
    
    Args:
        openai_api_key (str): Clave API de OpenAI
        
    Returns:
        EcoAgent: Agente inicializado
    """
    agent = EcoAgent(openai_api_key)
    agent.initialize_agent()
    return agent


if __name__ == "__main__":
    # Pruebas del EcoAgent
    print("🧪 Probando EcoAgent...")
    
    # Crear agente
    agent = create_eco_agent()
    
    # Pruebas de consultas
    test_queries = [
        "¿Puedo devolver un smartphone que compré hace 20 días?",
        "Necesito una etiqueta de devolución para el producto PROD001 del cliente CLI001",
        "¿Cuáles son las políticas de devolución para electrónicos?",
        "¿Cómo funciona el proceso de devolución?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Consulta: {query}")
        result = agent.process_query(query)
        print(f"✅ Respuesta: {result['response']}")
        print(f"📊 Estado: {result['agent_status']}")
    
    # Mostrar estadísticas
    print(f"\n📈 Estadísticas: {agent.get_stats()}")
