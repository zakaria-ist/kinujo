GENDER_TYPE = (
    (0, 'NONE'),
    (1, 'MALE'),
    (2, 'FEMALE')
)

YES_NO = (
    (0, 'NO'),
    (1, 'YES')
)

ACCOUNT_TYPE = (
    (1, 'Normal'),
    (2, 'Current'),
    (3, 'Savings')
)

SALON_TYPE = (
    ('SALONS', 1),
    ('STYLISTS', 2)
)

SALON_CATEGORY = (
    (1, 'SALONS'),
    (2, 'STYLISTS')
)

PRODUCT_VARIETY = (
    (0, 'NONE'),
    (1, 'HOROZONTAL'),
    (2, 'VERTICAL AND HOROZONTAL')
)

TARGET_TYPE = (
    (0, 'ALL'),
    (1, 'GENERAL ONLY'),
    (2, 'STORE ONLY')
)

GROUP_TYPE = (
    ('PAIR', 0),
    ('GROUP', 1)
)

PAYMENT_STATUS = (
    ('UNPAID', 0),
    ('PAID', 1)
)

AUTHORITY_TYPE = {
    'MASTER': 1,
    'SPECIAL': 2,
    'AMBASSADOR': 3,
    'STORE': 4,
    'GENERAL': 5
}