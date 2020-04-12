from binascii import hexlify
import config as cfg
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy, Pagination, abort
from sqlalchemy import and_, or_
import sqlalchemy
from flask_marshmallow import Marshmallow
import pyodbc

# Initialize app
app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://' + cfg.db['username'] + ':' + cfg.db['password'] + '@' + cfg.db['server'] + ':' + cfg.db['port'] + '/' + cfg.db['database'] + '?driver=ODBC+DRIVER+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
db = SQLAlchemy(app)
# Initialize marshmallow
ma = Marshmallow(app)

PAGE_SIZE = 10
TOTAL_IN = 100_000_000_000


class FrequencyAnalysis(db.Model):
    __tablename__ = 'frequencyanalysis'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    dataday = db.Column(db.Date, nullable=False)
    nulldata = db.Column(db.Integer, nullable=False)
    p2pk = db.Column(db.Integer, nullable=False)
    p2pkh = db.Column(db.Integer, nullable=False)
    p2ms = db.Column(db.Integer, nullable=False)
    p2sh = db.Column(db.Integer, nullable=False)
    unknowntype = db.Column(db.Integer, nullable=False)

    def __init__(self, dataday, nulldata, p2pk, p2pkh, p2ms, p2sh, unknowntype):
        self.dataday = dataday
        self.nulldata = nulldata
        self.p2pk = p2pk
        self.p2pkh = p2pkh
        self.p2ms = p2ms
        self.p2sh = p2sh
        self.unknowntype = unknowntype


class FrequencyAnalysisSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dataday', 'nulldata', 'p2pk', 'p2pkh', 'p2ms', 'p2sh', 'unknowntype')


class SizeAnalysis(db.Model):
    __tablename__ = 'sizeanalysis'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    dataday = db.Column(db.Date, nullable=False)
    avgsize = db.Column(db.Integer, nullable=False)
    outputs = db.Column(db.Integer, nullable=False)

    def __init__(self, dataday, avgsize, outputs):
        self.dataday = dataday
        self.avgsize = avgsize
        self.outputs = outputs


class SizeAnalysisSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dataday', 'avgsize', 'outputs')


class ProtocolAnalysis(db.Model):
    __tablename__ = 'protocolanalysis'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    dataday = db.Column(db.Date, nullable=False)
    ascribe = db.Column(db.Integer, nullable=False)
    bitproof = db.Column(db.Integer, nullable=False)
    blockaibindedpixsy = db.Column(db.Integer, nullable=False)
    blocksign = db.Column(db.Integer, nullable=False)
    blockstoreblockstack = db.Column(db.Integer, nullable=False)
    chainpoint = db.Column(db.Integer, nullable=False)
    coinspark = db.Column(db.Integer, nullable=False)
    colu = db.Column(db.Integer, nullable=False)
    counterparty = db.Column(db.Integer, nullable=False)
    counterpartytest = db.Column(db.Integer, nullable=False)
    cryptocopyright = db.Column(db.Integer, nullable=False)
    diploma = db.Column(db.Integer, nullable=False)
    emptytx = db.Column(db.Integer, nullable=False)
    eternitywall = db.Column(db.Integer, nullable=False)
    factom = db.Column(db.Integer, nullable=False)
    lapreuve = db.Column(db.Integer, nullable=False)
    monegraph = db.Column(db.Integer, nullable=False)
    omni = db.Column(db.Integer, nullable=False)
    openassets = db.Column(db.Integer, nullable=False)
    openchain = db.Column(db.Integer, nullable=False)
    originalmy = db.Column(db.Integer, nullable=False)
    proofofexistence = db.Column(db.Integer, nullable=False)
    provebit = db.Column(db.Integer, nullable=False)
    remembr = db.Column(db.Integer, nullable=False)
    smartbit = db.Column(db.Integer, nullable=False)
    stampd = db.Column(db.Integer, nullable=False)
    stampery = db.Column(db.Integer, nullable=False)
    universityofnicosia = db.Column(db.Integer, nullable=False)
    unknownprotocol = db.Column(db.Integer, nullable=False)
    veriblock = db.Column(db.Integer, nullable=False)

    def __init__(self, dataday, ascribe, bitproof, blockaibindedpixsy, blocksign, blockstoreblockstack, chainpoint,
                 coinspark, colu, counterparty, counterpartytest, cryptocopyright, diploma, emptytx, eternitywall,
                 factom, lapreuve, monegraph, omni, openassets, openchain, originalmy, proofofexistence, provebit,
                 remembr, smartbit, stampd, stampery, universityofnicosia, unknownprotocol, veriblock):
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


class ProtocolAnalysisSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dataday', 'ascribe', 'bitproof', 'blockaibindedpixsy', 'blocksign', 'blockstoreblockstack',
                  'chainpoint', 'coinspark', 'colu', 'counterparty', 'counterpartytest', 'cryptocopyright', 'diploma',
                  'emptytx', 'eternitywall', 'factom', 'lapreuve', 'monegraph', 'omni', 'openassets', 'openchain',
                  'originalmy', 'proofofexistence', 'provebit', 'remembr', 'smartbit', 'stampd', 'stampery',
                  'universityofnicosia', 'unknownprotocol', 'veriblock')


class TransactionOutputs(db.Model):
    __tablename__ = 'transactionoutputs'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    txhash = db.Column(db.CHAR(64), nullable=False)
    blocktime = db.Column(db.BigInteger, nullable=False)
    blockhash = db.Column(db.CHAR(64), nullable=False)
    outvalue = db.Column(db.Float, nullable=False)
    outtype = db.Column(db.VARCHAR, nullable=False)
    outasm = db.Column(db.VARCHAR, nullable=False)
    outhex = db.Column(db.VARCHAR, nullable=False)
    protocol = db.Column(db.VARCHAR, nullable=True)
    fileheader = db.Column(db.VARCHAR, nullable=True)

    def __init__(self, txhash, blocktime, blockhash, outvalue, outtype, outasm, outhex, protocol, fileheader):
        self.txhash = txhash
        self.blocktime = blocktime
        self.blockhash = blockhash
        self.outvalue = outvalue
        self.outtype = outtype
        self.outasm = outasm
        self.outhex = outhex
        self.protocol = protocol
        self.fileheader = fileheader


class TransactionOutputsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'txhash', 'blocktime', 'blockhash', 'outvalue', 'outtype', 'outasm', 'outhex', 'protocol', 'fileheader')


freq_analysis_schema = FrequencyAnalysisSchema(many=True)
size_analysis_schema = SizeAnalysisSchema(many=True)
prot_analysis_schema = ProtocolAnalysisSchema(many=True)
tx_outputs_schema = TransactionOutputsSchema(many=True)
tx_output_schema = TransactionOutputsSchema(many=False)


@app.route('/frequency-analysis', methods=['GET'])
def get_frequency_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    if min_date is None and max_date is None:
        days = FrequencyAnalysis.query.all()
    elif min_date is None:
        days = FrequencyAnalysis.query.filter(FrequencyAnalysis.dataday <= max_date)
    elif max_date is None:
        days = FrequencyAnalysis.query.filter(FrequencyAnalysis.dataday >= min_date)
    else:
        days = FrequencyAnalysis.query.filter(FrequencyAnalysis.dataday.between(min_date, max_date))
    return freq_analysis_schema.jsonify(days)


@app.route('/size-analysis', methods=['GET'])
def get_size_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    if min_date is None and max_date is None:
        days = SizeAnalysis.query.all()
    elif min_date is None:
        days = SizeAnalysis.query.filter(SizeAnalysis.dataday <= max_date)
    elif max_date is None:
        days = SizeAnalysis.query.filter(SizeAnalysis.dataday >= min_date)
    else:
        days = SizeAnalysis.query.filter(SizeAnalysis.dataday.between(min_date, max_date))
    return size_analysis_schema.jsonify(days)


@app.route('/protocol-analysis', methods=['GET'])
def get_protocol_analysis():
    min_date = request.args.get('min_date')
    max_date = request.args.get('max_date')
    if min_date is None and max_date is None:
        days = ProtocolAnalysis.query.all()
    elif min_date is None:
        days = ProtocolAnalysis.query.filter(ProtocolAnalysis.dataday <= max_date)
    elif max_date is None:
        days = ProtocolAnalysis.query.filter(ProtocolAnalysis.dataday >= min_date)
    else:
        days = ProtocolAnalysis.query.filter(ProtocolAnalysis.dataday.between(min_date, max_date))
    return prot_analysis_schema.jsonify(days)


