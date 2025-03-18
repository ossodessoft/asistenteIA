import openai  # Librería para conectarse a la API de OpenAI
import os  # Manejo de variables de entorno
import time  # Para manejar los reintentos en caso de error
from dotenv import load_dotenv  # Carga variables desde .env
import sys  # Para manejar errores de ejecución

# 🔹 Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# 🔹 Obtenemos la API Key desde el archivo .env
API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Validamos que la API Key esté presente antes de continuar
if not API_KEY:
    print("⚠️ ERROR: No se encontró la API Key. Verifica el archivo .env y asegúrate de haberla agregado correctamente.")
    sys.exit(1)

# 🔹 Configuramos la API Key en OpenAI
openai.api_key = API_KEY


# 🔹 Función para obtener respuesta de OpenAI con reintentos
def obtener_respuesta(pregunta_usuario):
    """
    Envía una pregunta al modelo GPT-3.5-Turbo y devuelve la respuesta.
    Maneja errores de conexión, autenticación y límite de uso de la API.
    """

    intentos = 3  # 🔄 Número de veces que intentará en caso de error

    for intento in range(intentos):
        try:
            respuesta_api = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pregunta_usuario}],
                max_tokens=50  # 🔹 Reducimos tokens para evitar gastar muchos créditos
            )
            return respuesta_api["choices"][0]["message"]["content"]

        except openai.error.AuthenticationError:
            print("❌ ERROR: Clave de API inválida. Verifica tu .env.")
            return "Error de autenticación con la API."

        except openai.error.APIConnectionError:
            print("❌ ERROR: No se pudo conectar con OpenAI. Verifica tu conexión a Internet.")
            return "Error de conexión con la API."

        except openai.error.RateLimitError:
            print(f"⏳ ERROR: Superaste el límite de uso. Intento {intento+1}/{intentos}. Esperando 5 segundos...")
            time.sleep(5)  # 🔄 Esperamos 5 segundos antes de intentar de nuevo
            continue  # 🔄 Intenta nuevamente en la siguiente iteración

        except openai.error.OpenAIError as e:
            print(f"⚠️ ERROR inesperado de OpenAI: {e}")
            return "Hubo un problema con la API."

        except Exception as e:
            print(f"⚠️ ERROR desconocido: {e}")
            return "Ocurrió un error inesperado."
    return "🚫 No se pudo obtener una respuesta después de varios intentos."


# 🔹 Función principal para interactuar con el asistente
def main():
    print("🤖 Asistente de IA - Escribe 'salir' para terminar.")

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower() == "salir":  # Si el usuario escribe "salir", terminamos el programa
            print("👋 ¡Hasta luego!")
            break

        respuesta = obtener_respuesta(pregunta)  # Obtenemos la respuesta de OpenAI
        print(f"🤖 Asistente: {respuesta}")


# 🔹 Ejecutamos la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
