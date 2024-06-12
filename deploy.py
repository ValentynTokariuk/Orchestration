import docker
client = docker.from_env()

# Define container names
postgres_container_name = 'postgres-db'

# Check if the container already exists
existing_containers = client.containers.list(all=True)
for container in existing_containers:
    if container.name == postgres_container_name:
        print(f"Stopping and removing existing container: {postgres_container_name}")
        container.stop()
        container.remove()

# Now, create the containers
print("Creating new PostgreSQL container")
postgres_container = client.containers.run(
    'postgres:latest',
    name=postgres_container_name,
    network='university-net',
    environment={
        'POSTGRES_DB': 'universitydb',
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'pass'
    },
    ports={'5432/tcp': 5432},
    detach=True
)

print("Containers running:")
for container in client.containers.list():
    print(container.name)

