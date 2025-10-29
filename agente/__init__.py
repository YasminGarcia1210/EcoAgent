"""
Módulo Agente - EcoAgent
========================

Este módulo contiene todos los componentes del agente inteligente:
- tools.py: Herramientas para automatización
- rag_pipeline.py: Pipeline RAG para recuperación de información
- eco_agent.py: Agente principal integrado

Autor: EcoAgent Team
Fecha: 2024
"""

from .tools import (
    verificar_elegibilidad_producto,
    generar_etiqueta_devolucion,
    consultar_politicas_devolucion,
    ProductoTools
)

from .rag_pipeline import (
    EcoRAGPipeline,
    create_rag_pipeline
)

from .eco_agent import (
    EcoAgent,
    EcoAgentLogger,
    create_eco_agent
)

__version__ = "1.0.0"
__author__ = "EcoAgent Team"

__all__ = [
    # Tools
    "verificar_elegibilidad_producto",
    "generar_etiqueta_devolucion", 
    "consultar_politicas_devolucion",
    "ProductoTools",
    
    # RAG Pipeline
    "EcoRAGPipeline",
    "create_rag_pipeline",
    
    # Main Agent
    "EcoAgent",
    "EcoAgentLogger",
    "create_eco_agent"
]
