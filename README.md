# Device Energy Supervisor

### (Implementation) Device - server/switch ***
  - name
  - description
  - serial number
  - number of unit which occupies within the rack (1+, only natural numbers)
  - electricity consumption of energy expressed in Watts (300W, 500W, 1200W...)

### (Implementation) Rack
  - name
  - description
  - serial number
  - number of unit witch can support (42U, 48U...)
  - maximum declared electricity consumption energy (5000W+)

### CRUD operation for devices and racks ***

### Returning rack, total capacity for energy consumption for rack and each device

### Functionality:
  - user input: specific devices and racks
  - output: balanced arrangement of given devices by given racks
  - condition : rack should have a similar consumption to each other (0%-100%)
  - Error: decide where to add or arrange devices
  - It is not necessary to take into account the current distribution and to which units the device goes

## Running the application

Start the app using Docker Compose:
```bash
docker compose up -d
```

OpenAPI docs are available at:
http://127.0.0.1:8000/docs

## Running tests:

```bash
pytest tests/ -v
```

## Data flow architecture

(Client) --> (Routers) --> (Services) --> (Repositories) --> (Database)

Each layer responsibility:
  - Client – sends requests to the API
  - Routers – FastAPI endpoints handling HTTP requests
  - Services – business logic and data processing
  - Repositories – database access
  - Database – data storage and management



