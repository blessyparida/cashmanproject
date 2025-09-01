from flask import Blueprint, request, jsonify
from .models import Transaction, db
from .schemas import TransactionSchema

bp = Blueprint("views", __name__)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

@bp.route("/")
def home():
    return jsonify({"message": "💰 Welcome to Cashman API! Use /transactions to interact."})

# Add transaction
@bp.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    tx = transaction_schema.load(data, session=db.session)
    db.session.add(tx)
    db.session.commit()
    return jsonify(transaction_schema.dump(tx)), 201

# Get all transactions
@bp.route("/transactions", methods=["GET"])
def get_transactions():
    txs = Transaction.query.all()
    return jsonify(transactions_schema.dump(txs)), 200

# Get single transaction
@bp.route("/transactions/<int:tx_id>", methods=["GET"])
def get_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if not tx:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction_schema.dump(tx)), 200

# Update transaction
@bp.route("/transactions/<int:tx_id>", methods=["PUT"])
def update_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if not tx:
        return jsonify({"error": "Transaction not found"}), 404
    data = request.get_json()
    tx.amount = data.get("amount", tx.amount)
    tx.description = data.get("description", tx.description)
    db.session.commit()
    return jsonify(transaction_schema.dump(tx)), 200

# Delete transaction
@bp.route("/transactions/<int:tx_id>", methods=["DELETE"])
def delete_transaction(tx_id):
    tx = Transaction.query.get(tx_id)
    if not tx:
        return jsonify({"error": "Transaction not found"}), 404
    db.session.delete(tx)
    db.session.commit()
    return jsonify(transaction_schema.dump(tx)), 200
