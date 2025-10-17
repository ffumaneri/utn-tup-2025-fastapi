#!/usr/bin/env python3
"""
Script para testear el CRUD de Personas directamente en la base de datos
usando SQLModel, Models y Repository (sin FastAPI)

Uso: python test_crud_direct.py

Este script testa directamente la capa de acceso a datos.
"""

from database import create_db_and_tables, get_session
from models import Persona, PersonaCreate, PersonaUpdate
from repository import PersonaRepository
import sys

def print_header(title: str):
    """Imprime un header con estilo"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_persona(persona: Persona):
    """Imprime los datos de una persona de forma formateada"""
    print(f"ID: {persona.id}")
    print(f"Nombre: {persona.nombre}")
    print(f"Apellido: {persona.apellido}")
    print(f"Edad: {persona.edad}")
    print("-" * 40)

def get_repository() -> PersonaRepository:
    """Obtiene una instancia del repository con la sesión de base de datos"""
    session_generator = get_session()
    session = next(session_generator)
    return PersonaRepository(session)

def crear_persona():
    """Crea una nueva persona"""
    print_header("CREAR NUEVA PERSONA")
    
    try:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return
            
        apellido = input("Apellido: ").strip()
        if not apellido:
            print("❌ El apellido no puede estar vacío")
            return
            
        edad_str = input("Edad: ").strip()
        try:
            edad = int(edad_str)
            if edad < 0 or edad > 150:
                print("❌ La edad debe estar entre 0 y 150 años")
                return
        except ValueError:
            print("❌ La edad debe ser un número válido")
            return
        
        # Crear instancia de PersonaCreate
        persona_create = PersonaCreate(
            nombre=nombre,
            apellido=apellido,
            edad=edad
        )
        
        # Usar el repository para crear la persona
        repo = get_repository()
        nueva_persona = repo.create(persona_create)
        
        print("✅ Persona creada exitosamente:")
        print_persona(nueva_persona)
        
    except Exception as e:
        print(f"❌ Error al crear persona: {e}")

def listar_personas():
    """Lista todas las personas"""
    print_header("LISTAR TODAS LAS PERSONAS")
    
    try:
        # Preguntar por parámetros de paginación
        skip_str = input("¿Cuántas personas omitir? (Enter para 0): ").strip()
        skip = 0 if not skip_str else int(skip_str) if skip_str.isdigit() else 0
        
        limit_str = input("¿Cuántas personas mostrar? (Enter para 100): ").strip()
        limit = 100 if not limit_str else int(limit_str) if limit_str.isdigit() else 100
        
        # Usar el repository para obtener las personas
        repo = get_repository()
        personas = repo.get_all(skip=skip, limit=limit)
        
        if personas:
            print(f"\n📋 Se encontraron {len(personas)} personas:")
            for persona in personas:
                print_persona(persona)
        else:
            print("📭 No se encontraron personas")
            
    except Exception as e:
        print(f"❌ Error al listar personas: {e}")

def obtener_persona_por_id():
    """Obtiene una persona por su ID"""
    print_header("OBTENER PERSONA POR ID")
    
    try:
        persona_id_str = input("ID de la persona: ").strip()
        if not persona_id_str.isdigit():
            print("❌ El ID debe ser un número")
            return
            
        persona_id = int(persona_id_str)
        
        # Usar el repository para obtener la persona
        repo = get_repository()
        persona = repo.get_by_id(persona_id)
        
        if persona:
            print("✅ Persona encontrada:")
            print_persona(persona)
        else:
            print(f"❌ No se encontró persona con ID {persona_id}")
            
    except Exception as e:
        print(f"❌ Error al obtener persona: {e}")

def actualizar_persona():
    """Actualiza una persona existente"""
    print_header("ACTUALIZAR PERSONA")
    
    try:
        # Primero obtener el ID
        persona_id_str = input("ID de la persona a actualizar: ").strip()
        if not persona_id_str.isdigit():
            print("❌ El ID debe ser un número")
            return
            
        persona_id = int(persona_id_str)
        
        # Verificar que existe
        repo = get_repository()
        persona_actual = repo.get_by_id(persona_id)
        if not persona_actual:
            print(f"❌ No se encontró persona con ID {persona_id}")
            return
            
        print("📝 Persona actual:")
        print_persona(persona_actual)
        
        # Solicitar nuevos datos (opcionales)
        print("\n💡 Deja en blanco los campos que no quieras cambiar:")
        nombre = input(f"Nuevo nombre (actual: {persona_actual.nombre}): ").strip()
        apellido = input(f"Nuevo apellido (actual: {persona_actual.apellido}): ").strip()
        edad_str = input(f"Nueva edad (actual: {persona_actual.edad}): ").strip()
        
        # Construir datos de actualización
        update_data = {}
        if nombre:
            update_data["nombre"] = nombre
        if apellido:
            update_data["apellido"] = apellido
        if edad_str:
            try:
                edad = int(edad_str)
                if edad < 0 or edad > 150:
                    print("❌ La edad debe estar entre 0 y 150 años")
                    return
                update_data["edad"] = edad
            except ValueError:
                print("❌ La edad debe ser un número válido")
                return
        
        if not update_data:
            print("ℹ️ No se especificaron cambios")
            return
            
        # Crear instancia de PersonaUpdate
        persona_update = PersonaUpdate(**update_data)
        
        # Usar el repository para actualizar la persona
        persona_actualizada = repo.update(persona_id, persona_update)
        
        if persona_actualizada:
            print("✅ Persona actualizada exitosamente:")
            print_persona(persona_actualizada)
        else:
            print(f"❌ No se pudo actualizar la persona con ID {persona_id}")
            
    except Exception as e:
        print(f"❌ Error al actualizar persona: {e}")

def eliminar_persona():
    """Elimina una persona"""
    print_header("ELIMINAR PERSONA")
    
    try:
        persona_id_str = input("ID de la persona a eliminar: ").strip()
        if not persona_id_str.isdigit():
            print("❌ El ID debe ser un número")
            return
            
        persona_id = int(persona_id_str)
        
        # Verificar que existe y mostrar datos antes de eliminar
        repo = get_repository()
        persona = repo.get_by_id(persona_id)
        if not persona:
            print(f"❌ No se encontró persona con ID {persona_id}")
            return
            
        print("⚠️  Persona a eliminar:")
        print_persona(persona)
        
        confirmacion = input("¿Estás seguro de que quieres eliminar esta persona? (s/N): ").strip().lower()
        if confirmacion not in ['s', 'si', 'sí', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
        
        # Usar el repository para eliminar la persona
        exito = repo.delete(persona_id)
        
        if exito:
            print(f"✅ Persona con ID {persona_id} eliminada exitosamente")
        else:
            print(f"❌ No se pudo eliminar la persona con ID {persona_id}")
            
    except Exception as e:
        print(f"❌ Error al eliminar persona: {e}")

def cargar_datos_prueba():
    """Carga datos de prueba en la base de datos"""
    print_header("CARGAR DATOS DE PRUEBA")
    
    try:
        personas_prueba = [
            PersonaCreate(nombre="Juan", apellido="Pérez", edad=30),
            PersonaCreate(nombre="María", apellido="González", edad=25),
            PersonaCreate(nombre="Carlos", apellido="López", edad=40),
            PersonaCreate(nombre="Ana", apellido="Martínez", edad=35),
            PersonaCreate(nombre="Pedro", apellido="Rodríguez", edad=28),
        ]
        
        repo = get_repository()
        personas_creadas = []
        
        for persona_create in personas_prueba:
            nueva_persona = repo.create(persona_create)
            personas_creadas.append(nueva_persona)
        
        print(f"✅ Se cargaron {len(personas_creadas)} personas de prueba:")
        for persona in personas_creadas:
            print_persona(persona)
            
    except Exception as e:
        print(f"❌ Error al cargar datos de prueba: {e}")

def contar_personas():
    """Cuenta el total de personas en la base de datos"""
    print_header("CONTAR PERSONAS")
    
    try:
        repo = get_repository()
        # Obtener todas las personas para contar (no es la forma más eficiente, pero funciona)
        personas = repo.get_all(limit=10000)
        total = len(personas)
        
        print(f"📊 Total de personas en la base de datos: {total}")
        
    except Exception as e:
        print(f"❌ Error al contar personas: {e}")

def limpiar_base_datos():
    """Elimina todas las personas de la base de datos"""
    print_header("LIMPIAR BASE DE DATOS")
    
    try:
        confirmacion = input("⚠️  ¿Estás seguro de que quieres eliminar TODAS las personas? (s/N): ").strip().lower()
        if confirmacion not in ['s', 'si', 'sí', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
        
        repo = get_repository()
        # Obtener todas las personas y eliminarlas una por una
        personas = repo.get_all(limit=10000)
        eliminadas = 0
        
        for persona in personas:
            if repo.delete(persona.id):
                eliminadas += 1
        
        print(f"✅ Se eliminaron {eliminadas} personas de la base de datos")
        
    except Exception as e:
        print(f"❌ Error al limpiar base de datos: {e}")

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("     🗃️  CRUD DIRECTO DE PERSONAS (SQLModel + Repository) 🗃️ ")
    print("="*60)
    print("1. 📝 Crear nueva persona")
    print("2. 📋 Listar todas las personas")
    print("3. 🔍 Obtener persona por ID")
    print("4. ✏️  Actualizar persona")
    print("5. 🗑️  Eliminar persona")
    print("6. 🎯 Cargar datos de prueba")
    print("7. 📊 Contar personas")
    print("8. 🧹 Limpiar base de datos")
    print("0. 🚪 Salir")
    print("="*60)

def inicializar_base_datos():
    """Inicializa la base de datos y las tablas"""
    try:
        print("🔧 Inicializando base de datos...")
        create_db_and_tables()
        print("✅ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        print("💡 Asegúrate de que la base de datos PostgreSQL esté corriendo")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando script de testing CRUD directo de Personas...")
    
    # Inicializar base de datos
    if not inicializar_base_datos():
        sys.exit(1)
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n👉 Selecciona una opción (0-8): ").strip()
            
            if opcion == "0":
                print("👋 ¡Hasta luego!")
                break
            elif opcion == "1":
                crear_persona()
            elif opcion == "2":
                listar_personas()
            elif opcion == "3":
                obtener_persona_por_id()
            elif opcion == "4":
                actualizar_persona()
            elif opcion == "5":
                eliminar_persona()
            elif opcion == "6":
                cargar_datos_prueba()
            elif opcion == "7":
                contar_personas()
            elif opcion == "8":
                limpiar_base_datos()
            else:
                print("❌ Opción inválida. Por favor selecciona una opción del 0 al 8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        input("\n⏸️  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
