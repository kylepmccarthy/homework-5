
import json
import logging

from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import geopandas as gpd
from shapely import wkt

# load credentials from a file
with open("C:/Users/Kyle McCarthy/Documents/MUSA509/final/credentials.json", "r") as f_in:
    pg_creds = json.load(f_in)

# mapbox
with open("C:/Users/Kyle McCarthy/Documents/MUSA509/final/mapbox_token.json", "r") as mb_token:
    MAPBOX_TOKEN = json.load(mb_token)["token"]

app = Flask(__name__, template_folder="templates")

# load credentials from JSON file
HOST = pg_creds["HOST"]
USERNAME = pg_creds["USERNAME"]
PASSWORD = pg_creds["PASSWORD"]
DATABASE = pg_creds["DATABASE"]
PORT = pg_creds["PORT"]


def get_sql_engine():
    return create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")



def get_neighborhood_names():
    """Gets all neighborhoods for Philadelphia"""
    engine = get_sql_engine()
    query = text(
        """
        SELECT DISTINCT community_area as neighborhood
        FROM facilityconditionindexsd
        ORDER BY 1 ASC
    """
    )
    resp = engine.execute(query).fetchall()
    # get a list of names
    names = [row["neighborhood"] for row in resp]
    return names


# index page
@app.route("/")
def index():
    """Index page"""
    names = get_neighborhood_names()
    return render_template("input.html", nnames=names)


def get_bounds(geodataframe):
    """returns list of sw, ne bounding box pairs"""
    bounds = geodataframe.geom.total_bounds
    bounds = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]
    return bounds


def get_num_buildings(nname):
    """Get number of buildings in a neighborhood"""
    engine = get_sql_engine()
    building_stats = text(
        """
        SELECT
          COUNT(building_name) as num_buildings, community_area
        FROM facilityconditionindexsd as f
        WHERE f.community_area = :nname
        GROUP BY 2 
    """
    )
    resp = engine.execute(building_stats, nname=nname).fetchone()
    return resp["num_buildings"]


def get_neighborhood_buildings(nname):
    """Get all buildings for a neighborhood"""
    engine = get_sql_engine()
    vacant_buildings = text(
        """
        SELECT
            geom, location_description, total_req, desc_full
        FROM facilityconditionindexsd as f
        WHERE f.community_area = :nname
    """
    )
    buildings = gpd.read_postgis(vacant_buildings, con=engine, params={"nname": nname})
    return buildings


@app.route("/vacantviewer", methods=["GET"])
def vacant_viewer():
    """Test for form"""
    name = request.args["neighborhood"]
    buildings = get_neighborhood_buildings(name)
    bounds = get_bounds(buildings)

    # generate interactive map
    map_html = render_template(
        "geojson_map.html",
        geojson_str=buildings.to_json(),
        bounds=bounds,
        center_lng=(bounds[0][0] + bounds[1][0]) / 2,
        center_lat=(bounds[0][1] + bounds[1][1]) / 2,
        mapbox_token=MAPBOX_TOKEN,
    )
    return render_template(
        "vacant.html",
        num_buildings=get_num_buildings(name),
        nname=name,
        map_html=map_html,
        buildings=buildings[["location_description", "total_req", "desc_full"]].values,
    )


# 404 page example
@app.errorhandler(404)
def page_not_found(err):
    """404 page"""
    return f"404 ({err})"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)
