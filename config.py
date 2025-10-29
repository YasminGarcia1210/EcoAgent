# EcoAgent Configuration
# ======================

# Configuración del entorno
ENVIRONMENT = "development"  # development, production, testing

# Configuración de OpenAI
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.1
OPENAI_MAX_TOKENS = 1000

# Configuración del agente
AGENT_MAX_ITERATIONS = 5
AGENT_VERBOSE = True
AGENT_EARLY_STOPPING = "generate"

# Configuración de RAG
RAG_CHUNK_SIZE = 1000
RAG_CHUNK_OVERLAP = 200
RAG_K_DOCUMENTS = 4

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/interacciones.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de Streamlit
STREAMLIT_THEME = "light"
STREAMLIT_LAYOUT = "wide"

# Configuración de base de datos (futuro)
DATABASE_URL = "sqlite:///ecoagent.db"

# Configuración de seguridad
ENABLE_RATE_LIMITING = True
MAX_REQUESTS_PER_MINUTE = 60

# Configuración de cache
ENABLE_CACHE = True
CACHE_TTL_SECONDS = 3600

# Configuración de monitoreo
ENABLE_METRICS = True
METRICS_PORT = 8000
