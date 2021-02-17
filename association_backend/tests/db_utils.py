import sqlalchemy
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm.session import object_session


def create_database(url) -> None:
    parsed_url = make_url(url)
    db_name = parsed_url.database

    with sqlalchemy.create_engine(
        "postgresql:///postgres", isolation_level="AUTOCOMMIT"
    ).connect() as connection:
        query = "CREATE DATABASE {0} TEMPLATE {1}".format(
            quote(connection, db_name), "template1"
        )
        connection.execute(query)


def drop_database(url) -> None:
    parsed_url = make_url(url)
    db_name = parsed_url.database

    with sqlalchemy.create_engine(
        "postgresql:///postgres", isolation_level="AUTOCOMMIT"
    ).connect() as connection:
        query = "DROP DATABASE {0}".format(quote(connection, db_name))
        connection.execute(query)


def database_exists(url) -> bool:
    parsed_url = make_url(url)

    with sqlalchemy.create_engine(
        "postgresql:///postgres", isolation_level="AUTOCOMMIT"
    ).connect() as connection:
        print(f"parsed_url.database : {parsed_url.database}")
        query = "SELECT 1 FROM pg_database WHERE datname='{0}'".format(
            parsed_url.database
        )
        result = connection.execute(query)
        return bool(result.scalar())


def quote(mixed, ident):
    """
    Conditionally quote an identifier.
    ::
        from sqlalchemy_utils import quote
        engine = create_engine('sqlite:///:memory:')
        quote(engine, 'order')
        # '"order"'
        quote(engine, 'some_other_identifier')
        # 'some_other_identifier'
    :param mixed: SQLAlchemy Session / Connection / Engine / Dialect object.
    :param ident: identifier to conditionally quote
    """
    if isinstance(mixed, Dialect):
        dialect = mixed
    else:
        dialect = get_bind(mixed).dialect
    return dialect.preparer(dialect).quote(ident)


def get_bind(obj):
    """
    Return the bind for given SQLAlchemy Engine / Connection / declarative
    model object.
    :param obj: SQLAlchemy Engine / Connection / declarative model object
    ::
        from sqlalchemy_utils import get_bind
        get_bind(session)  # Connection object
        get_bind(user)
    """
    if hasattr(obj, "bind"):
        conn = obj.bind
    else:
        try:
            conn = object_session(obj).bind
        except UnmappedInstanceError:
            conn = obj

    if not hasattr(conn, "execute"):
        raise TypeError(
            "This method accepts only Session, Engine, Connection and "
            "declarative model objects."
        )
    return conn
