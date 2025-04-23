import os
from logica import Articulo, ParserHtml, LongitudInvalidaError

articulos_ejemplo = [
    ("El clima en la ciudad", "  juan perez  ", "Hoy el clima es soleado y cálido. Las temperaturas se mantienen alrededor de los 28°C durante el día, lo que lo convierte en un día ideal para disfrutar de actividades al aire libre. La brisa suave ayuda a mitigar el calor, creando condiciones agradables para caminar por el parque o ir a la playa. A lo largo de la tarde, las nubes comenzarán a cubrir parcialmente el cielo, pero no se esperan lluvias. En la noche, la temperatura descenderá a unos 18°C, lo que permitirá una noche fresca y agradable. Este tipo de clima es típico en los meses de primavera, cuando las temperaturas son moderadas y las lluvias aún no se presentan con regularidad. Los expertos recomiendan aprovechar estos días para realizar actividades que mejoren nuestra salud física y mental, como hacer ejercicio al aire libre o simplemente disfrutar de una caminata por la ciudad. Las personas que viven en áreas urbanas deben aprovechar el buen clima para desconectarse del ajetreo cotidiano y disfrutar de la naturaleza que la ciudad ofrece, ya sea en parques, jardines o en la orilla de algún río cercano. También se puede disfrutar de una buena taza de café mientras se observa el paisaje urbano, algo que puede ser muy relajante para aquellos que necesitan un respiro de la rutina diaria. No olvides usar protector solar si planeas pasar mucho tiempo al sol, ya que la exposición prolongada puede ser perjudicial para la piel."),
    ("Las últimas tecnologías", "Ana Gomez", "Las últimas tendencias en tecnología son fascinantes."),
    ("Importancia de la salud", "Luis Martinez", "Es importante cuidar nuestra salud mental y física."),
    ("Avances científicos destacables del 2024", "Maria Lopez", "Los avances científicos están cambiando el mundo."),
    ("El impacto del cambio climático", "Maria Lopez", "El cambio climático está afectando a todas las regiones del mundo. Las temperaturas extremas, las sequías prolongadas y las lluvias torrenciales son solo algunos de los efectos visibles. Es crucial tomar medidas para mitigar estos impactos."),
    ("Nuevas fronteras en la exploración espacial", "Maria Lopez", "La exploración espacial ha alcanzado nuevos hitos con misiones a Marte y el desarrollo de tecnologías para la colonización lunar. Estos avances están marcando el comienzo de una nueva era en la ciencia."),
    ("Cómo mejorar la productividad en el trabajo", "Juan Perez", "La productividad en el trabajo puede mejorarse con una buena planificación, descansos regulares y el uso de herramientas tecnológicas. Además, mantener un equilibrio entre la vida laboral y personal es clave."),
    ("Tendencias en inteligencia artificial", "Ana Gomez", "La inteligencia artificial está transformando industrias como la salud, la educación y el transporte. Las nuevas aplicaciones de aprendizaje automático están revolucionando la forma en que interactuamos con la tecnología.")
]

art = []

for titulo, autor, texto in articulos_ejemplo:
    try:
        articulo = Articulo(titulo, autor, texto)
        art.append(articulo)
    except LongitudInvalidaError as e:
        print(f"Error al crear artículo: {e}")

parser = ParserHtml(art)

parser.generar_index()

print("Archivos generados correctamente:")
print("- index.html")
print("- artículos individuales en carpeta /articulos")

palabra = "clima"
filtrados = parser.filtrar_por_palabra(palabra)
print(f"Artículos que contienen la palabra clave '{palabra}':")
for articulo in filtrados:
    print(" -", articulo.titulo)
