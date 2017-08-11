import numpy as np
from feedforward import get_embedding

def generate_signature(img_path):
    """Generates an image signature.

    Args:
        img_path (string or numpy.ndarray): image path, or image array

    Returns:
        The image signature: A rank 1 numpy array of length n x n x 8
            (or n x n x 4 if diagonal_neighbors == False)

    Examples:
        >>> from image_match.goldberg import ImageSignature
        >>> gis = ImageSignature()
        >>> gis.generate_signature('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
    """
    try:
        signature = get_embedding(img_path)
    except IOError:
        raise TypeError('Cannot predict image successfully.')
    return signature

def normalized_distance(_a, _b):
    """Compute normalized distance between two points.

    Computes 1 - a * b / ( ||a|| * ||b||)

    Args:
        _a (numpy.ndarray): array of size m
        _b (numpy.ndarray): array of size m

    Returns:
        normalized distance between signatures (float)

    Examples:
        >>> a = gis.generate_signature('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
        >>> b = gis.generate_signature('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
        >>> gis.normalized_distance(a, b)
        0.0332806110382

    """

    # return (1.0 - np.dot(_a, _b) / (np.linalg.norm(_a) * np.linalg.norm(_b)))
    return np.dot(_a, _b) / (np.linalg.norm(_a) * np.linalg.norm(_b))
