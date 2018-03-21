__URL_EU = 'https://api-eu.restb.ai'
__URL_US = 'https://api-us.restb.ai'
__MODELS = {
    'real_estate_global_v2': '/vision/v1/classify',
    're_styles': '/vision/v1/classify',
    're_features_v3': '/vision/v1/segmentation',
    're_logo': '/vision/v1/segmentation',
    're_privacy': '/vision/v1/segmentation',
    'blurry': '/vision/v1/blurry'
}
__PARAMS = {
    'client_key': None,
    'model_id': None,
    'image_url': None,
    'image_base64': None
}


__all__ = [
    '__URL_EU',
    '__URL_US',
    '__MODELS',
    '__PARAMS'
]
