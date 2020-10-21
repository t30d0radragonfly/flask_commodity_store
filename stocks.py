from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

commodityStore = Flask(__name__)
commodityStore.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks_manager.db'
commodityStore.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data_base = SQLAlchemy(commodityStore)


class CommodityStore(data_base.Model):
    __tablename__ = 'stocks'
    stocks_id = data_base.Column(data_base.Integer, primary_key=True)
    stocks_name = data_base.Column(data_base.String(40), nullable=False)
    customer_name = data_base.Column(data_base.String(60), nullable=False)
    retailer_name = data_base.Column(data_base.String(20), nullable=False)
    stocks_price = data_base.Column(data_base.Integer, nullable=False)
    stocks_quantity = data_base.Column(data_base.Integer, nullable=False)


data_base.create_all()


@commodityStore.route('/', methods=['POST', 'GET'])
def store_info():
    if request.method == 'POST':
        stocks_name = request.form['stockname']
        customer_name = request.form['customername']
        retailer_name = request.form['retailername']
        stock_price = request.form['stocksprice']
        stock_quantity = request.form['stocksquantity']
        new_stock = CommodityStore(stocks_name=stocks_name, customer_name=customer_name, retailer_name=retailer_name, stocks_price=stock_price, stocks_quantity=stock_quantity)
        data_base.session.add(new_stock)
        data_base.session.commit()
        commodity_chart = CommodityStore.query.order_by(CommodityStore.stocks_id).all()
        return render_template('index.html', chart=commodity_chart)
    else:
        commodity_chart = CommodityStore.query.order_by(CommodityStore.stocks_id).all()
        return render_template('index.html', chart=commodity_chart)


@commodityStore.route('/update/<int:stocks_id>', methods=['GET', 'POST'])
def update(stocks_id):
    commodity_chart = CommodityStore.query.get_or_404(stocks_id)
    if request.method == 'POST':
        commodity_chart.stocks_name = request.form['stocksname']
        commodity_chart.customer_name = request.form['customername']
        commodity_chart.retailer_name = request.form['retailername']
        commodity_chart.stocks_price = request.form['price']
        commodity_chart.stocks_quantity = request.form['quantity']
        data_base.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', chart=commodity_chart)


@commodityStore.route('/delete/<int:stocks_id>')
def delete(stocks_id):
    stock_to_del = CommodityStore.query.get_or_404(stocks_id)
    try:
        data_base.session.delete(stock_to_del)
        data_base.session.commit()
        return redirect('/')
    except ValueError:
        return 'There was a problem deleting that task'


# Execution of the programme
if __name__ == "__main__":
    commodityStore.run(debug=True)
