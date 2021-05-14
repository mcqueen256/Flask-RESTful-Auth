"""
`Storage Adaptors` are database/datastorage abstractions. Is is not known if the
developer will be using an SQL database, MongoDB, Redis or another method of
storing data. The Storage Adaptors serve as a bridge between the actions this
library needs to perform and concrete implementation of the data storage
service.

`Storage Adaptors` are transaction based. A client object can be retreived from
the data store and manipulated with the storage adaptor functions. The client
object should have all the necessary attributes.

"""

import uuid
from passlib.hash import sha256_crypt

class StorageAdaptorInterface(object):
    """`StorageAdaptorInterface` is an interface that describes the minimum
    required actions (function) the database will perform. When implementing
    an adaptor, this class should be inherited. A Concrete adaptor must
    override every fucntion in this interface.
    """

    def get_client_by_id(self, id):
        """Get a client object from the given ID.

        :raises NotImplementedError: if the function has not been overrided
            and is used.

        :param id: A unique identifier for the client object.
        :return: An ORM client object.
        """
        raise NotImplementedError()

    def get_client_by_username(self, username):
        raise NotImplementedError()
    
    def set_client_token(self, client, token: str):
        raise NotImplementedError()

    def set_client_authenticated_status(self, client, status: bool):
        raise NotImplementedError()
    
    def save_client(self, client):
        raise NotImplementedError()


from flask_sqlalchemy import SQLAlchemy

class SQLAlchemyStorageAdaptor(StorageAdaptorInterface):

    def __init__(self, db: SQLAlchemy, ClientClass):
        self.ClientClass = ClientClass
        self.db = db

    def get_client_by_id(self, id):
        return self.ClientClass.query.filter_by(id=id).first()
    
    def get_client_by_username(self, username):
        return self.ClientClass.query.filter_by(username=username).first()

    def set_client_token(self, client, token: str):
        client.token = token
    def set_client_Refresh_token(self, client, token: str):
        client.r_token = token

    def set_client_authenticated_status(self, client, status: bool):
        client.is_authenticated = status
    
    def save_client(self, client):
        self.db.session.add(client)
        self.db.session.commit()
    
    def create_client(self, username, password):
        # Check if the client already exists.
        client = self.get_client_by_username(username)
        if client is not None:
            return None # Not allowed to re-create clients.
        new_user = self.ClientClass(
            id=str(uuid.uuid4()),
            is_active=True,
            is_authenticated=False,
            password=sha256_crypt.hash(password),
            username=username,
        )
        return new_user