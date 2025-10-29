# 🚀 Instalación Rápida de EcoAgent

## Instalación en 3 Pasos

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Entorno (Opcional)
```bash
# Para usar OpenAI (opcional)
export OPENAI_API_KEY="tu clave"
```

### 3. Ejecutar EcoAgent
```bash
# Opción 1: Script de inicio rápido
python run_ecoagent.py

# Opción 2: Streamlit directamente
streamlit run app/app_streamlit.py

# Opción 3: Modo CLI
python run_ecoagent.py --mode cli
```

## Verificación de Instalación

```bash
# Ejecutar ejemplos
python ejemplos_uso.py

# Ejecutar pruebas
python run_ecoagent.py --mode test
```

## Acceso a la Aplicación

- **Streamlit**: http://localhost:8501
- **CLI**: Terminal interactivo
- **API**: Futura implementación

## Solución de Problemas

### Error: "No module named 'langchain'"
```bash
pip install langchain langchain-openai langchain-community
```

### Error: "No module named 'streamlit'"
```bash
pip install streamlit
```

### Error: "OpenAI API key not found"
- El sistema funciona en modo simulado sin API key
- Para usar OpenAI, configurar OPENAI_API_KEY

## Estructura de Archivos

```
EcoAgent/
├── agente/           # Módulo principal
├── app/             # Aplicación Streamlit
├── data/            # Datos y documentos
├── logs/            # Archivos de log
├── requirements.txt # Dependencias
├── run_ecoagent.py  # Script de inicio
└── README.md        # Documentación completa
```

¡Listo! EcoAgent está instalado y funcionando 🎉
