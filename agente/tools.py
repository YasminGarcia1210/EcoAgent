"""
Herramientas (Tools) para el EcoAgent
=====================================

Este módulo contiene las herramientas que el agente puede utilizar para
automatizar tareas relacionadas con devoluciones de productos.

Autor: EcoAgent Team
Fecha: 2024
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random
import string

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductoTools:
    """Clase que contiene las herramientas para manejo de productos y devoluciones."""
    
    def __init__(self):
        """Inicializar la clase con datos simulados."""
        # Base de datos simulada de productos
        self.productos_db = {
            "PROD001": {
                "nombre": "Smartphone EcoTech Pro",
                "categoria": "Electrónicos",
                "precio": 299.99,
                "garantia_dias": 30,
                "elegible_devolucion": True
            },
            "PROD002": {
                "nombre": "Laptop EcoFriendly",
                "categoria": "Computadoras",
                "precio": 899.99,
                "garantia_dias": 15,
                "elegible_devolucion": True
            },
            "PROD003": {
                "nombre": "Auriculares Wireless",
                "categoria": "Audio",
                "precio": 79.99,
                "garantia_dias": 14,
                "elegible_devolucion": True
            },
            "PROD004": {
                "nombre": "Tablet EcoPad",
                "categoria": "Tablets",
                "precio": 199.99,
                "garantia_dias": 7,
                "elegible_devolucion": False  # Producto no elegible
            }
        }
        
        # Base de datos simulada de clientes
        self.clientes_db = {
            "CLI001": {"nombre": "Juan Pérez", "email": "juan@email.com", "tipo": "premium"},
            "CLI002": {"nombre": "María García", "email": "maria@email.com", "tipo": "estándar"},
            "CLI003": {"nombre": "Carlos López", "email": "carlos@email.com", "tipo": "premium"},
        }
    
    def verificar_elegibilidad_producto(self, producto_id: str, fecha_compra: str) -> str:
        """
        Verifica si un producto es elegible para devolución según su ID y fecha de compra.
        
        Args:
            producto_id (str): ID del producto a verificar
            fecha_compra (str): Fecha de compra en formato YYYY-MM-DD
            
        Returns:
            str: Resultado de la verificación con detalles
        """
        try:
            logger.info(f"Verificando elegibilidad para producto {producto_id} comprado el {fecha_compra}")
            
            # Verificar si el producto existe
            if producto_id not in self.productos_db:
                return f"❌ Error: El producto {producto_id} no existe en nuestro sistema."
            
            producto = self.productos_db[producto_id]
            
            # Verificar si el producto es elegible para devolución
            if not producto["elegible_devolucion"]:
                return f"❌ El producto {producto['nombre']} ({producto_id}) no es elegible para devolución según nuestras políticas."
            
            # Calcular días desde la compra
            try:
                fecha_compra_obj = datetime.strptime(fecha_compra, "%Y-%m-%d")
                dias_transcurridos = (datetime.now() - fecha_compra_obj).days
            except ValueError:
                return f"❌ Error: Formato de fecha inválido. Use YYYY-MM-DD"
            
            # Verificar si está dentro del período de garantía
            if dias_transcurridos > producto["garantia_dias"]:
                return f"❌ El producto {producto['nombre']} ({producto_id}) ya no es elegible para devolución. " \
                       f"Han transcurrido {dias_transcurridos} días desde la compra, " \
                       f"pero el período de devolución es de {producto['garantia_dias']} días."
            
            # Verificar condiciones adicionales
            condiciones_adicionales = self._verificar_condiciones_adicionales(producto_id, dias_transcurridos)
            
            resultado = f"✅ El producto {producto['nombre']} ({producto_id}) ES ELEGIBLE para devolución.\n" \
                      f"📅 Días transcurridos: {dias_transcurridos}/{producto['garantia_dias']}\n" \
                      f"💰 Precio: ${producto['precio']}\n" \
                      f"📦 Categoría: {producto['categoria']}\n" \
                      f"{condiciones_adicionales}"
            
            logger.info(f"Verificación exitosa para producto {producto_id}")
            return resultado
            
        except Exception as e:
            error_msg = f"❌ Error interno al verificar elegibilidad: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def generar_etiqueta_devolucion(self, producto_id: str, cliente_id: str) -> str:
        """
        Genera una etiqueta de devolución para un producto y cliente específicos.
        
        Args:
            producto_id (str): ID del producto
            cliente_id (str): ID del cliente
            
        Returns:
            str: Etiqueta de devolución generada con instrucciones
        """
        try:
            logger.info(f"Generando etiqueta de devolución para producto {producto_id} y cliente {cliente_id}")
            
            # Verificar que el producto existe
            if producto_id not in self.productos_db:
                return f"❌ Error: El producto {producto_id} no existe en nuestro sistema."
            
            # Verificar que el cliente existe
            if cliente_id not in self.clientes_db:
                return f"❌ Error: El cliente {cliente_id} no existe en nuestro sistema."
            
            producto = self.productos_db[producto_id]
            cliente = self.clientes_db[cliente_id]
            
            # Generar código único de devolución
            codigo_devolucion = self._generar_codigo_devolucion()
            
            # Crear etiqueta de devolución
            etiqueta = f"""
🏷️ ETIQUETA DE DEVOLUCIÓN GENERADA
=====================================

