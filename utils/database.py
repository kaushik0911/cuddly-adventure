import psycopg2


class DatabaseUtil:
    def __init__(self, db_config) -> None:
        self.db_config = db_config

        try:
            self.connection = psycopg2.connect(**db_config)
        except Exception as ex:
            print(f"Error connecting to the database: {ex}")

    def schema_details(self, schema_name: str) -> str:
        schema_info_context: str = ""

        connection = self.connection
        cursor = connection.cursor()

        schema_info_context = f"Database Schema: {schema_name} \n"

        try:
            cursor.execute("select table_name from information_schema.tables where table_schema = %s;", (schema_name, ))
            table_list: list[str] = cursor.fetchall()

            for table in table_list:
                table_name = table[0]

                schema_info_context = f"{schema_info_context}\nTable: {table_name}\n"

                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", (table_name,))
                columns_list = cursor.fetchall()

                for column in columns_list:
                    column_name = column[0]
                    data_type = column[1]

                    schema_info_context = f"{schema_info_context}  Column: {column_name}, Data Type: {data_type}\n"

                # Adding Sample Data
                cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT 5;")
                sample_data = cursor.fetchall()
                schema_info_context = f"{schema_info_context}  Sample Data:\n"
                for row in sample_data:
                    schema_info_context = f"{schema_info_context}    {row}\n"

        except Exception as ex:
            print(f"Error fetching the schema: {ex}")
            schema_info_context = f"Error fetching the schema: {ex}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return schema_info_context


    def execute_sql(self, query: str):
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.commit()
            return str(results)
        except Exception as ex:
            print(f"Error executing the query: {ex}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
