# Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia

import json


class StockInvalidoError(Exception):
    pass


class DispositivoEcologico:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = float(precio)
        self._stock = 0
        self.stock = stock  

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise StockInvalidoError(
                f"No se puede asignar un stock negativo ({nuevo_stock}) al producto '{self.nombre}'."
            )
        self._stock = int(nuevo_stock)

    def ficha_tecnica(self):
        return f"Dispositivo: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock} unidades"

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


DispositivoEcológico = DispositivoEcologico


class PanelSolar(DispositivoEcologico):
    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = float(potencia_w)
        self.eficiencia = float(eficiencia)

    def ficha_tecnica(self):
        ficha_base = super().ficha_tecnica()
        return f"{ficha_base} | Potencia: {self.potencia_w}W | Eficiencia: {self.eficiencia}%"

    def to_dict(self):
        datos = super().to_dict()
        datos["potencia_w"] = self.potencia_w
        datos["eficiencia"] = self.eficiencia
        return datos


class GestorInventario:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        datos_serializados = [disp.to_dict() for disp in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_serializados, archivo, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Creación de productos válidos
    bateria = DispositivoEcologico("Batería de Litio EcoVolt", 850.0, 12)
    panel_mono = PanelSolar("Panel Solar Monocristalino", 320.5, 25, 450, 21.5)
    panel_poli = PanelSolar("Panel Solar Policristalino", 210.0, 18, 330, 17.8)

    catalogo = [bateria, panel_mono, panel_poli]

    print("--- Fichas Técnicas del Catálogo ---")
    for prod in catalogo:
        print(prod.ficha_tecnica())

    print("\n--- Prueba de validación de stock ---")
    try:
        print("Intentando actualizar el stock del panel monocristalino a -5...")
        panel_mono.stock = -5
    except StockInvalidoError as e:
        print(f"Error capturado correctamente: {e}")

    try:
        print("Intentando crear un dispositivo con stock inicial -10...")
        producto_invalido = PanelSolar("Panel Defectuoso", 150.0, -10, 300, 15.0)
    except StockInvalidoError as e:
        print(f"Error capturado correctamente: {e}")

    # Guardado de los productos válidos en JSON
    gestor = GestorInventario()
    archivo_salida = "catalogo_ecotech.json"
    gestor.guardar_catalogo_json(catalogo, archivo_salida)
    print(f"\nCatálogo exportado exitosamente en '{archivo_salida}'.")
