__URL_EU = 'https://api-eu.restb.ai'
__URL_US = 'https://api-us.restb.ai'
__ENDPOINT = '/vision/v2/predict'
__MODELS = [
    'real_estate_global_v2',
    're_styles',
    're_features_v3',
    're_logo',
    're_appliances',
    're_compliance',
    're_cond_bathroom',
    're_cond_kitchen',
    'blurry'
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
    '__MODELS',
    '__PARAMS'
]
