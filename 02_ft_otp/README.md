# ft_otp

oathtool --totp $(cat key.hex)

HMAC: Keyed-Hashing for Message Authentication
https://www.rfc-editor.org/info/rfc2104

HOTP: An HMAC-Based One-Time Password Algorithm
https://www.rfc-editor.org/info/rfc4226

TOTP: Time-Based One-Time Password Algorithm
https://www.rfc-editor.org/info/rfc6238


HMAC(K XOR opad, H(K XOR ipad, text))
H = a cryptographic hash function (SHA-1)
K = a secret key

HOTP(K,C) = Truncate(HMAC-SHA-1(K,C))
K Key
C Counter

TOTP = HOTP(K, T)
K Key
T Time