📋 Información de la Devolución:
• Código de Devolución: {codigo_devolucion}
• Producto: {producto['nombre']} ({producto_id})
• Cliente: {cliente['nombre']} ({cliente_id})
• Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📦 Instrucciones de Empaque:
1. Envuelva el producto en su empaque original si está disponible
2. Incluya todos los accesorios y manuales
3. Use una caja resistente para el envío
4. Pegue esta etiqueta en el exterior del paquete

🚚 Información de Envío:
• Dirección de Retorno: EcoTech Returns Center, Calle Verde 123, Ciudad Eco
• Código Postal: ECO-001
• Teléfono de Contacto: +1-800-ECO-TECH

⚠️ Notas Importantes:
• El reembolso se procesará dentro de 5-7 días hábiles después de recibir el producto
• Mantenga este código de devolución para seguimiento
• Para consultas, contacte: soporte@ecotech.com

🔗 Enlace de Seguimiento: https://ecotech.com/track/{codigo_devolucion}
"""
            
            logger.info(f"Etiqueta generada exitosamente: {codigo_devolucion}")
            return etiqueta.strip()
            
        except Exception as e:
            error_msg = f"❌ Error interno al generar etiqueta: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def consultar_politicas_devolucion(self, categoria: str = None) -> str:
        """
        Consulta las políticas de devolución según la categoría del producto.
        
        Args:
            categoria (str, optional): Categoría específica a consultar
            
        Returns:
            str: Políticas de devolución aplicables
        """
        try:
            logger.info(f"Consultando políticas de devolución para categoría: {categoria}")
            
            politicas_generales = """
📋 POLÍTICAS GENERALES DE DEVOLUCIÓN
====================================

⏰ Períodos de Devolución:
• Electrónicos: 30 días
• Computadoras: 15 días  
• Audio: 14 días
• Tablets: 7 días

✅ Condiciones para Devolución:
• Producto en estado original
• Empaque y accesorios incluidos
• Recibo de compra válido
• No haber sido usado excesivamente

❌ Productos No Elegibles:
• Productos personalizados
• Software con licencia activada
• Productos de higiene personal
• Alimentos perecederos

💰 Proceso de Reembolso:
• Reembolso completo si cumple condiciones
• Procesamiento en 5-7 días hábiles
• Mismo método de pago original
"""
            
            if categoria:
                categoria_politicas = {
                    "Electrónicos": "📱 Electrónicos: Garantía extendida de 30 días, incluye smartphones, tablets y dispositivos móviles.",
                    "Computadoras": "💻 Computadoras: Garantía de 15 días, incluye laptops, desktops y componentes.",
                    "Audio": "🎧 Audio: Garantía de 14 días, incluye auriculares, altavoces y equipos de sonido.",
                    "Tablets": "📱 Tablets: Garantía de 7 días, dispositivos táctiles y tablets."
                }
                
                if categoria in categoria_politicas:
                    return f"{politicas_generales}\n\n{categoria_politicas[categoria]}"
                else:
                    return f"{politicas_generales}\n\n❓ Categoría '{categoria}' no encontrada. Consulte las categorías disponibles."
            
            return politicas_generales
            
        except Exception as e:
            error_msg = f"❌ Error al consultar políticas: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _verificar_condiciones_adicionales(self, producto_id: str, dias_transcurridos: int) -> str:
        """Verifica condiciones adicionales para la devolución."""
        producto = self.productos_db[producto_id]
        
        condiciones = []
        
        # Verificar si es cliente premium
        if dias_transcurridos > producto["garantia_dias"] * 0.8:
            condiciones.append("⚠️ Nota: Está cerca del límite del período de devolución.")
        
        # Verificar precio alto
        if producto["precio"] > 500:
            condiciones.append("💎 Producto de alto valor: Se requiere inspección adicional.")
        
        return "\n".join(condiciones) if condiciones else "✅ Todas las condiciones cumplidas."
    
    def _generar_codigo_devolucion(self) -> str:
        """Genera un código único de devolución."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"DEV-{timestamp}-{random_suffix}"


# Instancia global de las herramientas
producto_tools = ProductoTools()


def verificar_elegibilidad_producto(producto_id: str, fecha_compra: str) -> str:
    """
    Función wrapper para verificar elegibilidad de producto.
    Compatible con LangChain Tool.
    """
    return producto_tools.verificar_elegibilidad_producto(producto_id, fecha_compra)


def generar_etiqueta_devolucion(producto_id: str, cliente_id: str) -> str:
    """
    Función wrapper para generar etiqueta de devolución.
    Compatible con LangChain Tool.
    """
    return producto_tools.generar_etiqueta_devolucion(producto_id, cliente_id)


def consultar_politicas_devolucion(categoria: str = None) -> str:
    """
    Función wrapper para consultar políticas de devolución.
    Compatible con LangChain Tool.
    """
    return producto_tools.consultar_politicas_devolucion(categoria)


if __name__ == "__main__":
    # Pruebas de las herramientas
    print("🧪 Probando herramientas del EcoAgent...")
    
    # Prueba de verificación de elegibilidad
    print("\n1. Verificando elegibilidad:")
    resultado1 = verificar_elegibilidad_producto("PROD001", "2024-10-01")
    print(resultado1)
    
    # Prueba de generación de etiqueta
    print("\n2. Generando etiqueta:")
    resultado2 = generar_etiqueta_devolucion("PROD001", "CLI001")
    print(resultado2)
    
    # Prueba de consulta de políticas
    print("\n3. Consultando políticas:")
    resultado3 = consultar_politicas_devolucion("Electrónicos")
    print(resultado3)
