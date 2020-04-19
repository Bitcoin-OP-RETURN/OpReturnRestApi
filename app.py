from binascii import hexlify
import config as cfg
from flask import Flask, request, jsonify, Response
from flask.json import JSONEncoder
import pyodbc


class FrequencyAnalysis:
    def __init__(self, internal_id, dataday, nulldata, p2pk, p2pkh, p2ms, p2sh, unknowntype):
        self.internal_id = internal_id
        self.dataday = dataday
        self.nulldata = nulldata
        self.p2pk = p2pk
        self.p2pkh = p2pkh
        self.p2ms = p2ms
        self.p2sh = p2sh
        self.unknowntype = unknowntype


class SizeAnalysis:
    def __init__(self, internal_id, dataday, avgsize, outputs):
        self.internal_id = internal_id
        self.dataday = dataday
        self.avgsize = avgsize
        self.outputs = outputs


class ProtocolAnalysis:
    def __init__(self, internal_id, dataday, ascribe, bitproof, blockaibindedpixsy, blocksign, blockstoreblockstack,
                 chainpoint,
                 coinspark, colu, counterparty, counterpartytest, cryptocopyright, diploma, emptytx, eternitywall,
                 factom, lapreuve, monegraph, omni, openassets, openchain, originalmy, proofofexistence, provebit,
                 remembr, smartbit, stampd, stampery, universityofnicosia, unknownprotocol, veriblock):
        self.internal_id = internal_id
        self.dataday = dataday
        self.ascribe = ascribe
        self.bitproof = bitproof
        self.blockaibindedpixsy = blockaibindedpixsy
        self.blocksign = blocksign
        self.blockstoreblockstack = blockstoreblockstack
        self.chainpoint = chainpoint
        self.coinspark = coinspark
        self.colu = colu
        self.counterparty = counterparty
        self.counterpartytest = counterpartytest
        self.cryptocopyright = cryptocopyright
        self.diploma = diploma
        self.emptytx = emptytx
        self.eternitywall = eternitywall
        self.factom = factom
        self.lapreuve = lapreuve
        self.monegraph = monegraph
        self.omni = omni
        self.openassets = openassets
        self.openchain = openchain
        self.originalmy = originalmy
        self.proofofexistence = proofofexistence
        self.provebit = provebit
        self.remembr = remembr
        self.smartbit = smartbit
        self.stampd = stampd
        self.stampery = stampery
        self.universityofnicosia = universityofnicosia
        self.unknownprotocol = unknownprotocol
        self.veriblock = veriblock


class TxOutput:
    def __init__(self, internal_id, txhash, blocktime, blockhash, outvalue, outtype, outasm, outhex, protocol,
                 fileheader):
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
        elif isinstance(obj, FrequencyAnalysis):
            return {
                'id': obj.internal_id,
                'dataday': str(obj.dataday),
                'nulldata': obj.nulldata,
                'p2pk': obj.p2pk,
                'p2pkh': obj.p2pkh,
                'p2ms': obj.p2ms,
                'p2sh': obj.p2sh,
                'unknowntype': obj.unknowntype
            }
        elif isinstance(obj, SizeAnalysis):
            return {
                'id': obj.internal_id,
                'dataday': str(obj.dataday),
                'avgsize': obj.avgsize,
                'outputs': obj.outputs
            }
        elif isinstance(obj, ProtocolAnalysis):
            return {
                'id': obj.internal_id,
                'dataday': str(obj.dataday),
                'ascribe': obj.ascribe,
                'bitproof': obj.bitproof,
                'blockaibindedpixsy': obj.blockaibindedpixsy,
                'blocksign': obj.blocksign,
                'blockstoreblockstack': obj.blockstoreblockstack,
                'chainpoint': obj.chainpoint,
                'coinspark': obj.coinspark,
                'colu': obj.colu,
                'counterparty': obj.counterparty,
                'counterpartytest': obj.counterpartytest,
                'cryptocopyright': obj.cryptocopyright,
                'diploma': obj.diploma,
                'emptytx': obj.emptytx,
                'eternitywall': obj.eternitywall,
                'factom': obj.factom,
                'lapreuve': obj.lapreuve,
                'monegraph': obj.monegraph,
                'omni': obj.omni,
                'openassets': obj.openassets,
                'openchain': obj.openchain,
                'originalmy': obj.originalmy,
                'proofofexistence': obj.proofofexistence,
                'provebit': obj.provebit,
                'remembr': obj.remembr,
                'smartbit': obj.smartbit,
                'stampd': obj.stampd,
                'stampery': obj.stampery,
                'universityofnicosia': obj.universityofnicosia,
                'unknownprotocol': obj.unknownprotocol,
                'veriblock': obj.veriblock,
            }


