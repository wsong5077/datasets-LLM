# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from db import connect_to_postgresql, disconnect_from_postgresql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

app = Flask(__name__)

@app.route('/')
def index():
    try:
        connection, cursor = connect_to_postgresql()
        # cursor.execute("select table_name, column_name, data_type from information_schema.columns where table_name = 'paintings';")
        # cursor.execute("drop table if exists paintings;")
        # cursor.execute("""
        #                create table paintings (
        #                     id varchar(64) primary key,
        #                     title varchar(255),
        #                     url varchar(255),
        #                     artistUrl varchar(255),
        #                     artistName varchar(255),
        #                     artistId varchar(64),
        #                     completitionYear int,
        #                     dictionaries varchar[],
        #                     location varchar(255),
        #                     period jsonb,
        #                     serie jsonb,
        #                     genres varchar[],
        #                     styles varchar[],
        #                     media varchar[],
        #                     sizeX float,
        #                     sizeY float,
        #                     diameter float,
        #                     galleries varchar[],
        #                     tags varchar[],
        #                     description text,
        #                     width int,
        #                     image varchar(255),
        #                     height int
        #                   );
        #                """)
        # cursor.execute("select table_name, column_name, data_type from information_schema.columns where table_name = 'paintings';")
        cursor.execute("select count(1) from paintings;")
        res = cursor.fetchone()
        res = 'paintings cnt: ' + str(res[0])
        connection.commit()
        # res = 'Connected to the PostgreSQL database.'
        # Perform database operations using the cursor, e.g., execute queries

        return jsonify(res), 200

    finally:
        disconnect_from_postgresql(connection, cursor)

@app.route("/paintings/<string:id>", methods=['POST'])
def add_painting(id):
    # if get_painting(id)[1] == 200:
    #     return jsonify({"message": "Painting already exists"}), 200
    data = request.get_json()
    required_fields = [
        'id',
        'title',
        'url',
        'artistUrl',
        'artistName',
        'artistId',
        'completitionYear',
        'dictionaries',
        'location',
        'period',
        'serie',
        'genres',
        'styles',
        'media',
        'sizeX',
        'sizeY',
        'diameter',
        'galleries',
        'tags',
        'description',
        'width',
        'image',
        'height'
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        connection, cursor = connect_to_postgresql()
        # print(
        #     """
        #     INSERT INTO paintings (
        #         id,
        #         title,
        #         url,
        #         artistUrl,
        #         artistName,
        #         artistId,
        #         completitionYear,
        #         dictionaries,
        #         location,
        #         period,
        #         serie,
        #         genres,
        #         styles,
        #         media,
        #         sizeX,
        #         sizeY,
        #         diameter,
        #         galleries,
        #         tags,
        #         description,
        #         width,
        #         image,
        #         height
        #     ) VALUES (
        #         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        #     );
        #     """, (
        #         data.get("id"),
        #         data.get("title"),
        #         data.get("url"),
        #         data.get("artistUrl"),
        #         data.get("artistName"),
        #         data.get("artistId"),
        #         data.get("completitionYear"),
        #         data.get("dictionaries"),
        #         data.get("location"),
        #         data.get("period"),
        #         data.get("serie"),
        #         data.get("genres"),
        #         data.get("styles"),
        #         data.get("media"),
        #         data.get("sizeX"),
        #         data.get("sizeY"),
        #         data.get("diameter"),
        #         data.get("galleries"),
        #         data.get("tags"),
        #         data.get("description"),
        #         data.get("width"),
        #         data.get("image"),
        #         data.get("height")
        #     ))
        cursor.execute(
            """
            INSERT INTO paintings (
                id,
                title,
                url,
                artistUrl,
                artistName,
                artistId,
                completitionYear,
                dictionaries,
                location,
                period,
                serie,
                genres,
                styles,
                media,
                sizeX,
                sizeY,
                diameter,
                galleries,
                tags,
                description,
                width,
                image,
                height
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
            """, (
                data.get("id"),
                data.get("title"),
                data.get("url"),
                data.get("artistUrl"),
                data.get("artistName"),
                data.get("artistId"),
                data.get("completitionYear"),
                data.get("dictionaries"),
                data.get("location"),
                json.dumps(data.get("period")) if data.get("period") else None,
                json.dumps(data.get("serie")) if data.get("serie") else None,
                data.get("genres"),
                data.get("styles"),
                data.get("media"),
                data.get("sizeX"),
                data.get("sizeY"),
                data.get("diameter"),
                data.get("galleries"),
                data.get("tags"),
                data.get("description"),
                data.get("width"),
                data.get("image"),
                data.get("height")
            ))
        
        connection.commit()
        return jsonify({"message": "Painting created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        disconnect_from_postgresql(connection, cursor)
    
@app.route("/paintings", methods=['GET'])
def get_paintings():
    connection, cursor = connect_to_postgresql()
    cursor.execute("select * from paintings;")
    result = cursor.fetchall()
    cursor.close()
    print(result)
    disconnect_from_postgresql(connection, cursor)
    return jsonify(result)

@app.route("/paintings/<string:id>", methods=['GET'])
def get_painting(id):
    connection, cursor = connect_to_postgresql()
    cursor.execute("select * from paintings where id = %s;", (id,))
    result = cursor.fetchall()
    cursor.close()
    disconnect_from_postgresql(connection, cursor)
    if len(result) == 0:
        return jsonify({"message": "Painting not found"}), 404
    return jsonify(result), 200

@app.route("/paintings/<string:id>", methods=['PUT'])
def update_painting(id):
    data = request.get_json()
    required_fields = [
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        connection, cursor = connect_to_postgresql()

        cursor.execute(f"""
            UPDATE paintings SET ( 
                title = {data.get("title")},
                url = {data.get("url")},
                artistUrl = {data.get("artistUrl")},
                artistName = {data.get("artistName")},
                artistId = {data.get("artistId")},
                completitionYear = {data.get("completitionYear")},
                dictionaries = {data.get("dictionaries")},
                location = {data.get("location")},
                period = {data.get("period")},
                serie = {data.get("serie")},
                genres = {data.get("genres")},
                styles = {data.get("styles")},
                media = {data.get("media")},
                sizeX = {data.get("sizeX")},
                sizeY = {data.get("sizeY")},
                diameter = {data.get("diameter")},
                galleries = {data.get("galleries")},
                tags = {data.get("tags")},
                description = {data.get("description")},
                width = {data.get("width")},
                image = {data.get("image")},
                height = {data.get("height")}
            ) WHERE id = {id};
            """)

        connection.commit()
        return jsonify({"message": "Painting updated successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        disconnect_from_postgresql(connection, cursor)
        
@app.route("/paintings/<string:id>", methods=['DELETE'])
def delete_painting(id):
    try:
        connection, cursor = connect_to_postgresql()
        cursor.execute("DELETE FROM paintings WHERE id = %s;", (id,))
        connection.commit()
        return jsonify({"message": "Painting deleted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        disconnect_from_postgresql(connection, cursor)

if __name__ == '__main__':
    app.run(debug=True)
