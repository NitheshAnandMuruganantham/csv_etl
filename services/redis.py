import redis
from bootstrap_config import app_config
from repository.customers import CustomerRepository
from repository.materials import MaterialRepository
from repository.vehicles import VehicleRepository
from repository.invoices import InvoicesRepository
from tqdm import tqdm


class RedisService:
    def __init__(self, db):
        self.client = redis.Redis(
            host=app_config["REDIS_URL"], password=app_config["REDIS_PASSWORD"], port=app_config["REDIS_PORT"], db=0)
        self.db = db

    def cache_customers(self):
        print("Caching customers")
        customers = CustomerRepository(self.db).findAll()
        for customer in tqdm(customers):
            self.client.hmset("customer_" + str(customer.id),
                              {
                                  "id": customer.id,
                                  "name": customer.name
            })

    def cache_materials(self):
        print("Caching materials")
        materials = MaterialRepository(self.db).findAll()
        for material in tqdm(materials):
            self.client.hmset("material_" + str(material.id),
                              {
                                  "id": material.id,
                                  "name": material.name,
            })

    def cache_vehicles(self):
        print("Caching vehicles")
        vehicles = VehicleRepository(self.db).findAll()
        for vehicle in tqdm(vehicles):
            self.client.hmset("vehicle_" + str(vehicle.id),
                              {
                                  "id": vehicle.id,
                                  "name": vehicle.name,
            })

    def cache_vehicle_numbers(self):
        print("Caching vehicle numbers")
        vehicles = InvoicesRepository(self.db).getVehicleNumbers()
        for vehicle in tqdm(vehicles):
            self.client.hmset("vehicle_number_" + str(vehicle.vehicle_number),
                              {
                                  "id": vehicle.id,
                                  "name": vehicle.name
            })

    def search(self, search_type, search):
        print(f"Searching {search_type}")
        results = []
        keys = self.client.keys(search_type + search + "*")
        for key in keys:
            results.append(dict(self.client.hgetall(key)))
        return results
