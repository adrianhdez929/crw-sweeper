from spendfrom import *
#from crown_pycurl.client import Client
#import pycurl


def try_conn(dialog, options):
    try:
        config = read_bitcoin_config(options.datadir, options.conffile)
        #print("Using %s and %s"%(config['rpcuser'], config['rpcpassword']))
        if options.testnet: config['testnet'] = True
        crownd = connect_JSON(config)
        #crownd = Client('crowncoinadrianrpc', 'LGzq9yTUZRyt72hd736T0FJgt5gdkj83yiMJsgt6ehfwt5DYFKO9HknLXawTUpqX3', '92.60.46.31')
        #crownd.client.setopt(pycurl.PROXY, 'http://92.60.46.19/')
        #crownd.client.setopt(pycurl.PROXYPORT, 3128)
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
        #crownd = Client('crowncoinadrianrpc', 'LGzq9yTUZRyt72hd736T0FJgt5gdkj83yiMJsgt6ehfwt5DYFKO9HknLXawTUpqX3', '92.60.46.31')
        #crownd.client.setopt(pycurl.PROXY, 'http://92.60.46.19/')
        #crownd.client.setopt(pycurl.PROXYPORT, 3128)
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
    #crownd = Client('crowncoinadrianrpc', 'LGzq9yTUZRyt72hd736T0FJgt5gdkj83yiMJsgt6ehfwt5DYFKO9HknLXawTUpqX3', '92.60.46.31')
    #crownd.client.setopt(pycurl.PROXY, 'http://92.60.46.19/')
    #crownd.client.setopt(pycurl.PROXYPORT, 3128)
    if options.toaddress is None:
        return dialog.notify("You must specify a to address")
        #if options.toaddress.lower() == 'new':
        #    options.toaddress = crownd.getnewaddress('')
        #    print("Sending to new address %s"%(options.toaddress))
    if not crownd.validateaddress(options.toaddress)['result']['isvalid']:
        return dialog.notify("To address is invalid")
    else:    
        fee = Decimal(options.fee)
        amount = Decimal(options.amount)
        while unlock_wallet(crownd) == False:
            pass # Keep asking for passphrase until they get it right
        txdata = create_tx(crownd, options.fromaddresses, options.toaddress, amount, fee, options.select, options.upto)
        sanity_test_fee(crownd, txdata, amount*Decimal("0.01"), fee)
        txlen = len(txdata)/2
        if txlen < 250000:
            txid = crownd.sendrawtransaction(txdata)
            return dialog.notify(txid)
        else:
            return dialog.notify("Transaction size is too large")

def selected_items(widget, options):
    items = list()
    selected_amount = 0
    for item in widget.selectedItems():
        item = item.text().split(" ")
        items.append(item[0])
        selected_amount += float(item[1])
    widget.parent().parent().label_8.setText(str(selected_amount))
    widget.parent().parent().lineEdit_7.setText(str(selected_amount))
    options.amount = str(selected_amount)
    options.fromaddresses = items

    return (items, selected_amount)

def get_input(widget, options):
    text = widget.text()
    
    if widget.objectName() == 'lineEdit_3':
        options.fee = text
    elif widget.objectName() == 'lineEdit_7':
        options.amount = text
    elif widget.objectName() == 'lineEdit_6':
        options.toaddress = text

def get_checkbox(widget, options):
    value = False if widget.checkState() == 0 else True

    if widget.objectName() == 'checkBox':
        options.testnet = value
        print(options.testnet)
    elif widget.objectName() == 'checkBox_2':
        options.dry_run = value
        print(options.dry_run)
    elif widget.objectName() == 'checkBox_3':
        options.upto = value
        print(options.upto)
    
