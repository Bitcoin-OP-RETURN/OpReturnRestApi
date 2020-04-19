from binascii import hexlify
import config as cfg
from flask import Flask, request, jsonify, Response
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy, Pagination, abort
from sqlalchemy import and_, or_
import sqlalchemy
from flask_marshmallow import Marshmallow
import pyodbc


class TxOutput:
    def __init__(self, internal_id, txhash, blocktime, blockhash, outvalue, outtype, outasm, outhex, protocol, fileheader):
        self.internal_id = internal_id,
        self.txhash = txhash
        self.blocktime = blocktime
        self.blockhash = blockhash
        self.outvalue = outvalue
        self.outtype = outtype
        self.outasm = outasm
        self.outhex = outhex
        self.protocol = protocol
        self.fileheader = fileheader


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TxOutput):
            return {
                'id': obj.internal_id[0],
                'txhash': obj.txhash,
                'blocktime': obj.blocktime,
                'blockhash': obj.blockhash,
                'outvalue': obj.outvalue,
                'outtype': obj.outtype,
                'outasm': obj.outasm,
                'outhex': obj.outhex,
                'protocol': obj.protocol,
                'fileheader': obj.fileheader
            }


# Initialize app
app = Flask(__name__)
app.json_encoder = MyJSONEncoder

database = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + cfg.db['server'] + ';DATABASE=' +
                          cfg.db['database'] + ';UID=' + cfg.db['username'] + ';PWD=' + cfg.db['password'] +
                          ';Trusted_Connection=Yes', autocommit=True)
database.setencoding(encoding='utf-8')
cursor = database.cursor()


@app.route('/test', methods=['GET'])
def get_test():
    cursor.execute('SELECT TOP(10) * FROM transactionoutputs where outhex like \'%74657374%\' order by id desc')
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(TxOutput(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    return jsonify(data)


def encoded_to_hex(input_string):
    hex_string = hexlify(input_string.encode())
    return hex_string.decode()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
