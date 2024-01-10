"""
Módulo de temporizador.
"""

TOLERANCIA: float = 0.1

class Temporizador:
    "Clase de temporizador."

    def __init__(self, temp_inicial: float) -> None:
        """
        Inicializa el temporizador.
        -
        'temp_inicial': El tiempo inicial desde el que contar.
        """

        if temp_inicial <= 0.0:
            raise ValueError(f"Valor temp_inicial={temp_inicial} no válido. Debe de ser "
                             f"un número mayor a cero.")

        self.inic: float = temp_inicial
        self.actual: float = temp_inicial


    def reiniciar(self) -> None:
        "Reinicia el tiempo al inicial."

        self.actual = self.inic


    def esta_contando(self) -> bool:
        "Determina si el temporizador puede contar."

        return self.actual > 0.0


    def porcentaje(self) -> float:
        "Devuelve un valor entre 0.0 y 1.0 que es el porcentaje del total inicial."

        return self.actual / self.inic


    def _no_se_sobrepasa(self, diferencia: float) -> bool:
        "Mide si al substraer algo no se va a ir abajo del piso."

        return (self.actual - diferencia) >= 0.0


    def agotar(self) -> None:
        "Salta el contador directamente a 0."

        self.actual = 0.0


    def contar(self, cuanto: float) -> float:
        """
        Cuenta en el temporizador. Devuelve el tiempo actual.
        -
        'cuanto': Cuánto contar (o descontar) del temporizador.
        """

        if cuanto <= 0.0:
            raise ValueError(f"Valor cuanto={cuanto} no válido. Debe ser un número "
                             "positivo mayor a 0.")

        if not abs(self.actual) <= TOLERANCIA:
            self.actual -= cuanto

        else:
            self.agotar() # Para evitar tener valores MUY cercanos a cero pero que no son cero

        return self.actual


    def actualizar(self, cuanto: float=1.0, reiniciar: bool=False) -> float:
        """
        Cuenta en el temporizador, reiniciándolo de ser necesario.
        También devuelve el tiempo actual.
        -
        'cuanto': Cuánto contar (o descontar) del temporizador.

        'reiniciar': Si se quiere reiniciar de ser posible.
        """

        if self.esta_contando():
            return self.contar(cuanto if self._no_se_sobrepasa(cuanto)
                               else self.actual)

        if reiniciar:
            self.reiniciar()

        return self.actual
