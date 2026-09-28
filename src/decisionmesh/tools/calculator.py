import ast
import operator
from typing import ClassVar


class Calculator:
    """Safely evaluate basic arithmetic expressions."""
    
    _OPERATORS: ClassVar = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def calculate(self, expression: str) -> float:
        """Evaluate a supported arithmetic expression."""
        if not expression.strip():
            raise ValueError("Expression cannot be empty.")
        
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("Invalid arithmetic expression.") from exc
        
        return float(self._evaluate(tree.body))
    
    def _evaluate(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPERATORS:
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Cannot divide by zero.")
            
            return self._OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPERATORS:
            operand = self._evaluate(node.operand)
            return self._OPERATORS[type(node.op)](operand)
        
        raise ValueError("Unsupported expression.")