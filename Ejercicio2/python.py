import json

class StockInvalidoError(Exception):
    """Excepción que se lanza cuando se asigna un stock negativo o no entero."""
    pass


class DispositivoEcológico:
    """Clase base que representa cualquier dispositivo ecológico del catálogo."""
    
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self._stock = 0
        self.stock = stock  # Usa el setter para validar desde el inicio

    @property
    def stock(self) -> int:
        """Obtiene el stock actual del dispositivo."""
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        """Asigna el stock validando que sea un número entero mayor o igual a cero."""
        if not isinstance(valor, int) or valor < 0:
            raise StockInvalidoError(f"El stock debe ser un entero positivo. Valor recibido: {valor}")
        self._stock = valor

    def ficha_tecnica(self) -> str:
        """Devuelve una cadena con la información básica del dispositivo."""
        return f"{self.nombre} ({self.codigo}) - ${self.precio:,.2f} - Stock: {self._stock}"

    def a_diccionario(self) -> dict:
        """Serializa los atributos del dispositivo a un diccionario estándar."""
        return {
            "tipo": self.__class__.__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self._stock
        }


class PanelSolar(DispositivoEcológico):
    """Clase especializada para paneles solares, heredando de DispositivoEcológico."""
    
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int, potencia_w: float, tipo_celda: str):
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_w = potencia_w
        self.tipo_celda = tipo_celda

    def ficha_tecnica(self) -> str:
        """Sobrescribe el método para incluir los datos específicos del panel (Polimorfismo)."""
        base = super().ficha_tecnica()
        return f"[Panel Solar] {base} | Potencia: {self.potencia_w}W | Celda: {self.tipo_celda}"

    def a_diccionario(self) -> dict:
        """Extiende el diccionario base sumando los atributos propios del panel."""
        d = super().a_diccionario()
        d.update({
            "potencia_w": self.potencia_w,
            "tipo_celda": self.tipo_celda
        })
        return d


class GestorInventario:
    """Clase encargada de las operaciones de persistencia del catálogo."""
    
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo: str):
        """Serializa la lista de dispositivos y los guarda en un archivo JSON."""
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print(f"Catálogo exportado exitosamente en '{ruta_archivo}'.")


if __name__ == "__main__":
    # 1. Prueba de excepción por stock negativo al instanciar
    try:
        p_error = PanelSolar("P99", "Panel Defectuoso", 1000.0, -5, 300, "Monocristalino")
    except StockInvalidoError as err:
        print(f"Excepción capturada correctamente: {err}")

    # 2. Creación de elementos válidos
    p1 = PanelSolar("PS1", "SolarMax", 250000.0, 10, 400, "Monocristalino")
    p2 = PanelSolar("PS2", "SolarLite", 180000.0, 15, 300, "Policristalino")
    disp = DispositivoEcológico("GEN1", "Termotanque Solar", 450000.0, 4)

    catalogo = [p1, p2, disp]

    # 3. Demostración de polimorfismo
    print("\nFichas técnicas del catálogo:")
    for item in catalogo:
        print(item.ficha_tecnica())

    # 4. Prueba de modificación inválida en un objeto existente
    try:
        p1.stock = -3
    except StockInvalidoError as err:
        print(f"\nError al modificar stock: {err}")

    # 5. Exportación final a JSON
    print("\nGuardando datos...")
    GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
