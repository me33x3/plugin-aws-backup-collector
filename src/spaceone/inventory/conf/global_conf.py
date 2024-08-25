CONNECTORS = {
    'SpaceConnector': {
        'backend': 'spaceone.core.connector.space_connector.SpaceConnector',
        'endpoints': {
            'identity': 'grpc://dev.cloudwiz.ktds.com:50051',
            'inventory': 'grpc://dev.cloudwiz.ktds.com:50052',
            'plugin': 'grpc://dev.cloudwiz.ktds.com:50053',
            'repository': 'grpc://dev.cloudwiz.ktds.com:50054',
            'secret': 'grpc://dev.cloudwiz.ktds.com:50055',
            'notification': 'grpc://dev.cloudwiz.ktds.com:50059'
        }
    },
    'ConsulConnector': {
        'host': 'dev.cloudwiz.ktds.com',
        'port': 8500
    },
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ]
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}
