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


freq_analysis_schema = FrequencyAnalysisSchema(many=True)


@app.route('/frequency-analysis', methods=['GET'])
def get_test():
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


if __name__ == '__main__':
    app.run(debug=True)
