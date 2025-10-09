from typing import Optional
from DataAccess.BaseRepository import BaseRepository
from Exceptions.Exceptions import MultipleRowsReturnedError
from psycopg2.extensions import cursor as PgCursor
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause
from Models.Models import BaseTableModel, BaseViewModel


class CommonQueriesRepository(BaseRepository):
    """Repository base class implementing common SQL operations shared by all table repositories.

    This class provides generic CRUD and filtering operations that can be reused across
    different database repositories. All subclasses of `BaseRepository` may inherit and
    extend these methods or override them for table-specific logic.

    It uses the model classes (`BaseTableModel` and `BaseViewModel`) to translate PostgreSQL
    records into structured Python objects.

    Typical usage:
        class UserRepository(CommonQueriesRepository):
            table_name = "users"
            model_class = UserModel
            view_model_class = UserViewModel

    Methods are implemented as class methods to allow easy use without instantiation.
    """
    
    # ─────────────────────────────── Basic Table Operations ───────────────────────────────
    @classmethod
    def get_one(cls, model : BaseTableModel, cursor : Optional[PgCursor] = None) -> Optional[BaseTableModel]:
        """Retrieve a single record matching the provided model’s non-null fields.

        Args:
            model (BaseTableModel): Model instance whose populated attributes are used to build the WHERE clause.
            cursor (Optional[PgCursor]): Optional cursor to reuse an existing transaction.

        Returns:
            Optional[BaseTableModel]: The matching record as a model instance, or None if not found.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        where_clause, values = build_where_clause(model, exclude=cls.where_clause_exclude)

        query = (
            f"""
            SELECT * FROM {cls.table_name} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        if result is None:
            return None
            
        return cls.model_class(*result)
       
    @classmethod
    def get_many(cls, model : BaseTableModel, cursor : Optional[PgCursor] = None) -> list[BaseTableModel]:
        """Retrieve multiple records matching the provided model’s filtering fields.

        Args:
            model (BaseTableModel): Model instance used as a filter (non-null attributes form WHERE conditions).
            cursor (Optional[PgCursor]): Optional cursor to reuse an existing transaction.

        Returns:
            list[BaseTableModel]: A list of model instances matching the filter.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True, exclude=cls.where_clause_exclude)
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {cls.table_name} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {cls.table_name}
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)
            
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return [cls.model_class(*row) for row in result]
    
    @classmethod
    def view_one(cls, model : BaseViewModel, cursor : Optional[PgCursor] = None) -> Optional[BaseViewModel]:
        """Retrieve a single record from the view corresponding to the provided model’s filters.

        Args:
            model (BaseViewModel): View model with fields to filter results.
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            Optional[BaseViewModel]: The matching record as a view model instance, or None if not found.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        where_clause, values = build_where_clause(model, exclude=cls.where_clause_exclude)

        query = (
            f"""
            SELECT * FROM {cls.view_name} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
                        
        if result is None:
            return None

        return cls.view_model_class(*result)

    @classmethod
    def view_many(cls, model : BaseViewModel, cursor : Optional[PgCursor] = None) -> list[BaseViewModel]:
        """Retrieve multiple records from the associated view.

        Args:
            model (BaseViewModel): View model instance containing filter fields.
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            list[BaseViewModel]: List of matching view model instances.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True, exclude=cls.where_clause_exclude)
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {cls.view_name} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {cls.view_name}
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)
            
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return [cls.view_model_class(*row) for row in result]
    
    @classmethod
    def add(cls, model : BaseTableModel, cursor : Optional[PgCursor] = None) -> BaseTableModel:
        """Insert a new record into the table.

        Args:
            model (BaseTableModel): Model instance containing data to insert.
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            BaseTableModel: Model instance representing the inserted record (possibly with generated fields like ID).
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        columns_clause, placeholders_clause, values = build_insert_clause(model, exclude=cls.insert_clause_exclude)

        query = (
            f"""
            INSERT INTO {cls.table_name} (
                {columns_clause}
            )
            VALUES ({placeholders_clause})
            RETURNING *
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return cls.model_class(*result)
    
    @classmethod
    def update(cls, model : BaseTableModel, cursor: Optional[PgCursor] = None) -> None:
        """Update an existing record in the table based on its primary key.

        Args:
            model (BaseTableModel): Model instance containing updated data.
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        if model.id is None:
            raise ValueError("Model must have an 'id' to perform update.")
    
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        set_clause, values = build_set_clause(model, exclude=cls.set_clause_exclude)

        if not set_clause:
            return  # Nothing to update

        query = f"""
            UPDATE {cls.table_name}
            SET {set_clause}
            WHERE id = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete(cls, id : int, cursor: Optional[PgCursor] = None) -> None:
        """Delete a record by its primary key ID.

        Args:
            id (int): The ID of the record to delete.
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {cls.table_name}
            WHERE id = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def remove(cls, model : BaseTableModel, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None) -> None:
        """Delete records matching non-null attributes of the model (filter-based deletion).

        Args:
            model (BaseTableModel): Model instance containing filter fields.
            use_like_for_strings (bool): Whether to use SQL LIKE for string comparisons (default True).
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings, cls.where_clause_exclude)

        query = f"""
            DELETE FROM {cls.table_name}
            WHERE {where_clause}
        """
    
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def clear(cls, cursor: Optional[PgCursor] = None) -> None:
        """Delete all records from the associated table.

        Args:
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        query = f"""
            DELETE FROM {cls.table_name}
        """
        cursor.execute(query)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()


    # ─────────────────────────────── Generic Table Operations ───────────────────────────────   
    @classmethod
    def get_one_from(cls, model, table : str, exclude : set = set(), cursor : Optional[PgCursor] = None) -> tuple:
        """Retrieve a single record from a specified table based on the model’s fields.

        Args:
            model: Model instance or dictionary containing filtering data.
            table (str): Name of the table to query.
            exclude (set): Fields to exclude from filtering.
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            tuple: Tuple representing the retrieved row, or None if not found.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        where_clause, values = build_where_clause(model, exclude=exclude)

        query = (
            f"""
            SELECT * FROM {table} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
       
    @classmethod
    def get_many_from(cls, model, table : str, exclude : set = set(),cursor : Optional[PgCursor] = None) -> list[tuple]:
        """Retrieve multiple records from a specified table.

        Args:
            model: Model instance or dict used for filtering.
            table (str): Name of the table to query.
            exclude (set): Fields to exclude from the WHERE clause.
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            list[tuple]: List of retrieved rows.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True, exclude=exclude)
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {table} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {table}
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)
            
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def add_to(cls, model, table : str, exclude : set = {'id'}, cursor : Optional[PgCursor] = None) -> tuple:
        """Insert a new record into a specified table.

        Args:
            model: Model instance or dict containing insert data.
            table (str): Table name to insert into.
            exclude (set): Fields excluded from insertion (default {'id'}).
            cursor (Optional[PgCursor]): Optional database cursor.

        Returns:
            tuple: The inserted row (or tuple representing generated fields).
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        columns_clause, placeholders_clause, values = build_insert_clause(model, exclude)

        query = (
            f"""
            INSERT INTO {table} (
                {columns_clause}
            )
            VALUES ({placeholders_clause})
            RETURNING *
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def update_from(cls, model, table : str, exclude : set = {'id'}, cursor: Optional[PgCursor] = None) -> None:
        """Update records in a specified table using the model’s fields.

        Args:
            model: Model instance containing updated values.
            table (str): Table name to update.
            exclude (set): Fields to exclude from the SET clause (default {'id'}).
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        if model.id is None:
            raise ValueError("Model must have an 'id' to perform update.")
    
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        set_clause, values = build_set_clause(model, exclude)

        if not set_clause:
            return  # Nothing to update

        query = f"""
            UPDATE {table}
            SET {set_clause}
            WHERE id = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete_from(cls, id : int, table : str, cursor: Optional[PgCursor] = None) -> None:
        """Delete a record from a specified table by its ID.

        Args:
            id (int): Record ID to delete.
            table (str): Table name.
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {table}
            WHERE id = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def remove_from(cls, model, table : str, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None) -> None:
        """Remove records from a specified table based on model filters.

        Args:
            model: Model instance or dict containing filter data.
            table (str): Table name.
            use_like_for_strings (bool): Whether to use SQL LIKE for string comparisons.
            cursor (Optional[PgCursor]): Optional database cursor.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings)

        query = f"""
            DELETE FROM {table}
            WHERE {where_clause}
        """
    
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            