import config as cfg
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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


freq_analysis_schema = FrequencyAnalysisSchema(many=True)
size_analysis_schema = SizeAnalysisSchema(many=True)


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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
