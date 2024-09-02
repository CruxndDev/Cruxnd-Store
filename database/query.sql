SELECT
    users.id AS usersId,
    password_hash,
    username,
    email_address,
    carts.id AS cartsid
FROM
    users
    LEFT JOIN carts ON carts.creator = users.id
WHERE
    carts.id IS NOT NULL
LIMIT
    10