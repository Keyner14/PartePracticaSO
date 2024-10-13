from collections import deque

class Process:
    def __init__(self, identifier, arrival_time, cpu_time, priority, queue):
        self.identifier = identifier
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time
        self.remaining_time = cpu_time
        self.priority = priority
        self.queue = queue
        self.completion_time = 0
        self.waiting_time = 0
        self.response_time = 0
        self.turnaround_time = 0
        self.start_time = None

    def __repr__(self):
        return f"Process({self.identifier}, arrival={self.arrival_time}, cpu={self.cpu_time}, priority={self.priority}, queue={self.queue})"
class Queue:
    def __init__(self, algorithm, quantum=None, queue_number=None):
        self.algorithm = algorithm
        self.quantum = quantum
        self.queue = deque()
        self.queue_number = queue_number

    def add_process(self, process):
        self.queue.append(process)

    def get_next_process(self, time):
        if self.algorithm == 'RR':
            return self.queue.popleft()
        elif self.algorithm == 'SJF':
            self.queue = deque(sorted(self.queue, key=lambda p: p.remaining_time))
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0

class MLQScheduler:
    def __init__(self):
        self.queues = [
            Queue('RR', quantum=1, queue_number=1),
            Queue('RR', quantum=3, queue_number=2),
            Queue('SJF', queue_number=3)
        ]
        self.time = 0
        self.completed_processes = []

    def add_process(self, process):
        self.queues[process.queue - 1].add_process(process)
        

    def load_processes(self, processes):
        for process in processes:
            self.add_process(process)

    def run(self):
        while any(not queue.is_empty() for queue in self.queues):
            for queue in self.queues:
                if not queue.is_empty():
                    if queue.algorithm == 'RR':
                        self.run_rr(queue)
                    else:
                        self.run_sjf(queue)

    def run_rr(self, queue):
        remaining_processes = list(queue.queue)
        queue.queue.clear()
        time = self.time
        quantum = queue.quantum
        completed = []

        while remaining_processes or queue.queue:
            # Agregar procesos a la cola de listos
            for process in sorted(remaining_processes[:], key=lambda x: (x.arrival_time, x.identifier)):      
                if process.arrival_time <= time and process.queue == queue.queue_number:
                    queue.queue.append(process)
                    remaining_processes.remove(process)

            if queue.queue:
                current_process = queue.queue.popleft()

                if current_process.start_time is None:
                    current_process.start_time = time
                    current_process.response_time = current_process.start_time - current_process.arrival_time

                execution_time = min(quantum, current_process.remaining_time)
                time += execution_time
                current_process.remaining_time -= execution_time

                if current_process.remaining_time == 0:
                    current_process.completion_time = time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.cpu_time
                    completed.append(current_process)
                    self.completed_processes.append(current_process)
                else:
                    queue.queue.append(current_process)
            else:
                # Incrementar el tiempo solo si no hay procesos en la cola
                time += 1

        self.time = time

    def run_sjf(self, queue):
        while not queue.is_empty():
            process = queue.get_next_process(self.time)
            if process.start_time is None:
                process.start_time = self.time
                process.response_time = self.time - process.arrival_time

            execution_time = process.remaining_time
            self.time += execution_time
            process.remaining_time -= execution_time

            if process.remaining_time == 0:
                process.completion_time = self.time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.cpu_time
                self.completed_processes.append(process)

    def leer_linea_y_caracter(self, archivo, indice_linea, indice_inicio, cantidad):
        with open(archivo, "r") as file:
            lines = file.readlines()
            if indice_linea < len(lines):
                texto_sin_salto = lines[indice_linea].strip()
                if indice_inicio + cantidad <= len(texto_sin_salto):
                    return texto_sin_salto[indice_inicio:indice_inicio + cantidad]
                else:
                    raise IndexError("El rango de caracteres está fuera de los límites de la línea.")
            else:
                raise IndexError("El índice de línea está fuera de rango.")
    def escribir_linea_y_caracter(self, archivo, indice_linea, indice_inicio, texto):
        with open(archivo, "r") as file:
            lines = file.readlines()

        # Asegurarse de que el archivo tenga suficientes líneas
        while len(lines) <= indice_linea:
            lines.append('\n')

        linea = lines[indice_linea]
        texto_sin_salto = linea.strip()
        nueva_linea = texto_sin_salto[:indice_inicio] + texto + texto_sin_salto[indice_inicio + len(texto):]
        lines[indice_linea] = nueva_linea + '\n'

        with open(archivo, "w") as file:
            file.writelines(lines)
    
    def calcular_promedios(self, n):
        if n > len(self.completed_processes):
            n = len(self.completed_processes)

        total_wt = sum(process.waiting_time for process in self.completed_processes[:n])
        total_ct = sum(process.completion_time for process in self.completed_processes[:n])
        total_rt = sum(process.response_time for process in self.completed_processes[:n])
        total_tat = sum(process.turnaround_time for process in self.completed_processes[:n])

        avg_wt = total_wt / n
        avg_ct = total_ct / n
        avg_rt = total_rt / n
        avg_tat = total_tat / n

        return f"WT={avg_wt:.2f}, CT={avg_ct:.2f}, RT={avg_rt:.2f}, TAT={avg_tat:.2f}"
    
    def get_completed_processes(self):
        return self.completed_processes


