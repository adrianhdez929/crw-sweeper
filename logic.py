from spendfrom import *
from PyQt5.QtWidgets import QCheckBox


def try_conn(dialog, options):
    try:
        config = read_bitcoin_config(options.datadir, options.conffile)
        if options.testnet: config['testnet'] = True
        crownd = connect_JSON(config)
        crownd.getinfo()
    except Exception:
        return False
    return True

def connect(dialog, options):
    try:
        check_json_precision()
        config = read_bitcoin_config(options.datadir, options.conffile)
        if options.testnet: config['testnet'] = True
        crownd = connect_JSON(config)
    except Exception:
        return False
    else:
        address_summary = list_available(crownd)
    return address_summary


def sweep(dialog, options):
    check_json_precision()
    config = read_bitcoin_config(options.datadir,options.conffile)
    if options.testnet: config['testnet'] = True
    crownd = connect_JSON(config)
    if not dialog.new_address_checkbox.isVisible():
        options.new = False
    if options.new:
        options.toaddress = crownd.getnewaddress('')
        dialog.to_address_edit.setText(options.toaddress)
    if options.toaddress is None:
        return dialog.notify("You must specify a to address")
    if not (crownd.validateaddress(options.toaddress))['isvalid']:
        return dialog.notify("To address is invalid")
    else:    
        fee = Decimal(options.fee)
        amount = Decimal(options.amount) - fee
        while unlock_wallet(crownd, dialog.options.passphrase) == False:
            if dialog.options.pswdcanceled:
                return
            dialog.pswdask()
        txdata = create_tx(crownd, options.fromaddresses, options.toaddress, amount, fee, options.select, options.upto)
        sanity_test_fee(crownd, txdata, amount*Decimal("0.01"), fee)
        txlen = len(txdata)/2
        if txlen < 250000:
            txid = crownd.sendrawtransaction(txdata)
            refresh(dialog, options)
            return dialog.showtx(txid)
        else:
            return dialog.notify("Transaction size is too large")

def selected_items(widget, options):
    items = list()
    selected_amount = 0
    for item in widget.selectedItems():
        item = item.text().split(" ")
        items.append(item[0])
        selected_amount += float(item[2])
    selected_amount = selected_amount
    widget.parent().parent().selected_label.setText(str(selected_amount))
    widget.parent().parent().amount_edit.setText(str(selected_amount))
    options.amount = str(selected_amount)
    options.fromaddresses = items

    return (items, selected_amount)

def get_input(widget, options):
    text = widget.text()
    
    if widget.objectName() == 'fee_edit':
        options.fee = text
    elif widget.objectName() == 'amount_edit':
        options.amount = text
    elif widget.objectName() == 'to_address_edit':
        options.toaddress = text

def get_checkbox(widget, options):
    value = False if widget.checkState() == 0 else True

    if widget.objectName() == 'new_address_checkbox':
        options.new = value
    elif widget.objectName() == 'upto_checkbox':
        options.upto = value
    
def refresh(widget, options):
    addresses = list()
    spendable_amount = 0
    address_summary = connect(widget, options)
    if address_summary.items():
        for address,info in address_summary.items():
            n_transactions = len(info['outputs'])
            elem = {
                'data': "%s Amount: %s Label: %s UTXO:(%s)"%(address, info['total'], info['account'], str(n_transactions)),
                'label': info['account'],
                'amount': info['total'],
            }
            addresses.append(elem)
            spendable_amount += info['total']

    spendable_amount = float(spendable_amount)
    order(addresses, widget.order_combobox.currentText())
    widget.available_label.setText(str(spendable_amount))
    widget.address_list_widget.clear()
    widget.new_address_checkbox.setVisible(True)
    for address in addresses:
        widget.address_list_widget.addItem(address['data'])

def order(addresses, by):
    if by == 'Smallest':
        addresses.sort(key=lambda k: k['amount'])
    elif by == 'Largest':
        addresses.sort(key=lambda k: k['amount'], reverse=True)
    elif by == 'Label':
        addresses.sort(key=lambda k: k['label'])
