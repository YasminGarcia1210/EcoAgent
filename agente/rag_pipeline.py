"""
Pipeline RAG para EcoAgent
==========================

Este módulo implementa el pipeline de Retrieval-Augmented Generation (RAG)
que permite al agente acceder a información contextual sobre políticas,
procedimientos y datos de la empresa.

Autor: EcoAgent Team
Fecha: 2024
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Importaciones de LangChain
# Importaciones modernas de LangChain y módulos asociados

# Embeddings y modelos de lenguaje
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Vectorstores y loaders
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# 🔥 Cambio importante aquí
from langchain.chains import RetrievalQA  # <-- CORRECTO

# LLMs (opcional si usas ChatOpenAI)
from langchain_community.llms import OpenAI

# Tipos de documentos
from langchain.schema import Document

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EcoRAGPipeline:
    """Pipeline RAG para el EcoAgent con capacidades de recuperación de información."""
    
    def __init__(self, openai_api_key: str = None, model_name: str = "gpt-4o-mini"):
        """
        Inicializar el pipeline RAG.
        
        Args:
            openai_api_key (str): Clave API de OpenAI
            model_name (str): Nombre del modelo a utilizar
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        
        if not self.openai_api_key:
            logger.warning("No se encontró OPENAI_API_KEY. Usando modelo simulado.")
            self.use_simulated_model = True
        else:
            self.use_simulated_model = False
        
        # Inicializar componentes
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        
        # Datos simulados para cuando no hay API key
        self.simulated_knowledge_base = self._create_simulated_knowledge_base()
        
        logger.info("Pipeline RAG inicializado correctamente")
    
    def _create_simulated_knowledge_base(self) -> Dict[str, str]:
        """Crea una base de conocimiento simulada para pruebas."""
        return {
            "politicas_devolucion": """
            POLÍTICAS DE DEVOLUCIÓN ECOAGENT
            =================================
            
            Períodos de Devolución:
            - Electrónicos: 30 días desde la compra
            - Computadoras: 15 días desde la compra
            - Audio: 14 días desde la compra
            - Tablets: 7 días desde la compra
            
            Condiciones Requeridas:
            1. Producto en estado original
            2. Empaque y accesorios incluidos
            3. Recibo de compra válido
            4. No haber sido usado excesivamente
            
            Proceso de Devolución:
            1. Verificar elegibilidad del producto
            2. Generar etiqueta de devolución
            3. Enviar producto a centro de retornos
            4. Procesar reembolso en 5-7 días hábiles
            
            Excepciones:
            - Productos personalizados no son elegibles
            - Software con licencia activada no es elegible
            - Productos de higiene personal no son elegibles
            """,
            
            "procedimientos_calidad": """
            PROCEDIMIENTOS DE CONTROL DE CALIDAD
            ====================================
            
            Inspección de Productos Devueltos:
            1. Verificar estado físico del producto
            2. Comprobar que todos los accesorios estén incluidos
            3. Verificar que el producto funcione correctamente
            4. Documentar cualquier daño o defecto
            
            Criterios de Aceptación:
            - Producto sin daños visibles
            - Funcionalidad completa
            - Accesorios originales incluidos
            - Empaque en buen estado
            
            Proceso de Reembolso:
            - Reembolso completo si cumple criterios
            - Reembolso parcial si hay daños menores
            - Sin reembolso si hay daños mayores
            """,
            
            "informacion_productos": """
            INFORMACIÓN DE PRODUCTOS ECOAGENT
            ==================================
            
            Categorías de Productos:
            
            Electrónicos:
            - Smartphones EcoTech Pro (PROD001)
            - Tablets EcoPad (PROD004)
            - Dispositivos IoT EcoSmart
            
            Computadoras:
            - Laptops EcoFriendly (PROD002)
            - Desktops EcoWorkstation
            - Accesorios EcoAccessories
            
            Audio:
            - Auriculares Wireless (PROD003)
            - Altavoces EcoSound
            - Sistemas de audio EcoAudio
            
            Especificaciones Técnicas:
            - Todos los productos son eco-friendly
            - Certificación de sostenibilidad
            - Garantía extendida disponible
            - Soporte técnico 24/7
            """,
            
            "soporte_cliente": """
            SOPORTE AL CLIENTE ECOAGENT
            ============================
            
            Canales de Contacto:
            - Email: soporte@ecotech.com
            - Teléfono: +1-800-ECO-TECH
            - Chat en vivo: Disponible 24/7
            - Centro de ayuda: help.ecotech.com
            
            Servicios Disponibles:
            - Consultas sobre devoluciones
            - Soporte técnico
            - Información de productos
            - Seguimiento de pedidos
            
            Tiempos de Respuesta:
            - Email: 2-4 horas
            - Teléfono: Inmediato
            - Chat: Inmediato
            - Tickets: 1-2 horas
            """
        }
    
    def initialize_embeddings(self):
        """Inicializa el modelo de embeddings."""
        try:
            if not self.use_simulated_model:
                self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
                logger.info("Embeddings de OpenAI inicializados")
            else:
                logger.info("Usando embeddings simulados")
        except Exception as e:
            logger.error(f"Error al inicializar embeddings: {e}")
            self.use_simulated_model = True
    
    def create_vectorstore(self, documents: List[Document] = None):
        """
        Crea el vectorstore con los documentos proporcionados.
        
        Args:
            documents (List[Document]): Lista de documentos para indexar
        """
        try:
            if documents is None:
                documents = self._load_default_documents()
            
            if not self.use_simulated_model and self.embeddings:
                # Usar embeddings reales
                self.vectorstore = FAISS.from_documents(documents, self.embeddings)
                logger.info(f"Vectorstore creado con {len(documents)} documentos")
            else:
                # Crear vectorstore simulado
                self.vectorstore = self._create_simulated_vectorstore(documents)
                logger.info("Vectorstore simulado creado")
                
        except Exception as e:
            logger.error(f"Error al crear vectorstore: {e}")
            self.vectorstore = self._create_simulated_vectorstore(documents or [])
    
    def _load_default_documents(self) -> List[Document]:
        """Carga documentos por defecto del directorio data."""
        documents = []
        
        # Crear documentos desde la base de conocimiento simulada
        for key, content in self.simulated_knowledge_base.items():
            doc = Document(
                page_content=content,
                metadata={"source": f"knowledge_base/{key}", "type": "policy"}
            )
            documents.append(doc)
        
        # Intentar cargar archivos del directorio data
        data_dir = "data"
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                file_path = os.path.join(data_dir, filename)
                try:
                    if filename.endswith('.txt'):
                        loader = TextLoader(file_path)
                        docs = loader.load()
                        documents.extend(docs)
                    elif filename.endswith('.pdf'):
                        loader = PyPDFLoader(file_path)
                        docs = loader.load()
                        documents.extend(docs)
                    elif filename.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            doc = Document(
                                page_content=str(data),
                                metadata={"source": file_path, "type": "json"}
                            )
                            documents.append(doc)
                except Exception as e:
                    logger.warning(f"No se pudo cargar {filename}: {e}")
        
        return documents
    
    def _create_simulated_vectorstore(self, documents: List[Document]):
        """Crea un vectorstore simulado para pruebas."""
        class SimulatedVectorStore:
            def __init__(self, docs):
                self.documents = docs
            
            def similarity_search(self, query: str, k: int = 4) -> List[Document]:
                """Búsqueda de similitud simulada."""
                # Simular búsqueda basada en palabras clave
                query_lower = query.lower()
                scored_docs = []
                
                for doc in self.documents:
                    content_lower = doc.page_content.lower()
                    score = 0
                    
                    # Calcular score basado en palabras clave
                    keywords = query_lower.split()
                    for keyword in keywords:
                        if keyword in content_lower:
                            score += content_lower.count(keyword)
                    
                    if score > 0:
                        scored_docs.append((score, doc))
                
                # Ordenar por score y retornar top k
                scored_docs.sort(key=lambda x: x[0], reverse=True)
                return [doc for _, doc in scored_docs[:k]]
        
        return SimulatedVectorStore(documents)
    
    def create_retriever(self, k: int = 4):
        """
        Crea el retriever para búsqueda de documentos.
        
        Args:
            k (int): Número de documentos a recuperar
        """
        if self.vectorstore:
            if hasattr(self.vectorstore, 'as_retriever'):
                self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
            else:
                # Retriever simulado
                self.retriever = self.vectorstore
            logger.info(f"Retriever creado con k={k}")
        else:
            logger.error("No se puede crear retriever sin vectorstore")
    
    def create_qa_chain(self):
        """Crea la cadena de QA para responder preguntas."""
        try:
            if not self.use_simulated_model and self.openai_api_key:
                llm = ChatOpenAI(
                    model_name=self.model_name,
                    openai_api_key=self.openai_api_key,
                    temperature=0.1
                )
            else:
                # LLM simulado
                llm = self._create_simulated_llm()
            
            if self.retriever:
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self.retriever,
                    return_source_documents=True
                )
                logger.info("Cadena QA creada exitosamente")
            else:
                logger.error("No se puede crear QA chain sin retriever")
                
        except Exception as e:
            logger.error(f"Error al crear QA chain: {e}")
            self.qa_chain = self._create_simulated_qa_chain()
    
    def _create_simulated_llm(self):
        """Crea un LLM simulado para pruebas."""
        class SimulatedLLM:
            def __init__(self):
                self.name = "SimulatedLLM"
            
            def __call__(self, prompt: str) -> str:
                """Simula respuesta del LLM basada en el prompt."""
                prompt_lower = prompt.lower()
                
                if "devolución" in prompt_lower or "devolver" in prompt_lower:
                    return "Para procesar una devolución, necesito verificar la elegibilidad del producto y generar una etiqueta de devolución."
                elif "política" in prompt_lower:
                    return "Las políticas de devolución varían según la categoría del producto. Los electrónicos tienen 30 días, computadoras 15 días, audio 14 días y tablets 7 días."
                elif "soporte" in prompt_lower or "ayuda" in prompt_lower:
                    return "Puedo ayudarte con consultas sobre devoluciones, información de productos y políticas de la empresa."
                else:
                    return "Soy EcoAgent, tu asistente para devoluciones. ¿En qué puedo ayudarte?"
        
        return SimulatedLLM()
    
    def _create_simulated_qa_chain(self):
        """Crea una cadena QA simulada."""
        class SimulatedQAChain:
            def __init__(self):
                self.llm = self._create_simulated_llm()
            
            def run(self, query: str) -> Dict[str, Any]:
                """Ejecuta la consulta QA simulada."""
                # Buscar documentos relevantes
                if hasattr(self, 'retriever') and self.retriever:
                    docs = self.retriever.similarity_search(query, k=2)
                else:
                    docs = []
                
                # Generar respuesta
                response = self.llm(query)
                
                return {
                    "result": response,
                    "source_documents": docs
                }
        
        return SimulatedQAChain()
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta en el pipeline RAG.
        
        Args:
            question (str): Pregunta a responder
            
        Returns:
            Dict[str, Any]: Respuesta y documentos fuente
        """
        try:
            logger.info(f"Ejecutando consulta: {question}")
            
            if self.qa_chain:
                if hasattr(self.qa_chain, 'run'):
                    result = self.qa_chain.run(question)
                else:
                    # Para cadenas simuladas
                    result = self.qa_chain.run(question)
                
                logger.info("Consulta ejecutada exitosamente")
                return result
            else:
                # Respuesta de fallback
                return {
                    "result": "Lo siento, el sistema RAG no está disponible en este momento.",
                    "source_documents": []
                }
                
        except Exception as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            return {
                "result": f"Error al procesar la consulta: {str(e)}",
                "source_documents": []
            }
    
    def initialize_pipeline(self):
        """Inicializa todo el pipeline RAG."""
        try:
            logger.info("Inicializando pipeline RAG completo...")
            
            # 1. Inicializar embeddings
            self.initialize_embeddings()
            
            # 2. Crear vectorstore
            self.create_vectorstore()
            
            # 3. Crear retriever
            self.create_retriever()
            
            # 4. Crear QA chain
            self.create_qa_chain()
            
            logger.info("Pipeline RAG inicializado completamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar pipeline: {e}")
            raise


# Función de conveniencia para crear el pipeline
def create_rag_pipeline(openai_api_key: str = None) -> EcoRAGPipeline:
    """
    Crea e inicializa un pipeline RAG completo.
    
    Args:
        openai_api_key (str): Clave API de OpenAI
        
    Returns:
        EcoRAGPipeline: Pipeline inicializado
    """
    pipeline = EcoRAGPipeline(openai_api_key)
    pipeline.initialize_pipeline()
    return pipeline


if __name__ == "__main__":
    # Pruebas del pipeline RAG
    print("🧪 Probando pipeline RAG...")
    
    # Crear pipeline
    pipeline = create_rag_pipeline()
    
    # Pruebas de consultas
    queries = [
        "¿Cuáles son las políticas de devolución?",
        "¿Cómo puedo devolver un smartphone?",
        "¿Qué productos son elegibles para devolución?",
        "¿Cuánto tiempo tengo para devolver una laptop?"
    ]
    
    for query in queries:
        print(f"\n❓ Consulta: {query}")
        result = pipeline.query(query)
        print(f"✅ Respuesta: {result['result']}")
        print(f"📄 Documentos fuente: {len(result.get('source_documents', []))}")
