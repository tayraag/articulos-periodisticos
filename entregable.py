import zipfile
import os

archivos_a_incluir = [
    "main.py",          
    "logica.py",        
    "test.py",       
    "style_arti.css",   
    "style_cpag.css",  
    "index.html",     
    "articulos",       
]

zip_filename = "entrega_tp2.zip"

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for item in archivos_a_incluir:
        if os.path.isfile(item):
            zipf.write(item)
        elif os.path.isdir(item):
            for foldername, subfolders, filenames in os.walk(item):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    zipf.write(filepath)

print(f"Archivo {zip_filename} creado con éxito.")
