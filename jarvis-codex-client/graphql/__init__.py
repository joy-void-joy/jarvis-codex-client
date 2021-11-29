import gql
from gql.transport.aiohttp import AIOHTTPTransport
import os

transport = AIOHTTPTransport(url=os.environ['GRAPHQL_BACKEND'])
client = gql.Client(transport=transport, fetch_schema_from_transport=True)