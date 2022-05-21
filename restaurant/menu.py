APPETIZERS = {
    'chicken livers': 5,
    'sauteed mushrooms': 5,
    'teppanyaki shrimp flambe': 5,
}

RICE_CHOICES = (
    (1, 'rice'),
    (2, 'fried_rice')
)
ENTREE_CHOICES = (
    (1, 'sakura vegetable dinner'),
    (2, 'tofu dinner'),
    (3, 'teriyaki chicken'),
    (4, 'new york steak'),
    (5, 'rib eye steak'),
    (6, 'filet mignon'),
    (7, 'salmon teriyaki'),
    (8, 'shrimp flambe'),
    (9, 'scallops'),
    (10, 'shrimp and scallops'),
    (11, 'shrimp and lobster'),
    (12, 'scallops and lobster'),
    (13, 'lobster, shrimp and scallops'),
    (14, 'lobster')
)
SIDE_CHOICES = (
    (1, 'scallops'),
    (2, 'shrimp flambe'),
    (3, 'sakura chicken livers'),
    (4, 'sakura fried rice'),
    (5, 'sauteed mushrooms'),
    (6, 'extra veggie')
)

APPETIZER_CHOICES = tuple((i, i) for i in APPETIZERS.keys())