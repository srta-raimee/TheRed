
import threading
import time
from random import randint
from pyfiglet import figlet_format

from threading import Thread, Condition

print(figlet_format("Restaurante\n The Red", font="standard"))
time.sleep(3)

report_file = "restaurant_report.txt"


class Garcom(Thread):
    def __init__(self, nome, cozinheiros, pedidos, condition, report_file):
        super().__init__()
        self.nome = nome
        self.cozinheiros = cozinheiros
        self.pedidos = pedidos
        self.condition = condition
        self.report_file = report_file
    
    def fazer_pedido(self, pedido):
        with self.condition:
            if all(cozinheiro.encerrar_programa for cozinheiro in self.cozinheiros):
                return

            self.pedidos.append(pedido)
            message = f"{self.nome}: Fez pedido {pedido}"
            with open(self.report_file, "a") as file:
                file.write(message + "\n")
            print(message)
            num = randint(1, 2)
            time.sleep(num)
    
    def run(self):
        for i in range(10):
            if all(cozinheiro.encerrar_programa for cozinheiro in self.cozinheiros):
                break

            pedido = f"{self.nome}-{i+1}"
            self.fazer_pedido(pedido)
            time.sleep(1)

        message = f"{self.nome}: Encerrando expediente..."
        with open(self.report_file, "a") as file:
            file.write(message + "\n")
        print(message)
        for cozinheiro in self.cozinheiros:
            cozinheiro.encerrar_programa = True


class Cozinheiro(Thread):
    def __init__(self, nome, garcons, pedidos, condition, report_file):
        super().__init__()
        self.nome = nome
        self.garcons = garcons
        self.pedidos = pedidos
        self.condition = condition
        self.report_file = report_file
        self.encerrar_programa = False
    
    def prepara_pedido(self):
        while True:
            with self.condition:
                if len(self.pedidos) == 0:
                    if all(garcom.cozinheiros[0].encerrar_programa and garcom.cozinheiros[1].encerrar_programa for garcom in self.garcons):
                        return True

                    message = f"{self.nome}: Sem pedidos, esperando..."
                    with open(self.report_file, "a") as file:
                        file.write(message + "\n")
                    print(message)
                    self.condition.wait(timeout=0.5)
                else:
                    pedido = self.pedidos.pop(0)
                    message = f"{self.nome}: Preparou pedido {pedido}"
                    with open(self.report_file, "a") as file:
                        file.write(message + "\n")
                    print(message)
                    time.sleep(3)
    
    def run(self):
        while not self.prepara_pedido():
            pass

        message = f"{self.nome}: Encerrando expediente...\nCozinha Fechada!!"
        with open(self.report_file, "a") as file:
            file.write(message + "\n")
        print(message)
        self.encerrar_programa = True


while True:
    print("========== MENU ==========")
    print("1. Um cozinheiro")
    print("2. Dois cozinheiros")
    print("0. Sair")
      
    n = input("Escolha uma opção: ")
   
    n = int(n)
    
    if n == 1:
        message = ("\n\n====== Um cozinheiro ======")
        with open("report_file.txt", "a") as file:
            file.write(message + "\n")

        pedidos = []
        condition = Condition()
        garcons = [
            Garcom("Garçom 1", [], pedidos, condition, report_file),
            Garcom("Garçom 2", [], pedidos, condition, report_file)
        ]
        cozinheiro1 = Cozinheiro("Cozinheiro 1", garcons, pedidos, condition, report_file)

        for garcom in garcons:
            garcom.cozinheiros = [cozinheiro1]

        tempo_inicial = time.time()

        # Inicia as threads
        cozinheiro1.start()
        for garcom in garcons:
            garcom.start()

        cozinheiro1.join()
        for garcom in garcons:
            garcom.join()

        tempo_final = time.time()

        tempo_total = tempo_final - tempo_inicial

        print("\n\n**** Relatório gerado! ****")
        message = f"Tempo total de atendimento: {tempo_total:.3f} segundos"
        with open("report_file.txt", "a") as file:
            file.write(message + "\n")
      
    elif n == 2:
        message = ("\n\n====== Dois cozinheiros ======")
        with open("report_file.txt", "a") as file:
            file.write(message + "\n")

        pedidos = []
        condition = Condition()
        garcons = [
            Garcom("Garçom 1", [], pedidos, condition, report_file),
            Garcom("Garçom 2", [], pedidos, condition, report_file)
        ]
        cozinheiro1 = Cozinheiro("Cozinheiro 1", garcons, pedidos, condition, report_file)
        cozinheiro2 = Cozinheiro("Cozinheiro 2", garcons, pedidos, condition, report_file)

        for garcom in garcons:
            garcom.cozinheiros = [cozinheiro1, cozinheiro2]

        tempo_inicial = time.time()

        # Inicia as threads
        cozinheiro1.start()
        cozinheiro2.start()
        for garcom in garcons:
            garcom.start()

        cozinheiro1.join()
        cozinheiro2.join()
        for garcom in garcons:
            garcom.join()

        tempo_final = time.time()

        tempo_total = tempo_final - tempo_inicial

        print("\n\n**** Relatório gerado! ****")
        message = f"Tempo total de atendimento: {tempo_total:.3f} segundos"
        with open("report_file.txt", "a") as file:
            file.write(message + "\n")
      
    else:
        print("\n\n**** Até a próxima! ****")
        break
