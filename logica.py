import os
from datetime import datetime

class LongitudInvalidaError(Exception):
    def __init__(self, campo, longitud_minima=10):
        super().__init__(f"El campo '{campo}' debe tener al menos {longitud_minima} caracteres.")

class Articulo:
    def __init__(self, titulo, autor, texto):
        if len(titulo.strip()) < 10:
            raise ValueError("El título debe tener al menos 10 caracteres.")
        if len(texto.strip()) < 10:
            raise ValueError("El texto debe tener al menos 10 caracteres.")

        self.titulo = titulo.strip()
        self.autor = self.normalizar_autor(autor)
        self.texto = texto.strip()

    def normalizar_autor(self, autor):
        return " ".join(p.capitalize() for p in autor.strip().split())

    def contiene_palabra_clave(self, palabra):
        return palabra.lower() in self.texto.lower()

class ParserHtml:
    def __init__(self, articulos):
        self.articulos = articulos

    def filtrar_por_palabra(self, palabra):
        return [a for a in self.articulos if a.contiene_palabra_clave(palabra)]

    def contar_articulos_autor(self):
        count = {}
        for articulo in self.articulos:
            autor = articulo.autor
            count[autor] = count.get(autor, 0) + 1
        return count

    def generar_tabla_count(self):
        count = self.contar_articulos_autor()

        autores_ordenados = sorted(count.items(), key=lambda item: item[0].split()[-1].lower())

        tabla = """
        <table class='table'>
            <thead class='thead'>
                <tr>
                    <th>Autor</th>
                    <th>Artículos</th>
                </tr>
            </thead>
        """
        for autor, cantidad in autores_ordenados:
            apellido = autor.split()[-1]
            inicial = apellido[0].upper()
            tabla += f"""
                <tr>
                    <td><a href="#{inicial}">{autor}</a></td>
                    <td>{cantidad}</td>
                </tr>
            """
        tabla += "</table>"
        return tabla

    def generar_lista_por_inicial(self):
        letras = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        lista = ""
        for letra in letras:
            lista += f"<a class='list-group-item list-group-item-action' href='#{letra}'>{letra}</a>\n"
        return lista


    def generar_footer(self):
        an_actual = datetime.now().year
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return f"""
        <footer class='text-center mt-5'>
            <hr>
            <p>Fecha de publicación: {fecha_hoy}</p>
        </footer>
        """

    def generar_articulos_individuales(self, output_dir="articulos"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total = len(self.articulos)

        for i, articulo in enumerate(self.articulos):
            index = i + 1
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            indices_autor = [j for j, a in enumerate(self.articulos) if a.autor == articulo.autor]
            pos_actual = indices_autor.index(i)
            anterior = indices_autor[pos_actual - 1] + 1 if pos_actual > 0 else indices_autor[-1] + 1
            siguiente = indices_autor[pos_actual + 1] + 1 if pos_actual < len(indices_autor) - 1 else indices_autor[0] + 1

            nav_links = "<nav aria-label='Page navigation example' class='d-flex justify-content-center mb-2'>"
            nav_links += "<ul class='pagination'>"

            nav_links += f"""
                <li class='page-item'>
                    <a class='page-link' href='articulo_{anterior}.html' aria-label='Previous'>
                        <span aria-hidden='true'>&laquo;</span>
                    </a>
                </li>"""

            for local_pos, j in enumerate(indices_autor):
                global_index = j + 1
                label = local_pos + 1
                active_class = "active" if j == i else ""
                nav_links += f"<li class='page-item {active_class}'><a class='page-link' href='articulo_{global_index}.html'>{label}</a></li>"

            nav_links += f"""
                <li class='page-item'>
                    <a class='page-link' href='articulo_{siguiente}.html' aria-label='Next'>
                        <span aria-hidden='true'>&raquo;</span>
                    </a>
                </li>"""

            nav_links += "</ul></nav>"

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset='UTF-8'>
                <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>
                <link rel='stylesheet' href='../style_cpag.css'>
            </head>
            <body>
                <nav class='navbar navbar-expand-lg navbar-light bg-light'>
                    <div class='container-fluid'>
                        <a class='navbar-brand' href='../index.html'>Inicio</a>
                    </div>
                </nav>
                <div class='container mt-4'>
                    <article class='mb-4'>
                        <h2>{articulo.titulo}</h2>
                        <p><strong>Autor:</strong> {articulo.autor}</p>
                        <p>{articulo.texto}</p>
                    </article>

                    {nav_links}

                    <hr>
                    <footer class='text-center mt-2'>
                        <p>Fecha de publicación: {fecha_hoy}</p>
                    </footer>
                </div>
            </body>
            </html>
            """

            filename = os.path.join(output_dir, f"articulo_{index}.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)


    def agrupar_por_autor_html(self):
        agrupado = {}
        for articulo in self.articulos:
            apellido = articulo.autor.split()[-1]
            inicial = apellido[0].upper()
            agrupado.setdefault(inicial, {}).setdefault(articulo.autor, []).append(articulo)

        html = ""
        for inicial in sorted(agrupado):
            html += f"<section class='mb-4' id='{inicial}'>"
            for autor in agrupado[inicial]:
                html += f"<h3>{autor}</h3><div class='row'>"
                for i, articulo in enumerate(agrupado[inicial][autor]):
                    index = self.articulos.index(articulo) + 1
                    html += f"""
                        <div class='col-md-3 mb-3'>
                            <article class='articulo'>
                                <h4>{articulo.titulo}</h4>
                                <a href='articulos/articulo_{index}.html' class='btn-leer'>Leer</a>
                            </article>
                        </div>
                    """
                html += "</div>"
            html += "</section>"
        return html

    def generar_index(self, filename="index.html"):
        self.generar_articulos_individuales()
        tabla_aut = self.generar_tabla_count()
        filtro_inicial = self.generar_lista_por_inicial()
        agrupado = self.agrupar_por_autor_html()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>
            <link rel='stylesheet' href='style_arti.css'>
        </head>
        <body>
            <header class="container mt-4">
                <h1 class="text-center mb-4">Artículos Periodísticos</h1>
            </header>

            <div class="tabla-recuadro container mb-4">
                <h2>Artículos por autor:</h2>
                {tabla_aut}
            </div>

            <div class="container" style="margin-left: 100px;">
                <div class="row">
                    <nav class="sidebar-filtro col-md-2">
                        <h5 class="text-center mb-3">Filtrar por apellido</h5>
                        <div id="list-example" class="list-group">
                            {filtro_inicial}
                        </div>
                    </nav>

                    <div class="col-md-10">
                        <div data-bs-spy="scroll" data-bs-target="#list-example" data-bs-smooth-scroll="true"
                            class="scrollspy-example" tabindex="0">
                            {agrupado}
                        </div>
                    </div>
                </div>
            </div>

            {self.generar_footer()}
        </body>
        </html>
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)