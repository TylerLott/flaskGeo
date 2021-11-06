import sqlite3
from io import StringIO, BytesIO
import base64
from PIL import Image
from flask import Flask, send_file, render_template, request, make_response
from flask_cors import CORS, cross_origin
from markupsafe import escape
import gzip
import zlib
import json

# Sqlite setup
con = sqlite3.connect('tiledata.mbtiles')
cur = con.cursor()

# sqlite testing
cur.execute('SELECT name FROM sqlite_master WHERE type="table";')
print('Tables in mbtiles file')
print(cur.fetchall())

print()
cur.execute('SELECT tile_data FROM tiles WHERE zoom_level=6 AND tile_column=0 AND tile_row=0')
print(cur.fetchone())

print()
print('grids below here')

# cur.execute('SELECT * FROM grids')
# cur.execute('.tables')
# print(cur.fetchone())

# cur.execute('''select grid from grid_utfgrid
#                      where zoom_level = %s 
#                      and tile_column = %s 
#                      and tile_row = %s''' % (self.zoom,self.col,self.row))
# row = cur.fetchone()

# bt = bytes(row[0])
# j = zlib.decompress(bt)
# tgd = json.loads(j)
# print(tgd)


# Flask routing

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/<z>/<x>/<y>.png')
@cross_origin()
def default(z, x, y):
    con = sqlite3.connect('sat_low.mbtiles')
    cur = con.cursor()
    cur.execute(f'SELECT tile_data FROM tiles WHERE zoom_level={escape(z)} AND tile_column={escape(x)} AND tile_row={escape(y)}')
    # cur.execute(f'SELECT tile_data FROM tiles')
    data = cur.fetchone()[0]

    # print(data)

    # img = Image.open(io.BytesIO(data))
    # file_object = io.StringIO()
    # img.save(file_object, 'PNG')
    # file_object.seek(0)
    # print(file_object)
    # encoded_img_data = base64.b64encode(file_object.getvalue())
 
    res = make_response(send_file(BytesIO(data), mimetype='image/png'))

    
    return res
    return send_file(BytesIO(data), mimetype='image/png')

    # return send_file(file_object, mimetype='image/png')
    # return f'<img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8d29ybGQlMjBtYXB8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80" />'
    # return render_template('index.html', img_data=encoded_img_data.decode('utf-8'))