@app.route('/tx-outputs', methods=['GET'])
def get_tx_outputs():
    page = request.args.get('page')
    if page is None:
        tx_outputs = TransactionOutputs.query.order_by(TransactionOutputs.id.desc()).limit(PAGE_SIZE).all()
    else:
        result = limited_paginate(TransactionOutputs.query.order_by(TransactionOutputs.id.desc()), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN)
        tx_outputs = tx_outputs_schema.dump(result.items)
    return tx_outputs_schema.jsonify(tx_outputs)


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

    txs = tx_outputs_schema.dump(limited_paginate(
        TransactionOutputs.query.filter(and_(
            TransactionOutputs.blocktime >= min_time if min_time is not None and int(min_time) >= 1230768000 else sqlalchemy.true() if min_time is None else abort(400, 'Time can not be before 2009'),
            TransactionOutputs.blocktime <= max_time if max_time is not None and (int(max_time) > int(min_time) if min_time is not None else True) else sqlalchemy.true() if max_time is None else abort(400, 'max_time has to be larger than min_time'),
            or_(TransactionOutputs.protocol == prot for prot in protocols) if protocols is not None else sqlalchemy.true(),
            or_(TransactionOutputs.fileheader == fh for fh in fileheaders) if fileheaders is not None else sqlalchemy.true(),
            sqlalchemy.true() if search_term is None else abort(400, 'Search term must be at least 3 characters long') if len(search_term) < 3 else TransactionOutputs.outhex.like('%{}%'.format(search_term)) if search_format is None else TransactionOutputs.outhex.like('%{}%'.format(encoded_to_hex(search_term))) if search_format == 'encoded' else TransactionOutputs.outhex.like('%{}%'.format(search_term) if search_format == 'hex' else abort(400, 'Invalid search format (use hex or encoded)'))
        )).order_by(TransactionOutputs.id if sort is None else TransactionOutputs.id.desc() if sort == 'desc' else TransactionOutputs.id), int(page) if page is not None else 1, PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)

    return tx_outputs_schema.jsonify(txs)


@app.route('/tx-outputs/txhash', methods=['GET'])
def get_tx_output_by_hash():
    txhash = request.args.get('hash')
    page = request.args.get('page')

    if txhash is None:
        abort(400, 'Provide a transaction hash')
    elif len(txhash) != 64:
        abort(400, 'Provide a valid transaction hash')
    else:
        if page is None:
            txs = TransactionOutputs.query.filter(TransactionOutputs.txhash == txhash).order_by(TransactionOutputs.id.asc()).limit(PAGE_SIZE).all()
        else:
            txs = tx_outputs_schema.dump(limited_paginate(
                TransactionOutputs.query.filter(TransactionOutputs.txhash == txhash).order_by(TransactionOutputs.id.asc()), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)
    return tx_outputs_schema.jsonify(txs)


@app.route('/tx-outputs/blockhash', methods=['GET'])
def get_tx_outputs_by_blockhash():
    blockhash = request.args.get('hash')
    page = request.args.get('page')

    if blockhash is None:
        abort(400, 'Provide a block hash')
    elif len(blockhash) != 64:
        abort(400, 'Provide a valid block hash')
    else:
        if page is None:
            txs = TransactionOutputs.query.filter(TransactionOutputs.blockhash == blockhash).order_by(TransactionOutputs.id.asc()).limit(PAGE_SIZE).all()
        else:
            txs = tx_outputs_schema.dump(limited_paginate(
                TransactionOutputs.query.filter(TransactionOutputs.blockhash == blockhash).order_by(TransactionOutputs.id.asc()), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)
    return tx_outputs_schema.jsonify(txs)


# https://github.com/pallets/flask-sqlalchemy/issues/518#issuecomment-322379524
def limited_paginate(query_in, page=None, per_page=None, error_out=True, total_in=None):
    """Returns ``per_page`` items from page ``page``.
    If no items are found and ``page`` is greater than 1, or if page is
    less than 1, it aborts with 404.
    This behavior can be disabled by passing ``error_out=False``.
    If ``page`` or ``per_page`` are ``None``, they will be retrieved from
    the request query.
    If the values are not ints and ``error_out`` is ``True``, it aborts
    with 404.
    If there is no request or they aren't in the query, they default to 1
    and 20 respectively.
    Returns a :class:`Pagination` object.
    """

    if request:
        if page is None:
            try:
                page = int(request.args.get('page', 1))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                page = 1

        if per_page is None:
            try:
                per_page = int(request.args.get('per_page', PAGE_SIZE))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                per_page = PAGE_SIZE
    else:
        if page is None:
            page = 1

        if per_page is None:
            per_page = PAGE_SIZE

    if error_out and page < 1:
        abort(404)

    items = query_in.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1 and error_out:
        abort(404)

    # No need to count if we're on the first page and there are fewer
    # items than we expected.
    if page == 1 and len(items) < per_page:
        total = len(items)
    elif total_in:
        total = total_in
    else:
        total = query_in.order_by(None).count()

    return Pagination(query_in, page, per_page, total, items)


def encoded_to_hex(input_string):
    hex_string = hexlify(input_string.encode())
    return hex_string.decode()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
