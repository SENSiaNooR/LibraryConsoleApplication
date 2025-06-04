from dataclasses import asdict
from typing import Tuple, Any

def build_set_clause(model: Any, exclude: set = {"id"}) -> Tuple[str, list]:
    """
    Produces the SQL SET clause and values for an UPDATE query from a model.
    
    Args:
        model: The data model (usually a dataclass).
        exclude: Set of field names to exclude from the SET clause (e.g., 'id').

    Returns:
        Tuple[str, list]: SQL SET clause string, and list of values.
    """
    model_dict = asdict(model)
    pairs = []
    values = []

    for key, value in model_dict.items():
        if key in exclude or value is None:
            continue
        pairs.append(f"{key} = %s")
        values.append(value)

    set_clause = ", ".join(pairs)
    return set_clause, values

def build_where_clause(model: Any) -> tuple[str, list]:
    """
    Builds a SQL WHERE clause based on non-None fields of the given model.

    This function converts the model (e.g., a dataclass or similar object) into a dictionary
    and generates conditional expressions in the form of `field = %s` for each field
    that is not None. It then joins these conditions with `AND` and returns both the
    resulting WHERE clause and the corresponding list of values.

    Useful for dynamically generating SQL queries where only provided fields should be
    included in the WHERE clause.

    Parameters:
        model (Any): A data model object (e.g., a dataclass) to extract fields from.

    Returns:
        tuple[str, list]:
            - A SQL-safe string representing the WHERE clause 
              (e.g., `"id = %s AND name = %s"`).
            - A list of the corresponding non-None values in the same order as the conditions.
    """
    fields = asdict(model)
    conditions = []
    values = []

    for field, value in fields.items():
        if value is not None:
            conditions.append(f"{field} = %s")
            values.append(value)

    where_clause = " AND ".join(conditions)
    return where_clause, values
