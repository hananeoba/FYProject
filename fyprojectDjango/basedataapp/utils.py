
#import django

from basedataapp.models import Structure

#django.setup()

from django.db import connection

def get_parent_structures(structure_id):
    # Construct the SQL query to call the PostgreSQL function
    query = f"SELECT * FROM basedata_schema.get_parent_structures({structure_id});"
    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Fetch the results
        rows = cursor.fetchall()

        instances = []
    for row in rows:
        instance = Structure(
            id=row[0],
            code=row[1],
            label=row[2],
            created_at=row[3],
            updated_at=row[4],
            company_id=row[5],
            created_by_id=row[6],
            state_id=row[7],
            parent_structure_id=row[8],
            structure_type_id=row[9],
            updated_by_id=row[10],
            attached_parent_structure=row[11],
        )
        instances.append(instance)

    return instances


def get_children_structures(structure_id):
    # Construct the SQL query to call the PostgreSQL function
    query = f"SELECT * FROM basedata_schema.get_children_structures({structure_id});"
    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Fetch the results
        rows = cursor.fetchall()

        instances = []
    for row in rows:
        instance = Structure(
            id=row[0],
            code=row[1],
            label=row[2],
            created_at=row[3],
            updated_at=row[4],
            company_id=row[5],
            created_by_id=row[6],
            state_id=row[7],
            parent_structure_id=row[8],
            structure_type_id=row[9],
            updated_by_id=row[10],
            attached_parent_structure=row[11],
        )
        instances.append(instance)

    return instances


def generate_new_code(code):
    return str(code).zfill(6)  # 6 digits


def generate_Event_code(year,company , struc, count ):
    YEAR= str(year).upper()
    COMPANY= str(company).upper()
    STRUC= str(struc).upper()
    COUNT= str(count).zfill(6)
    code= "_".join([YEAR,COMPANY,STRUC,COUNT])
    return code
