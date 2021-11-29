from __future__ import annotations
from dotenv import load_dotenv
import os
load_dotenv('.env.default')
load_dotenv('.env')

import click
import pygments, pygments.lexers, pygments.formatters
from .To_Exec import to_exec

from . import graphql
from .graphql.generated.command import command
from .graphql.generated.login import Login
from .graphql.generated.clear import Clear
from .spotify import spotify
from retry import retry

locals = {}

@retry()
def main():
    def fetch_login_token():
        username = os.environ.get('USERNAME', "")
        password = os.environ.get('PASSWORD', "")

        while not (token := Login.execute(graphql.client, username=username, password=password)).tokenAuth.success:
            username = click.prompt("Username")
            password = click.prompt("Password", hide_input=True)
        
        return token

    graphql.client.transport.headers = {"Authorization": f"JWT {fetch_login_token().tokenAuth.token}"}

    try:
        while (text:=click.prompt('')):
            if text == "clear":
                Clear.execute(graphql.client)
                continue

            answer = command.execute(graphql.client, text=text).createCommand
            if answer.direct:
                click.echo(answer.response.answer)
            else:
                click.echo(pygments.highlight(
                    inner_code := answer.response.code.answer,
                    pygments.lexers.PythonLexer(),
                    pygments.formatters.TerminalFormatter(),
                ))

                if click.confirm(answer.response.description.answer):
                    try:
                        exec(to_exec(inner_code), {'spotify': spotify}, locals)
                    except Exception as e:
                        click.echo(e, err=True)
                    else:
                        click.echo(locals['_retval'])

    except (EOFError, click.exceptions.Abort):
        pass

main()