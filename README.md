# Address Book
A simple address book API where users can maintain their addresses.

# Local development
Docker and docker-compose are needed to run the project locally.

The easiest way to work with the project is
to install the make tool (https://www.gnu.org/software/make/) which can be used to build the project, run the
containers, list their statuses, etc.

To build the development image run:
```
make build
```

By default, the image will use the _address_book_development_ name and _latest_ tag

You can also build the production image by running:
```
make build env=production
```

After that, you can start the development server with:
```
make server
```

To run the server with a different image and tag (e.g. production), you can specify the `TARGET_ENV` and `IMAGE_TAG`
environment variables before running `make server`.

This will start the _server_ and _db_ containers.

To display the logs of all running containers run
```
make logs
```

To see all commands supported by Makefile run
```
make help
```
