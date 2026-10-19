"""Tokenize, parse and evaluate arithmetic expressions.

Grammar (lowest to highest precedence)::

    expression := term (("+" | "-") term)*
    term       := unary (("*" | "/") unary)*
    unary      := "-" unary | power
    power      := primary ("^" unary)?
    primary    := NUMBER | "(" expression ")"
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN = re.compile(r"\s*(?:(\d+\.\d*|\.\d+|\d+)|(.))")


class CalcError(ValueError):
    """An expression that cannot be evaluated."""


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    position: int


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    position = 0
    while position < len(source):
        match = _TOKEN.match(source, position)
        if match is None:
            break
        number, symbol = match.groups()
        if number is not None:
            tokens.append(Token("number", number, match.start(1)))
        elif symbol is not None:
            if symbol not in "+-*/^()":
                raise CalcError(f"unexpected character {symbol!r} at position {match.start(2)}")
            tokens.append(Token(symbol, symbol, match.start(2)))
        position = match.end()
    tokens.append(Token("end", "", len(source)))
    return tokens


class _Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._index = 0

    def _peek(self) -> Token:
        return self._tokens[self._index]

    def _take(self) -> Token:
        token = self._tokens[self._index]
        self._index += 1
        return token

    def parse(self) -> float:
        value = self._expression()
        token = self._peek()
        if token.kind != "end":
            raise CalcError(f"unexpected {token.text!r} at position {token.position}")
        return value

    def _expression(self) -> float:
        value = self._term()
        while self._peek().kind in ("+", "-"):
            operator = self._take().kind
            right = self._term()
            value = value + right if operator == "+" else value - right
        return value

    def _term(self) -> float:
        value = self._unary()
        while self._peek().kind in ("*", "/"):
            operator = self._take().kind
            right = self._unary()
            value = value * right if operator == "*" else value / right
        return value

    def _unary(self) -> float:
        if self._peek().kind == "-":
            self._take()
            return -self._unary()
        return self._power()

    def _power(self) -> float:
        base = self._primary()
        if self._peek().kind == "^":
            self._take()
            exponent = self._unary()
            try:
                result = base**exponent
            except (ZeroDivisionError, OverflowError) as error:
                raise CalcError(f"cannot compute power: {error}") from error
            if isinstance(result, complex):
                raise CalcError("power has no real result")
            return result
        return base

    def _primary(self) -> float:
        token = self._take()
        if token.kind == "number":
            return float(token.text)
        if token.kind == "(":
            value = self._expression()
            closing = self._take()
            if closing.kind != ")":
                raise CalcError(f"expected ')' at position {closing.position}")
            return value
        if token.kind == "end":
            raise CalcError("unexpected end of expression")
        raise CalcError(f"unexpected {token.text!r} at position {token.position}")


def evaluate(source: str) -> float:
    """Evaluate ``source`` and return its value."""
    return _Parser(tokenize(source)).parse()


def format_number(value: float) -> str:
    """Render integral values without a fractional part."""
    if value.is_integer():
        return str(int(value))
    return repr(value)
