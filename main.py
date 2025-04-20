import os
from logica import Articulo, ParserHtml

articulos_ejemplo = [
    Articulo("El clima en la ciudad", "  juan perez  ", "Hoy el clima es soleado y cálido. Las temperaturas se mantienen alrededor de los 28°C durante el día, lo que lo convierte en un día ideal para disfrutar de actividades al aire libre. La brisa suave ayuda a mitigar el calor, creando condiciones agradables para caminar por el parque o ir a la playa. A lo largo de la tarde, las nubes comenzarán a cubrir parcialmente el cielo, pero no se esperan lluvias. En la noche, la temperatura descenderá a unos 18°C, lo que permitirá una noche fresca y agradable. Este tipo de clima es típico en los meses de primavera, cuando las temperaturas son moderadas y las lluvias aún no se presentan con regularidad. Los expertos recomiendan aprovechar estos días para realizar actividades que mejoren nuestra salud física y mental, como hacer ejercicio al aire libre o simplemente disfrutar de una caminata por la ciudad. Las personas que viven en áreas urbanas deben aprovechar el buen clima para desconectarse del ajetreo cotidiano y disfrutar de la naturaleza que la ciudad ofrece, ya sea en parques, jardines o en la orilla de algún río cercano. También se puede disfrutar de una buena taza de café mientras se observa el paisaje urbano, algo que puede ser muy relajante para aquellos que necesitan un respiro de la rutina diaria. No olvides usar protector solar si planeas pasar mucho tiempo al sol, ya que la exposición prolongada puede ser perjudicial para la piel."),
    Articulo("Tecnología", "Ana Gomez", "Las últimas tendencias en tecnología son fascinantes."),
    Articulo("Salud", "Luis Martinez", "Es importante cuidar nuestra salud mental y física."),
    Articulo("Ciencia", "Maria Lopez", "Los avances científicos están cambiando el mundo.")
]

parser = ParserHtml(articulos_ejemplo)

ruta_actual = os.getcwd()
html_general = parser.genera_html()
print("¿Contenido generado?:", html_general[:100])

ruta_general = os.path.join(ruta_actual, "todos_los_articulos.html")
with open(ruta_general, "w", encoding="utf-8") as f:
    f.write(html_general)
print(f"Archivo general generado: {ruta_general}")


palabra = "clima"
filtrados = parser.filtrar_por_palabra(palabra)
print(f"Artículos que contienen la palabra clave '{palabra}':")
for articulo in filtrados:
    print("-", articulo.titulo)
