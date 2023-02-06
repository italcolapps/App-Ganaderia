import pymysql
import pymysql.cursors

def add_row_db(tabla, data):
    ## Datos de acceso
    DB_instance_identifier = 'DB-APP'
    username = 'nutricion'
    password = 'Nutr1c10n$'
    host = 'db-app.cyvxpxlgwwja.us-east-2.rds.amazonaws.com'
    Database_port = 3306

    # Connect to the database
    connection = pymysql.connect(host = host,
                                user = username,
                                password = password,
                                database='AppGanaderia',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            #sql = 'SELECT * FROM comparacion_economico_nutricional'
            #sql = 'DELETE FROM comparacion_economico_nutricional'
            sql = f'''
                INSERT INTO `{tabla}` (fecha, nombre, contacto, pais, departamento, municipio, alimento_1, precio_kg_1, materia_seca_porc_1, proteina_porc_1, valor_kg_materia_seca_1, valor_kg_proteina_1, alimento_2, precio_kg_2, materia_seca_porc_2, proteina_porc_2, valor_kg_materia_seca_2, valor_kg_proteina_2, diferencia_costo_materia_seca, diferencia_costo_proteina)
                VALUES ('{data["Fecha"]}', '{data["Nombre"]}', '{data["Contacto"]}', '{data["Pais"]}', '{data["Departamento"]}',	'{data["Municipio"]}', '{data["Alimento 1"]}', '{data["Precio (kg) 1"]}', '{data["Materia seca % 1"]}', '{data["Proteina % 1"]}', '{data["Valor kg materia seca 1"]}', '{data["Valor kg proteina 1"]}', '{data["Alimento 2"]}', '{data["Precio (kg) 2"]}', '{data["Materia seca % 2"]}', '{data["Proteina seca % 2"]}', '{data["Valor kg materia seca 2"]}', '{data["Valor kg proteina 2"]}', '{data["Diferencia costo materia seca %"]}', '{data["Diferencia costo proteina %"]}');
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                print(i)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
