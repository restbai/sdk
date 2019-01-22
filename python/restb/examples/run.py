from restb.examples import basic, multipredict, rate_limiting_simple, rate_limiting_robust


if __name__ == '__main__':
    client_key = 'YOUR_CLIENT_KEY_HERE'
    print('1. running basic example')
    basic.run(client_key)
    print('2. running multipredict example')
    multipredict.run(client_key)
    print('3. running simple rate limiting example')
    rate_limiting_simple.run(client_key)
    print('4. running robust rate limiting example')
    rate_limiting_robust.run(client_key)
