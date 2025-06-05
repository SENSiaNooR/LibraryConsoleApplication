from dataclasses import asdict
from typing import Tuple, Any
from DataAccess.Models import UnsetType

def build_set_clause(model: Any, exclude: set = {"id"}) -> Tuple[str, list]:
    """
    Builds the SQL SET clause and corresponding values for an UPDATE query
    based on the fields of a model object.

    Fields that are instances of `UnsetType` or listed in the `exclude` set 
    will be ignored in the SET clause.

    Args:
        model (Any): A dataclass-like object containing field data.
        exclude (set, optional): A set of field names to exclude from the SET clause 
                                 (commonly 'id'). Defaults to {"id"}.

    Returns:
        Tuple[str, list]:
            - A string for the SQL SET clause (e.g., `"name = %s, age = %s"`).
            - A list of values matching the placeholders in the SET clause.
    """
    model_dict = asdict(model)
    pairs = []
    values = []

    for key, value in model_dict.items():
        if key in exclude or isinstance(value, UnsetType):
            continue
        pairs.append(f"{key} = %s")
        values.append(value)

    set_clause = ", ".join(pairs)
    return set_clause, values


def build_where_clause(model: Any) -> Tuple[str, list]:
    """
    Builds a SQL WHERE clause and corresponding values based on the 
    fields of a model object that are not instances of `UnsetType`.

    Useful for dynamically generating filters from partially filled models.

    Args:
        model (Any): A dataclass-like object containing field data.

    Returns:
        Tuple[str, list]:
            - A SQL-safe WHERE clause string (e.g., `"id = %s AND name = %s"`).
            - A list of values matching the placeholders in the WHERE clause.
    """
    fields = asdict(model)
    conditions = []
    values = []

    for field, value in fields.items():
        if not isinstance(value, UnsetType):
            conditions.append(f"{field} = %s")
            values.append(value)

    where_clause = " AND ".join(conditions)
    return where_clause, values

def build_insert_clause(model: Any, exclude: set = {"id"}) -> Tuple[str, str, list]:
    """
    Builds SQL column list, placeholder list, and values for an INSERT statement.

    Args:
        model: The dataclass instance to insert.
        exclude: Set of field names to exclude from the insert (e.g., 'id').

    Returns:
        Tuple[str, str, list]:
            - Column names (e.g., "name, address")
            - Placeholders (e.g., "%s, %s")
            - List of values in order
    """
    model_dict = asdict(model)
    columns = []
    placeholders = []
    values = []

    for key, value in model_dict.items():
        if key in exclude or isinstance(value, UnsetType):
            continue
        columns.append(key)
        placeholders.append("%s")
        values.append(value)
        
    columns_clause = ", ".join(columns)
    placeholders_clause = ", ".join(placeholders)
    
    return columns_clause, placeholders_clause, values