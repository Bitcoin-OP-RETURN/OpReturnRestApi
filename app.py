import config as cfg
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy, Pagination, abort
from flask_marshmallow import Marshmallow

# Initialize app
app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + cfg.db['username'] + ':' + cfg.db['password'] + '@' + cfg.db['server'] + ':' + cfg.db['port'] + '/' + cfg.db['database']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
db = SQLAlchemy(app)
# Initialize marshmallow
ma = Marshmallow(app)

PAGE_SIZE = 50
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


@app.route('/tx-outputs/time', methods=['GET'])
def get_tx_outputs_by_time():
    min_time = request.args.get('min_time')
    max_time = request.args.get('max_time')
    page = request.args.get('page')

    if min_time is not None and int(min_time) < 1230768000:
        abort(400, 'Time can not be before 2009')
    if max_time is not None and int(min_time) < 1230768000:
        abort(400, 'Time can not be before 2009')

    if min_time is None and max_time is None:
        abort(400, 'Provide the parameters min_time or max_time')
    elif min_time is None:
        if page is None:
            txs = TransactionOutputs.query.filter(TransactionOutputs.blocktime <= max_time).order_by(TransactionOutputs.id).limit(PAGE_SIZE)
        else:
            txs = tx_outputs_schema.dump(limited_paginate(TransactionOutputs.query.filter(TransactionOutputs.blocktime <= max_time).order_by(TransactionOutputs.id), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)
    elif max_time is None:
        if page is None:
            txs = TransactionOutputs.query.filter(TransactionOutputs.blocktime >= min_time).order_by(TransactionOutputs.id).limit(PAGE_SIZE)
        else:
            txs = tx_outputs_schema.dump(limited_paginate(TransactionOutputs.query.filter(TransactionOutputs.blocktime >= min_time).order_by(TransactionOutputs.id), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)
    else:
        if page is None:
            txs = TransactionOutputs.query.filter(TransactionOutputs.blocktime.between(min_time, max_time)).order_by(TransactionOutputs.id).limit(PAGE_SIZE)
        else:
            txs = tx_outputs_schema.dump(limited_paginate(TransactionOutputs.query.filter(TransactionOutputs.blocktime.between(min_time, max_time)).order_by(TransactionOutputs.id), int(page), PAGE_SIZE, error_out=True, total_in=TOTAL_IN).items)
    return tx_outputs_schema.jsonify(txs)


@app.route('/tx-outputs/txhash', methods=['GET'])
def get_tx_output_by_hash():
    txhash = request.args.get('hash')

    if txhash is None:
        abort(400, 'Provide a transaction hash')
    elif len(txhash) != 64:
        abort(400, 'Provide a valid transaction hash')
    else:
        tx = TransactionOutputs.query.filter(TransactionOutputs.txhash == txhash).first()
    return tx_output_schema.jsonify(tx)


@app.route('/tx-outputs/blockhash', methods=['GET'])
def get_tx_outputs_by_blockhash():
    blockhash = request.args.get('hash')

    if blockhash is None:
        abort(400, 'Provide a block hash')
    elif len(blockhash) != 64:
        abort(400, 'Provide a valid block hash')
    else:
        txs = TransactionOutputs.query.filter(TransactionOutputs.blockhash == blockhash).all()
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
