__URL_EU = 'https://api-eu.restb.ai'
__URL_US = 'https://api-us.restb.ai'
__ENDPOINT = '/vision/v2/predict'
__ENDPOINT_MULTIPREDICT = '/vision/v2/multipredict'
__MODELS = [
    're_roomtype_global_v2',
    're_exterior_styles',
    're_features_v4',
    're_logo',
    're_compliance_v2',
    're_condition_r1r6_global'
]
__PARAMS = {
    'client_key': None,
    'model_id': None,
    'image_url': None,
    'image_base64': None
}


__all__ = [
    '__URL_EU',
    '__URL_US',
    '__ENDPOINT',
    '__ENDPOINT_MULTIPREDICT',
    '__MODELS',
    '__PARAMS'
]
