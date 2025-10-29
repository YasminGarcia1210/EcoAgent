"""
Ejemplos de Uso de EcoAgent
===========================

Este archivo contiene ejemplos prácticos de cómo usar EcoAgent
en diferentes escenarios de devolución.

Autor: EcoAgent Team
Fecha: 2024
"""

from agente import create_eco_agent
import json
from datetime import datetime, timedelta

def ejemplo_basico():
    """Ejemplo básico de uso del EcoAgent."""
    print("🤖 Ejemplo Básico de EcoAgent")
    print("=" * 40)
    
    # Crear agente
    agent = create_eco_agent()
    
    # Consulta simple
    query = "¿Puedo devolver un smartphone que compré hace 20 días?"
    print(f"👤 Consulta: {query}")
    
    result = agent.process_query(query)
    print(f"🤖 Respuesta: {result['response']}")
    print(f"📊 Estado: {result['agent_status']}")
    print()

def ejemplo_verificacion_elegibilidad():
    """Ejemplo de verificación de elegibilidad."""
    print("🔍 Ejemplo: Verificación de Elegibilidad")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    # Diferentes escenarios
    escenarios = [
        {
            "producto": "PROD001",
            "fecha": "2024-10-01",
            "descripcion": "Smartphone comprado hace 20 días"
        },
        {
            "producto": "PROD002", 
            "fecha": "2024-09-01",
            "descripcion": "Laptop comprada hace 2 meses"
        },
        {
            "producto": "PROD003",
            "fecha": "2024-10-20",
            "descripcion": "Auriculares comprados hace 5 días"
        }
    ]
    
    for escenario in escenarios:
        query = f"¿Puedo devolver el producto {escenario['producto']} comprado el {escenario['fecha']}?"
        print(f"👤 Consulta: {query}")
        
        result = agent.process_query(query)
        print(f"🤖 Respuesta: {result['response']}")
        print("-" * 40)

def ejemplo_generacion_etiqueta():
    """Ejemplo de generación de etiqueta de devolución."""
    print("🏷️ Ejemplo: Generación de Etiqueta")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    # Generar etiqueta
    query = "Necesito una etiqueta de devolución para el producto PROD001 del cliente CLI001"
    print(f"👤 Consulta: {query}")
    
    result = agent.process_query(query)
    print(f"🤖 Respuesta: {result['response']}")
    print()

def ejemplo_consulta_politicas():
    """Ejemplo de consulta de políticas."""
    print("📋 Ejemplo: Consulta de Políticas")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    politicas = [
        "¿Cuáles son las políticas de devolución?",
        "¿Qué políticas aplican para electrónicos?",
        "¿Cuánto tiempo tengo para devolver una laptop?",
        "¿Qué productos no son elegibles para devolución?"
    ]
    
    for politica in politicas:
        print(f"👤 Consulta: {politica}")
        result = agent.process_query(politica)
        print(f"🤖 Respuesta: {result['response']}")
        print("-" * 40)

def ejemplo_consulta_rag():
    """Ejemplo de consultas RAG."""
    print("🔍 Ejemplo: Consultas RAG")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    consultas_rag = [
        "¿Cómo funciona el proceso de devolución?",
        "¿Cuáles son los procedimientos de calidad?",
        "¿Qué información tengo sobre soporte al cliente?",
        "¿Cómo puedo contactar soporte técnico?"
    ]
    
    for consulta in consultas_rag:
        print(f"👤 Consulta: {consulta}")
        result = agent.process_query(consulta)
        print(f"🤖 Respuesta: {result['response']}")
        print("-" * 40)

def ejemplo_flujo_completo():
    """Ejemplo de flujo completo de devolución."""
    print("🔄 Ejemplo: Flujo Completo de Devolución")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    # Paso 1: Verificar elegibilidad
    print("Paso 1: Verificar elegibilidad")
    query1 = "¿Puedo devolver el producto PROD001 comprado el 2024-10-01?"
    result1 = agent.process_query(query1)
    print(f"🤖 Respuesta: {result1['response']}")
    print()
    
    # Paso 2: Generar etiqueta si es elegible
    if "ELEGIBLE" in result1['response'].upper():
        print("Paso 2: Generar etiqueta de devolución")
        query2 = "Genera una etiqueta de devolución para PROD001 del cliente CLI001"
        result2 = agent.process_query(query2)
        print(f"🤖 Respuesta: {result2['response']}")
        print()
    
    # Paso 3: Consultar políticas
    print("Paso 3: Consultar políticas específicas")
    query3 = "¿Cuáles son las políticas de devolución para electrónicos?"
    result3 = agent.process_query(query3)
    print(f"🤖 Respuesta: {result3['response']}")

def ejemplo_estadisticas():
    """Ejemplo de obtención de estadísticas."""
    print("📊 Ejemplo: Estadísticas del Agente")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    # Hacer algunas consultas para generar estadísticas
    consultas = [
        "¿Puedo devolver PROD001?",
        "¿Cuáles son las políticas?",
        "Genera una etiqueta para PROD002"
    ]
    
    for consulta in consultas:
        agent.process_query(consulta)
    
    # Obtener estadísticas
    stats = agent.get_stats()
    print("📈 Estadísticas del Agente:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

def ejemplo_manejo_errores():
    """Ejemplo de manejo de errores."""
    print("⚠️ Ejemplo: Manejo de Errores")
    print("=" * 40)
    
    agent = create_eco_agent()
    
    # Consultas que pueden generar errores
    consultas_error = [
        "¿Puedo devolver un producto inexistente?",
        "Genera etiqueta para producto inválido",
        "Consulta con formato incorrecto"
    ]
    
    for consulta in consultas_error:
        print(f"👤 Consulta: {consulta}")
        result = agent.process_query(consulta)
        print(f"🤖 Respuesta: {result['response']}")
        print(f"📊 Estado: {result['agent_status']}")
        if result['agent_status'] == 'error':
            print(f"❌ Error: {result.get('error', 'Error desconocido')}")
        print("-" * 40)

def main():
    """Ejecutar todos los ejemplos."""
    print("🚀 Ejecutando Ejemplos de EcoAgent")
    print("=" * 50)
    
    try:
        ejemplo_basico()
        ejemplo_verificacion_elegibilidad()
        ejemplo_generacion_etiqueta()
        ejemplo_consulta_politicas()
        ejemplo_consulta_rag()
        ejemplo_flujo_completo()
        ejemplo_estadisticas()
        ejemplo_manejo_errores()
        
        print("✅ Todos los ejemplos ejecutados correctamente!")
        
    except Exception as e:
        print(f"❌ Error ejecutando ejemplos: {e}")

if __name__ == "__main__":
    main()
