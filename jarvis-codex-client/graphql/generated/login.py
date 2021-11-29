# TODO: graphql-codegen-python

from typing import Union
from dataclasses import dataclass

from gql import gql
import dacite

query = gql(
  """
mutation login($username:String!, $password: String!)
{
  tokenAuth(username:$username, password:$password)
  {
      success
      token
  }
}
""")

@dataclass
class Login:
  @dataclass
  class TokenAuth:
    success: bool = False
    token: str = ""
  tokenAuth: TokenAuth = TokenAuth()

  @classmethod    
  def execute(cls, client, **kwargs) -> 'Login':
    response = client.execute(query, variable_values=kwargs)
    return dacite.from_dict(data_class=Login, data=response, config=dacite.Config(check_types=False))