# Initialize app
app = Flask(__name__)
app.json_encoder = MyJSONEncoder

database = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + cfg.db['server'] + ';DATABASE=' +
                          cfg.db['database'] + ';UID=' + cfg.db['username'] + ';PWD=' + cfg.db['password'] +
                          ';Trusted_Connection=Yes', autocommit=True)
database.setencoding(encoding='utf-8')
cursor = database.cursor()


@app.route('/frequency-analysis', methods=['GET'])
def get_frequency_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    query = "SELECT * FROM frequencyanalysis"
    if min_date is None and max_date is None:
        query += ";"
    elif min_date is None:
        query += " WHERE dataday <= '{0}';".format(max_date)
    elif max_date is None:
        query += " WHERE dataday >= '{0}';".format(min_date)
    else:
        query += " WHERE dataday >= '{0}' AND dataday <= '{1}';".format(min_date, max_date)

    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(FrequencyAnalysis(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    return jsonify(data)


@app.route('/size-analysis', methods=['GET'])
def get_size_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    query = "SELECT * FROM sizeanalysis"
    if min_date is None and max_date is None:
        query += ";"
    elif min_date is None:
        query += " WHERE dataday <= '{0}';".format(max_date)
    elif max_date is None:
        query += " WHERE dataday >= '{0}';".format(min_date)
    else:
        query += " WHERE dataday >= '{0}' AND dataday <= '{1}';".format(min_date, max_date)

    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(SizeAnalysis(row[0], row[1], row[2], row[3]))
    return jsonify(data)


@app.route('/protocol-analysis', methods=['GET'])
def get_protocol_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    query = "SELECT * FROM protocolanalysis"
    if min_date is None and max_date is None:
        query += ";"
    elif min_date is None:
        query += " WHERE dataday <= '{0}';".format(max_date)
    elif max_date is None:
        query += " WHERE dataday >= '{0}';".format(min_date)
    else:
        query += " WHERE dataday >= '{0}' AND dataday <= '{1}';".format(min_date, max_date)

    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(ProtocolAnalysis(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31]))
    return jsonify(data)


@app.route('/tx-outputs', methods=['GET'])
def get_tx_outputs():
    page = request.args.get('page')
    query = "SELECT * FROM transactionoutputs ORDER BY id DESC OFFSET {0} ROWS FETCH NEXT 10 ROWS ONLY;".format(int(page) * 10 if page is not None else 0)
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(TxOutput(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    return jsonify(data)


@app.route('/tx-outputs/search', methods=['GET'])
def get_tx_outputs_search():
    search_term = request.args.get('search')
    search_format = request.args.get('format')
    min_time = request.args.get('min_time')
    max_time = request.args.get('max_time')
    protocol = request.args.get('protocol')
    fileheader = request.args.get('fileheader')
    sort = request.args.get('sort')
    page = request.args.get('page')

    protocols = [x.strip() for x in protocol.split(',')] if protocol is not None else None
    fileheaders = [x.strip() for x in fileheader.split(',')] if fileheader is not None else None

    query = "SELECT * FROM transactionoutputs"
    if search_term is not None or min_time is not None or max_time is not None or protocol is not None or fileheader is not None:
        query += " WHERE"
        added_at_least_one = False
        if min_time is not None and int(min_time) >= 1230768000:
            if added_at_least_one:
                query += " AND"
            else:
                added_at_least_one = True
            query += " blocktime >= {0}".format(min_time)

        if max_time is not None:
            if added_at_least_one:
                query += " AND"
            else:
                added_at_least_one = True
            query += " blocktime <= {0}".format(max_time)

        if protocol is not None:
            if added_at_least_one:
                query += " AND"
            else:
                added_at_least_one = True
            query += " ("
            for i, prot in enumerate(protocols):
                if i > 0:
                    query += " or "
                query += "protocol = '{0}'".format(prot)
            query += ")"

        if fileheader is not None:
            if added_at_least_one:
                query += " AND"
            else:
                added_at_least_one = True
            query += " ("
            for i, fh in enumerate(fileheaders):
                if i > 0:
                    query += " or "
                query += "fileheader = '{0}'".format(fh)
            query += ")"

    query += " ORDER BY id {0}".format(sort if sort is not None else "ASC")
    query += " OFFSET " + str((int(page) - 1) * 10 if page is not None else 0) + " ROWS FETCH NEXT 10 ROWS ONLY;"

    cursor.execute(query)
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
