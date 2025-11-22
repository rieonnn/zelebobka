from flask import Blueprint, render_template, request, session

# Переименовано, чтобы не конфликтовало с именем файла
lab6_bp = Blueprint('lab6', __name__, template_folder='templates')

# Создаём список офисов
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 900 + i*3})


@lab6_bp.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


@lab6_bp.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    # Метод info — вернуть список офисов
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    # Метод booking — забронировать офис
    elif data['method'] == 'booking':
        login = session.get('login')

        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Unauthorized'},
                'id': id
            }

        office_number = data.get('params')

        if not office_number:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Параметр params обязателен'
                },
                'id': id
            }

        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': f'Офис {office_number} не существует'
            },
            'id': id
        }

    elif data['method'] == 'cancellation':

        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data.get('params')
        if office_number is None:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Параметр params обязателен'
                },
                'id': id
            }

        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }
                office['tenant'] = ""
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': f'Офис {office_number} не существует'
            },
            'id': id
        }

    # Неизвестный метод
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
