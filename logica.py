import os
from datetime import datetime

class Articulo:

    def __init__(self, titulo, autor, texto):
        if len(titulo.strip()) < 5:
            raise ValueError("El título debe tener al menos 10 caracteres.")
        if len(texto.strip()) < 10:
            raise ValueError("El texto debe tener al menos 10 caracteres.")

        self.titulo = titulo.strip()
        self.autor = self.normalizar_autor(autor)
        self.texto = self.truncate_text(texto.strip())

    def normalizar_autor(self, autor):
        return " ".join(p.capitalize() for p in autor.strip().split())

    def to_html(self):
        return f"""
        <article class='mb-4'>
            <h2>{self.titulo}</h2>
            <p><strong>Autor:</strong> {self.autor}</p>
            <p>{self.texto}</p>
        </article>
        """

    def contiene_palabra_clave(self, palabra):
        return palabra.lower() in self.texto.lower()

    @staticmethod
    def truncate_text(texto, length=300):
        return texto[:length] + "..." if len(texto) > length else texto


class ParserHtml:
    def __init__(self, articulos):
        self.articulos = articulos

    def filtrar_por_palabra(self, palabra):
        return [a for a in self.articulos if a.contiene_palabra_clave(palabra)]

    def contar_articulos_autor(self):
        count = {}
        for articulo in self.articulos:
            autor = articulo.autor
            if autor in count:
                count[autor] += 1
            else:
                count[autor] = 1
        return count

    def generar_tabla_count(self):
        count = self.contar_articulos_autor()
        tabla ="""
            <table class='table table-bordered'>
                <thead class='thead-light'>
                    <tr>
                        <th>Autor</th>
                        <th>Artículos</th>
                    </tr>
                </thead>
            <tbody>"""
        for autor, cantidad in count.items():
            tabla += f"""
                    <tr>
                        <td>{autor}</td>
                        <td>{cantidad}</td>
                    </tr>"""
        tabla += """
            </tbody>
            </table>"""
        return tabla

    def generar_footer(self):
       an_actual = datetime.now().year
       fecha_hoy = datetime.now().strftime("%Y-%m-%d")
       return f"""
        <footer class='text-center mt-5'>
            <p>Fecha de publicación: {fecha_hoy}</p>
            <p>&copy; {an_actual} Artículos Periodísticos</p>
        </footer>
        """

    def genera_html(self):
        tabla_aut = self.generar_tabla_count()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <title>Articulos Periodisticos</title>
            <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'>
        </head>
        <body class='bg-light'>
            <nav class='navbar navbar-expand-lg navbar-light bg-white border-bottom'>
                <div class='container'>
                    <a class='navbar-brand' href='articulos.html'>Inicio</a>
                </div>
            </nav>
            <div class='container mt-4'>
                <h1 class='text-center mb-4'>Artículos Periodísticos</h1>
                <div class = 'mb-4'>
                    <strong>Artículos por autor:</strong>
                    {tabla_aut}
                </div>"""

        for articulo in self.articulos:
            html += articulo.to_html()
            html += "<hr>"

        html += self.generar_footer()
        
        html +="""
            </div>
        </body>
        </html>
        """
        return html
