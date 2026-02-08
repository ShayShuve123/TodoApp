from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = 'sql:///./todos.db' # used to create a location of this db on our fastapi application

create_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}) # db agent to Opan up a connction to use our db