# Crear el planificador MLQ
scheduler = MLQScheduler()


mlq = "mlq001.txt"


# Crear procesos
# identifier, arrival_time, cpu_time, priority, queue
if (mlq == "mlq001.txt"):
    processes = [
    Process(scheduler.leer_linea_y_caracter("mlq001.txt", 1, 0, 1), int(scheduler.leer_linea_y_caracter("mlq001.txt", 1, 5, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 1, 2, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 1, 11, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 1, 8, 1))),
    Process(scheduler.leer_linea_y_caracter("mlq001.txt", 2, 0, 1), int(scheduler.leer_linea_y_caracter("mlq001.txt", 2, 5, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 2, 2, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 2, 11, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 2, 8, 1))),
    Process(scheduler.leer_linea_y_caracter("mlq001.txt", 3, 0, 1), int(scheduler.leer_linea_y_caracter("mlq001.txt", 3, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 3, 2, 2)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 3, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 3, 9, 1))),
    Process(scheduler.leer_linea_y_caracter("mlq001.txt", 4, 0, 1), int(scheduler.leer_linea_y_caracter("mlq001.txt", 4, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 4, 2, 2)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 4, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 4, 9, 1))),
    Process(scheduler.leer_linea_y_caracter("mlq001.txt", 5, 0, 1), int(scheduler.leer_linea_y_caracter("mlq001.txt", 5, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 5, 2, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 5, 10, 1)), int(scheduler.leer_linea_y_caracter("mlq001.txt", 5, 7, 1)))
]
if (mlq == "mlq006.txt"):
    processes = [
        Process(scheduler.leer_linea_y_caracter("mlq006.txt", 1, 0, 1), int(scheduler.leer_linea_y_caracter("mlq006.txt", 1, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 1, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 1, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 1, 10, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq006.txt", 2, 0, 1), int(scheduler.leer_linea_y_caracter("mlq006.txt", 2, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 2, 3, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 2, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 2, 9, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq006.txt", 3, 0, 1), int(scheduler.leer_linea_y_caracter("mlq006.txt", 3, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 3, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 3, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 3, 10, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq006.txt", 4, 0, 1), int(scheduler.leer_linea_y_caracter("mlq006.txt", 4, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 4, 3, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 4, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 4, 9, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq006.txt", 5, 0, 1), int(scheduler.leer_linea_y_caracter("mlq006.txt", 5, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 5, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 5, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq006.txt", 5, 10, 1)))
    ]
if (mlq == "mlq010.txt"):
    processes = [
        Process(scheduler.leer_linea_y_caracter("mlq010.txt", 1, 0, 1), int(scheduler.leer_linea_y_caracter("mlq010.txt", 1, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 1, 3, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 1, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 1, 9, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq010.txt", 2, 0, 1), int(scheduler.leer_linea_y_caracter("mlq010.txt", 2, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 2, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 2, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 2, 10, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq010.txt", 3, 0, 1), int(scheduler.leer_linea_y_caracter("mlq010.txt", 3, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 3, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 3, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 3, 10, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq010.txt", 4, 0, 1), int(scheduler.leer_linea_y_caracter("mlq010.txt", 4, 7, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 4, 3, 2)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 4, 13, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 4, 10, 1))),
        Process(scheduler.leer_linea_y_caracter("mlq010.txt", 5, 0, 1), int(scheduler.leer_linea_y_caracter("mlq010.txt", 5, 6, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 5, 3, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 5, 12, 1)), int(scheduler.leer_linea_y_caracter("mlq010.txt", 5, 9, 1)))
    ]

# Cargar los procesos en el planificador
scheduler.load_processes(processes)

# Ejecutar el planificador
scheduler.run()

# Obtener y mostrar los procesos completados
completed_processes = scheduler.get_completed_processes()

# Ordenar los procesos completados por identifier
completed_processes.sort(key=lambda p: p.identifier)

for index, process in enumerate(completed_processes):
    frase = f"{process.identifier};{process.cpu_time};{process.arrival_time};{process.queue};{process.priority};{process.waiting_time};{process.completion_time};{process.response_time};{process.turnaround_time}"
    scheduler.escribir_linea_y_caracter(mlq, index + 1, 0, frase)

# Calcular y mostrar los promedios
n = len(completed_processes)
promedios = scheduler.calcular_promedios(n)
scheduler.escribir_linea_y_caracter(mlq, len(completed_processes) + 1, 0, promedios)