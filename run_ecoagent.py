#!/usr/bin/env python3
"""
Script de inicio rápido para EcoAgent
=====================================

Este script facilita el inicio rápido del sistema EcoAgent
con todas las configuraciones necesarias.

Uso:
    python run_ecoagent.py [--mode streamlit|cli|test]
"""

import argparse
import sys
import os
from pathlib import Path

def setup_environment():
    """Configurar el entorno para EcoAgent."""
    print("🔧 Configurando entorno...")
    
    # Crear directorios necesarios
    directories = ["logs", "data", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio {directory} creado/verificado")
    
    # Verificar archivos de datos
    data_files = ["data/faq.json", "data/politicas_devolucion.txt"]
    for file_path in data_files:
        if not Path(file_path).exists():
            print(f"⚠️  Archivo {file_path} no encontrado")
        else:
            print(f"✅ Archivo {file_path} verificado")

def run_streamlit():
    """Ejecutar la aplicación Streamlit."""
    print("🚀 Iniciando aplicación Streamlit...")
    try:
        import streamlit
        os.system("streamlit run app/app_streamlit.py")
    except ImportError:
        print("❌ Streamlit no está instalado. Ejecuta: pip install streamlit")
        sys.exit(1)

def run_cli():
    """Ejecutar EcoAgent en modo CLI."""
    print("💻 Iniciando EcoAgent en modo CLI...")
    try:
        from agente import create_eco_agent
        
        # Crear agente
        agent = create_eco_agent()
        print("✅ EcoAgent inicializado correctamente!")
        
        # Loop de interacción
        print("\n🤖 EcoAgent CLI - Escribe 'salir' para terminar")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 Tú: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 EcoAgent procesando...")
                result = agent.process_query(user_input)
                
                print(f"\n🤖 EcoAgent: {result['response']}")
                
                if result['agent_status'] == 'error':
                    print(f"❌ Error: {result.get('error', 'Error desconocido')}")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        sys.exit(1)

def run_tests():
    """Ejecutar pruebas del sistema."""
    print("🧪 Ejecutando pruebas del sistema...")
    try:
        import pytest
        os.system("pytest tests/ -v")
    except ImportError:
        print("❌ pytest no está instalado. Ejecuta: pip install pytest")
        sys.exit(1)

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="EcoAgent - Script de inicio rápido")
    parser.add_argument(
        "--mode", 
        choices=["streamlit", "cli", "test"], 
        default="streamlit",
        help="Modo de ejecución (default: streamlit)"
    )
    
    args = parser.parse_args()
    
    print("🤖 EcoAgent - Sistema de Devoluciones Inteligentes")
    print("=" * 50)
    
    # Configurar entorno
    setup_environment()
    
    # Ejecutar según el modo
    if args.mode == "streamlit":
        run_streamlit()
    elif args.mode == "cli":
        run_cli()
    elif args.mode == "test":
        run_tests()

if __name__ == "__main__":
    main()
