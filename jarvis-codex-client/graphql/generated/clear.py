# TODO: graphql-codegen-python

from typing import Union
from dataclasses import dataclass
from types import SimpleNamespace

from gql import gql
import dacite

query = gql(
  """
mutation clear
{
  clear
  {
    Pass
  }
}
""")

@dataclass
class Clear:
  @classmethod    
  def execute(cls, client, **kwargs) -> 'Clear':
    response = client.execute(query, variable_values=kwargs)
    return dacite.from_dict(data_class=Clear, data=response)
