from datetime import datetime
from logica import Articulo, ParserHtml

a1 = Articulo("Título válido", "juan pérez", "Este es un texto de prueba.")
assert a1.titulo == "Título válido"
assert a1.autor == "Juan Pérez"
assert a1.contiene_palabra_clave("prueba")
assert not a1.contiene_palabra_clave("inexistente")

try:
    Articulo("Corto", "Autor", "Texto válido")
    assert False, "El título corto no lanzó excepción"
except ValueError:
    pass

try:
    Articulo("Título válido", "Autor", "Corto")
    assert False, "El texto corto no lanzó excepción"
except ValueError:
    pass

a2 = Articulo("Otro artículo", "ana gomez", "Contenido con la palabra clave.")
a3 = Articulo("Artículo sin keyword", "ana gomez", "Otro texto que no contiene nada.")
parser = ParserHtml([a1, a2, a3])
filtrados = parser.filtrar_por_palabra("clave")
assert len(filtrados) == 1
assert filtrados[0] == a2

conteo = parser.contar_articulos_autor()
assert conteo["Juan Pérez"] == 1
assert conteo["Ana Gomez"] == 2

tabla_html = parser.generar_tabla_count()
assert "<table" in tabla_html
assert "Juan Pérez" in tabla_html
assert "Ana Gomez" in tabla_html

lista_html = parser.generar_lista_por_inicial()
for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    assert f">{letra}</a>" in lista_html

footer_html = parser.generar_footer()
hoy = datetime.now().strftime("%Y-%m-%d")
assert hoy in footer_html
