from macros_sdk import *


def analyze(tree: Module) -> None:
    """Add your AST analysis code here."""

    for node in walk(tree):
        match node:
            case NamedExpr():
                add_issue("PM-W001", "Never use assignment expressions", node=node)

            case Compare(
                left=Constant(),
                op=Is(),
                comparators=[Constant()],
            ):
                add_issue(
                    "PM-W002",
                    "Don't compare literals with `is`, use `==`",
                    node=node,
                )

            case For(body=body, orelse=else_block) if len(else_block) != 0:
                if not any(
                    isinstance(child, Break)
                    for subnode in body
                    for child in walk(subnode)
                ):
                    add_issue(
                        "PM-W003",
                        "For statement has else block, but no `break` statement inside",
                        node=node,
                    )

            # Let's say you want to disallow all metaclass inheritance in your codebase
            case ClassDef(keywords=keywords):
                if any(kwarg.arg == "metaclass" for kwarg in keywords):
                    add_issue(
                        "PM-W004",
                        "Using metaclasses not allowed",
                        node=node,
                    )
