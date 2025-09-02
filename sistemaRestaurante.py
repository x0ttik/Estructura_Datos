# nodo para la lista enlazada
class Node:
    def __init__(self, client_name, party_size, reservation_time):
        self.client_name = client_name
        self.party_size = party_size
        self.reservation_time = reservation_time
        self.next = None

# clase para la lista de espera del restaurante
class RestaurantWaitlist:
    def __init__(self):
        self.head = None

        # Mesas disponibles por tamaño temp 2 4 6 personas
        self.tables = {2: 5, 4: 3, 6: 2}  # inicial 5 mesas de 2, 3 de 4, 2 de 6
        self.wait_time_per_table = 30  # tiempo promedio por mesa en minutos

    def add_client(self, client_name, party_size, reservation_time):
        """Anotar cliente en la lista de espera"""
        new_node = Node(client_name, party_size, reservation_time)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        print(f"cliente {client_name} añadido a la lista de espera para {party_size} personas.")

    def call_next_table(self):
        """llamar a la siguiente mesa disponible"""
        if not self.head:
            print("no hay clientes en la lista de espera.")
            return

        current = self.head
        table_size = self._find_suitable_table(current.party_size)
        
        if table_size and self.tables[table_size] > 0:
            print(f"Llamando a {current.client_name} para una mesa de {table_size} personas.")
            self.tables[table_size] -= 1  # Ocupar mesa
            self.head = current.next  # Remover de la lista
        else:
            print(f"no hay mesas disponibles para {current.client_name} (grupo de {current.party_size}).")

    def _find_suitable_table(self, party_size):
        """Encontrar mesa adecuada segun el tamaño del grupo"""
        for size in sorted(self.tables.keys()):
            if party_size <= size:
                return size
        return None

    def view_waitlist(self):
        """ver la lista completa de espera"""
        if not self.head:
            print("la lista de espera esta vacia.")
            return
        
        current = self.head
        print("Lista de espera:")
        while current:
            print(f"- {current.client_name} (Grupo de {current.party_size}, reservado a las {current.reservation_time})")
            current = current.next

    def cancel_reservation(self, client_name):
        """cancelar una reservacion"""
        if not self.head:
            print("la lista de espera esta vacia.")
            return
        
        if self.head.client_name == client_name:
            self.head = self.head.next
            print(f"Reservación de {client_name} cancelada.")
            return

        current = self.head
        while current.next and current.next.client_name != client_name:
            current = current.next
        
        if current.next:
            current.next = current.next.next
            print(f"Reservación de {client_name} cancelada.")
        else:
            print(f"no se encontro a {client_name} en la lista de espera.")

    def estimate_wait_time(self, party_size):
        """Estimar tiempo de espera para un grupo"""
        count = 0
        current = self.head
        while current:
            if current.party_size <= party_size:
                count += 1
            current = current.next
        
        table_size = self._find_suitable_table(party_size)
        if not table_size or self.tables[table_size] == 0:
            wait_time = count * self.wait_time_per_table
        else:
            wait_time = (count - self.tables[table_size]) * self.wait_time_per_table
        
        wait_time = max(0, wait_time)  # No tiempos negativos
        print(f"Tiempo estimado de espera para grupo de {party_size}: {wait_time} minutos.")
        return wait_time

    def show_available_tables(self):
        """mostrar mesas disponibles por tamaño"""
        print("mesas disponibles:")
        for size, count in self.tables.items():
            print(f"- mesas para {size} personas: {count}")

# ejemplo de uso
if __name__ == "__main__":
    waitlist = RestaurantWaitlist()
    
    # añadir clientes
    waitlist.add_client("juan", 4, "18:00")
    waitlist.add_client("maria", 2, "18:10")
    waitlist.add_client("carlos", 6, "18:15")
    
    # ver lista de espera
    waitlist.view_waitlist()
    
    # mostrar mesas disponibles
    waitlist.show_available_tables()
    
    # estimar tiempo de espera
    waitlist.estimate_wait_time(4)
    
    # llamar siguiente mesa
    waitlist.call_next_table()
    
    # cancelar una reservacion
    waitlist.cancel_reservation("María Gómez")
    
    # ver lista actualizada
    waitlist.view_waitlist()
    
    # mostrar mesas disponibles actualizadas
    waitlist.show_available_tables()