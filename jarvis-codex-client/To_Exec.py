from __future__ import annotations
from typing import Any

import ast

class ToExec(ast.NodeTransformer):
    def __init__(self, return_name):
        self.context = {'outer': True}
        self.return_name = return_name


    ### Visitors
    def generic_visit(self, node: ast.AST, **kwargs) -> ast.AST:
        old_context = dict(self.context)
        self.context |= kwargs

        result =  super().generic_visit(node)

        self.context = old_context
        return result

        ## Transforms "return something" into "_retval = something"
    def visit_Return(self, node: ast.Return) -> Any:
        if not self.context['outer']:
            return self.generic_visit(node)

        return ast.Assign(targets=[ast.Name(id=self.return_name, ctx=ast.Store())], value=self.generic_visit(node.value))

        ## Skip returns in function definition
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        return self.generic_visit(node, outer=False)
    

def to_exec(code, return_name="_retval"):
    code = ast.parse(code)
    return ast.unparse(ast.fix_missing_locations(ToExec(return_name=return_name).visit(code)))

if __name__ == "__main__":
    import sys
    print("Enter code to be executed")
    code = sys.stdin.read()
    print(to_exec(code))