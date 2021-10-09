# Address Book
A simple address book API where users can maintain their addresses.

# Local development
Docker and docker-compose are needed to run the project locally.

The easiest way to work with the project is
to install the make tool (https://www.gnu.org/software/make/) which can be used to build, run or debug
the project.

To build the project image run
```
make build
```

After that, you can start the server with
```
make server
```

This will start the "server" container and the "db" container.

To see all commands supported by Makefile run
```
make help
```
