# TODO: graphql-codegen-python

from typing import Union
from dataclasses import dataclass
from types import SimpleNamespace

from gql import gql
import dacite

query = gql(
  """
mutation command($text:String)
{
  createCommand(command:$text)
  {
    direct
    response
  	{
      ...on CodeResponse
      {
        code
        {
          answer
        }
        description
        {
          answer
          anonymizedCode
        }
      }
      ...on DirectResponse
      {
        answer
      }
  	}
  }
}
""")

@dataclass
class command:
  @dataclass
  class createCommand:
    direct: bool

    @dataclass
    class directResponse:
      answer: str

    @dataclass
    class codeResponse:
      @dataclass
      class code:    
        answer: str
      code: code

      @dataclass
      class description:
        answer: str
        anonymizedCode: str    
      description: description
      
    response: Union[directResponse, codeResponse]
  createCommand: createCommand    

  @classmethod    
  def execute(cls, client, **kwargs) -> 'command':
    response = client.execute(query, variable_values=kwargs)
    return dacite.from_dict(data_class=command, data=response)
