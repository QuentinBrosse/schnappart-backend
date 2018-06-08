import docker
from django.core.management import BaseCommand

DEFAULT_IMAGE_NAME = "postgres"
DEFAULT_IMAGE_VERSION = "9-alpine"

DEFAULT_CONTAINER_HOSTNAME = "schnappart_db"
DEFAULT_CONTAINER_NAME = "schnappart_db"
DEFAULT_CONTAINER_PORT = 5433


class Command(BaseCommand):
    help = "This command set up a postgres container with a default database"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = docker.from_env()
        self.image_name = "{}:{}".format(
            DEFAULT_IMAGE_NAME,
            DEFAULT_IMAGE_VERSION
        )

    def get_existing_container(self):
        """
        Return the container id if a previous container exist or None if not.
        :return:
        """
        for container in self.client.containers.list(all=True):
            if container.name == DEFAULT_CONTAINER_NAME:
                return container.id
        return None

    def remove_container(self, id=None):
        """
        Stop and remove the container with the identifier id.
        :param id: Id of a container
        :return:
        """
        if id:
            self.stdout.write("Removing container %s" % id)
            container = self.client.containers.get(id)
            container.stop()
            container.remove()

    def pull_image(self):
        self.client.images.pull(self.image_name)

    def handle(self, *args, **options):
        self.pull_image()
        container_id = self.get_existing_container()
        self.remove_container(container_id)
        try:
            container = self.client.containers.run(
                self.image_name,
                name=DEFAULT_CONTAINER_NAME,
                hostname=DEFAULT_CONTAINER_HOSTNAME,
                ports={
                    '5432/tcp': DEFAULT_CONTAINER_PORT
                },
                detach=True,
                stdout=True
            )

            self.stdout.write("New database container %s" % container.id)

        except docker.errors.APIError:
            message_template = (
                'Failed to lunch a databse container. '
                'The port {} might be used by an other container.'
            )
            self.stderr.write(message_template.format(DEFAULT_CONTAINER_PORT))
        except Exception as ex:
            message_template = (
                'Failed to lunch a databse container. '
                'An exception as occured.\n {}'
            )
            self.stderr.write(message_template.format(ex))
