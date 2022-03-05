# Address Book
Assignment for a senior backend engineer position at Qogita. A simple address book API where users can maintain their addresses.

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

After that, you can start the development server with:
```
make server
```

which will start the _server_ and _db_ containers.

To run the server with a different image and tag (e.g. production), you can specify the `TARGET_ENV` and `IMAGE_TAG`
environment variables before running `make server`.



To display the logs of all running containers run
```
make logs
```

To run the tests run:
```
make test
```

To see all commands supported by Makefile run
```
make help
```

A swagger documentation of the project can be accessed by the http://localhost:8000/swagger/ url.
